#!/usr/bin/env python3
"""Render compact counts and schemas from the official multimodal card snapshot."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
records = json.loads((ROOT / "multimodal-official-cards.json").read_text(encoding="utf-8"))
summary = []
for record in records:
    meta = record.get("metadata", {})
    card = meta.get("cardData") or {}
    info = meta.get("dataset_info") or card.get("dataset_info") or {}
    infos = info if isinstance(info, list) else [info]
    splits = []
    features = []
    for entry in infos:
        if not isinstance(entry, dict):
            continue
        config = entry.get("config_name", "default")
        for split in entry.get("splits") or []:
            splits.append({
                "config": config,
                "name": split.get("name"),
                "num_examples": split.get("num_examples"),
            })
        if not features and isinstance(entry.get("features"), list):
            features = [{"name": x.get("name"), "dtype": x.get("dtype")} for x in entry["features"] if isinstance(x, dict)]
    summary.append({
        "repo": record["repo"],
        "error": record.get("metadata_error"),
        "sha": meta.get("sha"),
        "last_modified": meta.get("lastModified"),
        "gated": meta.get("gated"),
        "license": card.get("license"),
        "splits": splits,
        "features": features,
    })
(ROOT / "multimodal-metadata-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
rendered = []
for item in summary:
    counts = ", ".join(f"{x['config']}/{x['name']}={x['num_examples']}" for x in item["splits"][:12])
    if len(item["splits"]) > 12:
        counts += f", ... {len(item['splits']) - 12} more"
    fields = ", ".join(x["name"] for x in item["features"] if x.get("name"))
    rendered.append(
        f"{item['repo']}\n"
        f"  error={item['error']} license={item['license']} gated={item['gated']}\n"
        f"  counts={counts or 'unavailable'}\n"
        f"  fields={fields or 'unavailable'}"
    )
text = "\n\n".join(rendered) + "\n"
(ROOT / "multimodal-metadata-summary.txt").write_text(text, encoding="utf-8")
print(text, end="")
