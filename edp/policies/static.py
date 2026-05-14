"""
Static widget policy: no personalization, no category awareness.

Pick the top-6 widgets by their initial `base` value from the default
modules config, always in the same order. This is the 'what if you
just shipped a sensible default' baseline.
"""
from __future__ import annotations
from edp.config import N_SLOTS
from edp.catalog import WIDGETS
from edp.policies.base import Policy
from edp.policies.edp import make_modules


def topk_by_base(k: int = N_SLOTS) -> list[str]:
    mods = make_modules()
    ranked = sorted(WIDGETS, key=lambda w: -mods[w]['base'])
    return ranked[:k]


class StaticPolicy(Policy):
    """Returns the same page every time."""

    def __init__(self, page: list[str] = None):
        if page is None:
            page = topk_by_base(N_SLOTS)
        assert len(page) == N_SLOTS, f'page must have {N_SLOTS} widgets'
        assert len(set(page)) == N_SLOTS, 'page widgets must be unique'
        self._page = list(page)

    def select_page(self, feat: dict) -> list[str]:
        return list(self._page)


if __name__ == '__main__':
    print(f'Static top-{N_SLOTS} by base: {topk_by_base()}')
