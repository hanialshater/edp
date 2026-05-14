"""
EDP policy: Layer-1 PWL problem shapes -> 7-d fingerprint ->
Layer-2 module GAM -> greedy submodular composition.

Learning happens out-of-band: an agent reads logs and proposes edits
(dotted-path tuples), applied via apply_edits().
"""
from __future__ import annotations
import copy
import json
import numpy as np

from edp.config import N_SLOTS, PROBLEMS
from edp.policies.base import Policy


def pwl(x: float, bps, vals) -> float:
    return float(np.interp(x, bps, vals))


def make_problem_shapes():
    """
    Layer-1 PWL shape registry. Each (problem, signal) is a dict with
    `bps` (breakpoints), `vals` (PWL values at breakpoints), and `weight`.
    Editable via apply_shape_edits paths like `F32.size_chart.weight`,
    `F32.size_chart.vals.2`, etc.
    """
    def s(bps, vals, w):
        return {'bps': list(bps), 'vals': list(vals), 'weight': w}
    return {
        'F32': {
            'size_chart':    s([0, .2, .5, .8, 1], [0, .1, .45, .75, .95], 0.45),
            'size_conf_inv': s([0, .3, .6, 1],     [.95, .6, .25, .05],    0.30),
            'return_hist':   s([0, .2, .5, 1],     [0, .1, .4, .7],        0.25),
        },
        'F33': {
            'zoom':          s([0, .3, .6, 1],     [0, .15, .5, .85],      0.55),
            'price_norm':    s([0, .3, .6, 1],     [0, .2, .5, .8],        0.45),
        },
        'F41': {
            'tab_switch':    s([0, .2, .5, .8, 1], [0, .1, .5, .85, .95],  0.55),
            'revisit':       s([0, .3, .6, 1],     [0, .2, .55, .8],       0.25),
            'price_dwell':   s([0, .3, .6, 1],     [0, .1, .35, .55],      0.20),
        },
        'F43': {
            'style_stretch': s([0, .3, .6, 1],     [0, .2, .6, .95],       0.65),
            'mobile':        s([0, .5, 1],         [0, .3, .55],           0.35),
        },
        'F45': {
            'price_dwell':   s([0, .3, .6, .9, 1], [0, .15, .5, .8, .95],  0.50),
            'price_sens':    s([0, .4, .7, 1],     [0, .2, .55, .85],      0.50),
        },
        'F46': {
            'return_view':   s([0, .2, .5, 1],     [0, .15, .55, .9],      0.55),
            'return_hist':   s([0, .2, .5, 1],     [0, .15, .5, .8],       0.45),
        },
        'F51': {
            'cart_osc':      s([0, .2, .5, 1],     [0, .15, .55, .9],      0.45),
            'wishlist':      s([0, .3, .6, 1],     [0, .1, .4, .7],        0.30),
            'revisit':       s([0, .3, .6, 1],     [0, .1, .4, .65],       0.25),
        },
    }


