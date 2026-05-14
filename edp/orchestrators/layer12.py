"""
Layer-1 + Layer-2 evolution orchestrator. Same as ReportOrchestrator but
the agent's prompt also exposes the Layer-1 PWL shapes and the agent can
emit `shape_edits` in addition to (Layer-2) `edits`.
"""
from __future__ import annotations
import json

from edp import N_SLOTS, WIDGETS, TRUE_NEEDS, CATEGORIES
from edp.catalog import CATEGORY_NEED_MULTIPLIERS, TRUE_PROVISIONS
from edp.policies.edp import make_problem_shapes
from edp.orchestrators.report import ReportOrchestrator
from edp.orchestrators.base import cli_main


LAYER12_PROMPT_TEMPLATE = '''\
You are an EDP evolution agent. You can edit BOTH layers of the EDP policy.

# Architecture (recap)

EDP composes a 6-slot page by greedy submodular selection over 22 widgets.
Two layers process each session:

**Layer 1 — PWL problem detection.** 14 raw signals → 7-d problem
fingerprint. Each problem `F` is a weighted average of piecewise-linear
shape functions over its relevant signals:

  problem_F = sum_sig (weight_F_sig · pwl(feat_sig, bps, vals)) / sum_weight

You can edit:
- `weight` (the signal's contribution weight to the problem)
- `vals.<i>` (i-th breakpoint value, in [0, 1])
- `bps.<i>` (i-th breakpoint position, must stay monotonic in [0, 1])

You may NOT delete signals or add new ones.

**Layer 2 — module GAM + greedy composition.** Per-widget score:

  score(widget, slot) = base
                      + sum_p on_rem[p] * remaining[p]
                      + sum_p on_cov[p] * coverage[p]
                      - slot_decay * slot

You can edit `base`, `slot_decay`, `on_rem.<problem>`, `on_cov.<problem>`.
You may NOT change `addr` (a fixed content property).

# Reference data

Problems: F32 Size Anxiety, F33 Quality Signal Deficit, F41 Comparison
Friction, F43 Outfit Visualization, F45 Price-Quality Confusion,
F46 Return Hesitation, F51 Decision Paralysis.

Persona base-need vectors:
{persona_needs}

Fashion-category need multipliers (each session is a (persona, category)
pair; effective need = persona_need * category_multiplier):
{category_mult}

Widget true provisions (use as priors):
{widget_provs}

# Current Layer-1 PWL shapes (editable)

```json
{shapes_json}
```

# Current Layer-2 modules (editable)

```json
{modules_json}
```

# Edit history so far

{edit_history}

# Latest checkpoint report

```
{report}
```

# Your task

Propose two batches of atomic edits in ONE JSON file. Both batches are
optional — you can emit only Layer-2 edits if Layer-1 looks fine, or
only Layer-1 edits if the issue is mis-detection rather than mis-routing.

Layer-1 edits are appropriate when the report shows a persona with high
regret AND the persona's true needs (above) include dimensions that
should map to a problem the current PWL is under-detecting. Examples:

- A persona who heavily uses size_chart but isn't getting size-relevant
  widgets → maybe F32's `size_chart.weight` is too low or `vals` rises
  too slowly.
- A premium-product session not getting quality content → maybe F33's
  `zoom.vals` saturates too low.
- An indecisive persona not getting decision-support → maybe F51's
  `cart_osc.vals` needs a steeper curve.

Layer-2 edits are appropriate for: dead widgets, over-firing defaults,
synergy chains, slot-decay tuning. (See prior agent guidance.)

Aim for 8–14 total edits across both layers. Heuristic: 70/30 split with
Layer-2 carrying most of the batch unless you specifically diagnose a
Layer-1 mis-detection.

# Output format

Write a JSON file at `{out_path}` with this shape:

```json
{{
  "note": "round X — short one-line rationale",
  "edits": [
    {{"widget": "return_explainer", "path": "base", "from": 0.05, "to": 0.15, "reason": "..."}},
    {{"widget": "easy_returns_promise", "path": "on_cov.F46", "from": 0.0, "to": 1.0, "reason": "..."}}
  ],
  "shape_edits": [
    {{"problem": "F32", "signal": "size_chart", "path": "weight", "from": 0.45, "to": 0.55, "reason": "size_anxious_new under-detected"}},
    {{"problem": "F32", "signal": "size_chart", "path": "vals.2", "from": 0.45, "to": 0.55, "reason": "steeper rise at mid-range"}}
  ]
}}
```

Constraints:
- ONLY write that one JSON file.
- Layer-2 paths: `base`, `slot_decay`, `on_rem.<F-code>`, `on_cov.<F-code>`. Range -1.5 to 2.8.
- Layer-1 paths: `weight` (≥ 0, typical 0.1-0.7), `vals.<i>` (∈ [0, 1]), `bps.<i>` (∈ [0, 1], monotonic).
- One-sentence `reason` on each edit.
- Final message in chat (under 80 words): which Layer-1 mis-detection (if any) you targeted, plus your top-3 most-impactful Layer-2 edits.
'''


class Layer12Orchestrator(ReportOrchestrator):

    def render_prompt(self, state, batch_start, batch_end, report_text, out_path):
        # Re-use the parent's persona/category/widget priors blocks.
        persona_lines = []
        for p, needs in TRUE_NEEDS.items():
            top = sorted(needs.items(), key=lambda x: -x[1])[:3]
            persona_lines.append(f'- {p}: ' + ', '.join(f'{k}={v:.2f}' for k, v in top))
        persona_needs = '\n'.join(persona_lines)

        cat_lines = []
        for c in CATEGORIES:
            mult = CATEGORY_NEED_MULTIPLIERS[c]
            top = sorted(mult.items(), key=lambda x: -x[1])[:3]
            cat_lines.append(f'- {c}: ' + ', '.join(f'{k}×{v:.2f}' for k, v in top))
        category_mult = '\n'.join(cat_lines)

        prov_lines = []
        for w, prov in TRUE_PROVISIONS.items():
            if not prov:
                continue
            top = sorted(prov.items(), key=lambda x: -x[1])[:3]
            prov_lines.append(f'- {w}: ' + ', '.join(f'{k}={v:.2f}' for k, v in top))
        widget_provs = '\n'.join(prov_lines)

        shapes = state.get('shapes') or make_problem_shapes()

        if state['edit_history']:
            edit_history = '\n'.join(
                f'  - session {h["session"]}: {h["count"]} edits '
                f'({h.get("module_count", "?")} module + {h.get("shape_count", 0)} shape) '
                f'— {h["note"]}'
                for h in state['edit_history']
            )
        else:
            edit_history = '  (none — baseline run)'

        return LAYER12_PROMPT_TEMPLATE.format(
            persona_needs=persona_needs,
            category_mult=category_mult,
            widget_provs=widget_provs,
            shapes_json=json.dumps(shapes, indent=2),
            modules_json=json.dumps(state['modules'], indent=2),
            edit_history=edit_history,
            report=report_text,
            out_path=out_path,
        )


if __name__ == '__main__':
    cli_main(Layer12Orchestrator)
