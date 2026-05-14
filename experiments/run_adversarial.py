"""P3-substitute: adversarial perturbation of TRUE_PROVISIONS.

The validity threat reviewers raise is "the LLM that authored
TRUE_PROVISIONS is the same family that authors edits." A cross-LLM
check (GPT-4 / Gemini) is the canonical answer but requires API access
we don't have. The next-best validity check is perturbing the LLM's
TRUE_PROVISIONS adversarially and rerunning the headline comparisons:
if EDP's win survives ±15 % random perturbation of every provision
value, the qualitative finding is at least not artefactually tied to
the exact LLM-authored numbers.

We run K=5 perturbation seeds × the headline methods on the parametric
simulator under production conditions.
"""
from __future__ import annotations
import argparse
import copy
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, DelayedFeedback, N_SLOTS, BanditPolicy,
                 EDPPolicy)
from edp.policies.bandit import context_warm
from edp.policies.comblinucb import CombLinUCB
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.edp import make_problem_shapes, load_edits_json, apply_edits
from edp.catalog import TRUE_PROVISIONS, WIDGETS


def perturb_provisions(rng: np.random.Generator, scale: float = 0.15):
    """Return a perturbed TRUE_PROVISIONS dict where each provision
    value is multiplied by uniform(1-scale, 1+scale), then clipped to
    [0, 1]. Nonzero entries stay nonzero; zero entries stay zero."""
    out = {}
    for w, provs in TRUE_PROVISIONS.items():
        out[w] = {}
        for need, val in provs.items():
            if val == 0:
                out[w][need] = 0.0
            else:
                factor = 1 + scale * (2 * rng.random() - 1)
                out[w][need] = float(np.clip(val * factor, 0.0, 1.0))
    return out


def perturbed_reward(persona, category, page, provisions, *, needs_map):
    """Submodular reward against a custom provisions map."""
    from edp.catalog import CATEGORY_NEED_MULTIPLIERS
    cat_mult = CATEGORY_NEED_MULTIPLIERS.get(category, {})
    needs = needs_map[persona]
    r = {need: needs.get(need, 0.0) * cat_mult.get(need, 1.0) for need in needs}
    total = 0.0
    for w in page:
        for need, p in provisions[w].items():
            give = min(r.get(need, 0.0), p)
            total += r.get(need, 0.0) * give
            r[need] = max(0.0, r.get(need, 0.0) - p)
    return total


def perturbed_oracle(persona, category, provisions, *, needs_map):
    """Greedy oracle under the perturbed provisions."""
    from edp.catalog import CATEGORY_NEED_MULTIPLIERS
    cat_mult = CATEGORY_NEED_MULTIPLIERS.get(category, {})
    needs = needs_map[persona]
    r = {need: needs.get(need, 0.0) * cat_mult.get(need, 1.0) for need in needs}
    total = 0.0
    used = set()
    for _ in range(N_SLOTS):
        best_w, best_g = None, -1e9
        for w in WIDGETS:
            if w in used:
                continue
            g = 0.0
            for need, p in provisions[w].items():
                g += r.get(need, 0.0) * min(r.get(need, 0.0), p)
            if g > best_g:
                best_g, best_w = g, w
        used.add(best_w)
        for need, p in provisions[best_w].items():
            r[need] = max(0.0, r.get(need, 0.0) - p)
        total += best_g
    return total


