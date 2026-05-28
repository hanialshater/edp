"""Canonical WPO-Gym leaderboard.

Runs every policy through the SAME environment + runner (edp/env.py,
edp/agents.py) under production reward conditions, on both simulators,
multi-seed where stochastic. One harness, one seed protocol, one JSON —
this is the provenance fix and the benchmark spine.

    python experiments/run_leaderboard.py --n 10000 --seeds 5

Output: results/leaderboard.json
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp.env import PageCompositionEnv
from edp.agents import EDPAgent, BanditAgent, BayesianEDPAgent, run_episode
from edp.policies.edp import EDPPolicy
from edp.policies.bandit import BanditPolicy
from edp.policies.slate import SlateLinTSPolicy
from edp.policies.comblinucb import CombLinUCB
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.static import StaticPolicy, topk_by_base
from edp.catalog import WIDGETS
from edp.config import N_SLOTS


class RandomAgent:
    """Lower bound: shuffle the registry, take the first N_SLOTS."""
    def __init__(self, seed=0):
        self.rng = np.random.default_rng(seed)
    def act(self, obs):
        return list(self.rng.permutation(WIDGETS)[:N_SLOTS]), None
    def learn(self, r, payload):
        pass
    def maybe_checkpoint(self, i):
        pass


class StaticAgent:
    """Deterministic page (default: top-N_SLOTS by base prior)."""
    def __init__(self, page=None):
        self.policy = StaticPolicy(page)
    def act(self, obs):
        return self.policy.select_page(obs.feat), None
    def learn(self, r, payload):
        pass
    def maybe_checkpoint(self, i):
        pass


def edits_dir(source):
    return 'state/evolve_state' if source == 'parametric' else 'state/evolve_state_llm'


def agent_trajectories(source):
    if source == 'parametric':
        return ['state/evolve_state_rep1', 'state/evolve_state_rep2', 'state/evolve_state_rep3']
    return ['state/evolve_state_llm', 'state/evolve_state_llm_rep2', 'state/evolve_state_llm_rep3']


def run_one(source, builder, seeds, n, *, stochastic=True, trajectories=None):
    """Run a policy `builder(seed, sched)` across seeds; return mean/sem/all."""
    vals = []
    if trajectories is not None:  # EDP-agent: one run per committed edit trajectory
        for d in trajectories:
            sched = {ms: f'{d}/edits_round_{ms}.json' for ms in (2500, 5000, 7500)
                     if os.path.exists(f'{d}/edits_round_{ms}.json')}
            env = PageCompositionEnv(n=n, seed=42, source=source, delay=500, noise_sigma=0.20)
            vals.append(run_episode(env, builder(0, sched))['regret_pct'])
    else:
        reps = seeds if stochastic else 1
        for rep in range(reps):
            env = PageCompositionEnv(n=n, seed=42, source=source, delay=500, noise_sigma=0.20)
            vals.append(run_episode(env, builder(1000 + rep * 17, None))['regret_pct'])
    a = np.array(vals)
    return {'mean_pct': float(a.mean()),
            'sem_pct': float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else 0.0,
            'all_pct': [float(x) for x in a]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--out', type=str, default='results/leaderboard.json')
    args = ap.parse_args()

    out = {'config': {'n': args.n, 'seeds': args.seeds,
                      'conditions': 'production (page-level, delay=500, sigma=0.20)'},
           'cells': {}}

    for source in ('llm', 'parametric'):   # LLM-persona is primary
        sched_dir = edits_dir(source)
        sched = {ms: f'{sched_dir}/edits_round_{ms}.json' for ms in (2500, 5000, 7500)
                 if os.path.exists(f'{sched_dir}/edits_round_{ms}.json')}

        policies = {
            'random':        (lambda s, _: RandomAgent(seed=s), True, None),
            'static_top6':   (lambda s, _: StaticAgent(), False, None),
            'lints_cold':    (lambda s, _: BanditAgent(BanditPolicy(ctx_dim=14, alpha=0.3, seed=s), context='cold'), True, None),
            'lints_warm':    (lambda s, _: BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.3, seed=s), context='warm'), True, None),
            'slate_lints':   (lambda s, _: BanditAgent(SlateLinTSPolicy(ctx_dim=7, alpha=0.3, seed=s), context='warm'), True, None),
            'comblinucb':    (lambda s, _: BanditAgent(CombLinUCB(ctx_dim=7, alpha=0.3), context='warm'), True, None),
            'greedy_lints':  (lambda s, _: BayesianEDPAgent(BayesianEDPPolicy(lr=5e-4, lam=0.0, prior_sigma=0.3), schedule={}), True, None),
            'edp_static':    (lambda s, _: EDPAgent(EDPPolicy()), False, None),
            'bayesian_edp':  (lambda s, _: BayesianEDPAgent(BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3), schedule=sched), True, None),
            'edp_agent':     (lambda s, sc: EDPAgent(EDPPolicy(), schedule=sc), False, agent_trajectories(source)),
        }

        out['cells'][source] = {}
        for name, (builder, stoch, traj) in policies.items():
            res = run_one(source, builder, args.seeds, args.n,
                          stochastic=stoch, trajectories=traj)
            out['cells'][source][name] = res
            print(f'[{source:10s}] {name:14s} {res["mean_pct"]:6.2f} ± {res["sem_pct"]:.2f} %')

    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
