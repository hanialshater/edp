"""
Customer simulator for bandit-vs-EDP comparison.

Realistic production stack:
  - Page-level reward (not per-slot)
  - Delayed observation (D sessions, ~2 days of traffic)
  - Observation noise (sigma)

Ground truth is LLM-authored: 7 latent shopping needs, persona need vectors,
widget provision vectors. Independent of any policy's internal representation.
"""
from __future__ import annotations
import numpy as np
from collections import deque
from dataclasses import dataclass, field

N_SLOTS = 6

# ---------- Personas ----------
# Each entry: signal distributions as (mean, std), clipped to [0, 1].
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

SIGNAL_NAMES = ['size_conf', 'price_sens', 'return_hist', 'style_stretch',
                'new', 'mobile', 'size_chart', 'tab_switch', 'zoom',
                'price_dwell', 'cart_osc', 'wishlist', 'return_view', 'revisit']

# ---------- Ground truth: 7 latent needs ----------
NEEDS = ['N1_fit', 'N2_visual', 'N3_peer', 'N4_compare',
         'N5_styling', 'N6_trust', 'N7_commit']

TRUE_NEEDS = {
    'size_anxious_new':   {'N1_fit':0.85, 'N2_visual':0.30, 'N3_peer':0.35, 'N4_compare':0.20, 'N5_styling':0.10, 'N6_trust':0.55, 'N7_commit':0.25},
    'comparison_shopper': {'N1_fit':0.20, 'N2_visual':0.30, 'N3_peer':0.45, 'N4_compare':0.85, 'N5_styling':0.15, 'N6_trust':0.20, 'N7_commit':0.35},
    'price_sensitive':    {'N1_fit':0.20, 'N2_visual':0.20, 'N3_peer':0.40, 'N4_compare':0.65, 'N5_styling':0.10, 'N6_trust':0.30, 'N7_commit':0.40},
    'outfit_seeker':      {'N1_fit':0.20, 'N2_visual':0.50, 'N3_peer':0.30, 'N4_compare':0.20, 'N5_styling':0.85, 'N6_trust':0.10, 'N7_commit':0.25},
    'paralyzed':          {'N1_fit':0.30, 'N2_visual':0.25, 'N3_peer':0.45, 'N4_compare':0.45, 'N5_styling':0.20, 'N6_trust':0.30, 'N7_commit':0.85},
    'returner_anxious':   {'N1_fit':0.55, 'N2_visual':0.30, 'N3_peer':0.45, 'N4_compare':0.25, 'N5_styling':0.10, 'N6_trust':0.85, 'N7_commit':0.30},
    'confident_buyer':    {'N1_fit':0.10, 'N2_visual':0.45, 'N3_peer':0.15, 'N4_compare':0.10, 'N5_styling':0.50, 'N6_trust':0.10, 'N7_commit':0.15},
    'browser_lurker':     {'N1_fit':0.20, 'N2_visual':0.45, 'N3_peer':0.30, 'N4_compare':0.30, 'N5_styling':0.30, 'N6_trust':0.20, 'N7_commit':0.30},
}

TRUE_PROVISIONS = {
    'fit_reassurance':       {'N1_fit':0.70, 'N6_trust':0.25, 'N3_peer':0.10},
    'size_guide':            {'N1_fit':0.60, 'N7_commit':0.10},
    'low_return_alts':       {'N1_fit':0.35, 'N6_trust':0.45, 'N4_compare':0.15},
    'comparison_card':       {'N4_compare':0.75, 'N7_commit':0.20},
    'customers_chose':       {'N3_peer':0.60, 'N7_commit':0.30, 'N4_compare':0.15},
    'value_breakdown':       {'N4_compare':0.45, 'N2_visual':0.20, 'N7_commit':0.30},
    'outfit_completion':     {'N5_styling':0.70, 'N2_visual':0.15},
    'style_bridge':          {'N5_styling':0.60, 'N2_visual':0.20, 'N7_commit':0.10},
    'occasion_lookbook':     {'N5_styling':0.50, 'N2_visual':0.30, 'N3_peer':0.10},
    'return_explainer':      {'N6_trust':0.75, 'N7_commit':0.15},
    'easy_returns_promise':  {'N6_trust':0.45, 'N7_commit':0.25},
    'brand_story':           {'N2_visual':0.45, 'N3_peer':0.25, 'N5_styling':0.20},
    'material_deep_dive':    {'N2_visual':0.55, 'N1_fit':0.10, 'N5_styling':0.15},
    'price_history':         {'N4_compare':0.40, 'N7_commit':0.30},
    'price_drop_notify':     {'N7_commit':0.45, 'N4_compare':0.15},
    'recently_viewed':       {'N7_commit':0.40, 'N4_compare':0.20},
    'wishlist_save':         {'N7_commit':0.55, 'N6_trust':0.15},
    'expert_pick':           {'N7_commit':0.40, 'N3_peer':0.30, 'N5_styling':0.10},
    'similar_items':         {'N4_compare':0.20, 'N5_styling':0.10, 'N7_commit':0.10},
    'also_bought':           {'N3_peer':0.25, 'N7_commit':0.15},
    'trending_now':          {'N3_peer':0.20, 'N5_styling':0.10},
    'personal_recs':         {'N5_styling':0.15, 'N7_commit':0.20, 'N4_compare':0.10},
}

