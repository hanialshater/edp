"""Shared constants. Imported by every other module."""
N_SLOTS = 6

SIGNAL_NAMES = ['size_conf', 'price_sens', 'return_hist', 'style_stretch',
                'new', 'mobile', 'size_chart', 'tab_switch', 'zoom',
                'price_dwell', 'cart_osc', 'wishlist', 'return_view', 'revisit']

# 7 latent shopping needs — ground truth dimensions
NEEDS = ['N1_fit', 'N2_visual', 'N3_peer', 'N4_compare',
         'N5_styling', 'N6_trust', 'N7_commit']

# EDP's 7-problem fingerprint (internal taxonomy, not aligned with NEEDS)
PROBLEMS = ['F32', 'F33', 'F41', 'F43', 'F45', 'F46', 'F51']
PROBLEM_NAMES = {
    'F32': 'Size Anxiety',
    'F33': 'Quality Signal Deficit',
    'F41': 'Comparison Friction',
    'F43': 'Outfit Visualization',
    'F45': 'Price-Quality Confusion',
    'F46': 'Return Hesitation',
    'F51': 'Decision Paralysis',
}
