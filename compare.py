"""
Head-to-head comparison: EDP vs LinTS bandits under the production reward stack.

Same 10k-session stream feeds every policy. Reward is page-level, delayed
by D sessions (~2 days of traffic), with Gaussian noise sigma.

Policies under test:
  - oracle              (upper bound, greedy over true provisions)
  - edp_static          (initial LLM prior, never updates)
  - edp_evolved         (canned LLM-agent edits at sessions 2500/5000/7500)
  - bandit_warm         (LinTS, 7-d problem fingerprint context)
  - bandit_cold         (LinTS, 14-d raw signal context)

The bandit sees delayed, page-level, noisy rewards through DelayedFeedback.
EDP also sees the same delayed signal -- but its "learning" is the agent
edit batch, not online updates, so the noisy/delayed signal only affects
WHICH widgets show low activation and high regret in the checkpoint report.
For determinism in this run, EDP applies the canned edits at fixed sessions.
"""
from __future__ import annotations
import argparse
import json
import os
import time
import numpy as np

from sim import (N_SLOTS, ORACLE_REWARDS, make_session_stream,
                 true_page_reward, DelayedFeedback)
from policy_edp import EDPPolicy, make_problem_shapes, load_edits_json
from policy_bandit import BanditPolicy, context_cold, context_warm


def run_edp(stream, policy: EDPPolicy, evolution_schedule=None, label='edp'):
    """Run EDP. evolution_schedule: list of (session_idx, edits_list)."""
    schedule = list(evolution_schedule or [])
    schedule.sort(key=lambda x: x[0])
    next_chk = 0
    rewards = np.zeros(len(stream))
    optimal = np.zeros(len(stream))
    pages = []
    for i, (persona, feat) in enumerate(stream):
        while next_chk < len(schedule) and schedule[next_chk][0] == i:
            edits = schedule[next_chk][1]
            policy.apply_edit_batch(edits)
            print(f'    [{label}] applied {len(edits)} edits at session {i}')
            next_chk += 1
        page = policy.select_page(feat)
        rewards[i] = true_page_reward(persona, page)
        optimal[i] = ORACLE_REWARDS[persona]
        pages.append(page)
    return rewards, optimal, pages


def run_bandit(stream, policy: BanditPolicy, ctx_fn, delay: int,
               noise_sigma: float, label='bandit', noise_seed: int = 0):
    rewards = np.zeros(len(stream))
    optimal = np.zeros(len(stream))
    fb = DelayedFeedback(delay=delay, noise_sigma=noise_sigma, seed=noise_seed)
    for i, (persona, feat) in enumerate(stream):
        # Drain feedback whose delay window has elapsed
        for r_obs, payload in fb.drain_ready(i):
            policy.record_feedback(payload, r_obs)
        x = ctx_fn(feat)
        page, payload = policy.select_page_with_payload(x)
        r_true = true_page_reward(persona, page)
        rewards[i] = r_true
        optimal[i] = ORACLE_REWARDS[persona]
        fb.submit(i, r_true, payload)
        if (i + 1) % 2500 == 0:
            recent = rewards[max(0, i - 500):i + 1].mean()
            print(f'    [{label}] session {i + 1}  recent_mean={recent:.4f}')
    # Drain residual delayed feedback at end of run
    for r_obs, payload in fb.drain_all():
        policy.record_feedback(payload, r_obs)
    return rewards, optimal


def cum_regret(reward: np.ndarray, oracle: np.ndarray) -> np.ndarray:
    return np.cumsum(oracle - reward)


