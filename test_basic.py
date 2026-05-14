"""Quick sanity tests. Run: python3 test_basic.py"""
import numpy as np

from sim import (make_session_stream, true_page_reward, oracle_reward,
                 ORACLE_REWARDS, DelayedFeedback, WIDGETS, N_SLOTS)
from policy_edp import (EDPPolicy, make_modules, make_problem_shapes,
                        score_problems, apply_edits, PROBLEMS)
from policy_bandit import BanditPolicy, context_warm, context_cold


def test_oracle_dominates_random():
    rng = np.random.default_rng(0)
    for persona in ORACLE_REWARDS:
        oracle = ORACLE_REWARDS[persona]
        rand_page = list(rng.choice(WIDGETS, size=N_SLOTS, replace=False))
        r_rand = true_page_reward(persona, rand_page)
        assert oracle >= r_rand - 1e-9, f'{persona}: oracle {oracle} < random {r_rand}'


def test_pwl_problem_in_unit_interval():
    shapes = make_problem_shapes()
    stream = make_session_stream(500, seed=1)
    for _, feat in stream:
        p = score_problems(feat, shapes)
        for k, v in p.items():
            assert 0.0 <= v <= 1.0, f'{k}={v} out of [0,1]'


def test_edp_returns_unique_widgets():
    pol = EDPPolicy()
    stream = make_session_stream(200, seed=2)
    for _, feat in stream:
        page = pol.select_page(feat)
        assert len(page) == N_SLOTS
        assert len(set(page)) == N_SLOTS


def test_apply_edits_creates_paths():
    mods = make_modules()
    # New synergy on a path that doesn't exist yet
    assert 'F45' not in mods['return_explainer'].get('on_cov', {})
    edits = [
        ('return_explainer', 'on_cov.F45', 0.0, 0.7, 'new synergy'),
        ('return_explainer', 'base', 0.05, 0.15, 'base bump'),
    ]
    new = apply_edits(mods, edits)
    assert new['return_explainer']['on_cov']['F45'] == 0.7
    assert new['return_explainer']['base'] == 0.15
    # Original unchanged (deepcopy)
    assert 'F45' not in mods['return_explainer']['on_cov']
    assert mods['return_explainer']['base'] == 0.05


def test_delay_queue_holds_then_releases():
    q = DelayedFeedback(delay=3, noise_sigma=0.0, seed=0)
    q.submit(0, 1.0, 'a')
    q.submit(1, 2.0, 'b')
    assert list(q.drain_ready(0)) == []
    assert list(q.drain_ready(2)) == []
    out = list(q.drain_ready(3))
    assert out == [(1.0, 'a')]
    out = list(q.drain_ready(4))
    assert out == [(2.0, 'b')]


def test_bandit_select_returns_distinct_widgets():
    pol = BanditPolicy(ctx_dim=7, seed=0)
    shapes = make_problem_shapes()
    stream = make_session_stream(20, seed=3)
    for _, feat in stream:
        x = context_warm(feat, shapes)
        page, payload = pol.select_page_with_payload(x)
        assert len(page) == N_SLOTS
        assert len(set(page)) == N_SLOTS
        # Feedback round-trip
        pol.record_feedback(payload, 0.5)


def test_context_cold_dim():
    stream = make_session_stream(5, seed=4)
    for _, feat in stream:
        x = context_cold(feat)
        assert x.shape == (14,)


if __name__ == '__main__':
    tests = [v for k, v in globals().items() if k.startswith('test_')]
    for t in tests:
        t()
        print(f'PASS  {t.__name__}')
    print(f'\n{len(tests)} tests passed.')
