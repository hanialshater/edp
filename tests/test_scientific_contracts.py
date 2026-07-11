"""Scientific-contract regression tests for WPO-Gym.

Run directly from the repository root:

    python tests/test_scientific_contracts.py

The tests are deliberately lightweight and do not require pytest.
"""
from __future__ import annotations

import random

from edp.catalog import WIDGETS, TRUE_PROVISIONS
from edp.config import N_SLOTS
from edp.env import PageCompositionEnv
from edp.ground_truth import (
    effective_needs,
    oracle_page,
    oracle_reward,
    set_source,
    true_page_reward,
)


def _legacy_greedy_reward(persona: str, category: str) -> float:
    """Reproduce the pre-audit greedy reference for one cell."""
    needs = effective_needs(persona, category)
    remaining = dict(needs)
    used: set[str] = set()
    total = 0.0
    for _ in range(N_SLOTS):
        best_widget = None
        best_gain = -1.0
        for widget, provisions in TRUE_PROVISIONS.items():
            if widget in used:
                continue
            gain = sum(
                needs[dimension] * min(remaining[dimension], amount)
                for dimension, amount in provisions.items()
            )
            if gain > best_gain:
                best_gain = gain
                best_widget = widget
        assert best_widget is not None
        used.add(best_widget)
        total += best_gain
        for dimension, amount in TRUE_PROVISIONS[best_widget].items():
            remaining[dimension] = max(0.0, remaining[dimension] - amount)
    return total


def test_reward_is_permutation_invariant():
    set_source('parametric')
    page = WIDGETS[:N_SLOTS]
    forward = true_page_reward('size_anxious_new', 'shoes', page)
    backward = true_page_reward('size_anxious_new', 'shoes', list(reversed(page)))
    assert abs(forward - backward) < 1e-12


def test_duplicate_widgets_are_rejected():
    set_source('parametric')
    page = [WIDGETS[0]] * N_SLOTS
    try:
        true_page_reward('size_anxious_new', 'shoes', page)
    except ValueError as error:
        assert 'duplicate' in str(error)
    else:
        raise AssertionError('duplicate-widget page was accepted')


def test_exact_oracle_is_attained_and_dominates_samples():
    rng = random.Random(7)
    for source, persona in (
        ('parametric', 'size_anxious_new'),
        ('llm', 'hesitant_first_buyer'),
    ):
        set_source(source)
        for category in ('dress', 'shoes', 'accessories'):
            page = oracle_page(persona, category)
            optimum = oracle_reward(persona, category)
            assert len(page) == N_SLOTS
            assert len(set(page)) == N_SLOTS
            assert abs(true_page_reward(persona, category, page) - optimum) < 1e-12
            for _ in range(100):
                candidate = rng.sample(WIDGETS, N_SLOTS)
                assert optimum + 1e-12 >= true_page_reward(
                    persona, category, candidate
                )


def test_exact_oracle_fixes_known_greedy_failure():
    set_source('llm')
    exact = oracle_reward('paralyzed_wishlister', 'shoes')
    greedy = _legacy_greedy_reward('paralyzed_wishlister', 'shoes')
    assert exact > greedy + 1e-6, (exact, greedy)


def test_environment_does_not_expose_latent_persona():
    env = PageCompositionEnv(
        n=2,
        seed=42,
        source='parametric',
        delay=0,
        noise_sigma=0.0,
    )
    obs = env.reset()
    step = env.step(WIDGETS[:N_SLOTS], payload={'action': 0})
    assert 'persona' not in step.info
    assert set(step.info) <= {'category'}
    assert not hasattr(obs, 'persona')


if __name__ == '__main__':
    tests = [value for name, value in globals().items() if name.startswith('test_')]
    for test in tests:
        test()
        print(f'PASS  {test.__name__}')
    print(f'\n{len(tests)} scientific-contract tests passed.')
