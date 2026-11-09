#!/usr/bin/env python3
"""Plot multimodal coverage from the final canonical YAML; never hard-code totals."""
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
DOC = yaml.safe_load((ROOT / "datasets-list.yaml").read_text(encoding="utf-8"))
MM = yaml.safe_load((ROOT / "datasets-multimodal.yaml").read_text(encoding="utf-8"))
assets = MM["datasets"]
modalities = ["text", "image", "video", "audio"]
groups = {
    "Training/research": [x for x in assets if x["usage_tier"] not in {"eval_only", "local_required"}],
    "Evaluation": [x for x in assets if x["usage_tier"] == "eval_only"],
    "Local required": [x for x in assets if x["usage_tier"] == "local_required"],
}
colors = {"Training/research": "#3973ac", "Evaluation": "#e07a3f", "Local required": "#5b9a68"}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7), gridspec_kw={"width_ratios": [1, 1.45]})
bottom = np.zeros(len(modalities))
for group, rows in groups.items():
    counts = Counter(modality for row in rows for modality in row["modalities"])
    values = np.array([counts[m] for m in modalities])
    ax1.bar(modalities, values, bottom=bottom, label=f"{group} ({len(rows)})", color=colors[group])
    for index, (base, value) in enumerate(zip(bottom, values)):
        if value:
            ax1.text(index, base + value / 2, str(value), ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    bottom += values
ax1.set_title("Multimodal extension by modality membership")
ax1.set_ylabel("Assets (multi-modal assets counted in each modality)")
ax1.legend(frameon=False, loc="upper right")
ax1.spines[["top", "right"]].set_visible(False)

coverage = MM["coverage_requirements"]
capabilities = list(coverage)
training = [len(coverage[c]["training_candidates"]) for c in capabilities]
evaluation = [len(coverage[c]["eval_ids"]) for c in capabilities]
y = np.arange(len(capabilities))
ax2.barh(y + 0.18, training, height=0.34, color="#3973ac", label="Training candidates")
ax2.barh(y - 0.18, evaluation, height=0.34, color="#e07a3f", label="Evaluation references")
ax2.set_yticks(y, capabilities)
ax2.invert_yaxis()
ax2.set_xlabel("Referenced assets")
ax2.set_title("Required capability coverage")
ax2.legend(frameon=False, loc="lower right")
ax2.spines[["top", "right"]].set_visible(False)
ax2.grid(axis="x", alpha=0.18)

fig.suptitle(f"Post-training multimodal extension: {len(assets)} assets, {len(coverage)} capabilities", fontsize=16, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.96))
out = ROOT / "research" / "multimodal-asset-coverage.png"
fig.savefig(out, dpi=180, bbox_inches="tight")
print(out)
