"""
Widget catalog, ground-truth provisions, fashion categories, and per-category
need multipliers.

Categories add a context dimension: the persona's needs are modulated by what
they are shopping for. The same persona shopping shoes vs. accessories has
different needs (more fit anxiety on shoes; more styling on accessories).
"""
from edp.config import NEEDS

# 6 fashion categories with stationary mixture weights summing to 1.
CATEGORIES = ['dress', 'top', 'bottoms', 'shoes', 'outerwear', 'accessories']

CATEGORY_MIX = {
    'dress':       0.18,
    'top':         0.22,
    'bottoms':     0.20,
    'shoes':       0.15,
    'outerwear':   0.10,
    'accessories': 0.15,
}

# Multipliers applied to a persona's base need importance, by category.
# Encodes "which needs matter more when shopping this category".
# Default (any need not listed for a category) is 1.0 — neutral.
# Authored from shopping psychology; intentionally has spread:
#   - shoes: fit/trust dominate (returns are expensive; sizing is hard)
#   - bottoms: fit critical, comparison frequent
#   - outerwear: visual presentation, trust on materials
#   - accessories: styling, visual; fit nearly irrelevant
#   - dresses: balanced, styling-heavy
#   - tops: easy returns, peer signal
CATEGORY_NEED_MULTIPLIERS = {
    'dress':        {'N1_fit': 1.0,  'N2_visual': 1.1,  'N3_peer': 1.0,  'N4_compare': 0.9, 'N5_styling': 1.3, 'N6_trust': 1.0, 'N7_commit': 1.0},
    'top':          {'N1_fit': 0.9,  'N2_visual': 0.9,  'N3_peer': 1.2,  'N4_compare': 1.0, 'N5_styling': 1.0, 'N6_trust': 0.9, 'N7_commit': 0.9},
    'bottoms':      {'N1_fit': 1.3,  'N2_visual': 0.8,  'N3_peer': 0.9,  'N4_compare': 1.2, 'N5_styling': 0.9, 'N6_trust': 1.0, 'N7_commit': 1.0},
    'shoes':        {'N1_fit': 1.4,  'N2_visual': 0.9,  'N3_peer': 1.0,  'N4_compare': 1.0, 'N5_styling': 0.9, 'N6_trust': 1.3, 'N7_commit': 1.0},
    'outerwear':    {'N1_fit': 1.1,  'N2_visual': 1.3,  'N3_peer': 0.8,  'N4_compare': 1.1, 'N5_styling': 1.0, 'N6_trust': 1.2, 'N7_commit': 1.1},
    'accessories':  {'N1_fit': 0.5,  'N2_visual': 1.3,  'N3_peer': 1.1,  'N4_compare': 0.9, 'N5_styling': 1.3, 'N6_trust': 0.8, 'N7_commit': 0.9},
}


def apply_category_multiplier(base_needs: dict, category: str) -> dict:
    """Return scaled-and-clipped need vector for (persona, category)."""
    mult = CATEGORY_NEED_MULTIPLIERS.get(category, {})
    out = {}
    for d in NEEDS:
        v = base_needs.get(d, 0.0) * mult.get(d, 1.0)
        out[d] = min(1.0, max(0.0, v))
    return out


# ---------- Widget provisions ----------
# Each widget delivers along 1-3 of the 7 latent need dimensions.
TRUE_PROVISIONS = {
    'fit_reassurance':       {'N1_fit': 0.70, 'N6_trust': 0.25, 'N3_peer': 0.10},
    'size_guide':            {'N1_fit': 0.60, 'N7_commit': 0.10},
    'low_return_alts':       {'N1_fit': 0.35, 'N6_trust': 0.45, 'N4_compare': 0.15},
    'comparison_card':       {'N4_compare': 0.75, 'N7_commit': 0.20},
    'customers_chose':       {'N3_peer': 0.60, 'N7_commit': 0.30, 'N4_compare': 0.15},
    'value_breakdown':       {'N4_compare': 0.45, 'N2_visual': 0.20, 'N7_commit': 0.30},
    'outfit_completion':     {'N5_styling': 0.70, 'N2_visual': 0.15},
    'style_bridge':          {'N5_styling': 0.60, 'N2_visual': 0.20, 'N7_commit': 0.10},
    'occasion_lookbook':     {'N5_styling': 0.50, 'N2_visual': 0.30, 'N3_peer': 0.10},
    'return_explainer':      {'N6_trust': 0.75, 'N7_commit': 0.15},
    'easy_returns_promise':  {'N6_trust': 0.45, 'N7_commit': 0.25},
    'brand_story':           {'N2_visual': 0.45, 'N3_peer': 0.25, 'N5_styling': 0.20},
    'material_deep_dive':    {'N2_visual': 0.55, 'N1_fit': 0.10, 'N5_styling': 0.15},
    'price_history':         {'N4_compare': 0.40, 'N7_commit': 0.30},
    'price_drop_notify':     {'N7_commit': 0.45, 'N4_compare': 0.15},
    'recently_viewed':       {'N7_commit': 0.40, 'N4_compare': 0.20},
    'wishlist_save':         {'N7_commit': 0.55, 'N6_trust': 0.15},
    'expert_pick':           {'N7_commit': 0.40, 'N3_peer': 0.30, 'N5_styling': 0.10},
    'similar_items':         {'N4_compare': 0.20, 'N5_styling': 0.10, 'N7_commit': 0.10},
    'also_bought':           {'N3_peer': 0.25, 'N7_commit': 0.15},
    'trending_now':          {'N3_peer': 0.20, 'N5_styling': 0.10},
    'personal_recs':         {'N5_styling': 0.15, 'N7_commit': 0.20, 'N4_compare': 0.10},
}

WIDGETS = list(TRUE_PROVISIONS.keys())
N_WIDGETS = len(WIDGETS)
WIDGET_IDX = {w: i for i, w in enumerate(WIDGETS)}
