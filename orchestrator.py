"""
Orchestrator for live agent-driven EDP evolution.

Workflow:
  1. orchestrator.py --reset --until 2500
        -> simulates with EDP-static
        -> writes evolve_state/state.json and evolve_state/report_at_2500.md
        -> ALSO writes evolve_state/AGENT_PROMPT_at_2500.md (input for subagent)
  2. A Claude subagent (or human) reads the report + prompt, writes
        evolve_state/edits_round_2500.json
  3. orchestrator.py --apply evolve_state/edits_round_2500.json --until 5000
  4. repeat for 7500, 10000.

State is delay/noise-aware: the policy state at session i has only been
informed by edits proposed from reports at sessions <= i - delay - margin.
For determinism, edits arrive INSTANTLY in the schedule -- the realistic
interpretation is that the report itself is built from logs whose reward
has already been observed (i.e. the orchestrator only runs out to a
checkpoint where it has reward data for everything up to that point).

This separation makes the live-agent path purely about WHO writes the JSON.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import numpy as np
from collections import Counter, defaultdict

from sim import (N_SLOTS, ORACLE_REWARDS, make_session_stream,
                 true_page_reward, WIDGETS, TRUE_NEEDS)
from policy_edp import (EDPPolicy, make_problem_shapes, make_modules,
                        apply_edits, score_problems, PROBLEMS, PROBLEM_NAMES)

STATE_DIR = 'evolve_state'
os.makedirs(STATE_DIR, exist_ok=True)


# ---------- State persistence ----------
def state_path():
    return os.path.join(STATE_DIR, 'state.json')


def load_state():
    if not os.path.exists(state_path()):
        return {
            'session_idx': 0,
            'modules': make_modules(),
            'rewards': [],
            'oracle': [],
            'recent_logs': [],   # only the last batch (cleared on each run_batch)
            'edit_history': [],
        }
    with open(state_path()) as f:
        return json.load(f)


def save_state(state):
    with open(state_path(), 'w') as f:
        json.dump(state, f)


# ---------- Batch run ----------
def run_batch(state, until_idx, seed=42):
    stream = make_session_stream(until_idx, seed=seed)
    policy = EDPPolicy(modules=state['modules'])
    rewards = list(state['rewards'])
    oracle = list(state['oracle'])
    new_logs = []
    start = state['session_idx']
    for i in range(start, until_idx):
        persona, feat = stream[i]
        page = policy.select_page(feat)
        r = true_page_reward(persona, page)
        rewards.append(r)
        oracle.append(ORACLE_REWARDS[persona])
        new_logs.append({
            'i': i,
            'persona': persona,
            'page': page,
            'reward': round(r, 4),
            'oracle': round(ORACLE_REWARDS[persona], 4),
            'regret': round(ORACLE_REWARDS[persona] - r, 4),
        })
    state['session_idx'] = until_idx
    state['rewards'] = rewards
    state['oracle'] = oracle
    state['recent_logs'] = new_logs
    return state


# ---------- Report generation (the input the agent reads) ----------
def make_report(state, batch_start, batch_end) -> str:
    logs = state['recent_logs']
    n = len(logs)
    wid_act = Counter()
    wid_reward = defaultdict(float)
    wid_slot_hist = defaultdict(Counter)
    pers_total_r = defaultdict(float)
    pers_total_o = defaultdict(float)
    pers_count = Counter()
    pers_wid_count = defaultdict(Counter)
    for L in logs:
        p = L['persona']
        pers_count[p] += 1
        pers_total_r[p] += L['reward']
        pers_total_o[p] += L['oracle']
        # We only logged page-level reward; per-slot reward not tracked here.
        # Distribute equally for the "reward/fire" approximation.
        per_slot = L['reward'] / N_SLOTS
        for slot, w in enumerate(L['page']):
            wid_act[w] += 1
            wid_reward[w] += per_slot
            wid_slot_hist[w][slot] += 1
            pers_wid_count[p][w] += 1

    rep = []
    rep.append(f'# EDP CHECKPOINT REPORT — sessions {batch_start} → {batch_end}  (N={n})')
    rep.append('')
    rep.append('## Aggregate performance')
    rew = np.array([L['reward'] for L in logs])
    orc = np.array([L['oracle'] for L in logs])
    reg = orc - rew
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
    rep.append('## Widget activation rate (% of all slots filled) and avg-slot-reward')
    rep.append(f'  {"widget":25s} {"act%":>6s}  {"avg_slot":>8s}  {"r/fire":>8s}')
    total_slots = n * N_SLOTS
    wrows = []
    for w in WIDGETS:
        c = wid_act[w]
        if c == 0:
            wrows.append((w, 0.0, 0.0, 0.0))
        else:
            avg_slot = sum(s * v for s, v in wid_slot_hist[w].items()) / c + 1
            wrows.append((w, c / total_slots * 100, avg_slot, wid_reward[w] / c))
    wrows.sort(key=lambda x: -x[1])
    for w, ap, asl, rf in wrows:
        rep.append(f'  {w:25s} {ap:6.1f}  {asl:8.2f}  {rf:8.4f}')

    rep.append('')
    rep.append('## Top 5 widgets per persona (composition signature)')
    for p, _, _, _, _ in rows:
        top = sorted(pers_wid_count[p].items(), key=lambda x: -x[1])[:5]
        sig = ', '.join(f'{w}({c})' for w, c in top)
        rep.append(f'  {p:22s}  {sig}')

    rep.append('')
    rep.append('## Edit history applied so far')
    if not state['edit_history']:
        rep.append('  (none — this is the baseline run)')
    else:
        for h in state['edit_history']:
            rep.append(f'  - session {h["session"]}: {h["count"]} edits ({h["note"]})')

    return '\n'.join(rep)


# ---------- Agent prompt (what the subagent sees) ----------
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

# Persona ground-truth needs (LLM-authored; you can use these as priors)

{persona_needs}

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
- Dead widgets (activation 0%%) that should fire for those personas
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `{out_path}` with this exact shape:

```json
{{
  "note": "round X — short one-line rationale for the batch",
  "edits": [
    {{"widget": "return_explainer", "path": "base", "from": 0.05, "to": 0.15, "reason": "F46 underserved, 0% activation"}},
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


def render_agent_prompt(state, batch_start, batch_end, report_text, out_path):
    persona_lines = []
    for p, needs in TRUE_NEEDS.items():
        top = sorted(needs.items(), key=lambda x: -x[1])[:3]
        persona_lines.append(f'- {p}: ' + ', '.join(f'{k}={v:.2f}' for k, v in top))
    persona_needs = '\n'.join(persona_lines)

    from sim import TRUE_PROVISIONS
    prov_lines = []
    for w, prov in TRUE_PROVISIONS.items():
        if not prov:
            continue
        top = sorted(prov.items(), key=lambda x: -x[1])[:3]
        prov_lines.append(f'- {w}: ' + ', '.join(f'{k}={v:.2f}' for k, v in top))
    widget_provs = '\n'.join(prov_lines)

    hist_lines = []
    if state['edit_history']:
        for h in state['edit_history']:
            hist_lines.append(f'  - session {h["session"]}: {h["count"]} edits — {h["note"]}')
    else:
        hist_lines = ['  (none — baseline run)']
    edit_history = '\n'.join(hist_lines)

    return AGENT_PROMPT_TEMPLATE.format(
        persona_needs=persona_needs,
        widget_provs=widget_provs,
        modules_json=json.dumps(state['modules'], indent=2),
        edit_history=edit_history,
        report=report_text,
        out_path=out_path,
    )


# ---------- Edit application ----------
def apply_edits_from_file(state, path):
    with open(path) as f:
        data = json.load(f)
    edit_tuples = []
    for e in data['edits']:
        edit_tuples.append((e['widget'], e['path'], e.get('from', 0.0),
                             e['to'], e.get('reason', '')))
    state['modules'] = apply_edits(state['modules'], edit_tuples)
    state['edit_history'].append({
        'session': state['session_idx'],
        'count': len(edit_tuples),
        'note': data.get('note', ''),
    })
    return state


# ---------- CLI ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--until', type=int, required=True)
    ap.add_argument('--apply', type=str, default=None, help='edits JSON path')
    ap.add_argument('--reset', action='store_true')
    ap.add_argument('--seed', type=int, default=42)
    args = ap.parse_args()

    if args.reset and os.path.exists(state_path()):
        os.remove(state_path())

    state = load_state()
    batch_start = state['session_idx']

    if args.apply:
        if batch_start == 0:
            print('Cannot apply edits before any sessions have run.')
            sys.exit(1)
        state = apply_edits_from_file(state, args.apply)
        print(f'Applied edits from {args.apply}.')

    state = run_batch(state, args.until, seed=args.seed)
    report = make_report(state, batch_start, args.until)
    rpt_path = os.path.join(STATE_DIR, f'report_at_{args.until}.md')
    with open(rpt_path, 'w') as f:
        f.write(report)
    save_state(state)

    # Agent prompt (input for the subagent)
    next_edits = os.path.join(STATE_DIR, f'edits_round_{args.until}.json')
    prompt = render_agent_prompt(state, batch_start, args.until, report, next_edits)
    prompt_path = os.path.join(STATE_DIR, f'AGENT_PROMPT_at_{args.until}.md')
    with open(prompt_path, 'w') as f:
        f.write(prompt)

    print(report)
    print()
    print(f'[state saved      → {state_path()}]')
    print(f'[report saved     → {rpt_path}]')
    print(f'[agent prompt     → {prompt_path}]')
    print(f'[expected edits   → {next_edits}]')

    # Summary metrics for the comparison
    rewards = np.array(state['rewards'])
    oracle = np.array(state['oracle'])
    cr = (oracle - rewards).cumsum()
    print(f'\nCum regret so far @ session {state["session_idx"]}: {cr[-1]:.2f}')


if __name__ == '__main__':
    main()
