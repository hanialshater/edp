"""
Ground-truth reward and exact reference oracle, parameterized by
(persona, category).

The current benchmark reward is a weighted capped-coverage objective:

    effective_needs[(persona, category)] = persona_needs * category_multipliers
    reward(page) = sum_d needs[d] * min(needs[d], sum_{w in page} provision[w, d])

Consequently the reward depends on the selected *set* of widgets, not their
order. WPO-Gym in its present form is therefore a module-selection benchmark;
position-sensitive page ordering is intentionally left to a future reward
model. Keeping that fact explicit prevents the paper or downstream users from
mistaking a set benchmark for an ordered-slate benchmark.

There are only C(22, 6) = 74,613 valid six-widget sets, so the oracle is
computed exactly by enumerating all sets. The previous implementation used the
standard greedy submodular approximation and called it an oracle. Greedy was
exact for the original parametric cells but is not guaranteed to be exact and
was suboptimal for several LLM-persona/category cells.
"""
from __future__ import annotations

from itertools import combinations
import importlib
import os

import numpy as np

from edp.config import N_SLOTS, NEEDS
from edp.catalog import (
    TRUE_PROVISIONS,
    WIDGETS,
    CATEGORIES,
    CATEGORY_MIX,
    apply_category_multiplier,
)


_PERSONA_SOURCE = os.environ.get('EDP_PERSONA_SOURCE', 'parametric')

# Build the finite action set once. 74,613 x 7 float64 values require only
# about 4 MiB and make every persona/category oracle lookup a vectorized max.
_NEED_INDEX = {name: i for i, name in enumerate(NEEDS)}
_PROVISION_MATRIX = np.zeros((len(WIDGETS), len(NEEDS)), dtype=float)
for _wi, _widget in enumerate(WIDGETS):
    for _need, _value in TRUE_PROVISIONS[_widget].items():
        _PROVISION_MATRIX[_wi, _NEED_INDEX[_need]] = float(_value)

_COMBINATION_INDICES = np.asarray(
    list(combinations(range(len(WIDGETS)), N_SLOTS)), dtype=np.int16
)
_COMBINATION_COVERAGE = _PROVISION_MATRIX[_COMBINATION_INDICES].sum(axis=1)


def get_source():
    return importlib.import_module(f'edp.personas.{_PERSONA_SOURCE}')


def set_source(name: str):
    global _PERSONA_SOURCE, _TRUE_NEEDS_CACHE, _ORACLE_CACHE
    global _ORACLE_PAGE_CACHE, _EFFECTIVE_CACHE
    _PERSONA_SOURCE = name
    _TRUE_NEEDS_CACHE = None
    _ORACLE_CACHE = None
    _ORACLE_PAGE_CACHE = None
    _EFFECTIVE_CACHE = None


_TRUE_NEEDS_CACHE = None       # persona -> base_needs (no category modulation)
_EFFECTIVE_CACHE = None        # (persona, category) -> modulated need vector
_ORACLE_CACHE = None           # (persona, category) -> exact oracle reward
_ORACLE_PAGE_CACHE = None      # (persona, category) -> exact oracle page


def _needs_array(needs: dict) -> np.ndarray:
    return np.asarray([float(needs.get(d, 0.0)) for d in NEEDS], dtype=float)


def _reward_from_coverage(needs: np.ndarray, coverage: np.ndarray) -> np.ndarray:
    """Vectorized weighted capped-coverage reward."""
    return (needs * np.minimum(needs, coverage)).sum(axis=-1)


def _exact_oracle_for_needs(needs: dict) -> tuple[float, list[str]]:
    """Return the exact best reward and one maximizing six-widget set."""
    n = _needs_array(needs)
    values = _reward_from_coverage(n, _COMBINATION_COVERAGE)
    best_idx = int(np.argmax(values))
    page = [WIDGETS[int(i)] for i in _COMBINATION_INDICES[best_idx]]
    return float(values[best_idx]), page


