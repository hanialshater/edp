"""Leakage-free report-based EDP evolution.

Unlike ``report.py`` (which reproduces the historical, privileged experiment),
this orchestrator exposes only information that a production learner could
observe:

- observable category and feature values at action time;
- the selected page;
- noisy page-level reward after the configured delay;
- the current EDP policy and prior edit history.

It does *not* expose persona labels, true needs, widget provisions, oracle
reward, per-persona regret, or immediate noise-free reward. The resulting
editor trajectory is the one that should be used in a fair main leaderboard.

Example:

    python -m edp.orchestrators.observable \
        --state-dir state/observable_editor_llm --reset --until 2500

Then ask an LLM/coding agent to follow the generated prompt and write the edit
JSON, and continue with ``--apply ... --until 5000``.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import json

import numpy as np

from edp import EDPPolicy, N_SLOTS, WIDGETS, make_session_stream
from edp.config import SIGNAL_NAMES
from edp.ground_truth import true_page_reward, oracle_reward
from edp.orchestrators.base import Orchestrator, cli_main


OBSERVABLE_PROMPT_TEMPLATE = '''\
You are editing an Evolvable Decision Program (EDP) for page-module selection.
Your objective is to improve future observed page reward.

You may use only the production-observable evidence below. The report contains
no persona labels, simulator needs, widget provisions, oracle reward, or
counterfactual regret.

# Policy

The policy greedily selects six distinct widgets. At each selection step:

  score = base
        + sum_p on_rem[p] * remaining[p]
        + sum_p on_cov[p] * coverage[p]
        - slot_decay * slot

The seven problem features are F32 size anxiety, F33 quality-signal deficit,
F41 comparison friction, F43 outfit visualization, F45 price-quality confusion,
F46 return hesitation, and F51 decision paralysis.

# Current modules

```json
{modules_json}
```

# Prior edits

{edit_history}

# Observable delayed-feedback report

```
{report}
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `{out_path}` with this shape:

```json
{{
  "note": "short rationale",
  "edits": [
    {{"widget": "size_guide", "path": "base", "from": 0.05,
      "to": 0.10, "reason": "under-used on high-size_chart sessions"}}
  ]
}}
```

Allowed paths: `base`, `slot_decay`, `on_rem.<F-code>`, `on_cov.<F-code>`.
Emit only the JSON file.
'''


class ObservableReportOrchestrator(Orchestrator):
    """EDP editor driven by delayed noisy page reward and observable context."""

    def __init__(self, state_dir: str, *, delay: int = 500,
                 noise_sigma: float = 0.20):
        super().__init__(state_dir)
        self.delay = int(delay)
        self.noise_sigma = float(noise_sigma)

    def run_batch(self, state, until_idx, seed=42):
        stream = make_session_stream(until_idx, seed=seed)
        policy = EDPPolicy(modules=state['modules'], shapes=state.get('shapes'))

        start = int(state['session_idx'])
        rewards = list(state.get('rewards', []))       # evaluator-only
        oracles = list(state.get('oracle', []))         # evaluator-only
        pending = list(state.get('pending_feedback', []))
        released = []

        rng = np.random.default_rng(seed * 7 + 1)
        if state.get('feedback_rng_state') is not None:
            rng.bit_generator.state = state['feedback_rng_state']

        def release_ready(index: int):
            nonlocal pending
            ready, waiting = [], []
            for item in pending:
                (ready if item['ready_at'] <= index else waiting).append(item)
            pending = waiting
            ready.sort(key=lambda item: item['action_index'])
            released.extend(ready)

        for index in range(start, until_idx):
            release_ready(index)
            persona, category, feat = stream[index]
            page = policy.select_page(feat)

            # The simulator needs the latent persona to generate reward, but it
            # is never copied into the feedback payload or the prompt.
            true_reward = true_page_reward(persona, category, page)
            observed_reward = true_reward + (
                float(rng.normal(0.0, self.noise_sigma))
                if self.noise_sigma > 0 else 0.0
            )
            pending.append({
                'action_index': index,
                'ready_at': index + self.delay,
                'category': category,
                'feat': {name: float(feat[name]) for name in SIGNAL_NAMES},
                'price_norm': float(feat.get('price_norm', 0.0)),
                'page': list(page),
                'observed_reward': observed_reward,
            })

            rewards.append(float(true_reward))
            oracles.append(float(oracle_reward(persona, category)))

        # Do not flush pending feedback at an intermediate checkpoint: a real
        # editor cannot observe rewards whose delay window has not elapsed.
        state['session_idx'] = until_idx
        state['rewards'] = rewards
        state['oracle'] = oracles
        state['pending_feedback'] = pending
        state['recent_observed_logs'] = released
        state['feedback_rng_state'] = rng.bit_generator.state
        state['recent_logs'] = []  # prevent accidental use of privileged logs
        return state

    def make_report(self, state, batch_start, batch_end) -> str:
        logs = state.get('recent_observed_logs', [])
        lines = [
            f'# OBSERVABLE EDP CHECKPOINT — actions {batch_start} → {batch_end}',
            f'- feedback items matured since previous checkpoint: {len(logs)}',
            f'- feedback delay: {self.delay} sessions',
            f'- observation noise sigma: {self.noise_sigma:.3f}',
        ]
        if not logs:
            lines.append('- no feedback has matured yet; make no edits')
            return '\n'.join(lines)

        rewards = np.asarray([item['observed_reward'] for item in logs], dtype=float)
        lines.extend([
            '',
            '## Aggregate observed reward',
            f'- mean: {rewards.mean():.4f}',
            f'- standard deviation: {rewards.std(ddof=1) if len(rewards) > 1 else 0.0:.4f}',
        ])

        category_values = defaultdict(list)
        widget_values = defaultdict(list)
        composition_counts = Counter()
        for item in logs:
            reward = float(item['observed_reward'])
            category_values[item['category']].append(reward)
            composition_counts[tuple(sorted(item['page']))] += 1
            for widget in item['page']:
                widget_values[widget].append(reward)

        lines.extend(['', '## Reward by observable category'])
        for category, values in sorted(category_values.items()):
            array = np.asarray(values)
            lines.append(
                f'- {category:12s} n={len(values):4d} mean={array.mean():.4f}'
            )

        lines.extend([
            '',
            '## Widget activation and associated page reward',
            '(Association only: every widget on a page shares the same page reward.)',
        ])
        total_slots = len(logs) * N_SLOTS
        for widget in WIDGETS:
            values = widget_values.get(widget, [])
            activation = 100.0 * len(values) / total_slots if total_slots else 0.0
            mean_reward = float(np.mean(values)) if values else float('nan')
            rendered = 'n/a' if not values else f'{mean_reward:.4f}'
            lines.append(
                f'- {widget:25s} act={activation:5.1f}% n={len(values):4d} '
                f'assoc_page_reward={rendered}'
            )

        lines.extend(['', '## Observable feature cohorts'])
        for signal in list(SIGNAL_NAMES) + ['price_norm']:
            high = [
                item['observed_reward'] for item in logs
                if float(item['feat'].get(signal, item.get(signal, 0.0))) >= 0.70
            ]
            low = [
                item['observed_reward'] for item in logs
                if float(item['feat'].get(signal, item.get(signal, 0.0))) <= 0.30
            ]
            high_text = f'{np.mean(high):.4f}' if high else 'n/a'
            low_text = f'{np.mean(low):.4f}' if low else 'n/a'
            lines.append(
                f'- {signal:14s} high(n={len(high):4d})={high_text} '
                f'low(n={len(low):4d})={low_text}'
            )

        lines.extend(['', '## Most common selected sets'])
        for page, count in composition_counts.most_common(10):
            lines.append(f'- n={count:4d}: {", ".join(page)}')

        lines.extend(['', '## Edit history'])
        if not state.get('edit_history'):
            lines.append('- none')
        else:
            for entry in state['edit_history']:
                lines.append(
                    f'- action {entry["session"]}: {entry["count"]} edits — '
                    f'{entry.get("note", "")}'
                )
        return '\n'.join(lines)

    def render_prompt(self, state, batch_start, batch_end, report_text, out_path):
        history = state.get('edit_history', [])
        edit_history = '\n'.join(
            f'- action {entry["session"]}: {entry["count"]} edits — '
            f'{entry.get("note", "")}'
            for entry in history
        ) or '- none'
        return OBSERVABLE_PROMPT_TEMPLATE.format(
            modules_json=json.dumps(state['modules'], indent=2),
            edit_history=edit_history,
            report=report_text,
            out_path=out_path,
        )


if __name__ == '__main__':
    cli_main(ObservableReportOrchestrator)
