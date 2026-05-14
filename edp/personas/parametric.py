"""
Parametric persona source: each persona is a fixed (mu, sigma) per signal.

This is the original setup from the paper, kept as a baseline simulator
to compare against the LLM-driven personas.
"""
from __future__ import annotations
import numpy as np

# Each entry: (mu, sigma) per signal.  p is the mixture weight.
PERSONAS = {
    'size_anxious_new':  dict(p=0.18, size_conf=(0.15, 0.10), price_sens=(0.5, 0.2),
                              return_hist=(0.40, 0.10), style_stretch=(0.4, 0.2),
                              new=(0.85, 0.1), mobile=(0.7, 0.1),
                              size_chart=(0.75, 0.15), tab_switch=(0.25, 0.15),
                              zoom=(0.55, 0.2), price_dwell=(0.3, 0.15),
                              cart_osc=(0.2, 0.15), wishlist=(0.3, 0.2),
                              return_view=(0.5, 0.2), revisit=(0.3, 0.2)),
    'comparison_shopper': dict(p=0.16, size_conf=(0.6, 0.15), price_sens=(0.65, 0.15),
                              return_hist=(0.20, 0.10), style_stretch=(0.3, 0.15),
                              new=(0.4, 0.2), mobile=(0.45, 0.2),
                              size_chart=(0.2, 0.15), tab_switch=(0.85, 0.1),
                              zoom=(0.4, 0.2), price_dwell=(0.6, 0.15),
                              cart_osc=(0.3, 0.15), wishlist=(0.5, 0.2),
                              return_view=(0.2, 0.15), revisit=(0.6, 0.2)),
    'price_sensitive':   dict(p=0.14, size_conf=(0.55, 0.15), price_sens=(0.85, 0.10),
                              return_hist=(0.25, 0.15), style_stretch=(0.3, 0.15),
                              new=(0.3, 0.2), mobile=(0.6, 0.2),
                              size_chart=(0.2, 0.15), tab_switch=(0.55, 0.2),
                              zoom=(0.3, 0.15), price_dwell=(0.85, 0.1),
                              cart_osc=(0.4, 0.2), wishlist=(0.6, 0.2),
                              return_view=(0.3, 0.2), revisit=(0.5, 0.2)),
    'outfit_seeker':     dict(p=0.12, size_conf=(0.7, 0.15), price_sens=(0.4, 0.2),
                              return_hist=(0.15, 0.10), style_stretch=(0.75, 0.15),
                              new=(0.3, 0.2), mobile=(0.5, 0.2),
                              size_chart=(0.15, 0.10), tab_switch=(0.3, 0.15),
                              zoom=(0.4, 0.2), price_dwell=(0.3, 0.15),
                              cart_osc=(0.2, 0.15), wishlist=(0.4, 0.2),
                              return_view=(0.15, 0.10), revisit=(0.4, 0.2)),
    'paralyzed':         dict(p=0.10, size_conf=(0.45, 0.2), price_sens=(0.55, 0.2),
                              return_hist=(0.30, 0.15), style_stretch=(0.4, 0.2),
                              new=(0.4, 0.2), mobile=(0.5, 0.2),
                              size_chart=(0.4, 0.2), tab_switch=(0.5, 0.2),
                              zoom=(0.5, 0.2), price_dwell=(0.5, 0.2),
                              cart_osc=(0.85, 0.1), wishlist=(0.85, 0.1),
                              return_view=(0.4, 0.2), revisit=(0.85, 0.1)),
    'returner_anxious':  dict(p=0.08, size_conf=(0.4, 0.15), price_sens=(0.5, 0.2),
                              return_hist=(0.65, 0.10), style_stretch=(0.4, 0.2),
                              new=(0.2, 0.15), mobile=(0.55, 0.2),
                              size_chart=(0.55, 0.2), tab_switch=(0.3, 0.15),
                              zoom=(0.4, 0.2), price_dwell=(0.4, 0.2),
                              cart_osc=(0.4, 0.2), wishlist=(0.4, 0.2),
                              return_view=(0.85, 0.1), revisit=(0.4, 0.2)),
    'confident_buyer':   dict(p=0.12, size_conf=(0.85, 0.10), price_sens=(0.3, 0.15),
                              return_hist=(0.10, 0.08), style_stretch=(0.3, 0.15),
                              new=(0.15, 0.10), mobile=(0.5, 0.2),
                              size_chart=(0.1, 0.08), tab_switch=(0.15, 0.10),
                              zoom=(0.25, 0.15), price_dwell=(0.2, 0.15),
                              cart_osc=(0.1, 0.08), wishlist=(0.2, 0.15),
                              return_view=(0.1, 0.08), revisit=(0.2, 0.15)),
    'browser_lurker':    dict(p=0.10, size_conf=(0.5, 0.2), price_sens=(0.5, 0.2),
                              return_hist=(0.20, 0.15), style_stretch=(0.5, 0.2),
                              new=(0.5, 0.2), mobile=(0.7, 0.15),
                              size_chart=(0.2, 0.15), tab_switch=(0.4, 0.2),
                              zoom=(0.3, 0.15), price_dwell=(0.3, 0.15),
                              cart_osc=(0.2, 0.15), wishlist=(0.3, 0.2),
                              return_view=(0.2, 0.15), revisit=(0.3, 0.2)),
}

