#!/usr/bin/env python3
from pathlib import Path
import json
import yaml

ROOT = Path(__file__).resolve().parents[1]
IDS = {
    "tulu3_sft_mixture", "aya_dataset", "openmath_reasoning", "tulu3_persona_if",
    "longcite_45k", "opencodeinstruct", "helpsteer3_preference", "dapo_math_17k",
    "opencode_reasoning", "chinese_r1_distill_110k", "m2lingual", "longform",
    "weblinx", "falsereject_train", "tulu3_preference_mixture", "enigmata_data",
}
doc = yaml.safe_load((ROOT / "datasets-list.yaml").read_text(encoding="utf-8"))
state = json.loads((ROOT / "data/dataset-catalog-state.json").read_text(encoding="utf-8"))
repos = state["repositories"]
for item in doc["datasets"]:
    if item["id"] not in IDS:
        continue
    repo = item["source"]["repo_id"]
    record = repos.get(repo, {})
    current = record.get("current", {})
    card = current.get("card_data") or {}
    print(json.dumps({
        "id": item["id"], "repo": repo, "split": item["source"]["split"],
        "tier": item["usage_tier"], "status": item["license"]["commercial_status"],
        "format": item["data_format"], "sha": current.get("sha"),
        "gated": current.get("gated"), "last_modified": current.get("last_modified"),
        "configs": card.get("configs"), "license": current.get("license"),
        "asset_ids": record.get("asset_ids"),
    }, ensure_ascii=False))
missing = IDS - {item["id"] for item in doc["datasets"]}
if missing:
    raise SystemExit(f"Missing IDs: {sorted(missing)}")
