"""
Run static + LLM-policy baselines on the LLM-persona simulator.

Both baselines are deterministic at a given seed, so single trace each.

Saves results to results_baselines_llm.npz with keys:
  - oracle, static_policy, llm_policy
"""
from __future__ import annotations
import argparse
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import make_session_stream, true_page_reward, oracle_reward
from edp.policies.static import StaticPolicy
from edp.policies.llm_policy import LLMPolicy


def run_policy(stream, policy, with_category=True):
    rewards = np.zeros(len(stream))
    oracle = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        if with_category and hasattr(policy, 'select_page_with_category'):
            page = policy.select_page_with_category(f, c)
        else:
            page = policy.select_page(f)
        rewards[i] = true_page_reward(p, c, page)
        oracle[i] = oracle_reward(p, c)
    return rewards, oracle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--source', type=str, default='llm',
                    help='persona source (parametric|llm)')
    ap.add_argument('--out', type=str, default='results_baselines_llm.npz')
    args = ap.parse_args()

    if args.source:
        from edp.ground_truth import set_source
        set_source(args.source)

    print(f'== Baselines on {args.source} personas ==')
    stream = make_session_stream(args.n, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])

    print('\n[static]')
    t0 = time.time()
    static = StaticPolicy()
    print(f'  page = {static._page}')
    r_static, _ = run_policy(stream, static, with_category=False)
    print(f'  cum regret = {(oracle - r_static).sum():.1f}  ({time.time() - t0:.1f}s)')

    print('\n[llm_policy]')
    t0 = time.time()
    llm = LLMPolicy()
    r_llm, _ = run_policy(stream, llm, with_category=True)
    print(f'  cum regret = {(oracle - r_llm).sum():.1f}  ({time.time() - t0:.1f}s)')

    # As % of oracle for direct comparison
    total_o = oracle.sum()
    print('\n== Summary (% of oracle reward lost) ==')
    print(f'  static_policy:  {(oracle - r_static).sum() / total_o * 100:.2f}%')
    print(f'  llm_policy:     {(oracle - r_llm).sum() / total_o * 100:.2f}%')

    np.savez(args.out, oracle=oracle, static_policy=r_static, llm_policy=r_llm)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
