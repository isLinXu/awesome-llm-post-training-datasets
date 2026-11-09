#!/usr/bin/env python3
"""Plot verified usage-tier counts from the canonical YAML and the recorded previous baseline."""
from collections import Counter
from pathlib import Path
import yaml
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
doc = yaml.safe_load((ROOT / "datasets-list.yaml").read_text(encoding="utf-8"))
current = Counter(x["usage_tier"] for x in doc["datasets"])
previous = {"core": 19, "optional": 31, "research_only": 10, "eval_only": 13, "local_required": 5}
tiers = ["core", "optional", "research_only", "eval_only", "local_required"]
labels = ["Core", "Optional", "Research only", "Eval only", "Local required"]
old = [previous[x] for x in tiers]
new = [current[x] for x in tiers]
assert sum(old) == 78 and sum(new) == 114

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
fig, ax = plt.subplots(figsize=(10, 5.4), dpi=180)
x = np.arange(len(tiers))
width = 0.36
bars1 = ax.bar(x - width / 2, old, width, label="Previous (78)", color="#A8B3C2")
bars2 = ax.bar(x + width / 2, new, width, label="Current (114)", color="#2563EB")
ax.set_title("Dataset catalogue growth by usage tier", fontsize=15, weight="bold", pad=14)
ax.set_ylabel("Number of assets")
ax.set_xticks(x, labels)
ax.set_ylim(0, max(new) + 9)
ax.grid(axis="y", alpha=0.18, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.legend(frameon=False, loc="upper left")
ax.bar_label(bars1, padding=3, color="#526071")
ax.bar_label(bars2, padding=3, color="#173F8A", weight="bold")
fig.text(0.99, 0.01, "Source: datasets-list.yaml; previous baseline recorded in the gap review", ha="right", fontsize=8, color="#64748B")
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(ROOT / "research" / "datasets-tier-comparison.png", bbox_inches="tight")
print("Wrote research/datasets-tier-comparison.png")
