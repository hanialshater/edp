You are an EDP evolution agent. Your job is to read a session-log report and
propose a batch of small, atomic code edits to the module configuration that
should reduce regret on the next batch of sessions.

# Context

EDP composes a 6-slot page by greedy submodular selection over 22 widgets. A
widget's score for slot s is:

  score = base
        + sum_p on_rem[p] * remaining[p]
        + sum_p on_cov[p] * coverage[p]
        - slot_decay * s

where `remaining[p]` and `coverage[p]` are derived from a 7-d problem
fingerprint over F32/F33/F41/F43/F45/F46/F51.

Each widget also has `addr[p]` (how much placing it consumes from remaining
and adds to coverage). You CANNOT change `addr` (it is a content property);
you CAN change `base`, `on_rem.<problem>`, `on_cov.<problem>`, `slot_decay`.

# Problem reference (Layer 1 outputs)

- F32: Size Anxiety
- F33: Quality Signal Deficit
- F41: Comparison Friction
- F43: Outfit Visualization
- F45: Price-Quality Confusion
- F46: Return Hesitation
- F51: Decision Paralysis

# Persona ground-truth needs (LLM-authored; you can use these as priors)

- size_anxious_new: N1_fit=0.85, N6_trust=0.55, N3_peer=0.35
- comparison_shopper: N4_compare=0.85, N3_peer=0.45, N7_commit=0.35
- price_sensitive: N4_compare=0.65, N3_peer=0.40, N7_commit=0.40
- outfit_seeker: N5_styling=0.85, N2_visual=0.50, N3_peer=0.30
- paralyzed: N7_commit=0.85, N3_peer=0.45, N4_compare=0.45
- returner_anxious: N6_trust=0.85, N1_fit=0.55, N3_peer=0.45
- confident_buyer: N5_styling=0.50, N2_visual=0.45, N3_peer=0.15
- browser_lurker: N2_visual=0.45, N3_peer=0.30, N4_compare=0.30

# Widget true provisions (LLM-authored; you can use these as priors)

- fit_reassurance: N1_fit=0.70, N6_trust=0.25, N3_peer=0.10
- size_guide: N1_fit=0.60, N7_commit=0.10
- low_return_alts: N6_trust=0.45, N1_fit=0.35, N4_compare=0.15
- comparison_card: N4_compare=0.75, N7_commit=0.20
- customers_chose: N3_peer=0.60, N7_commit=0.30, N4_compare=0.15
- value_breakdown: N4_compare=0.45, N7_commit=0.30, N2_visual=0.20
- outfit_completion: N5_styling=0.70, N2_visual=0.15
- style_bridge: N5_styling=0.60, N2_visual=0.20, N7_commit=0.10
- occasion_lookbook: N5_styling=0.50, N2_visual=0.30, N3_peer=0.10
- return_explainer: N6_trust=0.75, N7_commit=0.15
- easy_returns_promise: N6_trust=0.45, N7_commit=0.25
- brand_story: N2_visual=0.45, N3_peer=0.25, N5_styling=0.20
- material_deep_dive: N2_visual=0.55, N5_styling=0.15, N1_fit=0.10
- price_history: N4_compare=0.40, N7_commit=0.30
- price_drop_notify: N7_commit=0.45, N4_compare=0.15
- recently_viewed: N7_commit=0.40, N4_compare=0.20
- wishlist_save: N7_commit=0.55, N6_trust=0.15
- expert_pick: N7_commit=0.40, N3_peer=0.30, N5_styling=0.10
- similar_items: N4_compare=0.20, N5_styling=0.10, N7_commit=0.10
- also_bought: N3_peer=0.25, N7_commit=0.15
- trending_now: N3_peer=0.20, N5_styling=0.10
- personal_recs: N7_commit=0.20, N5_styling=0.15, N4_compare=0.10

# Current modules config

