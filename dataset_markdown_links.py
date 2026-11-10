#!/usr/bin/env python3
"""Link canonical dataset names and IDs in Markdown tables to official sources."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
ID_RE = re.compile(r"`([a-z][a-z0-9_]+)`")
LINK_RE = re.compile(r'!?\[[^\]]*\]\([^)\s]+(?:\s+"[^"]*")?\)')
CODE_SPAN_RE = re.compile(r"`[^`\n]+`")

# Explicit display aliases used by curated reports. Generic family names are not
# mapped when doing so would ambiguously select one asset from several variants.
ALIASES = {
    "Dolly": "dolly_15k",
    "M2Lingual": "m2lingual",
    "Tulu 3 Persona IF": "tulu3_persona_if",
    "IFEval-like filtered": "ifeval_like_filtered",
    "IFEval-like": "ifeval_like_filtered",
    "LongAlign": "longalign_10k",
    "DeepScaleR": "deepscaler_preview",
    "GSM8K": "gsm8k_test",
    "AceCode": "acecode_87k",
    "xLAM": "xlam_function_calling",
    "WebLINX": "weblinx",
    "HelpSteer3": "helpsteer3_preference",
    "Arena": "arena_human_preference_140k",
    "Skywork v0.2": "skywork_reward_preference_80k",
    "RewardBench": "rewardbench",
    "Aegis 2.0": "aegis_content_safety_2",
    "FalseReject": "falsereject_train",
    "Nemotron RL": "nemotron_cascade_2_rl",
    "PixMo Ask": "pixmo_ask_model_anything",
    "Mantis": "mantis_instruct",
    "LLaVA-Video": "llava_video_178k",
    "VideoChat-Flash": "videochat_flash_training",
    "Molmo2-VideoPoint": "molmo2_videopoint",
    "Visual-RFT": "visual_rft_tasks",
    "VoiceAssistant": "voice_assistant_400k",
    "OS-Atlas action": "os_atlas_action_sft",
    "GUIOdyssey": "gui_odyssey_train",
    "VLGuard": "vlguard_train",
    "SPA-VL": "spa_vl_train",
    "SafeVid": "safe_vid_350k",
    "AudioBench": "audiobench",
    "CMMMU": "cmmmu_test",
}


def load_assets(path: Path | None = None) -> dict[str, dict[str, Any]]:
    catalog = path or ROOT / "datasets-list.yaml"
    doc = yaml.safe_load(catalog.read_text(encoding="utf-8"))
    return {item["id"]: item for item in doc["datasets"]}


def official_url(item: dict[str, Any]) -> str | None:
    url = item["source"]["url"]
    return url if url.startswith("https://") else None


def dataset_link(item: dict[str, Any], label: str | None = None) -> str:
    label = label or item["name"]
    url = official_url(item)
    return f"[{label}]({url})" if url else label


def link_dataset_table_entries(text: str, assets: dict[str, dict[str, Any]]) -> str:
    """Idempotently link canonical names, explicit aliases and code-formatted IDs."""
    labels = [(item["name"], item) for item in assets.values() if official_url(item)]
    labels += [
        (alias, assets[dataset_id])
        for alias, dataset_id in ALIASES.items()
        if dataset_id in assets and official_url(assets[dataset_id])
    ]
    labels.sort(key=lambda pair: len(pair[0]), reverse=True)
    rendered_lines = []
    for raw_line in text.splitlines(keepends=True):
        ending = "\n" if raw_line.endswith("\n") else ""
        line = raw_line[:-1] if ending else raw_line
        if not line.lstrip().startswith("|"):
            rendered_lines.append(raw_line)
            continue

        def replace_id(match: re.Match[str]) -> str:
            item = assets.get(match.group(1))
            if not item or not official_url(item):
                return match.group(0)
            # Already rendered as [`canonical_id`](https://...).
            if match.start() > 0 and line[match.start() - 1] == "[" and line[match.end():match.end() + 2] == "](":
                return match.group(0)
            return dataset_link(item, f"`{item['id']}`")

        line = ID_RE.sub(replace_id, line)
        protected: list[str] = []

        def protect(value: str) -> str:
            token = f"\x00{len(protected)}\x00"
            protected.append(value)
            return token

        # Existing links must not be nested. Other code spans contain repo IDs,
        # revisions or configs rather than display names and stay verbatim.
        line = LINK_RE.sub(lambda match: protect(match.group(0)), line)
        line = CODE_SPAN_RE.sub(lambda match: protect(match.group(0)), line)
        for name, item in labels:
            if name not in line:
                continue
            pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(name) + r"(?![A-Za-z0-9_])")
            token = protect(dataset_link(item, name))
            line = pattern.sub(lambda _match: token, line)
        for index, value in enumerate(protected):
            line = line.replace(f"\x00{index}\x00", value)
        rendered_lines.append(line + ending)
    return "".join(rendered_lines)


def validate_primary_catalog(text: str, assets: dict[str, dict[str, Any]]) -> list[str]:
    """Require one official name link per public asset in a primary catalogue."""
    errors = []
    for item in assets.values():
        name = item["name"]
        if official_url(item):
            expected = dataset_link(item)
            if expected not in text:
                errors.append(f"{item['id']}: 缺少名称链接 {expected}")
        elif name not in text:
            errors.append(f"{item['id']}: 缺少本地物料名称")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="要原地处理的 Markdown 文件")
    args = parser.parse_args()
    assets = load_assets()
    for path in args.paths:
        resolved = path.resolve()
        if ROOT != resolved and ROOT not in resolved.parents:
            raise ValueError(f"路径越出仓库：{path}")
        original = resolved.read_text(encoding="utf-8")
        rendered = link_dataset_table_entries(original, assets)
        if rendered != original:
            resolved.write_text(rendered, encoding="utf-8")
        print(f"{resolved.relative_to(ROOT)}: {'updated' if rendered != original else 'already linked'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
