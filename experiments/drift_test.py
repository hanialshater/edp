"""
Drift test: rotate the persona mixture mid-stream and re-run every method.

At session 5000 we shift the persona-mixture probabilities — bumping
returner_anxious (8% -> 25%), browser_lurker (10% -> 18%), and dropping
confident_buyer (12% -> 4%) and outfit_seeker (12% -> 5%). The total mix
stays normalised. This simulates a seasonality / channel-mix shift.

We run:
  - LinTS-warm (the production-stack baseline)
  - EDP-static
  - EDP-canned (canned edits at the original 2500/5000/7500 schedule)
  - EDP-agent  (using the existing evolve_state_llm trajectory; reads
    the same edit-batch sequence on the new stream)

Also compute the oracle on the new stream and report cum regret per method
on the post-drift segment (5000-10000) as well as the full stream.

Persona source is held to LLM (paper §2.2c) since that's the harder
simulator.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (oracle_reward, true_page_reward, DelayedFeedback, EDPPolicy,
                 BanditPolicy)
from edp.policies.bandit import context_warm
from edp.policies.edp import make_problem_shapes, load_edits_json, apply_edits


# Pre-drift mixture (from data/personas_text.yaml renormalised)
# Post-drift: spike returner_anxious + browser_lurker, drop confident +
# outfit. Drop new=hesitant_first_buyer (10% drop) since they're a stable
# acquisition channel.
SHIFT_AT = 5000


def make_drift_stream(n=10_000, seed=42):
    """
    Reproducible (persona, category, feat) stream with persona mixture
    shift at session SHIFT_AT.
    """
    from edp.ground_truth import set_source, get_source
    from edp.catalog import CATEGORIES, CATEGORY_MIX
    set_source('llm')
    src = get_source()
    p_names = src.persona_names()
    base_w = src.mixture_weights()

    # Drifted weights
    drifted = dict(base_w)
    bumps = {'returner_anxious': 0.25, 'browser_lurker': 0.18,
             'post_return_returner': 0.15}
    drops = {'confident_repeat_buyer': 0.04, 'outfit_event_planner': 0.05,
             'tabbed_comparison_shopper': 0.05, 'birthday_rush_gifter': 0.04}
    for k, v in bumps.items():
        if k in drifted:
            drifted[k] = v
    for k, v in drops.items():
        if k in drifted:
            drifted[k] = v
    # renormalise
    s = sum(drifted.values())
    drifted = {k: v / s for k, v in drifted.items()}

    pre_probs = np.array([base_w[k] for k in p_names])
    pre_probs /= pre_probs.sum()
    post_probs = np.array([drifted[k] for k in p_names])
    post_probs /= post_probs.sum()

    c_names = CATEGORIES
    c_probs = np.array([CATEGORY_MIX[k] for k in c_names])
    c_probs /= c_probs.sum()

    r = np.random.default_rng(seed)
    stream = []
    for i in range(n):
        probs = pre_probs if i < SHIFT_AT else post_probs
        pn = r.choice(p_names, p=probs)
        cn = r.choice(c_names, p=c_probs)
        feat = src.sample_session(r, pn)
        stream.append((pn, cn, feat))
    return stream


def run_bandit_warm(stream, oracle, *, delay=500, sigma=0.2, alpha=0.3,
                    policy_seed=7, noise_seed=701):
    shapes = make_problem_shapes()
    pol = BanditPolicy(ctx_dim=7, alpha=alpha, seed=policy_seed)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = context_warm(f, shapes, c, with_category=False)
        page, payload = pol.select_page_with_payload(x)
        r = true_page_reward(p, c, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)
    return rewards


def run_edp(stream, schedule=None):
    pol = EDPPolicy()
    if schedule:
        # we apply the schedule at session indices in the order given
        sched = list(schedule)
    else:
        sched = []
    sched.sort(key=lambda x: x[0])
    next_chk = 0
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        while next_chk < len(sched) and sched[next_chk][0] == i:
            pol.apply_edit_batch(sched[next_chk][1])
            next_chk += 1
        page = pol.select_page(f)
        rewards[i] = true_page_reward(p, c, page)
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=str, default='results_drift_test.json')
    args = ap.parse_args()

    stream = make_drift_stream(seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])

    pre = slice(0, SHIFT_AT)
    post = slice(SHIFT_AT, None)

    print('Running EDP-static...')
    r_static = run_edp(stream)
    print('Running EDP-canned...')
    sched = [
        (2500, load_edits_json('edits/round1.json')[0]),
        (5000, load_edits_json('edits/round2.json')[0]),
        (7500, load_edits_json('edits/round3.json')[0]),
    ]
    r_canned = run_edp(stream, schedule=sched)
    print('Running EDP-agent (re-applies the LLM-source live-agent edits)...')
    sched_agent = [
        (2500, load_edits_json('evolve_state_llm/edits_round_2500.json')[0]),
        (5000, load_edits_json('evolve_state_llm/edits_round_5000.json')[0]),
        (7500, load_edits_json('evolve_state_llm/edits_round_7500.json')[0]),
    ]
    r_agent = run_edp(stream, schedule=sched_agent)
    print('Running LinTS-warm (5 seeds)...')
    r_warm = []
    for rep in range(5):
        seed_base = 1000 + rep * 17
        r_warm.append(run_bandit_warm(stream, oracle,
                                       policy_seed=seed_base,
                                       noise_seed=seed_base * 7 + 1))
    r_warm = np.stack(r_warm)

    def pct_lost(r, sl):
        if r.ndim == 1:
            return float((oracle[sl] - r[sl]).sum() / oracle[sl].sum() * 100)
        return float((oracle[None, sl] - r[:, sl]).sum(axis=1).mean()
                     / oracle[sl].sum() * 100)

    def sem_pct(r, sl):
        if r.ndim == 1:
            return 0.0
        vals = (oracle[None, sl] - r[:, sl]).sum(axis=1) / oracle[sl].sum() * 100
        return float(vals.std(ddof=1) / np.sqrt(len(vals)))

    rows = [
        ('EDP-static',  r_static),
        ('EDP-canned',  r_canned),
        ('EDP-agent',   r_agent),
        ('LinTS-warm',  r_warm),
    ]

    summary = {}
    print('\n' + '=' * 88)
    print('DRIFT TEST  ·  shift at session 5000  ·  LLM personas + categories')
    print('=' * 88)
    print(f'  {"method":14s} {"pre-drift":>14s}  {"post-drift":>14s}  {"full":>14s}')
    for name, r in rows:
        a = pct_lost(r, pre)
        b = pct_lost(r, post)
        c = pct_lost(r, slice(None))
        sa, sb, sc = sem_pct(r, pre), sem_pct(r, post), sem_pct(r, slice(None))
        summary[name] = {
            'pre_pct': a, 'pre_sem': sa,
            'post_pct': b, 'post_sem': sb,
            'full_pct': c, 'full_sem': sc,
        }
        def fmt(p, s):
            return f'{p:5.2f}% ± {s:.2f}%' if s > 0.05 else f'{p:5.2f}%'
        print(f'  {name:14s} {fmt(a, sa):>14s}  {fmt(b, sb):>14s}  {fmt(c, sc):>14s}')

    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