def make_modules():
    return {
        'fit_reassurance':       dict(addr={'F32': 0.55, 'F46': 0.20},
            base=0.10, on_rem={'F32': 2.2, 'F46': 0.6},
            on_cov={'F32': -1.2}, slot_decay=0.05, type='reassurance'),
        'size_guide':            dict(addr={'F32': 0.50},
            base=0.05, on_rem={'F32': 2.0}, on_cov={'F32': -1.4},
            slot_decay=0.10, type='guide'),
        'low_return_alts':       dict(addr={'F32': 0.30, 'F46': 0.45},
            base=0.05, on_rem={'F32': 1.0, 'F46': 1.8},
            on_cov={'F46': -1.0}, slot_decay=0.06, type='alternatives'),
        'comparison_card':       dict(addr={'F41': 0.60, 'F45': 0.20},
            base=0.05, on_rem={'F41': 2.3, 'F45': 0.7},
            on_cov={'F41': -1.3}, slot_decay=0.04, type='comparison'),
        'customers_chose':       dict(addr={'F41': 0.30, 'F51': 0.25},
            base=0.10, on_rem={'F41': 0.8, 'F51': 1.2},
            on_cov={'F41': 0.5, 'F51': -0.6}, slot_decay=0.05, type='social'),
        'value_breakdown':       dict(addr={'F45': 0.55, 'F33': 0.20},
            base=0.05, on_rem={'F45': 2.1, 'F33': 0.5},
            on_cov={'F45': -1.2}, slot_decay=0.06, type='value'),
        'outfit_completion':     dict(addr={'F43': 0.55},
            base=0.20, on_rem={'F43': 1.8}, on_cov={'F43': -0.8},
            slot_decay=0.04, type='outfit'),
        'style_bridge':          dict(addr={'F43': 0.40},
            base=0.05, on_rem={'F43': 2.0}, on_cov={'F43': -1.0},
            slot_decay=0.06, type='outfit'),
        'occasion_lookbook':     dict(addr={'F43': 0.30},
            base=0.08, on_rem={'F43': 1.4}, on_cov={'F43': -0.5},
            slot_decay=0.05, type='outfit'),
        'return_explainer':      dict(addr={'F46': 0.50},
            base=0.05, on_rem={'F46': 2.0}, on_cov={'F46': -1.3},
            slot_decay=0.07, type='returns'),
        'easy_returns_promise':  dict(addr={'F46': 0.30},
            base=0.10, on_rem={'F46': 1.2}, on_cov={'F46': -0.5},
            slot_decay=0.05, type='returns'),
        'brand_story':           dict(addr={'F33': 0.50},
            base=0.10, on_rem={'F33': 1.9}, on_cov={'F33': -1.0},
            slot_decay=0.05, type='premium'),
        'material_deep_dive':    dict(addr={'F33': 0.45},
            base=0.05, on_rem={'F33': 1.7}, on_cov={'F33': -0.9},
            slot_decay=0.07, type='premium'),
        'price_history':         dict(addr={'F45': 0.45},
            base=0.05, on_rem={'F45': 1.7}, on_cov={'F45': -0.8},
            slot_decay=0.06, type='price'),
        'price_drop_notify':     dict(addr={'F51': 0.35, 'F45': 0.20},
            base=0.08, on_rem={'F51': 1.3, 'F45': 0.6},
            on_cov={'F51': -0.5}, slot_decay=0.05, type='price'),
        'recently_viewed':       dict(addr={'F51': 0.20},
            base=0.10, on_rem={'F51': 0.7}, on_cov={'F51': -0.3},
            slot_decay=0.05, type='context'),
        'wishlist_save':         dict(addr={'F51': 0.30},
            base=0.05, on_rem={'F51': 1.2}, on_cov={'F51': -0.6},
            slot_decay=0.06, type='action'),
        'expert_pick':           dict(addr={'F51': 0.30, 'F33': 0.15},
            base=0.05, on_rem={'F51': 1.4, 'F33': 0.4},
            on_cov={'F51': -0.7}, slot_decay=0.07, type='guidance'),
        'similar_items':         dict(addr={'F41': 0.10, 'F43': 0.05, 'F51': 0.05},
            base=0.45, on_rem={}, on_cov={}, slot_decay=0.03, type='default'),
        'also_bought':           dict(addr={'F41': 0.10, 'F51': 0.10},
            base=0.40, on_rem={}, on_cov={}, slot_decay=0.03, type='default'),
        'trending_now':          dict(addr={},
            base=0.30, on_rem={}, on_cov={}, slot_decay=0.04, type='default'),
        'personal_recs':         dict(addr={'F43': 0.10, 'F51': 0.10},
            base=0.35, on_rem={}, on_cov={}, slot_decay=0.04, type='default'),
    }


def score_problems(feat: dict, shapes: dict) -> dict:
    out = {}
    for prob, sigs in shapes.items():
        s, w_sum = 0.0, 0.0
        for sig_name, cfg in sigs.items():
            # Backward-compat: accept either the new dict form
            # {'bps': ..., 'vals': ..., 'weight': ...} or a 3-tuple.
            if isinstance(cfg, dict):
                bps, vals, w = cfg['bps'], cfg['vals'], cfg['weight']
            else:
                bps, vals, w = cfg
            if w == 0:
                continue
            x = feat['size_conf'] if sig_name == 'size_conf_inv' else feat.get(sig_name, 0.0)
            s += w * pwl(x, bps, vals)
            w_sum += w
        out[prob] = float(np.clip(s / max(w_sum, 1e-9), 0.0, 1.0))
    return out


def score_module(mod: dict, remaining: dict, coverage: dict, slot: int) -> float:
    s = mod['base']
    for p, w in mod.get('on_rem', {}).items():
        s += w * remaining.get(p, 0.0)
    for p, w in mod.get('on_cov', {}).items():
        s += w * coverage.get(p, 0.0)
    s -= mod['slot_decay'] * slot
    return s


