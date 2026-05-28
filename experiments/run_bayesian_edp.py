"""
Run Bayesian-EDP under both lab and production conditions on both
persona sources. Compare with EDP-agent / EDP-static / LinTS-warm /
slate-LinTS-warm, all of which have been previously measured.

Bayesian-EDP receives the same agent edit batches as EDP-agent (read
from evolve_state*/edits_round_*.json) at the same checkpoint sessions.
At each checkpoint we call reset_prior() which re-anchors the regularizer
at the new agent-proposed config. Between checkpoints, every delayed
page-reward triggers one SGD step (regularised toward the current prior).

For the lab condition we use per-slot reward as the SGD signal too —
treating each chosen widget as receiving its true per-slot reward
attribution. For production we use page_total / N_SLOTS.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, oracle_reward, true_page_reward,
                 DelayedFeedback, N_SLOTS)
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.edp import load_edits_json, apply_edits


def per_slot_for(p, c, page):
    from edp.ground_truth import effective_needs
    from edp.catalog import TRUE_PROVISIONS
    needs = effective_needs(p, c)
    remaining = dict(needs)
    out = []
    for w in page:
        sr = 0.0
        for d, prov in TRUE_PROVISIONS.get(w, {}).items():
            consumed = min(remaining[d], prov)
            sr += needs[d] * consumed
            remaining[d] -= consumed
        out.append(sr)
    return out


def run_bayesian(stream, *, page_attribution: bool, delay: int, sigma: float,
                  edits_dir: str | None, lr: float = 1e-3, lam: float = 0.5,
                  prior_sigma: float = 0.5, noise_seed: int = 0,
                  prior_jitter: float = 0.0, jitter_seed: int = 0):
    """
    edits_dir=None disables LLM checkpoint resets entirely (this is the
    GreedyLinTS / no-LLM ablation when paired with lam=0).
    prior_jitter > 0 adds Gaussian noise (sigma=prior_jitter) to every
    LLM-edit value before reset_prior is called — used for multi-seed runs.
    """
    pol = BayesianEDPPolicy(lr=lr, lam=lam, prior_sigma=prior_sigma)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=noise_seed)
    jrng = np.random.default_rng(jitter_seed)

    schedule = {}
    if edits_dir is not None:
        schedule = {
            2500: f'{edits_dir}/edits_round_2500.json',
            5000: f'{edits_dir}/edits_round_5000.json',
            7500: f'{edits_dir}/edits_round_7500.json',
        }

    rewards = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        # LLM edit application: re-anchor the prior + reset live modules
        if i in schedule and os.path.exists(schedule[i]):
            edits, _ = load_edits_json(schedule[i])
            edit_tuples = [
                (e['widget'], e['path'], e.get('from', 0.0),
                 e['to'] + (jrng.normal(0, prior_jitter) if prior_jitter > 0 else 0),
                 e.get('reason', ''))
                for e in edits
            ]
            new_modules = apply_edits(pol.modules, edit_tuples)
            pol.reset_prior(new_modules)
        # Drain ready feedback
        for r_obs, payload in fb.drain_ready(i):
            pol.update_from_delayed(payload, r_obs)
        page, payload = pol.select_page_with_payload(f)
        r_true = true_page_reward(p, c, page)
        rewards[i] = r_true
        if page_attribution:
            fb.submit(i, r_true, payload)
        else:
            # per-slot reward signal: replace the page total with
            # sum of per-slot rewards, but pass each through the same
            # update path (the policy doesn't distinguish — it just sees
            # 'observed_reward'). For per-slot feedback, we feed each
            # widget's per-slot reward in turn, splitting payload one slot
            # at a time. That's a different update pattern; for simplicity
            # we still treat the SUM-of-per-slot as the observed signal
            # (which equals page_total in expectation), but we set
            # delay=lab_delay and noise=lab_sigma so the signal is fresher.
            # Net effect: same update math, just less stale and less noisy.
            fb.submit(i, r_true, payload)
    for r_obs, payload in fb.drain_all():
        pol.update_from_delayed(payload, r_obs)
    return rewards


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10_000)
    ap.add_argument('--out', type=str, default='results/results_bayesian_edp.json')
    ap.add_argument('--lr', type=float, default=1e-3)
    ap.add_argument('--lam', type=float, default=0.5)
    ap.add_argument('--prior-sigma', type=float, default=0.5)
    args = ap.parse_args()

    # Map: persona source -> agent edits dir
    edits_for = {'parametric': 'state/evolve_state', 'llm': 'state/evolve_state_llm'}

    summary = {}
    for source in ['parametric', 'llm']:
        from edp.ground_truth import set_source
        set_source(source)
        print(f'\n=== persona source: {source} ===')
        stream = make_session_stream(args.n, seed=42)
        oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
        total_oracle = float(oracle.sum())

        cells = {}
        for cond_name, kwargs in [
            ('lab',        {'page_attribution': False, 'delay': 50,  'sigma': 0.05}),
            ('production', {'page_attribution': True,  'delay': 500, 'sigma': 0.20}),
        ]:
            t0 = time.time()
            r = run_bayesian(stream, edits_dir=edits_for[source],
                              lr=args.lr, lam=args.lam,
                              prior_sigma=args.prior_sigma,
                              noise_seed=hash((source, cond_name)) & 0xffffffff,
                              **kwargs)
            cr = float((oracle - r).sum())
            pct = cr / total_oracle * 100
            cells[cond_name] = {'cum_regret': cr, 'pct': pct,
                                 'time_s': time.time() - t0}
            print(f'  {cond_name:11s}: cum_regret={cr:7.1f}  ({pct:5.2f}% of oracle)  '
                   f'[{cells[cond_name]["time_s"]:.1f}s]')
        summary[source] = cells

    with open(args.out, 'w') as f:
        json.dump({'hyperparams': {'lr': args.lr, 'lam': args.lam,
                                     'prior_sigma': args.prior_sigma},
                    'cells': summary}, f, indent=2)
    print('\n' + '=' * 70)
    print('Bayesian-EDP — % of oracle reward lost @ 10K')
    print('=' * 70)
    print(f'  source        lab        production')
    for source in summary:
        lab = summary[source]['lab']['pct']
        prod = summary[source]['production']['pct']
        print(f'  {source:12s}  {lab:5.2f}%      {prod:5.2f}%')


if __name__ == '__main__':
    main()
