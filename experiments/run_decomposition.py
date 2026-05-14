"""
Decomposition study: separate the EDP-agent gain into (architecture)
+ (LLM prior) + (continuous SGD updates).

Methods:
  - GreedyLinTS                  : EDP architecture, λ=0, no LLM checkpoint resets
  - EDP-static                   : EDP architecture, LLM cold-start, no updates
  - EDP-agent (single trial)     : EDP architecture, LLM prior + LLM checkpoint edits
  - Bayesian-EDP (multi-seed)    : LLM prior + continuous SGD updates

Run all four on parametric and LLM, lab and production. Multi-seed only
applies to Bayesian-EDP and GreedyLinTS (both have an SGD noise channel
worth varying); EDP-static and EDP-agent are deterministic given the
edit JSONs.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run_bayesian_edp import run_bayesian
from edp import (make_session_stream, oracle_reward, true_page_reward, EDPPolicy)
from edp.policies.edp import load_edits_json, apply_edits


def run_edp_static(stream):
    pol = EDPPolicy()
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        rewards[i] = true_page_reward(p, c, pol.select_page(f))
    return rewards


def run_edp_agent(stream, edits_dir):
    pol = EDPPolicy()
    sched = {}
    for ms in (2500, 5000, 7500):
        path = f'{edits_dir}/edits_round_{ms}.json'
        if os.path.exists(path):
            sched[ms] = load_edits_json(path)[0]
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        if i in sched:
            pol.apply_edit_batch(sched[i])
        rewards[i] = true_page_reward(p, c, pol.select_page(f))
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--seeds', type=int, default=5,
                    help='reps for stochastic methods (Bayesian-EDP, GreedyLinTS)')
    ap.add_argument('--lr', type=float, default=5e-4)
    ap.add_argument('--lam', type=float, default=2.0)
    ap.add_argument('--prior-sigma', type=float, default=0.3)
    ap.add_argument('--prior-jitter', type=float, default=0.05)
    ap.add_argument('--out', type=str, default='results_decomposition.json')
    args = ap.parse_args()

    edits_for = {'parametric': 'evolve_state', 'llm': 'evolve_state_llm'}

    summary = {}
    for source in ['parametric', 'llm']:
        from edp.ground_truth import set_source
        set_source(source)
        print(f'\n=== persona source: {source} ===')
        stream = make_session_stream(args.n, seed=42)
        oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
        total = float(oracle.sum())
        cells = {}

        # Deterministic methods (lab and prod give same result since they
        # never look at the bandit signal)
        print('  EDP-static (deterministic)...')
        r = run_edp_static(stream)
        edp_static_pct = float((oracle - r).sum() / total * 100)
        cells['edp_static'] = {'lab':  {'mean_pct': edp_static_pct, 'sem_pct': 0.0},
                                'production': {'mean_pct': edp_static_pct, 'sem_pct': 0.0}}
        print(f'    {edp_static_pct:.2f}% (both conditions)')

        print('  EDP-agent (single-trial, deterministic)...')
        r = run_edp_agent(stream, edits_for[source])
        edp_agent_pct = float((oracle - r).sum() / total * 100)
        cells['edp_agent'] = {'lab':  {'mean_pct': edp_agent_pct, 'sem_pct': 0.0},
                               'production': {'mean_pct': edp_agent_pct, 'sem_pct': 0.0}}
        print(f'    {edp_agent_pct:.2f}% (both conditions)')

        # Stochastic methods — multi-seed
        for method, edits_dir, lam in [
            ('greedy_lints', None,                 0.0),
            ('bayesian_edp', edits_for[source],    args.lam),
        ]:
            for cond, kwargs in [
                ('lab',        {'page_attribution': False, 'delay': 50,  'sigma': 0.05}),
                ('production', {'page_attribution': True,  'delay': 500, 'sigma': 0.20}),
            ]:
                vals = []
                for rep in range(args.seeds):
                    seed_base = 1000 + rep * 17
                    t0 = time.time()
                    r = run_bayesian(stream, edits_dir=edits_dir,
                                      lr=args.lr, lam=lam,
                                      prior_sigma=args.prior_sigma,
                                      noise_seed=seed_base * 7 + 1,
                                      prior_jitter=args.prior_jitter,
                                      jitter_seed=seed_base * 11 + 3,
                                      **kwargs)
                    pct = float((oracle - r).sum() / total * 100)
                    vals.append(pct)
                    if rep == 0:
                        print(f'  {method:14s} {cond:11s}: rep1 {pct:5.2f}% ({time.time()-t0:.1f}s)')
                v = np.array(vals)
                key = method
                if key not in cells:
                    cells[key] = {}
                cells[key][cond] = {
                    'mean_pct': float(v.mean()),
                    'sem_pct': float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
                    'all_pct': vals,
                }
            print(f'  {method:14s} done — lab {cells[method]["lab"]["mean_pct"]:.2f}±{cells[method]["lab"]["sem_pct"]:.2f}%  '
                   f'prod {cells[method]["production"]["mean_pct"]:.2f}±{cells[method]["production"]["sem_pct"]:.2f}%')

        summary[source] = cells

    with open(args.out, 'w') as f:
        json.dump({'hyperparams': vars(args), 'cells': summary}, f, indent=2)

    print('\n' + '=' * 90)
    print('DECOMPOSITION — % of oracle reward lost @ 10K  (mean ± SE across seeds)')
    print('=' * 90)
    for source in summary:
        print(f'\n  source: {source}')
        print(f'    {"method":18s}  {"lab":>14s}  {"production":>14s}')
        for m in ('greedy_lints', 'edp_static', 'edp_agent', 'bayesian_edp'):
            l = summary[source][m]['lab']
            p = summary[source][m]['production']
            def fmt(v):
                if v.get('sem_pct', 0) > 0.01:
                    return f'{v["mean_pct"]:5.2f}±{v["sem_pct"]:.2f}%'
                return f'{v["mean_pct"]:5.2f}%'
            print(f'    {m:18s}  {fmt(l):>14s}  {fmt(p):>14s}')

    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