def _ensure_loaded():
    global _TRUE_NEEDS_CACHE, _EFFECTIVE_CACHE
    global _ORACLE_CACHE, _ORACLE_PAGE_CACHE
    if _TRUE_NEEDS_CACHE is not None:
        return
    src = get_source()
    _TRUE_NEEDS_CACHE = {n: src.true_needs(n) for n in src.persona_names()}
    _EFFECTIVE_CACHE = {}
    _ORACLE_CACHE = {}
    _ORACLE_PAGE_CACHE = {}
    for persona, base in _TRUE_NEEDS_CACHE.items():
        for category in CATEGORIES:
            effective = apply_category_multiplier(base, category)
            reward, page = _exact_oracle_for_needs(effective)
            key = (persona, category)
            _EFFECTIVE_CACHE[key] = effective
            _ORACLE_CACHE[key] = reward
            _ORACLE_PAGE_CACHE[key] = page


def effective_needs(persona_name: str, category: str) -> dict:
    _ensure_loaded()
    return dict(_EFFECTIVE_CACHE[(persona_name, category)])


def _category_mix_items():
    total = sum(CATEGORY_MIX.values())
    for category, weight in CATEGORY_MIX.items():
        yield category, weight / total


def _validate_page(page: list[str]) -> None:
    if len(page) > N_SLOTS:
        raise ValueError(f'page has {len(page)} widgets; maximum is {N_SLOTS}')
    if len(set(page)) != len(page):
        raise ValueError('page contains duplicate widgets; actions are without replacement')
    unknown = [widget for widget in page if widget not in TRUE_PROVISIONS]
    if unknown:
        raise ValueError(f'unknown widget(s): {unknown}')


def true_page_reward(persona_name: str, category: str | list[str],
                     page: list[str] | None = None) -> float:
    """Return the noise-free set reward for a valid page.

    The order of ``page`` does not affect this reward. The explicit validation
    keeps the environment's action contract aligned with the exact oracle.
    """
    if page is None:
        # Back-compat for old callers: true_page_reward(persona, page).
        # Return the category-mixture expectation instead of choosing a
        # synthetic category.
        old_page = category
        return sum(
            weight * true_page_reward(persona_name, cat, old_page)
            for cat, weight in _category_mix_items()
        )

    _validate_page(page)
    _ensure_loaded()
    needs = _needs_array(_EFFECTIVE_CACHE[(persona_name, category)])
    if not page:
        return 0.0
    indices = [WIDGETS.index(widget) for widget in page]
    coverage = _PROVISION_MATRIX[indices].sum(axis=0)
    return float(_reward_from_coverage(needs, coverage))


def oracle_reward(persona_name: str, category: str | None = None) -> float:
    """Return the exact maximum reward over all valid six-widget sets."""
    _ensure_loaded()
    if category is None:
        # Back-compat for old callers: oracle_reward(persona).
        return sum(
            weight * _ORACLE_CACHE[(persona_name, cat)]
            for cat, weight in _category_mix_items()
        )
    return _ORACLE_CACHE[(persona_name, category)]


def oracle_page(persona_name: str, category: str) -> list[str]:
    """Return one exact maximizing six-widget set."""
    _ensure_loaded()
    return list(_ORACLE_PAGE_CACHE[(persona_name, category)])


# ---------- Module-level proxies for back-compat ----------
class _LazyDict:
    def __init__(self, getter):
        self._getter = getter

    def __getitem__(self, key):
        return self._getter()[key]

    def __iter__(self):
        return iter(self._getter())

    def __contains__(self, key):
        return key in self._getter()

    def keys(self):
        return self._getter().keys()

    def items(self):
        return self._getter().items()

    def values(self):
        return self._getter().values()

    def __len__(self):
        return len(self._getter())


class _OracleRewardsDict(_LazyDict):
    def __getitem__(self, key):
        data = self._getter()
        if isinstance(key, tuple):
            return data[key]
        return oracle_reward(key)

    def __contains__(self, key):
        data = self._getter()
        if isinstance(key, tuple):
            return key in data
        return any(persona == key for persona, _ in data)


def _persona_needs():
    _ensure_loaded()
    return _TRUE_NEEDS_CACHE


def _oracle_table():
    _ensure_loaded()
    return _ORACLE_CACHE


TRUE_NEEDS = _LazyDict(_persona_needs)              # persona -> base needs
ORACLE_REWARDS = _OracleRewardsDict(_oracle_table)  # (persona, category) -> oracle
