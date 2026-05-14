"""
LLM-driven persona source.

  - Personas are defined as natural-language descriptions in
    data/personas_text.yaml.
  - For each persona, a Claude subagent has generated:
      (a) a TRUE_NEEDS vector (LLM-inferred from the description)
      (b) a pool of K=50 exemplar feature vectors — concrete (signal -> value)
          realizations of "what would a session from this persona look like"
  - The cache is data/personas_llm_cache.json.
  - At simulation time:
      1. sample a persona by mixture
      2. sample an exemplar uniformly from that persona's pool
      3. add Gaussian noise sigma=0.05 per signal, clipped to [0, 1]

Generated separately via experiments/persona_generate.py; this module only
reads the cache.
"""
from __future__ import annotations
import json
import os
import numpy as np

from edp.config import SIGNAL_NAMES

CACHE_PATH = 'data/personas_llm_cache.json'


_CACHE = None


def _load():
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    if not os.path.exists(CACHE_PATH):
        raise FileNotFoundError(
            f'LLM persona cache not found at {CACHE_PATH}. Run '
            '`python3 experiments/persona_generate.py` first.'
        )
    with open(CACHE_PATH) as f:
        _CACHE = json.load(f)
    return _CACHE


def persona_names():
    return list(_load()['personas'].keys())


def mixture_weights():
    out = {}
    for name, info in _load()['personas'].items():
        out[name] = float(info['mixture_weight'])
    s = sum(out.values())
    return {k: v / s for k, v in out.items()}


def true_needs(name):
    return dict(_load()['personas'][name]['true_needs'])


def descriptions():
    return {n: info['description'] for n, info in _load()['personas'].items()}


def sample_session(rng: np.random.Generator, name: str,
                   noise_sigma: float = 0.05):
    """
    Sample one (persona, feat). Picks an exemplar from the persona's pool
    then adds clipped Gaussian noise per signal.
    """
    pool = _load()['personas'][name]['exemplars']
    ex = pool[int(rng.integers(0, len(pool)))]
    feat = {}
    for s in SIGNAL_NAMES:
        base = float(ex.get(s, 0.5))
        v = base + float(rng.normal(0.0, noise_sigma)) if noise_sigma > 0 else base
        feat[s] = float(np.clip(v, 0.0, 1.0))
    # price_norm is product-side and persona-independent
    feat['price_norm'] = float(np.clip(rng.beta(2, 3), 0.0, 1.0))
    return feat