WIDGETS = list(TRUE_PROVISIONS.keys())
N_WIDGETS = len(WIDGETS)
WIDGET_IDX = {w: i for i, w in enumerate(WIDGETS)}


def true_page_reward(persona_name: str, page: list[str]) -> float:
    """Diminishing-returns reward: each slot consumes from remaining need budget."""
    needs = dict(TRUE_NEEDS[persona_name])
    remaining = dict(needs)
    total = 0.0
    for widget in page:
        for dim, p in TRUE_PROVISIONS.get(widget, {}).items():
            consumed = min(remaining[dim], p)
            total += needs[dim] * consumed
            remaining[dim] -= consumed
    return total


def oracle_reward(persona_name: str) -> float:
    """Greedy oracle over true provisions — upper bound at N_SLOTS slots."""
    needs = dict(TRUE_NEEDS[persona_name])
    remaining = dict(needs)
    used = set()
    total = 0.0
    for _ in range(N_SLOTS):
        best_w, best_r = None, -1.0
        for w, prov in TRUE_PROVISIONS.items():
            if w in used:
                continue
            r = sum(needs[d] * min(remaining[d], p) for d, p in prov.items())
            if r > best_r:
                best_r, best_w = r, w
        if best_w is None:
            break
        used.add(best_w)
        total += best_r
        for d, p in TRUE_PROVISIONS[best_w].items():
            remaining[d] = max(0.0, remaining[d] - p)
    return total


ORACLE_REWARDS = {p: oracle_reward(p) for p in TRUE_NEEDS}


# ---------- Session stream ----------
def make_session_stream(n: int, seed: int = 42) -> list[tuple[str, dict]]:
    """Reproducible (persona, feature_vector) stream."""
    r = np.random.default_rng(seed)
    names = list(PERSONAS.keys())
    probs = np.array([PERSONAS[k]['p'] for k in names])
    probs /= probs.sum()
    stream = []
    for _ in range(n):
        pn = r.choice(names, p=probs)
        persona = PERSONAS[pn]
        feat = {}
        for s in SIGNAL_NAMES:
            m, sd = persona[s]
            feat[s] = float(np.clip(r.normal(m, sd), 0.0, 1.0))
        feat['price_norm'] = float(np.clip(r.beta(2, 3), 0.0, 1.0))
        stream.append((pn, feat))
    return stream


# ---------- Delay + noise queue ----------
@dataclass
class DelayedFeedback:
    """
    Queue that holds (session_idx, payload) tuples and releases them when
    `current_idx >= session_idx + delay`. Models the 2-day attribution lag.
    """
    delay: int
    noise_sigma: float = 0.0
    seed: int = 0
    _q: deque = field(default_factory=deque)
    _rng: np.random.Generator = field(init=False)

    def __post_init__(self):
        self._rng = np.random.default_rng(self.seed)

    def submit(self, session_idx: int, true_reward: float, payload):
        """Stash a payload tagged with the true reward (which gets noised on release)."""
        self._q.append((session_idx, true_reward, payload))

    def drain_ready(self, current_idx: int):
        """Yield (observed_reward, payload) for entries whose delay has elapsed."""
        while self._q and self._q[0][0] + self.delay <= current_idx:
            _, r_true, payload = self._q.popleft()
            r_obs = r_true + (self._rng.normal(0.0, self.noise_sigma)
                              if self.noise_sigma > 0 else 0.0)
            yield r_obs, payload

    def drain_all(self):
        """Force-release everything (end of run)."""
        while self._q:
            _, r_true, payload = self._q.popleft()
            r_obs = r_true + (self._rng.normal(0.0, self.noise_sigma)
                              if self.noise_sigma > 0 else 0.0)
            yield r_obs, payload


if __name__ == '__main__':
    print('Oracle rewards by persona (N_SLOTS=6):')
    for p, r in ORACLE_REWARDS.items():
        print(f'  {p:22s}  {r:.4f}')
    stream = make_session_stream(1000, seed=42)
    from collections import Counter
    counts = Counter(p for p, _ in stream)
    print('\nPersona mix in 1k stream:')
    for p, c in counts.most_common():
        print(f'  {p:22s}  {c/10:.1f}%')
