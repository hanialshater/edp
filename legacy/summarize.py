"""
Print the final paper table from all available data.

Loads:
  - results_multiseed.npz  (10 bandit seeds, deterministic edp static/canned)
  - evolve_state_rep*/state.json (3 EDP-agent reps)
  - opro_state_rep*/state.json   (3 OPRO reps)

Prints means ± SE @ each milestone session count.
"""
from __future__ import annotations
import glob
import json
import os
import numpy as np

from sim import ORACLE_REWARDS, make_session_stream

def cum_regret(r, o):
    return np.cumsum(o - r)


def stats_at(reps, oracle, m):
    if reps.shape[0] == 0:
        return float('nan'), 0.0
    vals = np.array([cum_regret(reps[i], oracle)[m - 1] for i in range(reps.shape[0])])
    sem = float(vals.std(ddof=1) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0
    return float(vals.mean()), sem


def load_agent_reps(prefix, n):
    dirs = sorted(glob.glob(f'{prefix}_rep*'))
    out = []
    for d in dirs:
        p = os.path.join(d, 'state.json')
        if os.path.exists(p):
            arr = np.array(json.load(open(p))['rewards'])
            if len(arr) >= n:
                out.append(arr[:n])
    return np.stack(out) if out else np.zeros((0, n))


def main():
    d = np.load('../results/results_multiseed.npz')
    oracle = d['oracle']
    n = len(oracle)
    agent = load_agent_reps('../state/evolve_state', n)
    opro = load_agent_reps('../state/opro_state', n)

    milestones = [500, 1000, 2500, 5000, 7500, 10000]
    methods = [
        ('LinTS-cold (10 seeds)',   d['bandit_cold']),
        ('LinTS-warm (10 seeds)',   d['bandit_warm']),
        ('EDP-static (det.)',       d['edp_static'][None, :]),
        ('EDP-OPRO (3 reps)',       opro),
        ('EDP-canned (det.)',       d['edp_canned'][None, :]),
        ('EDP-agent (3 reps)',      agent),
    ]

    # Header
    print('=' * 110)
    print('  Cumulative regret at milestone session counts  (mean ± SE across reps)')
    print('=' * 110)
    print(f'  {"method":24s} ' + ' '.join(f'{m:>12,}' for m in milestones))
    for name, reps in methods:
        cells = []
        for m in milestones:
            mu, se = stats_at(reps, oracle, m)
            if reps.shape[0] > 1 and se > 0.05:
                cells.append(f'{mu:>7.1f}±{se:>4.1f}')
            else:
                cells.append(f'{mu:>12.1f}')
        print(f'  {name:24s} ' + ' '.join(cells))

    # Last-1000 mean reward
    print()
    print(f'  {"method":24s} {"last-1k mean reward":>22s}')
    for name, reps in methods:
        if reps.shape[0] == 0:
            continue
        v = reps[:, -1000:].mean()
        print(f'  {name:24s} {v:>22.4f}')


if __name__ == '__main__':
    main()