def compose(feat: dict, shapes: dict, modules: dict) -> list[str]:
    problems = score_problems(feat, shapes)
    remaining = dict(problems)
    coverage = {p: 0.0 for p in PROBLEMS}
    page, used = [], set()
    for slot in range(N_SLOTS):
        best, best_s = None, -1e9
        for name, mod in modules.items():
            if name in used:
                continue
            s = score_module(mod, remaining, coverage, slot)
            if s > best_s:
                best_s, best = s, name
        page.append(best)
        used.add(best)
        mod = modules[best]
        for p, addr in mod['addr'].items():
            remaining[p] = max(0.0, remaining[p] - addr)
            coverage[p] = min(1.0, coverage[p] + addr)
    return page


# ---------- Code-edit application ----------
def _set_dot(d: dict, path: str, value):
    """
    Set a dotted path inside a nested dict. Numeric path segments are
    treated as list indices (e.g. `vals.2` indexes vals[2]).
    """
    parts = path.split('.')
    cur = d
    for i, p in enumerate(parts[:-1]):
        is_idx = p.isdigit()
        nxt = parts[i + 1]
        nxt_is_idx = nxt.isdigit()
        if is_idx:
            cur = cur[int(p)]
            continue
        if p not in cur or (not isinstance(cur[p], dict) and not nxt_is_idx):
            cur[p] = {} if not nxt_is_idx else []
        cur = cur[p]
    last = parts[-1]
    if last.isdigit():
        cur[int(last)] = value
    else:
        cur[last] = value


def apply_edits(modules: dict, edits: list) -> dict:
    """
    Apply Layer-2 (module) edits.

    edits: list of (widget, path, from, to, reason) tuples or
           dicts {widget, path, [from], to, [reason]}.
    Returns a NEW modules dict (deep-copied).
    """
    out = copy.deepcopy(modules)
    for e in edits:
        if isinstance(e, dict):
            widget, path, to = e['widget'], e['path'], e['to']
        else:
            widget, path, _from, to = e[0], e[1], e[2], e[3]
        if widget not in out:
            continue
        _set_dot(out[widget], path, to)
    return out


def apply_shape_edits(shapes: dict, edits: list) -> dict:
    """
    Apply Layer-1 (PWL shape) edits.

    Each edit dict has: {problem, signal, path, [from], to, [reason]}.
    `path` is one of:
      - 'weight'         (scalar)
      - 'bps.<i>'        (i-th breakpoint, scalar; must remain monotonic
                          increasing in [0, 1])
      - 'vals.<i>'       (i-th PWL value, scalar in [0, 1])

    Returns a NEW shapes dict (deep-copied).
    """
    out = copy.deepcopy(shapes)
    for e in edits:
        prob = e['problem']
        sig = e['signal']
        path = e['path']
        to = e['to']
        if prob not in out or sig not in out[prob]:
            # Allow ADDING a new (problem, signal) entry
            if 'bps' in e and 'vals' in e and 'weight' in e:
                out.setdefault(prob, {})[sig] = {
                    'bps': list(e['bps']), 'vals': list(e['vals']),
                    'weight': float(e['weight']),
                }
                continue
            else:
                continue
        cfg = out[prob][sig]
        # Convert tuple form to dict form if needed (back-compat).
        if not isinstance(cfg, dict):
            bps, vals, w = cfg
            cfg = {'bps': list(bps), 'vals': list(vals), 'weight': w}
            out[prob][sig] = cfg
        _set_dot(cfg, path, to)
    return out


def load_edits_json(path: str):
    with open(path) as f:
        data = json.load(f)
    return data['edits'], data.get('note', '')


class EDPPolicy(Policy):
    """Stateful EDP policy. State == (shapes, modules)."""

    def __init__(self, shapes=None, modules=None):
        self.shapes = shapes or make_problem_shapes()
        self.modules = modules or make_modules()

    def select_page(self, feat: dict) -> list[str]:
        return compose(feat, self.shapes, self.modules)

    def apply_edit_batch(self, edits: list):
        self.modules = apply_edits(self.modules, edits)

    def apply_shape_edit_batch(self, shape_edits: list):
        self.shapes = apply_shape_edits(self.shapes, shape_edits)


def load_shape_edits_json(path: str):
    """
    Loads a Layer-1 edit batch JSON. Same shape as Layer-2 except each
    edit has fields {problem, signal, path, [from], to, [reason]}.
    """
    with open(path) as f:
        data = json.load(f)
    return data.get('shape_edits', []), data.get('note', '')