def print_milestones(label_to_arr, oracle):
    milestones = [100, 500, 1000, 2500, 5000, 7500, 10000]
    print('\nCumulative regret at milestones:')
    headers = list(label_to_arr.keys())
    print(f'  {"session":>8s}  ' + '  '.join(f'{h:>17s}' for h in headers))
    for m in milestones:
        if m > len(oracle):
            continue
        row = []
        for h in headers:
            cr = cum_regret(label_to_arr[h], oracle)[m - 1]
            row.append(f'{cr:>17.2f}')
        print(f'  {m:>8d}  ' + '  '.join(row))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000, help='session count')
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--delay', type=int, default=500,
                    help='reward delay in sessions (~2 days of traffic)')
    ap.add_argument('--noise', type=float, default=0.05,
                    help='Gaussian sigma on observed page reward')
    ap.add_argument('--alpha', type=float, default=0.3, help='LinTS exploration')
    ap.add_argument('--out', type=str, default='results.npz')
    ap.add_argument('--methods', type=str, default='all',
                    help='comma-separated subset (edp_static,edp_evolved,bandit_warm,bandit_cold)')
    args = ap.parse_args()

    print(f'== EDP vs Bandit comparison ==')
    print(f'  n_sessions     = {args.n}')
    print(f'  seed           = {args.seed}')
    print(f'  reward delay   = {args.delay} sessions  (~2 days at ~250 sessions/day)')
    print(f'  observation noise sigma = {args.noise}')
    print(f'  attribution    = page-level')
    print(f'  LinTS alpha    = {args.alpha}')
    print()

    stream = make_session_stream(args.n, seed=args.seed)
    requested = set(args.methods.split(',')) if args.methods != 'all' else {
        'edp_static', 'edp_evolved', 'bandit_warm', 'bandit_cold'
    }
    results = {}
    shapes = make_problem_shapes()
    t0_total = time.time()

    # Oracle (no policy)
    oracle = np.array([ORACLE_REWARDS[p] for p, _ in stream])

    # EDP static
    if 'edp_static' in requested:
        print('-- edp_static --')
        t0 = time.time()
        r, o, _ = run_edp(stream, EDPPolicy(), evolution_schedule=None, label='edp_static')
        print(f'  mean reward={r.mean():.4f}  mean regret={(o - r).mean():.4f}  ({time.time() - t0:.1f}s)')
        results['edp_static'] = r

    # EDP evolved via canned edits
    if 'edp_evolved' in requested:
        print('\n-- edp_evolved --')
        t0 = time.time()
        edits_r1, _ = load_edits_json('edits/round1.json')
        edits_r2, _ = load_edits_json('edits/round2.json')
        edits_r3, _ = load_edits_json('edits/round3.json')
        schedule = [(2500, edits_r1), (5000, edits_r2), (7500, edits_r3)]
        r, o, _ = run_edp(stream, EDPPolicy(), evolution_schedule=schedule, label='edp_evolved')
        print(f'  mean reward={r.mean():.4f}  mean regret={(o - r).mean():.4f}  ({time.time() - t0:.1f}s)')
        results['edp_evolved'] = r

    # Bandit-warm
    if 'bandit_warm' in requested:
        print('\n-- bandit_warm (7-d problem fingerprint context) --')
        t0 = time.time()
        pol = BanditPolicy(ctx_dim=7, alpha=args.alpha, seed=7)
        ctx_fn = lambda f: context_warm(f, shapes)
        r, o = run_bandit(stream, pol, ctx_fn, args.delay, args.noise,
                          label='bandit_warm', noise_seed=101)
        print(f'  mean reward={r.mean():.4f}  mean regret={(o - r).mean():.4f}  ({time.time() - t0:.1f}s)')
        results['bandit_warm'] = r

    # Bandit-cold
    if 'bandit_cold' in requested:
        print('\n-- bandit_cold (14-d raw signal context) --')
        t0 = time.time()
        pol = BanditPolicy(ctx_dim=14, alpha=args.alpha, seed=11)
        r, o = run_bandit(stream, pol, context_cold, args.delay, args.noise,
                          label='bandit_cold', noise_seed=202)
        print(f'  mean reward={r.mean():.4f}  mean regret={(o - r).mean():.4f}  ({time.time() - t0:.1f}s)')
        results['bandit_cold'] = r

    # Summary
    print('\n' + '=' * 72)
    print('CUMULATIVE REGRET vs ORACLE')
    print('=' * 72)
    print_milestones(results, oracle)

    print('\nLast-1000 mean reward:')
    print(f'  oracle:               {oracle[-1000:].mean():.4f}')
    for name, r in results.items():
        print(f'  {name:20s}  {r[-1000:].mean():.4f}')

    # Save
    np.savez(args.out, oracle=oracle,
             stream_personas=np.array([p for p, _ in stream]),
             **{k: v for k, v in results.items()})
    print(f'\nResults saved -> {args.out}')

    # Chart-ready: 50 evenly-spaced milestones
    pts = np.linspace(50, args.n, 50, dtype=int)
    print('\n# Chart-ready arrays (50 milestones)')
    for name, r in results.items():
        arr = cum_regret(r, oracle)
        print(f'reg_{name} = {[round(float(arr[m - 1]), 1) for m in pts]}')

    print(f'\nTotal time: {time.time() - t0_total:.1f}s')


if __name__ == '__main__':
    main()