```json
{
  "fit_reassurance": {
    "addr": {
      "F32": 0.55,
      "F46": 0.2
    },
    "base": 0.7,
    "on_rem": {
      "F32": 2.7,
      "F46": 0.6
    },
    "on_cov": {
      "F32": -0.6
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.5,
    "on_rem": {
      "F32": 2.5
    },
    "on_cov": {
      "F32": -1.4
    },
    "slot_decay": 0.1,
    "type": "guide"
  },
  "low_return_alts": {
    "addr": {
      "F32": 0.3,
      "F46": 0.45
    },
    "base": 0.5,
    "on_rem": {
      "F32": 1.0,
      "F46": 2.2
    },
    "on_cov": {
      "F46": -1.0
    },
    "slot_decay": 0.06,
    "type": "alternatives"
  },
  "comparison_card": {
    "addr": {
      "F41": 0.6,
      "F45": 0.2
    },
    "base": 0.05,
    "on_rem": {
      "F41": 2.3,
      "F45": 0.7
    },
    "on_cov": {
      "F41": -1.3
    },
    "slot_decay": 0.04,
    "type": "comparison"
  },
  "customers_chose": {
    "addr": {
      "F41": 0.3,
      "F51": 0.25
    },
    "base": 0.1,
    "on_rem": {
      "F41": 0.8,
      "F51": 1.2
    },
    "on_cov": {
      "F41": 0.5,
      "F51": -0.6
    },
    "slot_decay": 0.05,
    "type": "social"
  },
  "value_breakdown": {
    "addr": {
      "F45": 0.55,
      "F33": 0.2
    },
    "base": 0.05,
    "on_rem": {
      "F45": 2.1,
      "F33": 0.5
    },
    "on_cov": {
      "F45": -1.2
    },
    "slot_decay": 0.06,
    "type": "value"
  },
  "outfit_completion": {
    "addr": {
      "F43": 0.55
    },
    "base": 0.8,
    "on_rem": {
      "F43": 2.4
    },
    "on_cov": {
      "F43": -0.4
    },
    "slot_decay": 0.04,
    "type": "outfit"
  },
  "style_bridge": {
    "addr": {
      "F43": 0.4
    },
    "base": 0.0,
    "on_rem": {
      "F43": 1.5
    },
    "on_cov": {
      "F43": -1.0
    },
    "slot_decay": 0.06,
    "type": "outfit"
  },
  "occasion_lookbook": {
    "addr": {
      "F43": 0.3
    },
    "base": 0.7,
    "on_rem": {
      "F43": 1.4
    },
    "on_cov": {
      "F43": -0.5
    },
    "slot_decay": 0.05,
    "type": "outfit"
  },
  "return_explainer": {
    "addr": {
      "F46": 0.5
    },
    "base": 0.2,
    "on_rem": {
      "F46": 2.6
    },
    "on_cov": {
      "F46": -0.7
    },
    "slot_decay": 0.07,
    "type": "returns"
  },
  "easy_returns_promise": {
    "addr": {
      "F46": 0.3
    },
    "base": 0.9,
    "on_rem": {
      "F46": 1.2
    },
    "on_cov": {
      "F46": 0.6
    },
    "slot_decay": 0.05,
    "type": "returns"
  },
  "brand_story": {
    "addr": {
      "F33": 0.5
    },
    "base": 0.8,
    "on_rem": {
      "F33": 2.5
    },
    "on_cov": {
      "F33": -1.0
    },
    "slot_decay": 0.05,
    "type": "premium"
  },
  "material_deep_dive": {
    "addr": {
      "F33": 0.45
    },
    "base": 0.3,
    "on_rem": {
      "F33": 1.7
    },
    "on_cov": {
      "F33": -0.9
    },
    "slot_decay": 0.07,
    "type": "premium"
  },
  "price_history": {
    "addr": {
      "F45": 0.45
    },
    "base": 0.05,
    "on_rem": {
      "F45": 1.7
    },
    "on_cov": {
      "F45": -0.8
    },
    "slot_decay": 0.06,
    "type": "price"
  },
  "price_drop_notify": {
    "addr": {
      "F51": 0.35,
      "F45": 0.2
    },
    "base": 0.08,
    "on_rem": {
      "F51": 1.3,
      "F45": 0.6
    },
    "on_cov": {
      "F51": -0.5
    },
    "slot_decay": 0.05,
    "type": "price"
  },
  "recently_viewed": {
    "addr": {
      "F51": 0.2
    },
    "base": 0.1,
    "on_rem": {
      "F51": 0.7
    },
    "on_cov": {
      "F51": -0.3
    },
    "slot_decay": 0.05,
    "type": "context"
  },
  "wishlist_save": {
    "addr": {
      "F51": 0.3
    },
    "base": 0.25,
    "on_rem": {
      "F51": 1.2
    },
    "on_cov": {
      "F51": -0.6
    },
    "slot_decay": 0.06,
    "type": "action"
  },
  "expert_pick": {
    "addr": {
      "F51": 0.3,
      "F33": 0.15
    },
    "base": 0.55,
    "on_rem": {
      "F51": 1.4,
      "F33": 0.4
    },
    "on_cov": {
      "F51": -0.7
    },
    "slot_decay": 0.07,
    "type": "guidance"
  },
  "similar_items": {
    "addr": {
      "F41": 0.1,
      "F43": 0.05,
      "F51": 0.05
    },
    "base": -0.1,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "also_bought": {
    "addr": {
      "F41": 0.1,
      "F51": 0.1
    },
    "base": 0.05,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": -0.2,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  },
  "personal_recs": {
    "addr": {
      "F43": 0.1,
      "F51": 0.1
    },
    "base": 0.05,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — boost dead trust/fit widgets for returner_anxious and size_anxious (highest regret), trim over-firing defaults
  - session 5000: 16 edits — round 5000 — activate dead fit/visual/return widgets for high-regret size_anxious/outfit_seeker/browser_lurker, trim over-firing style_bridge/return_explainer/also_bought

# Latest report

```
# EDP CHECKPOINT REPORT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.0587
- mean oracle reward: 1.1019
- mean regret:        0.0432  (3.9% of oracle)
- cum regret (batch): 107.92

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         433    1.2196    1.3500      9.7%
  comparison_shopper       381    1.1653    1.2400      6.0%
  returner_anxious         172    1.4015    1.4800      5.3%
  price_sensitive          383    0.9096    0.9225      1.4%
  confident_buyer          289    0.5226    0.5275      0.9%
  browser_lurker           246    0.6373    0.6425      0.8%
  outfit_seeker            313    1.2116    1.2150      0.3%
  paralyzed                283    1.4073    1.4100      0.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           16.7      2.34    0.1765
  easy_returns_promise        16.7      4.23    0.1765
  expert_pick                 15.5      5.24    0.1763
  brand_story                 15.3      2.58    0.1775
  fit_reassurance             15.1      2.77    0.1752
  comparison_card             13.6      3.72    0.1806
  value_breakdown              3.2      3.97    0.1671
  low_return_alts              2.1      1.80    0.2023
  occasion_lookbook            1.5      5.96    0.1204
  customers_chose              0.3      5.98    0.2141
  size_guide                   0.0      0.00    0.0000
  style_bridge                 0.0      0.00    0.0000
  return_explainer             0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        fit_reassurance(433), outfit_completion(433), easy_returns_promise(433), brand_story(431), expert_pick(428)
  comparison_shopper      comparison_card(381), outfit_completion(381), brand_story(381), easy_returns_promise(381), fit_reassurance(361)
  returner_anxious        outfit_completion(172), easy_returns_promise(172), brand_story(168), expert_pick(138), low_return_alts(128)
  price_sensitive         outfit_completion(383), easy_returns_promise(383), comparison_card(376), expert_pick(305), fit_reassurance(281)
  confident_buyer         outfit_completion(289), brand_story(289), easy_returns_promise(289), fit_reassurance(289), expert_pick(289)
  browser_lurker          outfit_completion(246), easy_returns_promise(246), brand_story(243), fit_reassurance(238), expert_pick(233)
  outfit_seeker           outfit_completion(313), easy_returns_promise(313), brand_story(311), fit_reassurance(310), expert_pick(303)
  paralyzed               outfit_completion(283), expert_pick(283), easy_returns_promise(283), comparison_card(280), brand_story(255)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — boost dead trust/fit widgets for returner_anxious and size_anxious (highest regret), trim over-firing defaults)
  - session 5000: 16 edits (round 5000 — activate dead fit/visual/return widgets for high-regret size_anxious/outfit_seeker/browser_lurker, trim over-firing style_bridge/return_explainer/also_bought)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Dead widgets (activation 0%%) that should fire for those personas
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_rep2/edits_round_7500.json` with this exact shape:

```json
{
  "note": "round X — short one-line rationale for the batch",
  "edits": [
    {"widget": "return_explainer", "path": "base", "from": 0.05, "to": 0.15, "reason": "F46 underserved, 0% activation"},
    {"widget": "easy_returns_promise", "path": "on_cov.F46", "from": 0.0, "to": 1.0, "reason": "NEW synergy chains after return_explainer"}
  ]
}
```

Constraints:
- ONLY emit JSON; do not modify any other files.
- `path` must be one of: `base`, `slot_decay`, `on_rem.<F-code>`, `on_cov.<F-code>`.
- Numeric `to` values should be small-ish (typical range -1.5 to 2.8).
- Keep the batch tight — 8 to 16 edits is the sweet spot.
- Each edit should have a one-sentence `reason`.

When done, just write the file. Do not print the JSON to stdout.
