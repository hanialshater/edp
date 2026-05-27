"""
Ground-truth reward and oracle, parameterized by (persona, category).

Reward model:
  effective_needs[(persona, category)] = persona_needs * category_multipliers
  Each page slot consumes from the persona's residual need budget; reward
  for the slot is sum_d (effective_needs[d] * consumed[d]).

The persona source (parametric or llm) supplies persona_needs.
"""
from __future__ import annotations
import importlib
import os
from edp.config import N_SLOTS, NEEDS
from edp.catalog import (TRUE_PROVISIONS, CATEGORIES, CATEGORY_MIX,
                         apply_category_multiplier)


_PERSONA_SOURCE = os.environ.get('EDP_PERSONA_SOURCE', 'parametric')


def get_source():
    return importlib.import_module(f'edp.personas.{_PERSONA_SOURCE}')


def set_source(name: str):
    global _PERSONA_SOURCE, _TRUE_NEEDS_CACHE, _ORACLE_CACHE, _EFFECTIVE_CACHE
    _PERSONA_SOURCE = name
    _TRUE_NEEDS_CACHE = None
    _ORACLE_CACHE = None
    _EFFECTIVE_CACHE = None


_TRUE_NEEDS_CACHE = None       # persona -> base_needs (no category modulation)
_EFFECTIVE_CACHE = None        # (persona, category) -> modulated need vector
_ORACLE_CACHE = None           # (persona, category) -> oracle reward


def _ensure_loaded():
    global _TRUE_NEEDS_CACHE, _EFFECTIVE_CACHE, _ORACLE_CACHE
    if _TRUE_NEEDS_CACHE is not None:
        return
    src = get_source()
    _TRUE_NEEDS_CACHE = {n: src.true_needs(n) for n in src.persona_names()}
    _EFFECTIVE_CACHE = {}
    _ORACLE_CACHE = {}
    for p, base in _TRUE_NEEDS_CACHE.items():
        for c in CATEGORIES:
            eff = apply_category_multiplier(base, c)
            _EFFECTIVE_CACHE[(p, c)] = eff
            _ORACLE_CACHE[(p, c)] = _greedy_oracle_for_needs(eff)


def _greedy_oracle_for_needs(needs: dict) -> float:
    remaining = dict(needs)
    used = set()
    total = 0.0
    for _ in range(N_SLOTS):
        best_w, best_r = None, -1.0
        for w, prov in TRUE_PROVISIONS.items():
            if w in used:
                continue
            r = sum(needs[d] * min(remaining[d], p) for d, p in prov.items())
            if r > best_r:
                best_r, best_w = r, w
        if best_w is None:
            break
        used.add(best_w)
        total += best_r
        for d, p in TRUE_PROVISIONS[best_w].items():
            remaining[d] = max(0.0, remaining[d] - p)
    return total


def effective_needs(persona_name: str, category: str) -> dict:
    _ensure_loaded()
    return dict(_EFFECTIVE_CACHE[(persona_name, category)])


def _category_mix_items():
    total = sum(CATEGORY_MIX.values())
    for category, weight in CATEGORY_MIX.items():
        yield category, weight / total


def true_page_reward(persona_name: str, category: str | list[str],
                     page: list[str] | None = None) -> float:
    if page is None:
        # Back-compat for old callers: true_page_reward(persona, page).
        # Return the category-mixture expectation instead of choosing a
        # synthetic category.
        old_page = category
        return sum(w * true_page_reward(persona_name, c, old_page)
                   for c, w in _category_mix_items())

    _ensure_loaded()
    needs = dict(_EFFECTIVE_CACHE[(persona_name, category)])
    remaining = dict(needs)
    total = 0.0
    for widget in page:
        for dim, p in TRUE_PROVISIONS.get(widget, {}).items():
            consumed = min(remaining[dim], p)
            total += needs[dim] * consumed
            remaining[dim] -= consumed
    return total


def oracle_reward(persona_name: str, category: str | None = None) -> float:
    _ensure_loaded()
    if category is None:
        # Back-compat for old callers: oracle_reward(persona).
        return sum(w * _ORACLE_CACHE[(persona_name, c)]
                   for c, w in _category_mix_items())
    return _ORACLE_CACHE[(persona_name, category)]


# ---------- Module-level proxies for back-compat ----------
class _LazyDict:
    def __init__(self, getter):
        self._getter = getter

    def __getitem__(self, k):
        return self._getter()[k]

    def __iter__(self):
        return iter(self._getter())

    def __contains__(self, k):
        return k in self._getter()

    def keys(self):
        return self._getter().keys()

    def items(self):
        return self._getter().items()

    def values(self):
        return self._getter().values()

    def __len__(self):
        return len(self._getter())


class _OracleRewardsDict(_LazyDict):
    def __getitem__(self, k):
        data = self._getter()
        if isinstance(k, tuple):
            return data[k]
        return oracle_reward(k)

    def __contains__(self, k):
        data = self._getter()
        if isinstance(k, tuple):
            return k in data
        return any(p == k for p, _ in data)


def _persona_needs():
    _ensure_loaded()
    return _TRUE_NEEDS_CACHE


def _oracle_table():
    _ensure_loaded()
    return _ORACLE_CACHE


TRUE_NEEDS = _LazyDict(_persona_needs)         # persona -> base needs
ORACLE_REWARDS = _OracleRewardsDict(_oracle_table)  # (persona, category) -> oracle
