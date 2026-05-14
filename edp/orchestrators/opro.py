"""
OPRO-style ablation orchestrator: at each checkpoint the agent's prompt
contains ONLY the history of (edits, batch_regret) pairs. No diagnostic.
"""
from __future__ import annotations
import json
from edp.catalog import WIDGETS
from edp.orchestrators.base import Orchestrator, cli_main


OPRO_PROMPT_TEMPLATE = '''\
You are a black-box optimizer for an EDP module-config policy. You see ONLY
a history of (edits, batch_regret) pairs. Lower regret is better.

You see NO diagnostic information beyond the (edits, score) pairs themselves.
You do NOT see per-persona regret, widget activation rates, or composition
signatures. You must reason purely from patterns in the score history.

# Action space

Each solution is a list of atomic edits. Each edit is:
- `widget`: one of 22 widget names (see below)
- `path`: `base`, `slot_decay`, `on_rem.<F-code>`, or `on_cov.<F-code>`
- `to`: numeric value, typical magnitude range -1.5 to 2.8
- `reason`: short string (opaque tag, no effect on score)

Widgets: {widget_list}
F-codes: F32, F33, F41, F43, F45, F46, F51.

# History of attempts (sorted by score: best first)

{history_block}

# Current cumulative regret across all batches: {cum_regret:.2f}

# Your task

Write a NEW edit batch of 8–16 edits to `{out_path}`:

```json
{{
  "note": "round X — one-line summary",
  "edits": [
    {{"widget": "...", "path": "...", "from": 0.0, "to": 0.0, "reason": "..."}}
  ]
}}
```

You can revisit edits from prior batches with different values or try
entirely different combinations. Reason from patterns in the score history.

Output: write the JSON file. Do NOT print it back. Final message: under 80
words on your hypothesis for why this batch should improve.
'''


class OPROOrchestrator(Orchestrator):

    def apply_edits_from_file(self, state, path):
        with open(path) as f:
            data = json.load(f)
        # Stash the edits + None batch regret; we'll fill it after running.
        state = super().apply_edits_from_file(state, path,
                                               edits=data['edits'],
                                               batch_regret=None)
        return state

    def run_batch(self, state, until_idx, seed=42):
        prev_batch_start = state['session_idx']
        state = super().run_batch(state, until_idx, seed=seed)
        # Fill batch_regret on the most recent edit_history entry, if any.
        if state['edit_history'] and state['edit_history'][-1].get('batch_regret') is None:
            rewards = state['rewards'][prev_batch_start:until_idx]
            oracle = state['oracle'][prev_batch_start:until_idx]
            state['edit_history'][-1]['batch_regret'] = float(sum(o - r for r, o in zip(rewards, oracle)))
        return state

    def make_report(self, state, batch_start, batch_end) -> str:
        # Minimal report — used to populate the prompt's history block.
        rewards = state['rewards']
        oracle = state['oracle']
        cum_regret = sum(o - r for r, o in zip(rewards, oracle))
        return f'# OPRO checkpoint @ session {batch_end} — cum regret {cum_regret:.2f}\n'

    def render_prompt(self, state, batch_start, batch_end, report_text, out_path):
        history = sorted(
            [h for h in state['edit_history'] if h.get('batch_regret') is not None],
            key=lambda h: h['batch_regret']
        )
        parts = []
        if not history:
            parts.append('(no prior attempts — this is the first round)')
        else:
            for h in history:
                parts.append(f'### attempt at session {h["session"]}: '
                             f'batch_regret = {h["batch_regret"]:.2f}')
                parts.append('```json')
                parts.append(json.dumps({'edits': h.get('edits', [])}, indent=2))
                parts.append('```')
                parts.append('')
        history_block = '\n'.join(parts)
        cum_regret = sum(o - r for r, o in zip(state['rewards'], state['oracle']))
        return OPRO_PROMPT_TEMPLATE.format(
            widget_list=', '.join(WIDGETS),
            history_block=history_block,
            cum_regret=cum_regret,
            out_path=out_path,
        )


if __name__ == '__main__':
    cli_main(OPROOrchestrator)
