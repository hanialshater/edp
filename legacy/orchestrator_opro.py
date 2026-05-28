"""
OPRO-style ablation orchestrator.

Difference from `orchestrator.py`:

  - The agent sees ONLY a history of (edit_batch, resulting_batch_regret) pairs,
    sorted by score. No structured diagnostic report. No persona/widget tables.
  - The agent is told it is optimizing a black-box score and should propose a
    new edit batch that improves over the best in the history.

This is the Yang et al. 2023 "Optimization by PROmpting" framing applied to
EDP module-config updates as the action. It tests whether the structured
diagnostic report (the report-based agent's input) carries information that
pure score-conditioned proposing cannot recover.

State is persisted under opro_state/ so the two orchestrators don't collide.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import numpy as np

from sim import (N_SLOTS, make_session_stream, true_page_reward,
                 oracle_reward)
from policy_edp import EDPPolicy, make_modules, apply_edits

STATE_DIR = os.environ.get('EDP_STATE_DIR', '../state/opro_state')
os.makedirs(STATE_DIR, exist_ok=True)


def state_path():
    return os.path.join(STATE_DIR, 'state.json')


def load_state():
    if not os.path.exists(state_path()):
        return {
            'session_idx': 0,
            'modules': make_modules(),
            'rewards': [],
            'oracle': [],
            'edit_history': [],   # list of {round_id, applied_at, edits, batch_regret, cum_regret}
            'checkpoints': [],    # session indexes where edits were applied
        }
    with open(state_path()) as f:
        return json.load(f)


def save_state(state):
    with open(state_path(), 'w') as f:
        json.dump(state, f)


def run_batch(state, until_idx, seed=42):
    stream = make_session_stream(until_idx, seed=seed)
    policy = EDPPolicy(modules=state['modules'])
    rewards = list(state['rewards'])
    oracle = list(state['oracle'])
    start = state['session_idx']
    batch_reward = 0.0
    batch_oracle = 0.0
    for i in range(start, until_idx):
        persona, category, feat = stream[i]
        page = policy.select_page(feat)
        r = true_page_reward(persona, category, page)
        o = oracle_reward(persona, category)
        rewards.append(r)
        oracle.append(o)
        batch_reward += r
        batch_oracle += o
    state['session_idx'] = until_idx
    state['rewards'] = rewards
    state['oracle'] = oracle
    return state, (batch_oracle - batch_reward), batch_oracle


# ---------- Agent prompt (no diagnostic info -- just history of scores) ----------
OPRO_PROMPT_TEMPLATE = '''\
You are a black-box optimizer for an EDP module-config policy. You will see a
history of edit batches that have been tried, each annotated with the
batch-aggregate regret it produced. Lower regret = better.

You see NO diagnostic information beyond the (edits, score) pairs themselves.
You do NOT see per-persona regret breakdowns, widget activation rates, or
composition signatures. You must reason purely from patterns in the score
history.

# Action space

Each "solution" is a list of atomic edits over the module config. Each edit is:
- `widget`: one of 22 widget names (see below)
- `path`: `base`, `slot_decay`, `on_rem.<F-code>`, or `on_cov.<F-code>`
- `to`: numeric value, typical magnitude range -1.5 to 2.8
- `reason`: short string (treated as opaque tag — does NOT affect the score)

The 22 widgets are: {widget_list}
The 7 problems (F-codes) are: F32, F33, F41, F43, F45, F46, F51.

# History of attempts (sorted by score: best first)

{history_block}

# Current cumulative regret across all batches so far: {cum_regret:.2f}

# Your task

Propose a NEW edit batch of 8–16 edits that you predict will produce a LOWER
batch_regret than the best attempt above. Write it to `{out_path}` with this
exact shape:

```json
{{
  "note": "round X — one-line summary",
  "edits": [
    {{"widget": "...", "path": "...", "from": 0.0, "to": 0.0, "reason": "..."}}
  ]
}}
```

You can revisit edits from prior batches (with different values) or try
entirely different combinations. You are an optimizer; choose what to try
based on patterns you infer from the score history.

Output: write the JSON file. Do NOT print it back. Final message: under 80
words on your hypothesis for why this batch should improve over the best one.
'''


def render_opro_prompt(state, out_path):
    from policy_edp import make_modules as _mk
    widgets = list(_mk().keys())
    # Build history block, sorted by batch_regret ascending (best first).
    history = sorted(state['edit_history'], key=lambda h: h['batch_regret'])
    parts = []
    if not history:
        parts.append('(no prior attempts — this is the first round)')
    else:
        for h in history:
            parts.append(f'### attempt at session {h["applied_at"]}: batch_regret = {h["batch_regret"]:.2f}')
            parts.append('```json')
            parts.append(json.dumps({'edits': h['edits']}, indent=2))
            parts.append('```')
            parts.append('')
    history_block = '\n'.join(parts)

    cum_regret = sum(o - r for r, o in zip(state['rewards'], state['oracle']))

    return OPRO_PROMPT_TEMPLATE.format(
        widget_list=', '.join(widgets),
        history_block=history_block,
        cum_regret=cum_regret,
        out_path=out_path,
    )


def apply_edits_from_file(state, path, applied_at: int):
    with open(path) as f:
        data = json.load(f)
    edit_tuples = []
    for e in data['edits']:
        edit_tuples.append((e['widget'], e['path'], e.get('from', 0.0),
                             e['to'], e.get('reason', '')))
    state['modules'] = apply_edits(state['modules'], edit_tuples)
    # We append the entry with a placeholder regret; it will be filled after
    # the batch runs.
    state['edit_history'].append({
        'round_id': len(state['edit_history']) + 1,
        'applied_at': applied_at,
        'note': data.get('note', ''),
        'edits': data['edits'],
        'batch_regret': None,
    })
    state['checkpoints'].append(applied_at)
    return state


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--until', type=int, required=True)
    ap.add_argument('--apply', type=str, default=None)
    ap.add_argument('--reset', action='store_true')
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--state-dir', type=str, default=None)
    args = ap.parse_args()

    if args.state_dir:
        global STATE_DIR
        STATE_DIR = args.state_dir
        os.makedirs(STATE_DIR, exist_ok=True)

    if args.reset and os.path.exists(state_path()):
        os.remove(state_path())

    state = load_state()
    batch_start = state['session_idx']

    if args.apply:
        if batch_start == 0:
            print('Cannot apply edits before any sessions have run.')
            sys.exit(1)
        state = apply_edits_from_file(state, args.apply, applied_at=batch_start)
        print(f'Applied edits from {args.apply}.')

    state, batch_regret, batch_oracle = run_batch(state, args.until, seed=args.seed)

    # Record the batch_regret for the most recent edit, if any
    if state['edit_history'] and state['edit_history'][-1]['batch_regret'] is None:
        state['edit_history'][-1]['batch_regret'] = float(batch_regret)
    save_state(state)

    cum_regret = sum(o - r for r, o in zip(state['rewards'], state['oracle']))
    print(f'\n[OPRO] sessions {batch_start} -> {args.until}')
    print(f'  batch regret  = {batch_regret:.2f}  (oracle batch = {batch_oracle:.2f})')
    print(f'  cum  regret   = {cum_regret:.2f}')
    if state['edit_history']:
        print(f'  edits applied at session {state["edit_history"][-1]["applied_at"]}')

    # Render next-round prompt
    next_edits = os.path.join(STATE_DIR, f'edits_round_{args.until}.json')
    prompt = render_opro_prompt(state, next_edits)
    prompt_path = os.path.join(STATE_DIR, f'OPRO_PROMPT_at_{args.until}.md')
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    print(f'  prompt saved  -> {prompt_path}')
    print(f'  expected edits -> {next_edits}')


if __name__ == '__main__':
    main()
