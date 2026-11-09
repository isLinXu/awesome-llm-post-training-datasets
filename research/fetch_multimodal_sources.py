#!/usr/bin/env python3
"""Fetch official Hugging Face metadata for multimodal curation; no samples are downloaded."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
REPOS = [
    "liuhaotian/LLaVA-Instruct-150K",
    "mvp-lab/LLaVA-OneVision-1.5-Instruct-Data",
    "HuggingFaceM4/FineVision",
    "allenai/pixmo-ask-model-anything",
    "allenai/pixmo-points",
    "allenai/pixmo-point-explanations",
    "allenai/pixmo-docs",
    "allenai/pixmo-count",
    "allenai/pixmo-cap-qa",
    "TIGER-Lab/Mantis-Instruct",
    "lmms-lab/LLaVA-Video-178K",
    "OpenGVLab/VideoChat-Flash-Training-Data",
    "allenai/Molmo2-VideoTrack",
    "allenai/Molmo2-VideoPoint",
    "zhiqings/LLaVA-Human-Preference-10K",
    "openbmb/RLAIF-V-Dataset",
    "MMInstruction/VLFeedback",
    "YiyangAiLab/POVID_preference_data_for_VLLMs",
    "Fancy-MLLM/R1-Onevision",
    "OS-Copilot/OS-Atlas-Data",
    "google-research-datasets/android_control",
    "hflqf88888/GUIOdyssey",
    "gpt-omni/VoiceAssistant-400K",
    "ys-zong/VLGuard",
    "yxwang/SafeVid-350K",
    "MMMU/MMMU",
    "MMMU/MMMU_Pro",
    "AI4Math/MathVista",
    "MathLLMs/MathVision",
    "lmms-lab/DocVQA",
    "lmms-lab/ChartQA",
    "lmms-lab/OCRBench",
    "lmms-lab/MMStar",
    "lmms-lab/BLINK",
    "TIGER-Lab/Mantis-Eval",
    "lmms-lab/Video-MME",
    "MLVU/MLVU",
    "longvideobench/LongVideoBench",
    "MMInstruction/VL-RewardBench",
    "zhiqings/VL-RewardBench",
    "OS-Copilot/ScreenSpot-v2",
    "CMMMU-Benchmark/CMMMU",
    "FlagOpen/CMMU",
    "opencompass/MMBench",
    "AudioLLMs/MMAU",
    "AudioLLMs/AudioBench",
    "qyang1021/AIR-Bench-Dataset",
    "hlt-lab/voicebench",
]


def get(url):
    headers = {"User-Agent": "multimodal-dataset-curation/1.0"}
    if os.environ.get("HF_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['HF_TOKEN']}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()


def fetch(repo):
    encoded = urllib.parse.quote(repo, safe="/")
    result = {"repo": repo}
    try:
        info = json.loads(get(f"https://huggingface.co/api/datasets/{encoded}"))
        result["metadata"] = {
            key: info.get(key)
            for key in (
                "id", "sha", "lastModified", "private", "gated", "tags", "description",
                "cardData", "configs", "dataset_info",
            )
        }
    except Exception as exc:
        result["metadata_error"] = str(exc)
    try:
        text = get(f"https://huggingface.co/datasets/{encoded}/resolve/main/README.md").decode("utf-8")
        result["readme"] = text[:40000]
        result["readme_truncated"] = len(text) > 40000
    except Exception as exc:
        result["readme_error"] = str(exc)
    return result


def main():
    with ThreadPoolExecutor(max_workers=6) as pool:
        records = list(pool.map(fetch, REPOS))
    (ROOT / "multimodal-official-cards.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for record in records:
        metadata = record.get("metadata", {})
        card = metadata.get("cardData") or {}
        print(json.dumps({
            "repo": record["repo"],
            "metadata_error": record.get("metadata_error"),
            "readme_error": record.get("readme_error"),
            "sha": metadata.get("sha"),
            "gated": metadata.get("gated"),
            "license": card.get("license"),
            "configs": card.get("configs") or metadata.get("configs"),
            "readme_chars": len(record.get("readme", "")),
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
