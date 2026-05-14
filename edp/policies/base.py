"""
Policy interface. All policies must implement select_page().

The optional record_feedback() lets policies that learn online (bandits)
consume delayed reward. EDP doesn't use it; its learning is edit batches
applied externally via apply_edit_batch().
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class Policy(ABC):
    """Abstract base for any page-composition policy."""

    @abstractmethod
    def select_page(self, feat: dict) -> list[str]:
        """Return a list of N_SLOTS unique widget names."""
        ...

    def record_feedback(self, payload, observed_reward: float):
        """Optional online update. Default: no-op."""
        return