def run_perturbation_seed(seed: int, stream, sched_files):
    """Run one perturbation seed for: LinTS-warm, CombLinUCB, EDP-static,
    EDP-agent (canned), Bayesian-EDP (canned). Return %-of-oracle-lost
    for each."""
    from edp.ground_truth import TRUE_NEEDS

    rng = np.random.default_rng(seed)
    provisions = perturb_provisions(rng, scale=0.15)

    oracle_cache = {}
    for p, c, _ in stream:
        if (p, c) not in oracle_cache:
            oracle_cache[(p, c)] = perturbed_oracle(p, c, provisions,
                                                     needs_map=TRUE_NEEDS)
    oracle = np.array([oracle_cache[(p, c)] for p, c, _ in stream])
    total = float(oracle.sum())
    R = lambda p, c, page: perturbed_reward(p, c, page, provisions,
                                              needs_map=TRUE_NEEDS)

    shapes = make_problem_shapes()
    out = {}

    # EDP-static
    pol = EDPPolicy()
    rewards = np.array([R(p, c, pol.select_page(f)) for p, c, f in stream])
    out['edp_static'] = float((oracle - rewards).sum() / total * 100)

    # EDP-agent (canned edits)
    pol = EDPPolicy()
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        if i in sched_files and os.path.exists(sched_files[i]):
            edits = load_edits_json(sched_files[i])[0]
            pol.apply_edit_batch(edits)
        rewards[i] = R(p, c, pol.select_page(f))
    out['edp_agent'] = float((oracle - rewards).sum() / total * 100)

    # LinTS-warm
    pol = BanditPolicy(ctx_dim=7, alpha=0.3, seed=seed * 7)
    fb = DelayedFeedback(delay=500, noise_sigma=0.20, seed=seed * 11)
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = context_warm(f, shapes, c, with_category=False)
        page, payload = pol.select_page_with_payload(x)
        r = R(p, c, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)
    out['lints_warm'] = float((oracle - rewards).sum() / total * 100)

    # CombLinUCB
    pol = CombLinUCB(ctx_dim=7, alpha=0.3)
    fb = DelayedFeedback(delay=500, noise_sigma=0.20, seed=seed * 13)
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = context_warm(f, shapes, c, with_category=False)
        page, payload = pol.select_page_with_payload(x)
        r = R(p, c, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)
    out['comblinucb'] = float((oracle - rewards).sum() / total * 100)

    # Bayesian-EDP (canned edits)
    pol = BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3)
    fb = DelayedFeedback(delay=500, noise_sigma=0.20, seed=seed * 17)
    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        if i in sched_files and os.path.exists(sched_files[i]):
            edits = load_edits_json(sched_files[i])[0]
            new_modules = apply_edits(pol.modules, [
                (e['widget'], e['path'], e.get('from', 0.0),
                 e['to'], e.get('reason', ''))
                for e in edits
            ])
            pol.reset_prior(new_modules)
        for r_obs, payload in fb.drain_ready(i):
            pol.update_from_delayed(payload, r_obs)
        page, payload = pol.select_page_with_payload(f)
        r = R(p, c, page)
        rewards[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.update_from_delayed(payload, r_obs)
    out['bayesian_edp'] = float((oracle - rewards).sum() / total * 100)

    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--out', type=str, default='results_adversarial.json')
    args = ap.parse_args()

    from edp.ground_truth import set_source
    set_source('parametric')
    stream = make_session_stream(args.n, seed=42)

    sched = {
        2500: 'evolve_state/edits_round_2500.json',
        5000: 'evolve_state/edits_round_5000.json',
        7500: 'evolve_state/edits_round_7500.json',
    }

    cells = {}
    for seed in range(1, args.seeds + 1):
        print(f'[seed {seed}/{args.seeds}] running...')
        out = run_perturbation_seed(seed, stream, sched)
        for k, v in out.items():
            cells.setdefault(k, []).append(v)
            print(f'    {k}: {v:.2f} %')

    summary = {}
    for k, vals in cells.items():
        a = np.array(vals)
        summary[k] = {
            'mean_pct': float(a.mean()),
            'sem_pct': float(a.std(ddof=1) / np.sqrt(len(a))),
            'min_pct': float(a.min()),
            'max_pct': float(a.max()),
            'all': vals,
        }

    with open(args.out, 'w') as f:
        json.dump({'scale': 0.15, 'seeds': args.seeds, 'cells': summary}, f, indent=2)
    print(f'\nsaved -> {args.out}')
    print(f'\nAdversarial perturbation (±15 %, N={args.seeds} seeds):')
    for k, v in summary.items():
        print(f'  {k:14s}  {v["mean_pct"]:5.2f} ± {v["sem_pct"]:.2f} %  '
              f'(range {v["min_pct"]:.2f}–{v["max_pct"]:.2f})')


if __name__ == '__main__':
    main()
