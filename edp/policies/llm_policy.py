"""
LLM-as-policy: a Claude subagent writes a Python function

    pick_page(feat: dict, category: str) -> list[str]

based on widget descriptions and signal schema. The function is stored at
data/llm_policy_fn.py and executed at simulation time. One subagent call
generates it; runs deterministically on every session afterward.

This baseline tests: 'what if you just asked the LLM to write the policy?'
The LLM does NOT see persona names or true_needs/provisions — only the
context features and widget descriptions, like a deployed system would.
"""
from __future__ import annotations
import importlib.util
import os
from edp.config import N_SLOTS
from edp.catalog import WIDGETS
from edp.policies.base import Policy

DEFAULT_FN_PATH = 'data/llm_policy_fn.py'


class LLMPolicy(Policy):
    """Wraps a Python pick_page function written by an LLM."""

    def __init__(self, fn_path: str = DEFAULT_FN_PATH):
        if not os.path.exists(fn_path):
            raise FileNotFoundError(
                f'LLM-policy function not found at {fn_path}. '
                'Run experiments/llm_policy_generate.py first.'
            )
        spec = importlib.util.spec_from_file_location('llm_policy_fn', fn_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, 'pick_page'):
            raise AttributeError(f'{fn_path} must define pick_page(feat, category)')
        self._pick = mod.pick_page
        self._widget_set = set(WIDGETS)

    def select_page(self, feat: dict) -> list[str]:
        # The Policy interface accepts only feat; we need category too. Use
        # a sentinel; in practice callers will use select_page_with_category.
        return self.select_page_with_category(feat, category='top')

    def select_page_with_category(self, feat: dict, category: str) -> list[str]:
        page = self._pick(feat, category)
        if not isinstance(page, list) or len(page) != N_SLOTS:
            raise ValueError(f'pick_page must return list of {N_SLOTS} widget names, got: {page!r}')
        if not all(w in self._widget_set for w in page):
            raise ValueError(f'pick_page returned unknown widget(s): {set(page) - self._widget_set}')
        if len(set(page)) != N_SLOTS:
            raise ValueError(f'pick_page returned duplicates: {page}')
        return page
