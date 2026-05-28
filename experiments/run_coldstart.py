"""Cold-start curve: regret vs sessions-seen.

The α-sweep (§5.3) shows a tuned bandit ties EDP at 10K sessions on the
stationary single-surface task. But production A/B arms mostly close well
before 10K, and the GAM launches competent from session 0 (LLM prior)
while a bandit — tuned or not — must warm up from an uninformative
posterior. This experiment measures regret-% over the FIRST M sessions
for M in {500, 1k, 2.5k, 5k, 7.5k, 10k}, so the cold-start advantage is
demonstrated, not asserted.

One 10K episode per policy (multi-seed/-trajectory where stochastic);
milestone regret is sliced from the per-session arrays the env records.

    python experiments/run_coldstart.py --out results/coldstart.json
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
from edp.policies.bayesian_edp import BayesianEDPPolicy

MILESTONES = [500, 1000, 2500, 5000, 7500, 10000]


def regret_at(env, m):
    o = env.oracles[:m].sum()
    r = env.rewards[:m].sum()
    return 100.0 * (o - r) / o if o else 0.0


def edits_dir(source):
    return 'state/evolve_state' if source == 'parametric' else 'state/evolve_state_llm'


def agent_trajectories(source):
    if source == 'parametric':
        return ['state/evolve_state_rep1', 'state/evolve_state_rep2', 'state/evolve_state_rep3']
    return ['state/evolve_state_llm', 'state/evolve_state_llm_rep2', 'state/evolve_state_llm_rep3']


def curve(source, builder, *, seeds=3, trajectories=None, n=10000):
    """Return {milestone: (mean, sem)} of first-M regret-%."""
    per_m = {m: [] for m in MILESTONES}
    if trajectories is not None:
        runs = trajectories
        for d in runs:
            sched = {ms: f'{d}/edits_round_{ms}.json' for ms in (2500, 5000, 7500)
                     if os.path.exists(f'{d}/edits_round_{ms}.json')}
            env = PageCompositionEnv(n=n, seed=42, source=source, delay=500, noise_sigma=0.20)
            run_episode(env, builder(0, sched))
            for m in MILESTONES:
                per_m[m].append(regret_at(env, m))
    else:
        for rep in range(seeds):
            env = PageCompositionEnv(n=n, seed=42, source=source, delay=500, noise_sigma=0.20)
            run_episode(env, builder(1000 + rep * 17, None))
            for m in MILESTONES:
                per_m[m].append(regret_at(env, m))
    out = {}
    for m in MILESTONES:
        a = np.array(per_m[m])
        out[m] = [float(a.mean()), float(a.std(ddof=1) / np.sqrt(len(a))) if len(a) > 1 else 0.0]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', choices=['parametric', 'llm'], default='llm')
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--out', type=str, default='results/coldstart.json')
    args = ap.parse_args()

    src = args.source
    sched = {ms: f'{edits_dir(src)}/edits_round_{ms}.json' for ms in (2500, 5000, 7500)
             if os.path.exists(f'{edits_dir(src)}/edits_round_{ms}.json')}

    policies = {
        'edp_static':       (lambda s, _: EDPAgent(EDPPolicy()), None),
        'edp_agent':        (lambda s, sc: EDPAgent(EDPPolicy(), schedule=sc), agent_trajectories(src)),
        'bayesian_edp':     (lambda s, _: BayesianEDPAgent(BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3), schedule=sched), None),
        'lints_warm_a0.3':  (lambda s, _: BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.3, seed=s), context='warm'), None),
        'lints_warm_a0.05': (lambda s, _: BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.05, seed=s), context='warm'), None),
    }

    out = {'source': src, 'milestones': MILESTONES, 'curves': {}}
    for name, (builder, traj) in policies.items():
        out['curves'][name] = curve(src, builder, seeds=args.seeds, trajectories=traj)
        row = '  '.join(f'{m//1000 if m>=1000 else m}{"k" if m>=1000 else ""}={out["curves"][name][m][0]:.1f}'
                        for m in MILESTONES)
        print(f'[{src}] {name:18s} {row}')

    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
