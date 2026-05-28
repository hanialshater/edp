"""Demonstrates the Gym-like env/agent split (edp/env.py + edp/agents.py).

Runs EDP-static, LinTS-warm, CombLinUCB, and Bayesian-EDP through the
*same* environment and the *same* runner, with no policy-specific loop
code. Prints the headline regret-percent for each and checks it against
the paper's §5.1 production-condition numbers, so the abstraction is
verified to reproduce the inlined-loop results rather than just run.

    python experiments/run_gym_demo.py --source parametric
"""
from __future__ import annotations
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp.env import PageCompositionEnv
from edp.agents import EDPAgent, BanditAgent, BayesianEDPAgent, run_episode
from edp.policies.edp import EDPPolicy
from edp.policies.bandit import BanditPolicy
from edp.policies.comblinucb import CombLinUCB
from edp.policies.bayesian_edp import BayesianEDPPolicy


# §5.1 production-condition reference (% of oracle reward lost)
REFERENCE = {
    'parametric': {'edp_static': 10.7, 'lints_warm': 18.9,
                   'comblinucb': 10.5, 'bayesian_edp': 7.6},
    'llm':        {'edp_static': 19.8, 'lints_warm': 21.6,
                   'comblinucb': 17.3, 'bayesian_edp': 11.0},
}


def edits_dir(source: str) -> str:
    return 'state/evolve_state' if source == 'parametric' else 'state/evolve_state_llm'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--source', choices=['parametric', 'llm'], default='parametric')
    args = ap.parse_args()

    d = edits_dir(args.source)
    schedule = {ms: f'{d}/edits_round_{ms}.json' for ms in (2500, 5000, 7500)
                if os.path.exists(f'{d}/edits_round_{ms}.json')}

    def fresh_env():
        return PageCompositionEnv(n=args.n, seed=args.seed, source=args.source,
                                  delay=500, noise_sigma=0.20)

    runs = {
        'edp_static':   (fresh_env(), EDPAgent(EDPPolicy())),
        'edp_agent':    (fresh_env(), EDPAgent(EDPPolicy(), schedule=schedule)),
        'lints_warm':   (fresh_env(), BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.3,
                                                               seed=7), context='warm')),
        'comblinucb':   (fresh_env(), BanditAgent(CombLinUCB(ctx_dim=7, alpha=0.3),
                                                  context='warm')),
        'bayesian_edp': (fresh_env(), BayesianEDPAgent(
            BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3), schedule=schedule)),
    }

    ref = REFERENCE[args.source]
    print(f'\nGym-API run — source={args.source}, n={args.n}, production '
          f'conditions (page-level, delay=500, sigma=0.20)\n')
    print(f'{"method":14s} {"regret%":>9s} {"paper ref":>10s} {"delta":>7s}')
    print('-' * 44)
    for name, (env, agent) in runs.items():
        out = run_episode(env, agent)
        pct = out['regret_pct']
        r = ref.get(name.replace('_agent', '_static') if name == 'edp_agent' else name)
        if name == 'edp_agent':
            r = None  # multi-seed mean in paper; single canned run here differs
        delta = f'{pct - r:+.1f}' if r is not None else '   —'
        rstr = f'{r:.1f}' if r is not None else '   —'
        print(f'{name:14s} {pct:8.2f}% {rstr:>10s} {delta:>7s}')
    print('\n(edp_static / lints_warm / comblinucb / bayesian_edp should land '
          'within ~1 pp of the paper reference; edp_agent uses the single '
          'canned edit trajectory, not the multi-seed mean.)')


if __name__ == '__main__':
    main()
