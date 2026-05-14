# Persona generation task — persona: `premium_silent_browser`

You are simulating sessions for a fashion-retail recommender system. Your
job: read the persona description below and produce a JSON file describing
this persona's needs and behaviour, in a strict schema.

## Persona description

Mid-thirties, considering a premium-priced item. Confident in their taste, looking for quality signals. Zooms in on product images repeatedly, reads brand-story content, materials, craftsmanship details. Doesn't browse alternatives — they want THIS item, but need to be convinced it's worth the spend. Low return history but premium products have higher abandonment.

mixture_weight (share of stream): 0.07

## Required output

Write a JSON file at `/home/user/edp/data/persona_drafts/premium_silent_browser.json` with this EXACT schema:

```json
{
  "name": "premium_silent_browser",
  "description": "<one-line summary you write, ≤200 chars>",
  "mixture_weight": 0.07,
  "true_needs": {
    "N1_fit": 0.0,
    "N2_visual": 0.0,
    "N3_peer": 0.0,
    "N4_compare": 0.0,
    "N5_styling": 0.0,
    "N6_trust": 0.0,
    "N7_commit": 0.0
  },
  "exemplars": [
    {
      "size_conf": 0.0, "price_sens": 0.0, "return_hist": 0.0,
      "style_stretch": 0.0, "new": 0.0, "mobile": 0.0,
      "size_chart": 0.0, "tab_switch": 0.0, "zoom": 0.0,
      "price_dwell": 0.0, "cart_osc": 0.0, "wishlist": 0.0,
      "return_view": 0.0, "revisit": 0.0
    },
    ... (50 exemplars total)
  ]
}
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
