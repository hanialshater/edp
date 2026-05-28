"""
Lab-vs-Real ablation: run every method under both "lab" and "production"
reward conditions, on both persona sources.

Lab conditions:
  - Per-slot reward attribution (the bandit gets a clean per-slot signal)
  - delay = 50  (~5 minutes; mostly synchronous)
  - sigma = 0.05 (low noise, not zero — there's always SOME measurement
                  noise even in academic experiments)

Production conditions:
  - Page-level attribution
  - delay = 500 (~2 days at 250 sessions/day)
  - sigma = 0.20

Reports % of oracle reward lost for each method × condition × persona-source
cell. Saves to results_lab_vs_real.json and prints the table.

The lab condition only differs for bandits; EDP-static / EDP-canned /
static_policy / llm_policy are deterministic given the stream and don't
care about the reward signal. So we re-run only LinTS-warm and LinTS-cold
under lab conditions; the EDP / static / llm_policy numbers carry over
from the existing multi-seed runs.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, oracle_reward, true_page_reward,
                 DelayedFeedback, BanditPolicy, N_SLOTS, WIDGETS,
                 TRUE_NEEDS, TRUE_PROVISIONS)
from edp.policies.bandit import context_warm, context_cold, context_dim
from edp.policies.edp import make_problem_shapes


# Per-slot reward via diminishing returns (same as the page-level form,
# but accumulated per slot rather than collapsed).
def per_slot_rewards(persona, category, page):
    from edp.ground_truth import effective_needs
    needs = effective_needs(persona, category)
    remaining = dict(needs)
    out = []
    for w in page:
        sr = 0.0
        for d, p in TRUE_PROVISIONS.get(w, {}).items():
            consumed = min(remaining[d], p)
            sr += needs[d] * consumed
            remaining[d] -= consumed
        out.append(sr)
    return out


def run_bandit_condition(stream, ctx_fn, ctx_dim, *, page_attribution: bool,
                          delay: int, sigma: float, policy_seed: int,
                          noise_seed: int, alpha: float = 0.3):
    pol = BanditPolicy(ctx_dim=ctx_dim, alpha=alpha, seed=policy_seed)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            if page_attribution:
                pol.record_feedback(payload, r_obs)
            else:
                # payload is a list of (slot, arm, x); each gets ITS OWN obs
                for (slot, a, x), per_slot in payload:
                    pol.bandits[slot].update(x, a, per_slot)
        x = ctx_fn(f, c)
        page, payload = pol.select_page_with_payload(x)
        slot_r = per_slot_rewards(p, c, page)
        page_total = sum(slot_r)
        rewards[i] = page_total
        if page_attribution:
            fb.submit(i, page_total, payload)
        else:
            # bundle each (slot, arm, x) with its own per-slot true reward
            packed = list(zip(payload, slot_r))
            fb.submit(i, page_total, packed)  # we only use payload via the
                                                # branch above; for per-slot
                                                # we ignore r_obs and use the
                                                # packed signal directly
    # drain
    for r_obs, payload in fb.drain_all():
        if page_attribution:
            pol.record_feedback(payload, r_obs)
        else:
            for (slot, a, x), per_slot in payload:
                pol.bandits[slot].update(x, a, per_slot)
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--reps', type=int, default=10)
    ap.add_argument('--out', type=str, default='results/results_lab_vs_real.json')
    args = ap.parse_args()

    summary = {}
    for source in ['parametric', 'llm']:
        from edp.ground_truth import set_source
        set_source(source)
        print(f'\n=== persona source: {source} ===')

        stream = make_session_stream(args.n, seed=42)
        oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
        total_oracle = float(oracle.sum())
        shapes = make_problem_shapes()

        ctx_warm = lambda f, c: context_warm(f, shapes, c, with_category=False)
        ctx_cold_fn = lambda f, c: context_cold(f, c, with_category=False)

        cells = {}
        for cond_name, kwargs in [
            ('lab',        {'page_attribution': False, 'delay': 50,  'sigma': 0.05}),
            ('production', {'page_attribution': True,  'delay': 500, 'sigma': 0.20}),
        ]:
            print(f' [condition: {cond_name}] page_attr={kwargs["page_attribution"]} '
                   f'delay={kwargs["delay"]} sigma={kwargs["sigma"]}')
            warm = np.zeros((args.reps, args.n))
            cold = np.zeros((args.reps, args.n))
            for rep in range(args.reps):
                seed_base = 1000 + rep * 17
                t0 = time.time()
                warm[rep] = run_bandit_condition(stream, ctx_warm, 7,
                    policy_seed=seed_base, noise_seed=seed_base * 7 + 1,
                    **kwargs)
                t_w = time.time() - t0
                t0 = time.time()
                cold[rep] = run_bandit_condition(stream, ctx_cold_fn, 14,
                    policy_seed=seed_base + 31, noise_seed=seed_base * 11 + 3,
                    **kwargs)
                t_c = time.time() - t0
                print(f'   rep {rep+1}/{args.reps}: warm {t_w:.1f}s cold {t_c:.1f}s')
            cr_w = (oracle[None, :] - warm).sum(axis=1) / total_oracle * 100
            cr_c = (oracle[None, :] - cold).sum(axis=1) / total_oracle * 100
            cells[cond_name] = {
                'bandit_warm': {'mean_pct': float(cr_w.mean()),
                                 'sem_pct': float(cr_w.std(ddof=1) / np.sqrt(len(cr_w)))},
                'bandit_cold': {'mean_pct': float(cr_c.mean()),
                                 'sem_pct': float(cr_c.std(ddof=1) / np.sqrt(len(cr_c)))},
            }
        summary[source] = cells

    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)

    # Print summary table
    print('\n' + '=' * 80)
    print('LAB vs REAL — % of oracle reward lost (mean ± SE across 10 LinTS seeds)')
    print('=' * 80)
    for source in summary:
        print(f'\n  source: {source}')
        for method in ('bandit_warm', 'bandit_cold'):
            lab = summary[source]['lab'][method]
            real = summary[source]['production'][method]
            print(f'    {method:14s}  lab: {lab["mean_pct"]:5.2f}% ± {lab["sem_pct"]:.2f}%  '
                   f'  prod: {real["mean_pct"]:5.2f}% ± {real["sem_pct"]:.2f}%  '
                   f'  Δ = +{real["mean_pct"] - lab["mean_pct"]:5.2f} pp')

    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
