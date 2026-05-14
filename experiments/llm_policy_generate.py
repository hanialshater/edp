"""
Generate the LLM-as-policy function.

Writes the prompt to data/LLM_POLICY_PROMPT.md; a subagent reads it and
writes data/llm_policy_fn.py containing a `pick_page(feat, category)`
function. This is a one-shot Software-3.0-style baseline: the LLM
authors the entire policy as Python.
"""
from __future__ import annotations
import os
import sys
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp.config import N_SLOTS, SIGNAL_NAMES
from edp.catalog import CATEGORIES, WIDGETS


PROMPT_TEMPLATE = '''\
# Task — write a page-composition policy in Python

You are designing a recommender page-composition policy for a fashion retail
site. Each user session is described by 14 numeric **context features** plus
a **product category**. Your policy must select 6 widgets (no repeats) from a
fixed catalogue of 22 for each session.

You will write a single Python function:

```python
def pick_page(feat: dict, category: str) -> list[str]:
    """Return a list of exactly 6 unique widget names from the catalog."""
    ...
```

The function must:
- Be self-contained Python (use only built-ins + the standard library).
- Return a list of exactly **6** widget names from the catalog (see below).
- Never repeat a widget within one returned list.
- Use the context features (`feat`) and category to personalise the page.
- Be deterministic: same input → same output. No randomness, no I/O.

## Context features available in `feat` (each in [0, 1])

{signal_doc}

(There is also `feat['price_norm']` in [0, 1] indicating how premium the
priced item is — 0 = budget, 1 = luxury. You may use it.)

## Category options

`category` is one of: {categories}

Different categories may have different needs (e.g. shoes have higher fit
anxiety than accessories; outerwear is more about visual presentation).

## Widget catalog with descriptions

{widget_doc}

## Guidance for your policy

You may reason however you like — if/else thresholds, scoring, weighted
ranking, a small decision tree. Aim for an interpretable rule set that:

- Personalises by context features (not the same page for every session).
- Recognises common shopper archetypes from the features (e.g. high
  `return_view` + high `return_hist` → consider return-trust widgets).
- Considers category effects (shoes & bottoms care more about fit; dress &
  accessories care more about styling).
- Uses 4–6 "personalised slot" picks plus 0–2 sensible defaults if needed.

## Output

Write your Python function to `data/llm_policy_fn.py`. Only define
`pick_page` (you may add helper functions). Do NOT include print statements
or top-level code that runs on import.

After writing, in under 100 words describe the structure of your policy
(thresholds you used, archetypes you defined, etc.). Do not paste the code.
'''


SIGNAL_DESCRIPTIONS = {
    'size_conf':     'how confident the user is in their size for this product right now',
    'price_sens':    'how price-driven this session is (1 = highly price-sensitive)',
    'return_hist':   'historical return rate (0 = new buyer, 1 = heavy returner)',
    'style_stretch': 'openness to discovery / unfamiliar styles',
    'new':           'how new this user is to the brand (0 = loyal, 1 = first visit)',
    'mobile':        'mobile vs desktop (1 = mobile)',
    'size_chart':    'time spent engaging the size chart this session',
    'tab_switch':    'how often they tab-switched (compare across retailers / pages)',
    'zoom':          'image-zoom engagement (proxy for examining details)',
    'price_dwell':   'time spent dwelling on price information',
    'cart_osc':      'add/remove-from-cart oscillation (proxy for indecision)',
    'wishlist':      'wishlist activity this session',
    'return_view':   'time spent on the returns-policy block',
    'revisit':       'how many times they revisited this product',
}


def render_prompt():
    sig_doc = '\n'.join(f'- `{s}`: {SIGNAL_DESCRIPTIONS[s]}' for s in SIGNAL_NAMES)
    with open('data/widget_descriptions.yaml') as f:
        wd = yaml.safe_load(f)
    wid_doc = '\n'.join(f'- `{w}`: {wd[w]}' for w in WIDGETS)
    cats = ', '.join(f'`{c}`' for c in CATEGORIES)
    return PROMPT_TEMPLATE.format(
        signal_doc=sig_doc, categories=cats, widget_doc=wid_doc
    )


def main():
    prompt = render_prompt()
    out_path = 'data/LLM_POLICY_PROMPT.md'
    with open(out_path, 'w') as f:
        f.write(prompt)
    print(f'Wrote prompt -> {out_path}')
    print(f'Expected output: data/llm_policy_fn.py (defining pick_page).')


if __name__ == '__main__':
    main()
