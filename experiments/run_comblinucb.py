"""Run CombLinUCB (warm + cold contexts) on both simulators × {lab, prod}."""
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
from edp.policies.comblinucb import CombLinUCB
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


def run_one(stream, ctx_fn, ctx_dim, *, page_attribution, delay, sigma,
            alpha=0.3, noise_seed=0):
    pol = CombLinUCB(ctx_dim=ctx_dim, alpha=alpha)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))

    def consume(r_obs, payload):
        if page_attribution:
            pol.record_feedback(payload, r_obs)
        else:
            for (a, x), per_slot in payload:
                # Update each arm with its own per-slot reward
                pol.A[a] += np.outer(x, x)
                pol.b[a] += x * per_slot
                Ax = pol.A_inv[a] @ x
                denom = 1.0 + float(x @ Ax)
                pol.A_inv[a] -= np.outer(Ax, Ax) / denom

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
    ap.add_argument('--out', type=str, default='results/results_comblinucb.json')
    args = ap.parse_args()

    summary = {}
    for source in ['parametric', 'llm']:
        from edp.ground_truth import set_source
        set_source(source)
        print(f'\n=== {source} ===')
        stream = make_session_stream(args.n, seed=42)
        oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
        total = float(oracle.sum())
        shapes = make_problem_shapes()
        ctx_warm_fn = lambda f, c: context_warm(f, shapes, c, with_category=False)
        ctx_cold_fn = lambda f, c: context_cold(f, c, with_category=False)

        cells = {}
        for cond, kw in [
            ('lab', {'page_attribution': False, 'delay': 50, 'sigma': 0.05}),
            ('production', {'page_attribution': True, 'delay': 500, 'sigma': 0.20}),
        ]:
            for label, ctx_fn, ctx_dim in [
                ('comb_warm', ctx_warm_fn, 7),
                ('comb_cold', ctx_cold_fn, 14),
            ]:
                vals = []
                for rep in range(args.reps):
                    t0 = time.time()
                    r = run_one(stream, ctx_fn, ctx_dim,
                                noise_seed=hash((source, cond, label, rep)) & 0xffff,
                                **kw)
                    cr = float((oracle - r).sum())
                    pct = cr / total * 100
                    vals.append(pct)
                v = np.array(vals)
                cells.setdefault(label, {})[cond] = {
                    'mean_pct': float(v.mean()),
                    'sem_pct': float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
                }
                print(f'  {label:10s} {cond:11s}: {v.mean():5.2f} ± '
                       f'{v.std(ddof=1) / np.sqrt(len(v)):.2f} %  '
                       f'(N={len(v)}, {time.time()-t0:.1f}s/rep)')
        summary[source] = cells

    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
