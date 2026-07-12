from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "artifacts" / "paper_results.json"
OUT = ROOT / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
data = json.loads(RESULTS.read_text())

fig, ax = plt.subplots(figsize=(7.2, 2.8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 4)
ax.axis("off")
boxes = [
    (0.3, 2.2, 2.0, 1.0, "Observable context\n14 signals + category"),
    (3.0, 2.2, 2.0, 1.0, "Layer 1\nPWL problem scores"),
    (5.7, 2.2, 2.0, 1.0, "Layer 2\nNamed GAM scores"),
    (8.4, 2.2, 2.0, 1.0, "Greedy set composer\n6 of 22 modules"),
    (5.7, 0.3, 2.0, 1.0, "Delayed aggregate reward\nnoise + return window"),
    (8.4, 0.3, 2.0, 1.0, "Offline update\nobservable editor / SGD"),
]
for x, y, width, height, label in boxes:
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height, boxstyle="round,pad=0.03", linewidth=1.2, fill=False
        )
    )
    ax.text(x + width / 2, y + height / 2, label, ha="center", va="center", fontsize=9)


def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.2))


arrow(2.3, 2.7, 3.0, 2.7)
arrow(5.0, 2.7, 5.7, 2.7)
arrow(7.7, 2.7, 8.4, 2.7)
arrow(9.4, 2.2, 7.0, 1.3)
arrow(7.7, 0.8, 8.4, 0.8)
arrow(9.4, 1.3, 6.7, 2.2)
arrow(10.4, 2.7, 11.7, 2.7)
ax.text(11.0, 2.95, "served page", ha="center", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "architecture.pdf", bbox_inches="tight")
plt.close(fig)

methods = data["held_out_primary"]
items = [
    ("Observable editor + SGD", "observable_editor_sgd"),
    ("LinTS warm, validation-selected alpha", "lints_warm_validation_selected"),
    ("Observable editor", "observable_editor"),
    ("EDP-SGD, LLM init, no editor", "edp_sgd_llm_init_no_editor"),
    ("Static LLM prior", "static_llm_prior"),
    ("LinTS warm, default alpha", "lints_warm_default"),
    ("EDP-SGD, random coefficients", "edp_sgd_random_coeff_no_editor"),
]
labels = [item[0] for item in items]
values = np.asarray([methods[item[1]]["mean_pct"] for item in items])
errors = np.asarray([methods[item[1]]["sem_pct"] for item in items])
y = np.arange(len(labels))
fig, ax = plt.subplots(figsize=(7.0, 4.2))
ax.barh(y, values, xerr=errors, capsize=3)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("Loss vs clairvoyant exact oracle (%)")
ax.grid(axis="x", alpha=0.3)
for index, value in zip(y, values):
    ax.text(value + 0.4, index, f"{value:.1f}", va="center", fontsize=8)
ax.set_xlim(0, max(values) + 4)
fig.tight_layout()
fig.savefig(OUT / "heldout.pdf", bbox_inches="tight")
plt.close(fig)

cold = data.get("cold_start_stream42", data.get("cold_start_seed42_sensitivity"))
sessions = np.asarray(cold["sessions"])
static = cold["static_llm_prior"]
lints = cold["lints_warm_alpha_005"]
fig, ax = plt.subplots(figsize=(6.9, 3.4))
ax.plot(sessions, static, marker="o", label="Static LLM prior")
ax.plot(sessions, lints, marker="o", label="LinTS warm, alpha=0.05")
ax.set_xlabel("Sessions")
ax.set_ylabel("Loss vs clairvoyant oracle (%)")
ax.set_xticks(sessions)
ax.set_xticklabels(["0.5k", "1k", "2.5k", "5k", "7.5k", "10k"])
ax.grid(True, alpha=0.3)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "coldstart.pdf", bbox_inches="tight")
plt.close(fig)
