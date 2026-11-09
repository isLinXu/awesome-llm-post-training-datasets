#!/usr/bin/env python3
"""Fetch compact official Hugging Face metadata and card excerpts for review."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent
REPOS = [
    "nvidia/OpenMathInstruct-2",
    "nvidia/OpenCodeInstruct",
    "m-a-p/CodeFeedback-Filtered-Instruction",
    "nvidia/HelpSteer3",
    "allenai/llama-3.1-tulu-3-8b-preference-mixture",
    "nvidia/Nemotron-Cascade-2-RL-data",
    "Skywork/Skywork-SynPref-40M",
    "Nanbeige/ToolMind",
    "argilla/ifeval-like-data",
    "akoksal/LongForm",
    "databricks/databricks-dolly-15k",
    "openai/webgpt_comparisons",
    "openai/summarize_from_feedback",
    "KbsdJames/Omni-MATH",
    "Idavidrein/gpqa",
    "HuggingFaceH4/mt_bench_prompts",
    "allenai/reward-bench-2",
    "sorry-bench/sorry-bench-202503",
    "ServiceNow-AI/M2Lingual",
    "Congliu/Chinese-DeepSeek-R1-Distill-data-110k",
    "AmazonScience/FalseReject",
    "BytedTsinghua-SIA/Enigmata-Data",
    "BytedTsinghua-SIA/Enigmata-Eval",
    "McGill-NLP/WebLINX",
    "ssmisya/PRMBench",
    "NVIDIA/RULER",
    "bigcode-project/bigcodebench",
    "ai-safety-institute/AgentHarm",
    "centerforaisafety/HarmBench",
    "dsbowen/strong_reject",
    "ethz-spylab/agentdojo",
]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dataset-gap-review/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read()


def fetch(repo):
    encoded = urllib.parse.quote(repo, safe="/")
    result = {"repo": repo}
    try:
        info = json.loads(get(f"https://huggingface.co/api/datasets/{encoded}"))
        result["metadata"] = {
            key: info.get(key)
            for key in ("id", "sha", "lastModified", "private", "gated", "tags", "cardData")
        }
    except Exception as exc:
        result["metadata_error"] = str(exc)
    try:
        text = get(f"https://huggingface.co/datasets/{encoded}/resolve/main/README.md").decode("utf-8")
        result["readme"] = text[:24000]
        result["readme_truncated"] = len(text) > 24000
    except Exception as exc:
        result["readme_error"] = str(exc)
    return result


with ThreadPoolExecutor(max_workers=5) as pool:
    records = list(pool.map(fetch, REPOS))
(ROOT / "official-cards.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
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
        "size_categories": card.get("size_categories"),
        "configs": card.get("configs"),
        "readme_chars": len(record.get("readme", "")),
    }, ensure_ascii=False))
