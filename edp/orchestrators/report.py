"""
Report-based orchestrator: at each checkpoint, generate a structured
diagnostic report (per-persona regret, per-category regret, per-widget
activation, composition signature) for the agent to read.
"""
from __future__ import annotations
import json
from collections import Counter, defaultdict

import numpy as np

from edp import N_SLOTS, WIDGETS, TRUE_NEEDS, CATEGORIES
from edp.catalog import CATEGORY_NEED_MULTIPLIERS, TRUE_PROVISIONS
from edp.orchestrators.base import Orchestrator, cli_main


AGENT_PROMPT_TEMPLATE = '''\
You are an EDP evolution agent. Your job is to read a session-log report and
propose a batch of small, atomic code edits to the module configuration that
should reduce regret on the next batch of sessions.

# Context

EDP composes a 6-slot page by greedy submodular selection over 22 widgets. A
widget's score for slot s is:

  score = base
        + sum_p on_rem[p] * remaining[p]
        + sum_p on_cov[p] * coverage[p]
        - slot_decay * s

where `remaining[p]` and `coverage[p]` are derived from a 7-d problem
fingerprint over F32/F33/F41/F43/F45/F46/F51.

Each widget also has `addr[p]` (how much placing it consumes from remaining
and adds to coverage). You CANNOT change `addr` (it is a content property);
you CAN change `base`, `on_rem.<problem>`, `on_cov.<problem>`, `slot_decay`.

# Problem reference (Layer 1 outputs)

- F32: Size Anxiety
- F33: Quality Signal Deficit
- F41: Comparison Friction
- F43: Outfit Visualization
- F45: Price-Quality Confusion
- F46: Return Hesitation
- F51: Decision Paralysis

# Persona base-need vectors (LLM-authored; you can use these as priors)

{persona_needs}

# Fashion-category need multipliers

Each session has both a persona and a fashion category (dress, top, bottoms,
shoes, outerwear, accessories). The persona's base needs are multiplied
element-wise by the category multiplier. So e.g. a `size_anxious_new`
shopper looking at shoes has even higher N1_fit than the same persona looking
at accessories.

{category_mult}

# Widget true provisions (LLM-authored; you can use these as priors)

{widget_provs}

# Current modules config

```json
{modules_json}
```

# Edit history so far

{edit_history}

# Latest report

```
{report}
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `{out_path}` with this exact shape:

```json
{{
  "note": "round X — short one-line rationale for the batch",
  "edits": [
    {{"widget": "return_explainer", "path": "base", "from": 0.05, "to": 0.15, "reason": "F46 underserved, 0%% activation on returner_anxious"}},
    {{"widget": "easy_returns_promise", "path": "on_cov.F46", "from": 0.0, "to": 1.0, "reason": "NEW synergy chains after return_explainer"}}
  ]
}}
```

Constraints:
- ONLY emit JSON; do not modify any other files.
- `path` must be one of: `base`, `slot_decay`, `on_rem.<F-code>`, `on_cov.<F-code>`.
- Numeric `to` values should be small-ish (typical range -1.5 to 2.8).
- Keep the batch tight — 8 to 16 edits is the sweet spot.
- Each edit should have a one-sentence `reason`.

When done, just write the file. Do not print the JSON to stdout.
'''


