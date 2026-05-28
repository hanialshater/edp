"""
Head-to-head EDP vs LinTS comparison harness.
Uses (persona, category, feat) sessions.
"""
from __future__ import annotations
import argparse
import time
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (N_SLOTS, make_session_stream, oracle_reward, true_page_reward,
                 DelayedFeedback, EDPPolicy, BanditPolicy)
from edp.policies.bandit import context_cold, context_warm, context_dim
from edp.policies.edp import make_problem_shapes, load_edits_json


def run_edp(stream, policy: EDPPolicy, evolution_schedule=None, label='edp'):
    schedule = list(evolution_schedule or [])
    schedule.sort(key=lambda x: x[0])
    next_chk = 0
    rewards = np.zeros(len(stream))
    optimal = np.zeros(len(stream))
    for i, (persona, category, feat) in enumerate(stream):
        while next_chk < len(schedule) and schedule[next_chk][0] == i:
            policy.apply_edit_batch(schedule[next_chk][1])
            print(f'    [{label}] applied {len(schedule[next_chk][1])} edits at session {i}')
            next_chk += 1
        page = policy.select_page(feat)
        rewards[i] = true_page_reward(persona, category, page)
        optimal[i] = oracle_reward(persona, category)
    return rewards, optimal


def run_bandit(stream, policy: BanditPolicy, ctx_fn, delay, sigma,
               label='bandit', noise_seed=0):
    rewards = np.zeros(len(stream))
    optimal = np.zeros(len(stream))
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    for i, (persona, category, feat) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            policy.record_feedback(payload, r_obs)
        x = ctx_fn(feat, category)
        page, payload = policy.select_page_with_payload(x)
        r_true = true_page_reward(persona, category, page)
        rewards[i] = r_true
        optimal[i] = oracle_reward(persona, category)
        fb.submit(i, r_true, payload)
        if (i + 1) % 2500 == 0:
            recent = rewards[max(0, i - 500):i + 1].mean()
            print(f'    [{label}] session {i + 1}  recent_mean={recent:.4f}')
    for r_obs, payload in fb.drain_all():
        policy.record_feedback(payload, r_obs)
    return rewards, optimal


def cum_regret(r, o):
    return np.cumsum(o - r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--delay', type=int, default=500)
    ap.add_argument('--noise', type=float, default=0.2)
    ap.add_argument('--alpha', type=float, default=0.3)
    ap.add_argument('--out', type=str, default='results/results.npz')
    ap.add_argument('--methods', type=str, default='all')
    ap.add_argument('--with-category-context', action='store_true',
                    help='append one-hot category to bandit context')
    ap.add_argument('--source', type=str, default=None,
                    help='override persona source (parametric|llm)')
    args = ap.parse_args()

    if args.source:
        from edp.ground_truth import set_source
        set_source(args.source)

    print('== EDP vs Bandit comparison ==')
    print(f'  n_sessions = {args.n}, seed = {args.seed}, delay = {args.delay}, '
          f'sigma = {args.noise}, alpha = {args.alpha}')
    print(f'  category context: {"on" if args.with_category_context else "off"}')
    print(f'  persona source: {os.environ.get("EDP_PERSONA_SOURCE", args.source or "parametric")}')

    stream = make_session_stream(args.n, seed=args.seed)
    requested = set(args.methods.split(',')) if args.methods != 'all' else {
        'edp_static', 'edp_evolved', 'bandit_warm', 'bandit_cold'
    }
    results = {}
    shapes = make_problem_shapes()
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])

    if 'edp_static' in requested:
        print('\n-- edp_static --')
        t0 = time.time()
        r, _ = run_edp(stream, EDPPolicy(), label='edp_static')
        print(f'  cum regret = {(oracle - r).sum():.1f}  ({time.time() - t0:.1f}s)')
        results['edp_static'] = r

    if 'edp_evolved' in requested:
        print('\n-- edp_evolved (canned) --')
        t0 = time.time()
        try:
            edits_r1, _ = load_edits_json('state/edits/round1.json')
            edits_r2, _ = load_edits_json('state/edits/round2.json')
            edits_r3, _ = load_edits_json('state/edits/round3.json')
            schedule = [(2500, edits_r1), (5000, edits_r2), (7500, edits_r3)]
            r, _ = run_edp(stream, EDPPolicy(), evolution_schedule=schedule, label='edp_evolved')
            print(f'  cum regret = {(oracle - r).sum():.1f}  ({time.time() - t0:.1f}s)')
            results['edp_evolved'] = r
        except FileNotFoundError as e:
            print(f'  SKIP (no canned edits: {e})')

    with_cat = args.with_category_context
    cat_dim_add = 6 if with_cat else 0
    if 'bandit_warm' in requested:
        print(f'\n-- bandit_warm ({context_dim("warm", with_cat)}-d context) --')
        t0 = time.time()
        pol = BanditPolicy(ctx_dim=context_dim('warm', with_cat),
                            alpha=args.alpha, seed=7)
        ctx_fn = lambda f, c: context_warm(f, shapes, c, with_cat)
        r, _ = run_bandit(stream, pol, ctx_fn, args.delay, args.noise,
                          label='bandit_warm', noise_seed=101)
        print(f'  cum regret = {(oracle - r).sum():.1f}  ({time.time() - t0:.1f}s)')
        results['bandit_warm'] = r

    if 'bandit_cold' in requested:
        print(f'\n-- bandit_cold ({context_dim("cold", with_cat)}-d context) --')
        t0 = time.time()
        pol = BanditPolicy(ctx_dim=context_dim('cold', with_cat),
                            alpha=args.alpha, seed=11)
        ctx_fn = lambda f, c: context_cold(f, c, with_cat)
        r, _ = run_bandit(stream, pol, ctx_fn, args.delay, args.noise,
                          label='bandit_cold', noise_seed=202)
        print(f'  cum regret = {(oracle - r).sum():.1f}  ({time.time() - t0:.1f}s)')
        results['bandit_cold'] = r

    print('\n== Summary ==')
    print(f'  {"method":20s} {"cum_regret":>12s}')
    for name, r in results.items():
        print(f'  {name:20s} {(oracle - r).sum():12.1f}')

    np.savez(args.out, oracle=oracle,
             personas=np.array([p for p, _, _ in stream]),
             categories=np.array([c for _, c, _ in stream]),
             **{k: v for k, v in results.items()})
    print(f'\nResults saved -> {args.out}')


if __name__ == '__main__':
    main()
