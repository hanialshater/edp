"""
Train LinTS-warm and LinTS-cold on the 10k parametric+categories stream,
then export the per-(slot, arm) posterior state (A_inv, b) to JSON for the
HTML demo to consume.

The demo can then compute posterior-mean scores (μ = A_inv @ b) for each
arm directly in JS at slider-drag latency, with no live training needed.
"""
from __future__ import annotations
import json
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp import (make_session_stream, true_page_reward, oracle_reward,
                 DelayedFeedback, BanditPolicy, N_SLOTS, WIDGETS)
from edp.policies.bandit import context_warm, context_cold, context_dim
from edp.policies.edp import make_problem_shapes


def train(stream, oracle, ctx_fn, ctx_dim, delay, sigma, seed=7):
    pol = BanditPolicy(ctx_dim=ctx_dim, alpha=0.3, seed=seed)
    fb = DelayedFeedback(delay=delay, noise_sigma=sigma, seed=seed + 1000)
    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = ctx_fn(f, c)
        page, payload = pol.select_page_with_payload(x)
        r = true_page_reward(p, c, page)
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)
    return pol


def export(pol: BanditPolicy):
    """Per-(slot, arm) (A_inv, b) as nested lists."""
    out = []
    for slot in range(N_SLOTS):
        b_slot = pol.bandits[slot]
        slot_arms = []
        for a in range(b_slot.K):
            slot_arms.append({
                'A_inv': b_slot.A_inv[a].tolist(),
                'b':     b_slot.b[a].tolist(),
            })
        out.append(slot_arms)
    return out


def main():
    stream = make_session_stream(10_000, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])
    shapes = make_problem_shapes()

    print('Training LinTS-warm (7-d problem fingerprint)...')
    pol_w = train(stream, oracle,
                   lambda f, c: context_warm(f, shapes, c, with_category=False),
                   ctx_dim=7, delay=500, sigma=0.2, seed=7)

    print('Training LinTS-cold (14-d raw signals)...')
    pol_c = train(stream, oracle,
                   lambda f, c: context_cold(f, c, with_category=False),
                   ctx_dim=14, delay=500, sigma=0.2, seed=11)

    payload = {
        'widgets': WIDGETS,
        'n_slots': N_SLOTS,
        'meta': {
            'n_train_sessions': 10_000,
            'delay': 500,
            'noise_sigma': 0.2,
            'alpha': 0.3,
            'persona_source': 'parametric',
            'page_level_attribution': True,
        },
        'warm': {
            'ctx_dim': 7,
            'ctx_signals': ['F32', 'F33', 'F41', 'F43', 'F45', 'F46', 'F51'],
            'arms': export(pol_w),
        },
        'cold': {
            'ctx_dim': 14,
            'ctx_signals': ['size_conf', 'price_sens', 'return_hist',
                             'style_stretch', 'new', 'mobile', 'size_chart',
                             'tab_switch', 'zoom', 'price_dwell', 'cart_osc',
                             'wishlist', 'return_view', 'revisit'],
            'arms': export(pol_c),
        },
    }

    out_path = 'demo/lints_state.json'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(payload, f)
    size_kb = os.path.getsize(out_path) / 1024
    print(f'Exported -> {out_path}  ({size_kb:.1f} KB)')


if __name__ == '__main__':
    main()