class ReportOrchestrator(Orchestrator):

    def make_report(self, state, batch_start, batch_end) -> str:
        logs = state['recent_logs']
        n = len(logs)

        wid_act = Counter()
        wid_reward = defaultdict(float)
        wid_slot_hist = defaultdict(Counter)
        pers_total_r = defaultdict(float)
        pers_total_o = defaultdict(float)
        pers_count = Counter()
        cat_total_r = defaultdict(float)
        cat_total_o = defaultdict(float)
        cat_count = Counter()
        pers_wid_count = defaultdict(Counter)
        # Per (persona, category) breakdown
        pc_total_r = defaultdict(float)
        pc_total_o = defaultdict(float)
        pc_count = Counter()

        for L in logs:
            p = L['persona']
            c = L['category']
            pers_count[p] += 1
            pers_total_r[p] += L['reward']
            pers_total_o[p] += L['oracle']
            cat_count[c] += 1
            cat_total_r[c] += L['reward']
            cat_total_o[c] += L['oracle']
            pc_count[(p, c)] += 1
            pc_total_r[(p, c)] += L['reward']
            pc_total_o[(p, c)] += L['oracle']
            per_slot = L['reward'] / N_SLOTS
            for slot, w in enumerate(L['page']):
                wid_act[w] += 1
                wid_reward[w] += per_slot
                wid_slot_hist[w][slot] += 1
                pers_wid_count[p][w] += 1

        rep = []
        rep.append(f'# EDP CHECKPOINT — sessions {batch_start} → {batch_end}  (N={n})')

        rew = np.array([L['reward'] for L in logs])
        orc = np.array([L['oracle'] for L in logs])
        reg = orc - rew
        rep.append('')
        rep.append('## Aggregate performance')
        rep.append(f'- mean reward:        {rew.mean():.4f}')
        rep.append(f'- mean oracle reward: {orc.mean():.4f}')
        rep.append(f'- mean regret:        {reg.mean():.4f}  '
                   f'({reg.mean()/orc.mean()*100:.1f}% of oracle)')
        rep.append(f'- cum regret (batch): {reg.sum():.2f}')

        rep.append('')
        rep.append('## Per-persona performance (sorted by regret %, worst first)')
        rows = []
        for p, c in pers_count.items():
            ar = pers_total_r[p] / c
            ao = pers_total_o[p] / c
            rows.append((p, c, ar, ao, (ao - ar) / ao * 100))
        rows.sort(key=lambda x: -x[4])
        rep.append(f'  {"persona":22s} {"N":>5s}  {"reward":>8s}  {"oracle":>8s}  {"regret%":>8s}')
        for p, c, ar, ao, rp in rows:
            rep.append(f'  {p:22s} {c:5d}  {ar:8.4f}  {ao:8.4f}  {rp:7.1f}%')

        rep.append('')
        rep.append('## Per-category performance (sorted by regret %, worst first)')
        crows = []
        for c, ct in cat_count.items():
            ar = cat_total_r[c] / ct
            ao = cat_total_o[c] / ct
            crows.append((c, ct, ar, ao, (ao - ar) / ao * 100))
        crows.sort(key=lambda x: -x[4])
        rep.append(f'  {"category":14s} {"N":>5s}  {"reward":>8s}  {"oracle":>8s}  {"regret%":>8s}')
        for c, ct, ar, ao, rp in crows:
            rep.append(f'  {c:14s} {ct:5d}  {ar:8.4f}  {ao:8.4f}  {rp:7.1f}%')

        rep.append('')
        rep.append('## Worst 8 (persona, category) cells by regret %')
        pcrows = []
        for (p, c), n_pc in pc_count.items():
            if n_pc < 5:
                continue
            ar = pc_total_r[(p, c)] / n_pc
            ao = pc_total_o[(p, c)] / n_pc
            pcrows.append((p, c, n_pc, ar, ao, (ao - ar) / max(ao, 1e-9) * 100))
        pcrows.sort(key=lambda x: -x[5])
        rep.append(f'  {"persona":22s} {"category":12s} {"N":>5s}  '
                   f'{"reward":>8s}  {"oracle":>8s}  {"regret%":>8s}')
        for p, c, n_pc, ar, ao, rp in pcrows[:8]:
            rep.append(f'  {p:22s} {c:12s} {n_pc:5d}  '
                       f'{ar:8.4f}  {ao:8.4f}  {rp:7.1f}%')

        rep.append('')
        rep.append('## Widget activation rate (% of all slots filled) and avg-slot-reward')
        rep.append(f'  {"widget":25s} {"act%":>6s}  {"avg_slot":>8s}  {"r/fire":>8s}')
        total_slots = n * N_SLOTS
        wrows = []
        for w in WIDGETS:
            cnt = wid_act[w]
            if cnt == 0:
                wrows.append((w, 0.0, 0.0, 0.0))
            else:
                avg_slot = sum(s * v for s, v in wid_slot_hist[w].items()) / cnt + 1
                wrows.append((w, cnt / total_slots * 100, avg_slot, wid_reward[w] / cnt))
        wrows.sort(key=lambda x: -x[1])
        for w, ap, asl, rf in wrows:
            rep.append(f'  {w:25s} {ap:6.1f}  {asl:8.2f}  {rf:8.4f}')

        rep.append('')
        rep.append('## Top 5 widgets per persona (composition signature)')
        for p, _, _, _, _ in rows:
            top = sorted(pers_wid_count[p].items(), key=lambda x: -x[1])[:5]
            sig = ', '.join(f'{w}({c_})' for w, c_ in top)
            rep.append(f'  {p:22s}  {sig}')

        rep.append('')
        rep.append('## Edit history applied so far')
        if not state['edit_history']:
            rep.append('  (none — this is the baseline run)')
        else:
            for h in state['edit_history']:
                rep.append(f'  - session {h["session"]}: {h["count"]} edits ({h["note"]})')

        return '\n'.join(rep)

    def render_prompt(self, state, batch_start, batch_end, report_text, out_path):
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

        if state['edit_history']:
            edit_history = '\n'.join(
                f'  - session {h["session"]}: {h["count"]} edits — {h["note"]}'
                for h in state['edit_history']
            )
        else:
            edit_history = '  (none — baseline run)'

        return AGENT_PROMPT_TEMPLATE.format(
            persona_needs=persona_needs,
            category_mult=category_mult,
            widget_provs=widget_provs,
            modules_json=json.dumps(state['modules'], indent=2),
            edit_history=edit_history,
            report=report_text,
            out_path=out_path,
        )


if __name__ == '__main__':
    cli_main(ReportOrchestrator)
