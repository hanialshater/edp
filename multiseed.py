"""
Multi-seed runs for paper-quality error bands.

Runs each method N_REPS times, varying:
  - LinTS internal seed (Thompson sampling stochasticity)
  - Delay-queue noise seed (Gaussian noise on observed reward)
  - Session stream is held fixed at seed=42 (so the oracle baseline is identical)

For EDP-static / EDP-canned: deterministic across reps (no policy stochasticity),
so a single trace stands in for all.

Output: results_multiseed.npz with per-rep per-method per-session rewards.
"""
from __future__ import annotations
import argparse
import json
import time
import numpy as np
import os

from sim import (N_SLOTS, make_session_stream, true_page_reward,
                 oracle_reward, DelayedFeedback)
from policy_edp import EDPPolicy, make_problem_shapes, load_edits_json
from policy_bandit import BanditPolicy, context_warm, context_cold


def run_bandit_rep(stream, oracle, ctx_fn, ctx_dim, delay, noise_sigma,
                    policy_seed, noise_seed, alpha=0.3):
    pol = BanditPolicy(ctx_dim=ctx_dim, alpha=alpha, seed=policy_seed)
    fb = DelayedFeedback(delay=delay, noise_sigma=noise_sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))
    for i, (persona, category, feat) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = ctx_fn(feat)
        page, payload = pol.select_page_with_payload(x)
        r = true_page_reward(persona, category, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)
    return rewards


def run_edp_static(stream, oracle):
    pol = EDPPolicy()
    rewards = np.zeros(len(stream))
    for i, (persona, category, feat) in enumerate(stream):
        rewards[i] = true_page_reward(persona, category, pol.select_page(feat))
    return rewards


def run_edp_canned(stream, oracle, edits_dir='edits'):
    pol = EDPPolicy()
    schedule = [
        (2500, load_edits_json(f'{edits_dir}/round1.json')[0]),
        (5000, load_edits_json(f'{edits_dir}/round2.json')[0]),
        (7500, load_edits_json(f'{edits_dir}/round3.json')[0]),
    ]
    schedule_idx = 0
    rewards = np.zeros(len(stream))
    for i, (persona, category, feat) in enumerate(stream):
        while schedule_idx < len(schedule) and i == schedule[schedule_idx][0]:
            pol.apply_edit_batch(schedule[schedule_idx][1])
            schedule_idx += 1
        rewards[i] = true_page_reward(persona, category, pol.select_page(feat))
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--reps', type=int, default=10)
    ap.add_argument('--delay', type=int, default=500)
    ap.add_argument('--noise', type=float, default=0.2)
    ap.add_argument('--out', type=str, default='results_multiseed.npz')
    args = ap.parse_args()

    print(f'== Multi-seed runs ==')
    print(f'  n={args.n}, reps={args.reps}, delay={args.delay}, sigma={args.noise}')

    stream = make_session_stream(args.n, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
    shapes = make_problem_shapes()

    # Deterministic methods: one trace each
    print('\n[edp_static] (deterministic)')
    t0 = time.time()
    edp_static = run_edp_static(stream, oracle)
    print(f'  done {time.time() - t0:.1f}s  cum_regret={float((oracle-edp_static).sum()):.1f}')

    print('\n[edp_canned] (deterministic)')
    t0 = time.time()
    edp_canned = run_edp_canned(stream, oracle)
    print(f'  done {time.time() - t0:.1f}s  cum_regret={float((oracle-edp_canned).sum()):.1f}')

    # Multi-seed bandits
    bandit_warm = np.zeros((args.reps, args.n))
    bandit_cold = np.zeros((args.reps, args.n))
    for rep in range(args.reps):
        seed_base = 1000 + rep * 17  # avoid alignment with default seeds
        print(f'\n[rep {rep + 1}/{args.reps}]  policy_seed={seed_base}')
        t0 = time.time()
        bandit_warm[rep] = run_bandit_rep(stream, oracle, lambda f: context_warm(f, shapes),
                                            7, args.delay, args.noise,
                                            policy_seed=seed_base,
                                            noise_seed=seed_base * 7 + 1)
        print(f'  warm: {time.time() - t0:.1f}s  cum_regret={float((oracle-bandit_warm[rep]).sum()):.1f}')
        t0 = time.time()
        bandit_cold[rep] = run_bandit_rep(stream, oracle, context_cold,
                                            14, args.delay, args.noise,
                                            policy_seed=seed_base + 31,
                                            noise_seed=seed_base * 11 + 3)
        print(f'  cold: {time.time() - t0:.1f}s  cum_regret={float((oracle-bandit_cold[rep]).sum()):.1f}')

    # Summary
    cr_warm = (oracle[None, :] - bandit_warm).sum(axis=1)
    cr_cold = (oracle[None, :] - bandit_cold).sum(axis=1)
    print('\n== Summary ==')
    print(f'  edp_static:  {float((oracle-edp_static).sum()):.1f}')
    print(f'  edp_canned:  {float((oracle-edp_canned).sum()):.1f}')
    print(f'  bandit_warm: mean={cr_warm.mean():.1f} ± {cr_warm.std(ddof=1):.1f}  '
          f'[min={cr_warm.min():.1f}, max={cr_warm.max():.1f}]')
    print(f'  bandit_cold: mean={cr_cold.mean():.1f} ± {cr_cold.std(ddof=1):.1f}  '
          f'[min={cr_cold.min():.1f}, max={cr_cold.max():.1f}]')

    np.savez(args.out,
             oracle=oracle,
             edp_static=edp_static, edp_canned=edp_canned,
             bandit_warm=bandit_warm,    # shape (reps, n)
             bandit_cold=bandit_cold)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