# Per-persona true-need vectors (LLM-authored, paper Section 2.2)
TRUE_NEEDS = {
    'size_anxious_new':   {'N1_fit': 0.85, 'N2_visual': 0.30, 'N3_peer': 0.35, 'N4_compare': 0.20, 'N5_styling': 0.10, 'N6_trust': 0.55, 'N7_commit': 0.25},
    'comparison_shopper': {'N1_fit': 0.20, 'N2_visual': 0.30, 'N3_peer': 0.45, 'N4_compare': 0.85, 'N5_styling': 0.15, 'N6_trust': 0.20, 'N7_commit': 0.35},
    'price_sensitive':    {'N1_fit': 0.20, 'N2_visual': 0.20, 'N3_peer': 0.40, 'N4_compare': 0.65, 'N5_styling': 0.10, 'N6_trust': 0.30, 'N7_commit': 0.40},
    'outfit_seeker':      {'N1_fit': 0.20, 'N2_visual': 0.50, 'N3_peer': 0.30, 'N4_compare': 0.20, 'N5_styling': 0.85, 'N6_trust': 0.10, 'N7_commit': 0.25},
    'paralyzed':          {'N1_fit': 0.30, 'N2_visual': 0.25, 'N3_peer': 0.45, 'N4_compare': 0.45, 'N5_styling': 0.20, 'N6_trust': 0.30, 'N7_commit': 0.85},
    'returner_anxious':   {'N1_fit': 0.55, 'N2_visual': 0.30, 'N3_peer': 0.45, 'N4_compare': 0.25, 'N5_styling': 0.10, 'N6_trust': 0.85, 'N7_commit': 0.30},
    'confident_buyer':    {'N1_fit': 0.10, 'N2_visual': 0.45, 'N3_peer': 0.15, 'N4_compare': 0.10, 'N5_styling': 0.50, 'N6_trust': 0.10, 'N7_commit': 0.15},
    'browser_lurker':     {'N1_fit': 0.20, 'N2_visual': 0.45, 'N3_peer': 0.30, 'N4_compare': 0.30, 'N5_styling': 0.30, 'N6_trust': 0.20, 'N7_commit': 0.30},
}


# ---------- Source API ----------
def persona_names():
    return list(PERSONAS.keys())


def mixture_weights():
    return {k: PERSONAS[k]['p'] for k in PERSONAS}


def true_needs(name):
    return dict(TRUE_NEEDS[name])


def sample_session(rng: np.random.Generator, name: str):
    """Sample one (persona, feat) using rng. rng must be a numpy Generator."""
    from edp.config import SIGNAL_NAMES
    p = PERSONAS[name]
    feat = {}
    for s in SIGNAL_NAMES:
        m, sd = p[s]
        feat[s] = float(np.clip(rng.normal(m, sd), 0.0, 1.0))
    feat['price_norm'] = float(np.clip(rng.beta(2, 3), 0.0, 1.0))
    return feat
