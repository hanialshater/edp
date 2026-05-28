"""Back-compat shim — imports moved to edp.sim and edp.ground_truth."""
from edp.config import N_SLOTS, SIGNAL_NAMES, NEEDS
from edp.catalog import (WIDGETS, TRUE_PROVISIONS, N_WIDGETS, WIDGET_IDX,
                         CATEGORIES, CATEGORY_MIX)
from edp.ground_truth import (TRUE_NEEDS, ORACLE_REWARDS, true_page_reward,
                              oracle_reward, effective_needs)
from edp.sim import make_session_stream, DelayedFeedback
# Parametric persona dict is also re-exported for any back-compat consumers.
from edp.personas.parametric import PERSONAS
