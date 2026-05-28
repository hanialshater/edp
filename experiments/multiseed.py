"""Multi-seed runs for error bands (categorized version)."""
from __future__ import annotations
import argparse
import time
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, oracle_reward, true_page_reward,
                 DelayedFeedback, EDPPolicy, BanditPolicy)
from edp.policies.bandit import context_cold, context_warm, context_dim
from edp.policies.edp import make_problem_shapes, load_edits_json


def run_bandit_rep(stream, oracle, ctx_fn, ctx_dim, delay, noise_sigma,
                    policy_seed, noise_seed, alpha=0.3):
    pol = BanditPolicy(ctx_dim=ctx_dim, alpha=alpha, seed=policy_seed)
    fb = DelayedFeedback(delay=delay, noise_sigma=noise_sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))
    for i, (persona, category, feat) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = ctx_fn(feat, category)
        page, payload = pol.select_page_with_payload(x)
        r = true_page_reward(persona, category, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)
    return rewards


def run_edp_static(stream):
    pol = EDPPolicy()
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        rewards[i] = true_page_reward(p, c, pol.select_page(f))
    return rewards


def run_edp_canned(stream, edits_dir='edits'):
    pol = EDPPolicy()
    sched = [
        (2500, load_edits_json(f'{edits_dir}/round1.json')[0]),
        (5000, load_edits_json(f'{edits_dir}/round2.json')[0]),
        (7500, load_edits_json(f'{edits_dir}/round3.json')[0]),
    ]
    idx = 0
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        while idx < len(sched) and i == sched[idx][0]:
            pol.apply_edit_batch(sched[idx][1])
            idx += 1
        rewards[i] = true_page_reward(p, c, pol.select_page(f))
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--reps', type=int, default=10)
    ap.add_argument('--delay', type=int, default=500)
    ap.add_argument('--noise', type=float, default=0.2)
    ap.add_argument('--out', type=str, default='results/results_multiseed.npz')
    ap.add_argument('--with-category-context', action='store_true')
    ap.add_argument('--source', type=str, default=None)
    args = ap.parse_args()

    if args.source:
        from edp.ground_truth import set_source
        set_source(args.source)

    print(f'== Multi-seed runs ==')
    print(f'  n={args.n}, reps={args.reps}, delay={args.delay}, sigma={args.noise}, '
          f'category_ctx={"on" if args.with_category_context else "off"}')

    stream = make_session_stream(args.n, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
    shapes = make_problem_shapes()

    print('\n[edp_static] (deterministic)')
    t0 = time.time()
    edp_static = run_edp_static(stream)
    print(f'  cum_regret={float((oracle-edp_static).sum()):.1f}  ({time.time()-t0:.1f}s)')

    print('\n[edp_canned] (deterministic)')
    t0 = time.time()
    edp_canned = run_edp_canned(stream)
    print(f'  cum_regret={float((oracle-edp_canned).sum()):.1f}  ({time.time()-t0:.1f}s)')

    cd_warm = context_dim('warm', args.with_category_context)
    cd_cold = context_dim('cold', args.with_category_context)
    bandit_warm = np.zeros((args.reps, args.n))
    bandit_cold = np.zeros((args.reps, args.n))
    for rep in range(args.reps):
        seed_base = 1000 + rep * 17
        print(f'\n[rep {rep + 1}/{args.reps}]  policy_seed={seed_base}')
        t0 = time.time()
        bandit_warm[rep] = run_bandit_rep(
            stream, oracle,
            lambda f, c: context_warm(f, shapes, c, args.with_category_context),
            cd_warm, args.delay, args.noise,
            policy_seed=seed_base, noise_seed=seed_base * 7 + 1)
        print(f'  warm: {time.time() - t0:.1f}s  cum_regret={float((oracle-bandit_warm[rep]).sum()):.1f}')
        t0 = time.time()
        bandit_cold[rep] = run_bandit_rep(
            stream, oracle,
            lambda f, c: context_cold(f, c, args.with_category_context),
            cd_cold, args.delay, args.noise,
            policy_seed=seed_base + 31, noise_seed=seed_base * 11 + 3)
        print(f'  cold: {time.time() - t0:.1f}s  cum_regret={float((oracle-bandit_cold[rep]).sum()):.1f}')

    cr_w = (oracle[None, :] - bandit_warm).sum(axis=1)
    cr_c = (oracle[None, :] - bandit_cold).sum(axis=1)
    print('\n== Summary ==')
    print(f'  edp_static:  {float((oracle-edp_static).sum()):.1f}')
    print(f'  edp_canned:  {float((oracle-edp_canned).sum()):.1f}')
    print(f'  bandit_warm: mean={cr_w.mean():.1f} ± {cr_w.std(ddof=1):.1f}')
    print(f'  bandit_cold: mean={cr_c.mean():.1f} ± {cr_c.std(ddof=1):.1f}')

    np.savez(args.out, oracle=oracle,
             edp_static=edp_static, edp_canned=edp_canned,
             bandit_warm=bandit_warm, bandit_cold=bandit_cold)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
