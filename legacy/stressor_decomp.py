"""
Stressor decomposition for Section 5.2 of the paper.

Holds the bandit fixed at LinTS-warm (7-d problem fingerprint context). Sweeps
the reward conditions: per-slot vs page-level attribution, delay ∈ {0, 500},
noise σ ∈ {0.0, 0.2}. Reports cum regret @ 10K for each cell.

This isolates which stressor dominates. Prior work claimed page-level
attribution is the dominant axis by an order of magnitude. We verify that.
"""
from __future__ import annotations
import json
import time
import numpy as np

from sim import (N_SLOTS, TRUE_PROVISIONS, WIDGETS, make_session_stream,
                 oracle_reward, effective_needs,
                 DelayedFeedback)
from policy_bandit import BanditPolicy, context_warm
from policy_edp import make_problem_shapes


def true_slot_rewards(persona_name: str, category: str, page: list[str]) -> list[float]:
    """Per-slot reward (diminishing returns model). Used for per-slot attribution."""
    needs = effective_needs(persona_name, category)
    remaining = dict(needs)
    slot_r = []
    for widget in page:
        sr = 0.0
        for dim, p in TRUE_PROVISIONS.get(widget, {}).items():
            consumed = min(remaining[dim], p)
            sr += needs[dim] * consumed
            remaining[dim] -= consumed
        slot_r.append(sr)
    return slot_r


def run_bandit_condition(stream, ctx_fn, ctx_dim, delay: int, noise: float,
                          page_attribution: bool, alpha=0.3, seed=7,
                          noise_seed=0) -> np.ndarray:
    """Runs LinTS-warm under (delay, noise, attribution) condition."""
    from policy_bandit import LinTS
    bandits = [LinTS(d=ctx_dim, n_arms=len(WIDGETS), alpha=alpha, seed=seed + s)
               for s in range(N_SLOTS)]
    fb = DelayedFeedback(delay=delay, noise_sigma=noise, seed=noise_seed)
    rewards = np.zeros(len(stream))
    for i, (persona, category, feat) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            for slot, a, x in payload:
                if page_attribution:
                    bandits[slot].update(x, a, r_obs / N_SLOTS)
                else:
                    # r_obs is the SLOT reward (possibly with noise on each
                    # slot independently). Just pass through.
                    bandits[slot].update(x, a, r_obs)
        # Per-slot attribution: each slot gets its own noisy delayed signal.
        x = ctx_fn(feat)
        used = np.zeros(len(WIDGETS), dtype=bool)
        slot_choices = []
        page = []
        for slot in range(N_SLOTS):
            a = bandits[slot].select(x, ~used)
            page.append(WIDGETS[a])
            slot_choices.append((slot, int(a), x))
            used[a] = True
        slot_r = true_slot_rewards(persona, category, page)
        page_total = sum(slot_r)
        rewards[i] = page_total
        if page_attribution:
            fb.submit(i, page_total, slot_choices)
        else:
            # Submit each slot independently with its own true reward.
            for k, sc in enumerate(slot_choices):
                fb.submit(i, slot_r[k], [sc])
    # Drain residual
    for r_obs, payload in fb.drain_all():
        for slot, a, x in payload:
            if page_attribution:
                bandits[slot].update(x, a, r_obs / N_SLOTS)
            else:
                bandits[slot].update(x, a, r_obs)
    return rewards


def main():
    n = 10_000
    stream = make_session_stream(n, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
    shapes = make_problem_shapes()
    ctx_fn = lambda f: context_warm(f, shapes)

    conditions = [
        # (label, delay, noise, page_attribution)
        ('clean (per-slot, delay=0, sigma=0)',       0,    0.0,  False),
        ('+page-attribution (delay=0, sigma=0)',     0,    0.0,  True),
        ('+delay=500 (per-slot, sigma=0)',           500,  0.0,  False),
        ('+delay=1000 (per-slot, sigma=0)',          1000, 0.0,  False),
        ('+noise sigma=0.2 (per-slot, delay=0)',     0,    0.2,  False),
        ('+page +delay=500 (sigma=0)',               500,  0.0,  True),
        ('+page +noise=0.2 (delay=0)',               0,    0.2,  True),
        ('full prod stack (page +delay=500 +noise=0.2)', 500, 0.2, True),
    ]

    results = {}
    print(f'== Stressor decomposition (LinTS-warm, 10K sessions) ==\n')
    print(f'  {"condition":50s} {"cum_regret":>12s} {"vs clean":>10s}  {"time":>6s}')
    clean_cr = None
    for label, delay, noise, page_attr in conditions:
        t0 = time.time()
        r = run_bandit_condition(stream, ctx_fn, 7, delay, noise, page_attr,
                                  alpha=0.3, seed=7,
                                  noise_seed=hash((delay, noise, page_attr)) & 0xffff)
        cr = float((oracle - r).sum())
        results[label] = {
            'delay': delay, 'noise': noise, 'page_attribution': page_attr,
            'cum_regret_10k': cr,
            'cum_regret_curve': [(int(m), float((oracle[:m] - r[:m]).sum()))
                                  for m in (100, 500, 1000, 2500, 5000, 7500, 10000)],
            'last_1k_mean_reward': float(r[-1000:].mean()),
        }
        if clean_cr is None:
            clean_cr = cr
        delta = cr - clean_cr
        sign = '+' if delta >= 0 else ''
        print(f'  {label:50s} {cr:12.1f} {sign}{delta:9.1f}  {time.time() - t0:5.1f}s')

    with open('stressor_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\nSaved -> stressor_results.json')

    # Also print at common milestones for the paper table
    print('\nCum regret at milestones:')
    print(f'  {"condition":50s} ' + ' '.join(f'{m:>8d}' for m in (1000, 2500, 5000, 10000)))
    for label, info in results.items():
        curve = dict(info['cum_regret_curve'])
        print(f'  {label:50s} ' + ' '.join(f'{curve[m]:8.1f}' for m in (1000, 2500, 5000, 10000)))


if __name__ == '__main__':
    main()
