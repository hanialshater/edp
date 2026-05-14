"""
Run Slate-LinTS (warm + cold contexts) under both lab and production
conditions, on both persona sources. Bands across 5 LinTS seeds.
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
                 DelayedFeedback)
from edp.policies.slate import SlateLinTSPolicy
from edp.policies.bandit import context_warm, context_cold
from edp.policies.edp import make_problem_shapes


def per_slot_for(p, c, page):
    from edp.ground_truth import effective_needs
    from edp.catalog import TRUE_PROVISIONS
    needs = effective_needs(p, c)
    remaining = dict(needs)
    out = []
    for w in page:
        sr = 0.0
        for d, prov in TRUE_PROVISIONS.get(w, {}).items():
            consumed = min(remaining[d], prov)
            sr += needs[d] * consumed
            remaining[d] -= consumed
        out.append(sr)
    return out


def run_slate(stream, ctx_fn, ctx_dim, *, page_attribution: bool, delay: int,
              sigma: float, policy_seed: int, noise_seed: int, alpha=0.3):
    pol = SlateLinTSPolicy(ctx_dim=ctx_dim, alpha=alpha, seed=policy_seed)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))

    def consume(r_obs, payload):
        if page_attribution:
            pol.record_feedback(payload, r_obs)
        else:
            # payload is the packed per-slot list: [((a, x), per_slot), ...]
            for (a, x), per_slot in payload:
                pol.bandit.update(x, a, per_slot)

    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            consume(r_obs, payload)
        x = ctx_fn(f, c)
        page, payload = pol.select_page_with_payload(x)
        r = true_page_reward(p, c, page)
        rewards[i] = r
        if page_attribution:
            fb.submit(i, r, payload)
        else:
            packed = list(zip(payload, per_slot_for(p, c, page)))
            fb.submit(i, r, packed)
    for r_obs, payload in fb.drain_all():
        consume(r_obs, payload)
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--reps', type=int, default=5)
    ap.add_argument('--out', type=str, default='results_slate_lints.json')
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

        ctx_warm_fn = lambda f, c: context_warm(f, shapes, c, with_category=False)
        ctx_cold_fn = lambda f, c: context_cold(f, c, with_category=False)

        cells = {}
        for cond_name, kwargs in [
            ('lab',        {'page_attribution': False, 'delay': 50,  'sigma': 0.05}),
            ('production', {'page_attribution': True,  'delay': 500, 'sigma': 0.20}),
        ]:
            print(f' [{cond_name}]')
            warm = np.zeros((args.reps, args.n))
            cold = np.zeros((args.reps, args.n))
            for rep in range(args.reps):
                seed_base = 1000 + rep * 17
                t0 = time.time()
                warm[rep] = run_slate(stream, ctx_warm_fn, 7,
                    policy_seed=seed_base, noise_seed=seed_base * 7 + 1,
                    **kwargs)
                t_w = time.time() - t0
                t0 = time.time()
                cold[rep] = run_slate(stream, ctx_cold_fn, 14,
                    policy_seed=seed_base + 31, noise_seed=seed_base * 11 + 3,
                    **kwargs)
                t_c = time.time() - t0
                print(f'   rep {rep+1}/{args.reps}: warm {t_w:.1f}s cold {t_c:.1f}s')
            cr_w = (oracle[None, :] - warm).sum(axis=1) / total_oracle * 100
            cr_c = (oracle[None, :] - cold).sum(axis=1) / total_oracle * 100
            cells[cond_name] = {
                'slate_warm': {'mean_pct': float(cr_w.mean()),
                                'sem_pct': float(cr_w.std(ddof=1) / np.sqrt(len(cr_w)))},
                'slate_cold': {'mean_pct': float(cr_c.mean()),
                                'sem_pct': float(cr_c.std(ddof=1) / np.sqrt(len(cr_c)))},
            }
        summary[source] = cells

    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)

    print('\n' + '=' * 80)
    print('SLATE-LinTS — % of oracle reward lost (mean ± SE across reps)')
    print('=' * 80)
    for source in summary:
        print(f'\n  source: {source}')
        for method in ('slate_warm', 'slate_cold'):
            lab = summary[source]['lab'][method]
            real = summary[source]['production'][method]
            print(f'    {method:12s}  lab: {lab["mean_pct"]:5.2f}% ± {lab["sem_pct"]:.2f}%  '
                   f'  prod: {real["mean_pct"]:5.2f}% ± {real["sem_pct"]:.2f}%  '
                   f'  Δ = +{real["mean_pct"] - lab["mean_pct"]:5.2f} pp')

    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
