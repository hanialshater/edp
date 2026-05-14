"""
edp — Evolvable Decision Programs comparison harness.

Public API:

  from edp import (
      make_session_stream,                       # (persona, category, feat) stream
      DelayedFeedback,
      true_page_reward, oracle_reward,           # ground-truth reward
      EDPPolicy, BanditPolicy,                   # policies
      N_SLOTS, WIDGETS, NEEDS, CATEGORIES,
  )

Switch persona source at runtime:

  from edp.ground_truth import set_source
  set_source('llm')                              # use LLM-generated personas
"""
from edp.config import N_SLOTS, SIGNAL_NAMES, NEEDS, PROBLEMS, PROBLEM_NAMES
from edp.catalog import (WIDGETS, TRUE_PROVISIONS, N_WIDGETS, WIDGET_IDX,
                         CATEGORIES, CATEGORY_MIX, CATEGORY_NEED_MULTIPLIERS,
                         apply_category_multiplier)
from edp.ground_truth import (TRUE_NEEDS, ORACLE_REWARDS,
                              true_page_reward, oracle_reward,
                              effective_needs, set_source, get_source)
from edp.sim import make_session_stream, DelayedFeedback
from edp.policies.edp import EDPPolicy
from edp.policies.bandit import BanditPolicy

__all__ = [
    'N_SLOTS', 'SIGNAL_NAMES', 'NEEDS', 'PROBLEMS', 'PROBLEM_NAMES',
    'WIDGETS', 'TRUE_PROVISIONS', 'N_WIDGETS', 'WIDGET_IDX',
    'CATEGORIES', 'CATEGORY_MIX', 'CATEGORY_NEED_MULTIPLIERS',
    'apply_category_multiplier',
    'TRUE_NEEDS', 'ORACLE_REWARDS', 'true_page_reward', 'oracle_reward',
    'effective_needs', 'set_source', 'get_source',
    'make_session_stream', 'DelayedFeedback',
    'EDPPolicy', 'BanditPolicy',
]
