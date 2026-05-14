"""
Compute R² of Bayesian-EDP's calibrated linear page-reward predictor.

Bayesian-EDP models R̂_i = a + b · Σ_k score_k(θ_{w_k}). We log
(R̂, R_obs) pairs over a 10K-session run and report R² to quantify how
well the linear approximation captures the actual (nonlinear, submodular)
page-reward function.

If R² is high, the linearization is empirically fine. If low, the
SGD-on-θ is regressing the wrong thing and the Gaussian regulariser is
doing more work than it should.
"""
from __future__ import annotations
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, true_page_reward, oracle_reward,
                 DelayedFeedback)
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.edp import load_edits_json, apply_edits


def main():
    for source in ['parametric', 'llm']:
        from edp.ground_truth import set_source
        set_source(source)
        stream = make_session_stream(10_000, seed=42)

        pol = BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3)
        fb = DelayedFeedback(delay=500, noise_sigma=0.2, seed=12345)

        edits_dir = 'evolve_state' if source == 'parametric' else 'evolve_state_llm'
        schedule = {
            2500: f'{edits_dir}/edits_round_2500.json',
            5000: f'{edits_dir}/edits_round_5000.json',
            7500: f'{edits_dir}/edits_round_7500.json',
        }

        # Collect (R̂, R_true, R_obs) tuples
        pred = []        # R̂ = a + b · score_sum (before update)
        true_r = []      # ground-truth page reward (noise-free)
        obs_r = []       # what the bandit sees (delayed + noisy)

        for i, (p, c, f) in enumerate(stream):
            if i in schedule and os.path.exists(schedule[i]):
                edits, _ = load_edits_json(schedule[i])
                new_modules = apply_edits(pol.modules, [
                    (e['widget'], e['path'], e.get('from', 0.0),
                     e['to'], e.get('reason', ''))
                    for e in edits
                ])
                pol.reset_prior(new_modules)
            for r_obs, payload in fb.drain_ready(i):
                _, _, scores = payload
                score_sum = sum(scores)
                pred.append(pol.a + pol.b * score_sum)
                obs_r.append(r_obs)
                pol.update_from_delayed(payload, r_obs)
            page, payload = pol.select_page_with_payload(f)
            r_true_i = true_page_reward(p, c, page)
            true_r.append(r_true_i)
            fb.submit(i, r_true_i, payload)
        # Drain residual
        for r_obs, payload in fb.drain_all():
            _, _, scores = payload
            score_sum = sum(scores)
            pred.append(pol.a + pol.b * score_sum)
            obs_r.append(r_obs)
            pol.update_from_delayed(payload, r_obs)

        pred = np.array(pred)
        obs_r = np.array(obs_r)
        # R² of pred vs observed (what the bandit's loss is against)
        ss_res = float(((pred - obs_r) ** 2).sum())
        ss_tot = float(((obs_r - obs_r.mean()) ** 2).sum())
        r2_obs = 1.0 - ss_res / max(ss_tot, 1e-9)

        # R² of pred vs NOISE-FREE true page reward (the cleaner measure)
        # We need to align: pred[i] was made at session j = i_in_stream after
        # release of delayed feedback for some earlier session. We can't
        # easily pair pred[i] with true_r[j] without preserving session
        # indices. Easier: use the last-batch correlation as a snapshot.
        n = min(len(pred), len(true_r))
        pred_tail = pred[-1000:]
        true_tail = np.array(true_r[-1000:])
        ss_res2 = float(((pred_tail - true_tail) ** 2).sum())
        ss_tot2 = float(((true_tail - true_tail.mean()) ** 2).sum())
        r2_true_tail = 1.0 - ss_res2 / max(ss_tot2, 1e-9)

        # Pearson correlation between pred and obs/true (interpretable)
        corr_obs = float(np.corrcoef(pred, obs_r)[0, 1])

        print(f'== {source} ==')
        print(f'  N predictions     = {len(pred)}')
        print(f'  pred range        = [{pred.min():.3f}, {pred.max():.3f}]')
        print(f'  R² vs observed    = {r2_obs:.4f}')
        print(f'  R² vs noise-free  = {r2_true_tail:.4f} (last-1k snapshot, indices may not align perfectly)')
        print(f'  Pearson corr      = {corr_obs:.4f}')
        print(f'  final (a, b)      = ({pol.a:.4f}, {pol.b:.4f})')
        print()


if __name__ == '__main__':
    main()
