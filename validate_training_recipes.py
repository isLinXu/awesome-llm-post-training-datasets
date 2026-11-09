#!/usr/bin/env python3
"""校验商用默认／研究隔离配方；不下载数据，不执行训练。"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

import yaml

from validate_post_training_manifest import validate as validate_manifest

ROOT = Path(__file__).resolve().parent
SHA40 = re.compile(r"[0-9a-f]{40}")
EXPECTED_PROFILES = {
    "commercial": {
        "commercial_general_sft",
        "commercial_code_sft",
        "commercial_long_sft",
        "commercial_preference_dpo",
        "commercial_math_rlvr",
    },
    "research": {
        "research_reasoning_sft",
        "research_browser_sft",
        "research_overrefusal_sft",
        "research_preference_dpo",
        "research_enigmata_rlvr",
    },
}
EXPECTED_DATASETS = {"commercial": 8, "research": 10}
EXPECTED_UNIQUE_SOURCES = 16


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"YAML 顶层必须是对象：{path}")
    return value


def overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def recipe_paths(manifest: dict[str, Any], root: Path) -> dict[str, Path]:
    paths = manifest.get("paths", {})
    result = {
        "raw": (root / paths.get("raw_root", "")).resolve(),
        "processed": (root / paths.get("processed_root", "")).resolve(),
        "cache": (root / paths.get("cache_root", "")).resolve(),
    }
    result["output"] = (root / manifest.get("project", {}).get("output_dir", "")).resolve()
    return result


def check_recipe(
    kind: str,
    manifest: dict[str, Any],
    assets: dict[str, dict[str, Any]],
    errors: list[str],
) -> dict[str, Any]:
    commercial = kind == "commercial"
    datasets = manifest.get("datasets", {})
    profiles = manifest.get("profiles", {})
    project = manifest.get("project", {})
    isolation = manifest.get("isolation", {})

    if len(datasets) != EXPECTED_DATASETS[kind]:
        errors.append(f"{kind}: 数据项应为 {EXPECTED_DATASETS[kind]}，实际为 {len(datasets)}")
    if set(profiles) != EXPECTED_PROFILES[kind]:
        errors.append(f"{kind}: profile 集合不完整或包含未知项：{sorted(profiles)}")
    if project.get("commercial_use") is not commercial:
        errors.append(f"{kind}: project.commercial_use 必须为 {str(commercial).lower()}")
    if isolation.get("recipe_class") != kind:
        errors.append(f"{kind}: isolation.recipe_class 不匹配")
    if isolation.get("allow_cross_recipe_raw_cache_or_output_reuse") is not False:
        errors.append(f"{kind}: 必须禁止跨配方复用 raw/cache/output")
    if isolation.get("research_to_commercial_promotion") != "requires_new_manifest_and_full_license_review":
        errors.append(f"{kind}: 研究晋升商用必须新建 Manifest 并完整重审")
    if isolation.get("eval_only_assets_allowed_in_mixture") is not False:
        errors.append(f"{kind}: 必须禁止 eval_only 进入混合训练")
    if not SHA40.fullmatch(str(project.get("base_model", {}).get("revision", ""))):
        errors.append(f"{kind}: Base 模型 revision 必须是 40 位 SHA")
    if not SHA40.fullmatch(str(project.get("base_model", {}).get("chat_template_bridge_revision", ""))):
        errors.append(f"{kind}: Bridge revision 必须是 40 位 SHA")

    signoff = manifest.get("signoff", {})
    for gate in ("data_quality", "license", "decontamination", "verifier"):
        if signoff.get(gate) is not False:
            errors.append(f"{kind}: 未执行真实审查，signoff.{gate} 必须保持 false")

    for name, dataset in datasets.items():
        prefix = f"{kind}/{name}"
        canonical_id = dataset.get("canonical_id")
        asset = assets.get(canonical_id)
        if canonical_id != name:
            errors.append(f"{prefix}: canonical_id 必须与数据键一致")
        if asset is None:
            errors.append(f"{prefix}: canonical_id 不在 canonical 总表")
        else:
            if asset.get("train_prohibited") is not False or asset.get("usage_tier") == "eval_only":
                errors.append(f"{prefix}: eval_only／禁止训练资产不得进入配方")
            if asset.get("modalities") != ["text"]:
                errors.append(f"{prefix}: ERNIE 文本配方只允许 modalities=[text] 的资产")
        source = dataset.get("source", {})
        if not SHA40.fullmatch(str(source.get("revision", ""))):
            errors.append(f"{prefix}: 数据 revision 必须是 40 位 SHA，不能为 main")
        if not str(source.get("subset", "")).strip():
            errors.append(f"{prefix}: 缺少 config/subset")
        if not str(source.get("split", "")).strip():
            errors.append(f"{prefix}: 缺少 split")
        if dataset.get("enabled") is not True:
            errors.append(f"{prefix}: 配方引用项必须 enabled=true")
        if commercial and dataset.get("license", {}).get("commercial_status") != "allowed_with_obligations":
            errors.append(f"{prefix}: 商用配方只允许 allowed_with_obligations")

    profile_results = {}
    for profile_name in profiles:
        errors_from_template, _, selected, _ = validate_manifest(manifest, profile_name, True)
        errors.extend(f"{kind}: {message}" for message in errors_from_template)
        if selected is None:
            continue
        mixture = profiles[profile_name].get("mixture", [])
        names = [item.get("dataset") for item in mixture]
        if len(names) != len(set(names)):
            errors.append(f"{kind}/{profile_name}: mixture 不得重复引用同一数据项")
        weights = [item.get("weight") for item in mixture]
        if not all(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0 for value in weights):
            errors.append(f"{kind}/{profile_name}: 权重必须是有限正数")
        elif not math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=1e-9):
            errors.append(f"{kind}/{profile_name}: 权重之和必须为 1")
        for item in mixture:
            dataset = datasets.get(item.get("dataset"), {})
            if commercial and dataset.get("license", {}).get("commercial_status") != "allowed_with_obligations":
                errors.append(f"{kind}/{profile_name}: 引用了非商用默认数据 {item.get('dataset')}")
        profile_results[profile_name] = {
            "stage": profiles[profile_name].get("stage"),
            "datasets": names,
            "weights": weights,
            "template_validation": "passed" if not errors_from_template else "failed",
        }

    return {
        "datasets": len(datasets),
        "profiles": len(profiles),
        "commercial_use": project.get("commercial_use"),
        "profile_results": profile_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="校验两套后训练配方及商用／研究隔离边界")
    parser.add_argument("--commercial", type=Path, default=ROOT / "commercial-default-manifest.yaml")
    parser.add_argument("--research", type=Path, default=ROOT / "research-isolated-manifest.yaml")
    parser.add_argument("--catalog", type=Path, default=ROOT / "datasets-list.yaml")
    parser.add_argument("--json", action="store_true", help="输出机器可读校验摘要")
    args = parser.parse_args()

    errors: list[str] = []
    try:
        commercial = load_yaml(args.commercial)
        research = load_yaml(args.research)
        catalog = load_yaml(args.catalog)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"读取配置失败：{exc}", file=sys.stderr)
        return 2

    assets = {item.get("id"): item for item in catalog.get("datasets", [])}
    if len(assets) < 114:
        errors.append(f"canonical 总表至少保留原 114 项，实际仅 {len(assets)}")
    if catalog.get("provenance", {}).get("text_assets_retained") != 114:
        errors.append("canonical provenance 未确认原 114 项文本资产全部保留")

    commercial_result = check_recipe("commercial", commercial, assets, errors)
    research_result = check_recipe("research", research, assets, errors)

    commercial_sources = set(commercial.get("datasets", {}))
    research_sources = set(research.get("datasets", {}))
    unique_sources = commercial_sources | research_sources
    if len(unique_sources) != EXPECTED_UNIQUE_SOURCES:
        errors.append(f"唯一数据来源应为 {EXPECTED_UNIQUE_SOURCES}，实际为 {len(unique_sources)}")

    for name in commercial_sources & research_sources:
        left = commercial["datasets"][name]["source"]
        right = research["datasets"][name]["source"]
        for field in ("provider", "repo_id", "revision", "subset", "split"):
            if left.get(field) != right.get(field):
                errors.append(f"共享数据 {name} 的 {field} 在两套配方中不一致")

    left_paths = recipe_paths(commercial, args.commercial.resolve().parent)
    right_paths = recipe_paths(research, args.research.resolve().parent)
    for left_name, left_path in left_paths.items():
        for right_name, right_path in right_paths.items():
            if overlap(left_path, right_path):
                errors.append(f"路径隔离失败：commercial/{left_name}={left_path} 与 research/{right_name}={right_path} 重叠")

    summary = {
        "status": "passed" if not errors else "failed",
        "commercial": commercial_result,
        "research": research_result,
        "shared_sources": sorted(commercial_sources & research_sources),
        "unique_sources": len(unique_sources),
        "path_isolation": "passed" if not any(message.startswith("路径隔离失败") for message in errors) else "failed",
        "errors": errors,
        "note": "通过仅表示结构、引用、配比和隔离有效；不代表许可、质量、去污或训练门禁已签署。",
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        if errors:
            print(f"配方校验失败，共 {len(errors)} 项：", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print("两套配方校验通过：8＋10 个数据项、5＋5 个 profile、16 个唯一来源。")
            print("40 位 revision、config/split、权重、canonical 引用及路径隔离均通过。")
            print("注意：真实签署门禁仍未完成，本结果不是开训授权。")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
