"""Back-compat shim."""
from edp.policies.edp import (EDPPolicy, make_problem_shapes, make_modules,
                               score_problems, score_module, compose,
                               apply_edits, load_edits_json, pwl)
from edp.config import PROBLEMS, PROBLEM_NAMES
