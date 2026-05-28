"""Bandit exploration-parameter sweep (addresses the 'baselines under-tuned'
review point). Sweeps alpha for LinTS-warm, Slate-LinTS, and CombLinUCB on
both simulators under production conditions, reports best-alpha per cell.

If the per-arm bandits still trail the EDP architecture at their *best*
alpha, the 'page-level attribution is the bottleneck' claim is robust to
tuning, not an artifact of a single alpha.

    python experiments/run_alpha_sweep.py --n 10000 --seeds 3

Output: results/alpha_sweep.json
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp.env import PageCompositionEnv
from edp.agents import BanditAgent, run_episode
from edp.policies.bandit import BanditPolicy
from edp.policies.slate import SlateLinTSPolicy
from edp.policies.comblinucb import CombLinUCB

ALPHAS = [0.05, 0.1, 0.2, 0.3, 0.5, 1.0]


def make(method, alpha, seed):
    if method == 'lints_warm':
        return BanditAgent(BanditPolicy(ctx_dim=7, alpha=alpha, seed=seed), context='warm')
    if method == 'slate_lints':
        return BanditAgent(SlateLinTSPolicy(ctx_dim=7, alpha=alpha, seed=seed), context='warm')
    if method == 'comblinucb':
        return BanditAgent(CombLinUCB(ctx_dim=7, alpha=alpha), context='warm')
    raise ValueError(method)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--out', type=str, default='results/alpha_sweep.json')
    args = ap.parse_args()

    out = {'alphas': ALPHAS, 'n': args.n, 'seeds': args.seeds, 'cells': {}}
    for source in ('llm', 'parametric'):
        out['cells'][source] = {}
        for method in ('lints_warm', 'slate_lints', 'comblinucb'):
            best = None
            for alpha in ALPHAS:
                vals = []
                reps = 1 if method == 'comblinucb' else args.seeds
                for rep in range(reps):
                    env = PageCompositionEnv(n=args.n, seed=42, source=source,
                                             delay=500, noise_sigma=0.20)
                    vals.append(run_episode(env, make(method, alpha, 1000 + rep * 17))['regret_pct'])
                m = float(np.mean(vals))
                if best is None or m < best['mean_pct']:
                    best = {'alpha': alpha, 'mean_pct': m,
                            'sem_pct': float(np.std(vals, ddof=1) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0}
                print(f'[{source:10s}] {method:12s} alpha={alpha:<4} -> {m:6.2f} %')
            out['cells'][source][method] = best
            print(f'[{source:10s}] {method:12s} BEST alpha={best["alpha"]} -> {best["mean_pct"]:.2f} ± {best["sem_pct"]:.2f} %')

    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
