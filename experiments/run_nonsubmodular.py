"""
P2-1: non-submodular reward experiment.

Tests whether the EDP-architecture advantage over bandits survives when
the reward function is NOT submodular. The base reward is diminishing
returns on (need × provision); we add a substitutes term that penalises
co-occurrence of widgets in the same `type` family.

Specifically: substitutes_penalty = α · Σ_pairs δ(type_i == type_j)
where the sum is over all pairs of widgets in the page, type is the
widget's `type` attribute (e.g. 'outfit', 'returns', 'premium', etc.),
and α is a tunable penalty weight.

So pages with two widgets of the same type lose α from the total.
This breaks the submodular structure (greedy-best-next is no longer
optimal) and tests whether EDP's architecture still beats bandits.

We run:
  - EDP-static (uses original GAM, doesn't know about substitutes)
  - EDP-agent (single rep — uses canonical edit JSONs, also doesn't know)
  - GreedyLinTS (learns from observed reward, can in principle find
    a complementary-types policy)
  - CombLinUCB (same)
  - Per-slot LinTS-warm
  - Slate-LinTS-warm

All on the parametric simulator (faster), under production conditions
(page-level, delay=500, σ=0.20).
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, DelayedFeedback, N_SLOTS, BanditPolicy,
                 EDPPolicy, true_page_reward as submodular_reward,
                 oracle_reward as submodular_oracle)
from edp.policies.bandit import context_warm, context_cold
from edp.policies.slate import SlateLinTSPolicy
from edp.policies.comblinucb import CombLinUCB
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.edp import make_problem_shapes, load_edits_json, make_modules
from edp.catalog import TRUE_PROVISIONS


# Widget → type, derived from `make_modules()`
def widget_types():
    mods = make_modules()
    return {w: m.get('type', 'default') for w, m in mods.items()}


def non_submodular_reward(persona, category, page, alpha=0.15):
    """Submodular reward minus a same-type substitutes penalty.

    Same-type widget pairs in a page are substitutes for each other —
    a fit-reassurance widget plus a size-guide widget (both `type='size'`
    in the original code's labelling family but actually different here)
    add less than the sum of their parts.
    """
    base = submodular_reward(persona, category, page)
    types = widget_types()
    pen = 0.0
    for i in range(len(page)):
        for j in range(i + 1, len(page)):
            if types.get(page[i], '?') == types.get(page[j], '??'):
                pen += alpha
    return max(0.0, base - pen)


def non_submodular_oracle(persona, category, alpha=0.15):
    """Best-page oracle under the new non-submodular reward.

    Since the reward is no longer submodular, greedy is not optimal.
    We do a small beam-search over the action space.
    """
    # Beam over partial pages. State: (page_so_far, predicted_total).
    # We use the submodular reward + penalty as a tractable score.
    from edp.catalog import WIDGETS
    beam = [([], 0.0)]
    for _ in range(N_SLOTS):
        new = []
        for page, _ in beam:
            for w in WIDGETS:
                if w in page:
                    continue
                trial = page + [w]
                # Score the partial page so far
                r = non_submodular_reward(persona, category, trial, alpha)
                new.append((trial, r))
        # Beam width 50
        new.sort(key=lambda x: -x[1])
        beam = new[:50]
    return beam[0][1]


def run_edp(stream, policy, reward_fn):
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        rewards[i] = reward_fn(p, c, policy.select_page(f))
    return rewards


def run_edp_with_schedule(stream, sched, reward_fn):
    pol = EDPPolicy()
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        if i in sched:
            pol.apply_edit_batch(sched[i])
        rewards[i] = reward_fn(p, c, pol.select_page(f))
    return rewards


def run_bandit(stream, ctx_fn, ctx_dim, reward_fn, *, page_attribution=True,
               delay=500, sigma=0.20, policy_seed=7, noise_seed=701, alpha=0.3,
               PolicyCls=BanditPolicy):
    if PolicyCls is BanditPolicy:
        pol = BanditPolicy(ctx_dim=ctx_dim, alpha=alpha, seed=policy_seed)
    elif PolicyCls is SlateLinTSPolicy:
        pol = SlateLinTSPolicy(ctx_dim=ctx_dim, alpha=alpha, seed=policy_seed)
    elif PolicyCls is CombLinUCB:
        pol = CombLinUCB(ctx_dim=ctx_dim, alpha=alpha)
    else:
        raise ValueError(PolicyCls)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))

    def consume(r_obs, payload):
        if PolicyCls is BanditPolicy:
            pol.record_feedback(payload, r_obs)
        else:
            # SlateLinTS and CombLinUCB share the same payload format
            pol.record_feedback(payload, r_obs)

    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            consume(r_obs, payload)
        x = ctx_fn(f, c)
        page, payload = pol.select_page_with_payload(x)
        r = reward_fn(p, c, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        consume(r_obs, payload)
    return rewards


def run_bayesian(stream, reward_fn, edits_dir):
    pol = BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3)
    fb = DelayedFeedback(delay=500, noise_sigma=0.20, seed=42)
    sched = {
        2500: f'{edits_dir}/edits_round_2500.json',
        5000: f'{edits_dir}/edits_round_5000.json',
        7500: f'{edits_dir}/edits_round_7500.json',
    }
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        if i in sched and os.path.exists(sched[i]):
            from edp.policies.edp import apply_edits
            edits, _ = load_edits_json(sched[i])
            new_modules = apply_edits(pol.modules, [
                (e['widget'], e['path'], e.get('from', 0.0),
                 e['to'], e.get('reason', ''))
                for e in edits
            ])
            pol.reset_prior(new_modules)
        for r_obs, payload in fb.drain_ready(i):
            pol.update_from_delayed(payload, r_obs)
        page, payload = pol.select_page_with_payload(f)
        r = reward_fn(p, c, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.update_from_delayed(payload, r_obs)
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--alpha', type=float, default=0.15,
                    help='same-type substitutes penalty per pair')
    ap.add_argument('--reps', type=int, default=3,
                    help='reps for stochastic bandit methods')
    ap.add_argument('--out', type=str, default='results_nonsubmodular.json')
    args = ap.parse_args()

    from edp.ground_truth import set_source
    set_source('parametric')

    stream = make_session_stream(args.n, seed=42)
    reward_fn = lambda p, c, page: non_submodular_reward(p, c, page, args.alpha)

    print(f'Computing non-submodular oracle (beam=50) for {args.n} sessions...')
    # Cache oracle per (persona, category) — only 8 × 6 = 48 entries
    oracle_cache = {}
    for p, c, _ in stream:
        if (p, c) not in oracle_cache:
            oracle_cache[(p, c)] = non_submodular_oracle(p, c, args.alpha)
    oracle = np.array([oracle_cache[(p, c)] for p, c, _ in stream])
    total = float(oracle.sum())
    print(f'Non-submodular oracle total: {total:.1f}')
    # Reference: submodular oracle on the same stream for comparison
    sub_total = float(sum(submodular_oracle(p, c) for p, c, _ in stream))
    print(f'Submodular oracle total (for ref): {sub_total:.1f}')

    shapes = make_problem_shapes()
    summary = {}

    # Deterministic methods
    print('\nEDP-static (deterministic, ignores reward)...')
    r = run_edp(stream, EDPPolicy(), reward_fn)
    pct = (oracle - r).sum() / total * 100
    summary['edp_static'] = {'mean_pct': float(pct), 'sem_pct': 0.0}
    print(f'  {pct:.2f}%')

    print('EDP-agent (canned edits from evolve_state, single rep)...')
    sched = {ms: load_edits_json(f'evolve_state/edits_round_{ms}.json')[0]
              for ms in (2500, 5000, 7500)
              if os.path.exists(f'evolve_state/edits_round_{ms}.json')}
    r = run_edp_with_schedule(stream, sched, reward_fn)
    pct = (oracle - r).sum() / total * 100
    summary['edp_agent'] = {'mean_pct': float(pct), 'sem_pct': 0.0}
    print(f'  {pct:.2f}%')

    print('Bayesian-EDP (single rep)...')
    r = run_bayesian(stream, reward_fn, 'evolve_state')
    pct = (oracle - r).sum() / total * 100
    summary['bayesian_edp'] = {'mean_pct': float(pct), 'sem_pct': 0.0}
    print(f'  {pct:.2f}%')

    # Stochastic bandits — multi-seed
    for label, ctx_fn, cd, PolCls in [
        ('lints_warm',   lambda f, c: context_warm(f, shapes, c, with_category=False), 7,  BanditPolicy),
        ('slate_warm',   lambda f, c: context_warm(f, shapes, c, with_category=False), 7,  SlateLinTSPolicy),
        ('comb_warm',    lambda f, c: context_warm(f, shapes, c, with_category=False), 7,  CombLinUCB),
    ]:
        print(f'\n{label} (N={args.reps})...')
        vals = []
        for rep in range(args.reps):
            seed = 1000 + rep * 17
            r = run_bandit(stream, ctx_fn, cd, reward_fn,
                            policy_seed=seed, noise_seed=seed * 7 + 1,
                            PolicyCls=PolCls)
            pct = (oracle - r).sum() / total * 100
            vals.append(pct)
        v = np.array(vals)
        summary[label] = {
            'mean_pct': float(v.mean()),
            'sem_pct': float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
        }
        print(f'  {v.mean():.2f} ± {v.std(ddof=1) / np.sqrt(len(v)):.2f} %')

    with open(args.out, 'w') as f:
        json.dump({'alpha': args.alpha, 'cells': summary}, f, indent=2)
    print(f'\nsaved -> {args.out}')
    print('\nSummary (% of non-submodular oracle reward lost):')
    for k, v in summary.items():
        if v.get('sem_pct', 0) > 0.01:
            print(f'  {k:14s}  {v["mean_pct"]:5.2f} ± {v["sem_pct"]:.2f} %')
        else:
            print(f'  {k:14s}  {v["mean_pct"]:5.2f} %')


if __name__ == '__main__':
    main()
