"""
Generate the LLM-persona cache.

For each persona in data/personas_text.yaml:

  Step A: produce a TRUE_NEEDS_BASE vector (7-d, [0,1]) from the description.
  Step B: produce 50 exemplar feature vectors — concrete (signal -> value)
          realizations of "what would a session from this persona look like",
          with realistic correlations between signals.

This script does NOT invoke an LLM directly (no API key). Instead it:
  - writes a per-persona instruction file the LLM subagent can read
  - the orchestrator (a human or a Claude Code session) drives the subagents
  - the resulting per-persona JSONs are merged into data/personas_llm_cache.json

Workflow:

  1. python3 experiments/persona_generate.py --prepare
     -> writes data/persona_instructions/<persona>.md for each entry
     -> writes the empty cache shell

  2. The Claude Code parent session invokes one subagent per persona
     using each instruction file. Each subagent writes
     data/persona_drafts/<persona>.json with the required schema.

  3. python3 experiments/persona_generate.py --merge
     -> validates all 14 drafts
     -> merges into data/personas_llm_cache.json
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from textwrap import dedent
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp.config import NEEDS, SIGNAL_NAMES
from edp.catalog import CATEGORIES

INSTR_DIR = 'data/persona_instructions'
DRAFTS_DIR = 'data/persona_drafts'
CACHE_PATH = 'data/personas_llm_cache.json'
TEXT_PATH = 'data/personas_text.yaml'


INSTR_TEMPLATE = dedent('''\
# Persona generation task — persona: `{name}`

You are simulating sessions for a fashion-retail recommender system. Your
job: read the persona description below and produce a JSON file describing
this persona's needs and behaviour, in a strict schema.

## Persona description

{description}

mixture_weight (share of stream): {weight}

## Required output

Write a JSON file at `{out_path}` with this EXACT schema:

```json
{{
  "name": "{name}",
  "description": "<one-line summary you write, ≤200 chars>",
  "mixture_weight": {weight},
  "true_needs": {{
    "N1_fit": 0.0,
    "N2_visual": 0.0,
    "N3_peer": 0.0,
    "N4_compare": 0.0,
    "N5_styling": 0.0,
    "N6_trust": 0.0,
    "N7_commit": 0.0
  }},
  "exemplars": [
    {{
      "size_conf": 0.0, "price_sens": 0.0, "return_hist": 0.0,
      "style_stretch": 0.0, "new": 0.0, "mobile": 0.0,
      "size_chart": 0.0, "tab_switch": 0.0, "zoom": 0.0,
      "price_dwell": 0.0, "cart_osc": 0.0, "wishlist": 0.0,
      "return_view": 0.0, "revisit": 0.0
    }},
    ... (50 exemplars total)
  ]
}}
```

## How to set `true_needs`

Each value is in [0, 1] and represents how much this persona cares about
the corresponding need dimension:

- **N1_fit**: getting the right size / fit
- **N2_visual**: seeing the product clearly (zoom, detail, materials)
- **N3_peer**: what other customers think (reviews, social)
- **N4_compare**: comparing prices / specs / alternatives
- **N5_styling**: outfit-building, occasion-matching, style discovery
- **N6_trust**: confidence the brand will not screw them (returns, quality)
- **N7_commit**: help making the final buy decision (save / wishlist / nudge)

These should reflect the persona's WANTS, not their behaviour. Pull from
the description carefully — e.g. a "premium silent browser" cares deeply
about N2_visual and quality signals but not about N3_peer.

## How to set `exemplars`

Each exemplar is a concrete session from this persona — 14 numeric values
in [0, 1] for these signals:

- **size_conf**: how confident the user is in their size right now
- **price_sens**: how much price drives this session's behaviour
- **return_hist**: their history of returning items (0=new, 1=heavy returner)
- **style_stretch**: openness to discovery / unfamiliar styles
- **new**: how new this user is (0=loyal, 1=first visit)
- **mobile**: 1 if mobile, 0 if desktop, fractional if blended
- **size_chart**: how much they engaged with the size chart this session
- **tab_switch**: tab-switching activity this session
- **zoom**: image-zoom engagement
- **price_dwell**: time spent on the price block
- **cart_osc**: how much they oscillated adding/removing from cart
- **wishlist**: wishlist activity this session
- **return_view**: time on the returns-policy block
- **revisit**: how often they've revisited this product

Vary the exemplars realistically — not all clones. Some sessions of this
persona will be more anxious than others; some more decisive. Signals
should be correlated in plausible ways (e.g. high cart_osc usually goes
with high revisit; high size_chart usually goes with low size_conf).
Aim for natural diversity — do not make all 50 look the same.

## Constraints

- ONLY write that one JSON file. Do not edit anything else under `/home/user/edp/`.
- All numeric values strictly in [0, 1].
- Exactly 50 exemplars.
- Final message in the conversation: under 80 words on (a) the dominant need
  axis you chose for `true_needs` and why, and (b) one notable correlation
  pattern you encoded in the exemplars.
''')


def load_text():
    with open(TEXT_PATH) as f:
        return yaml.safe_load(f)


def prepare():
    os.makedirs(INSTR_DIR, exist_ok=True)
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    cfg = load_text()
    for p in cfg['personas']:
        name = p['name']
        instr = INSTR_TEMPLATE.format(
            name=name,
            description=p['description'].strip(),
            weight=p['mixture_weight'],
            out_path=os.path.abspath(os.path.join(DRAFTS_DIR, f'{name}.json')),
        )
        with open(os.path.join(INSTR_DIR, f'{name}.md'), 'w') as f:
            f.write(instr)
    print(f'Wrote {len(cfg["personas"])} persona instructions to {INSTR_DIR}/')
    print(f'Drafts go to: {DRAFTS_DIR}/')


def _validate_draft(name, d):
    assert d['name'] == name, f'{name}: name mismatch'
    assert isinstance(d['mixture_weight'], (int, float))
    tn = d['true_needs']
    for k in NEEDS:
        assert k in tn, f'{name}: missing need {k}'
        assert 0.0 <= tn[k] <= 1.0, f'{name}: need {k} out of [0,1]: {tn[k]}'
    ex = d['exemplars']
    # Accept 40-60; truncate to 50 in the merge.
    assert 40 <= len(ex) <= 60, f'{name}: expected ~50 exemplars, got {len(ex)}'
    for i, e in enumerate(ex[:50]):
        for s in SIGNAL_NAMES:
            assert s in e, f'{name} ex{i}: missing signal {s}'
            assert 0.0 <= e[s] <= 1.0, f'{name} ex{i} {s}: {e[s]} out of [0,1]'
    # Pad to 50 by duplicating with tiny jitter, if undershot.
    if len(ex) < 50:
        import random
        rng = random.Random(hash(name))
        while len(ex) < 50:
            base = dict(ex[rng.randrange(len(ex))])
            for s in SIGNAL_NAMES:
                base[s] = max(0.0, min(1.0, base[s] + rng.uniform(-0.02, 0.02)))
            ex.append(base)
    d['exemplars'] = ex[:50]


def merge():
    cfg = load_text()
    out = {'personas': {}}
    missing = []
    for p in cfg['personas']:
        name = p['name']
        path = os.path.join(DRAFTS_DIR, f'{name}.json')
        if not os.path.exists(path):
            missing.append(name)
            continue
        with open(path) as f:
            d = json.load(f)
        _validate_draft(name, d)
        out['personas'][name] = {
            'description': d['description'],
            'mixture_weight': d['mixture_weight'],
            'true_needs': d['true_needs'],
            'exemplars': d['exemplars'],
        }
        print(f'  {name}  ok (50 exemplars, {len(d["true_needs"])} needs)')
    if missing:
        print(f'\nMissing drafts ({len(missing)}): {missing}')
        sys.exit(1)
    with open(CACHE_PATH, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nMerged into {CACHE_PATH}.  Total personas: {len(out["personas"])}.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['prepare', 'merge'])
    args = ap.parse_args()
    if args.mode == 'prepare':
        prepare()
    else:
        merge()


if __name__ == '__main__':
    main()
