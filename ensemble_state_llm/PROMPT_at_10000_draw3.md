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

# Persona base-need vectors (LLM-authored; you can use these as priors)

- hesitant_first_buyer: N6_trust=0.92, N1_fit=0.82, N7_commit=0.70
- tabbed_comparison_shopper: N4_compare=0.95, N7_commit=0.70, N6_trust=0.55
- birthday_rush_gifter: N6_trust=0.92, N7_commit=0.70, N1_fit=0.55
- post_return_returner: N1_fit=0.95, N6_trust=0.90, N3_peer=0.70
- outfit_event_planner: N5_styling=0.95, N2_visual=0.55, N7_commit=0.55
- bargain_hunter_returning: N4_compare=0.85, N7_commit=0.55, N2_visual=0.20
- premium_silent_browser: N2_visual=0.92, N6_trust=0.78, N7_commit=0.70
- paralyzed_wishlister: N7_commit=0.95, N4_compare=0.82, N5_styling=0.60
- mobile_evening_browser: N7_commit=0.70, N5_styling=0.55, N2_visual=0.35
- confident_repeat_buyer: N6_trust=0.55, N2_visual=0.30, N5_styling=0.20
- size_specific_anxious: N1_fit=0.97, N6_trust=0.88, N3_peer=0.78
- trend_chaser: N3_peer=0.82, N2_visual=0.78, N5_styling=0.68
- corporate_uniform_buyer: N1_fit=0.85, N6_trust=0.70, N2_visual=0.35
- returner_from_recent_order: N6_trust=0.88, N1_fit=0.78, N2_visual=0.55

# Fashion-category need multipliers

Each session has both a persona and a fashion category (dress, top, bottoms,
shoes, outerwear, accessories). The persona's base needs are multiplied
element-wise by the category multiplier. So e.g. a `size_anxious_new`
shopper looking at shoes has even higher N1_fit than the same persona looking
at accessories.

- dress: N5_styling×1.30, N2_visual×1.10, N1_fit×1.00
- top: N3_peer×1.20, N4_compare×1.00, N5_styling×1.00
- bottoms: N1_fit×1.30, N4_compare×1.20, N6_trust×1.00
- shoes: N1_fit×1.40, N6_trust×1.30, N3_peer×1.00
- outerwear: N2_visual×1.30, N6_trust×1.20, N1_fit×1.10
- accessories: N2_visual×1.30, N5_styling×1.30, N3_peer×1.10

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
    "base": 0.3,
    "on_rem": {
      "F32": 3.1,
      "F46": 0.6
    },
    "on_cov": {
      "F32": -1.2
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.55,
    "on_rem": {
      "F32": 2.0
    },
    "on_cov": {
      "F32": 0.6
    },
    "slot_decay": 0.1,
    "type": "guide"
  },
  "low_return_alts": {
    "addr": {
      "F32": 0.3,
      "F46": 0.45
    },
    "base": 0.35,
    "on_rem": {
      "F32": 1.0,
      "F46": 1.8
    },
    "on_cov": {
      "F46": -1.0,
      "F32": 0.8
    },
    "slot_decay": 0.06,
    "type": "alternatives"
  },
  "comparison_card": {
    "addr": {
      "F41": 0.6,
      "F45": 0.2
    },
    "base": -0.15,
    "on_rem": {
      "F41": 2.3,
      "F45": 0.7
    },
    "on_cov": {
      "F41": -1.3
    },
    "slot_decay": 0.07,
    "type": "comparison"
  },
  "customers_chose": {
    "addr": {
      "F41": 0.3,
      "F51": 0.25
    },
    "base": 0.32,
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
    "base": 0.3,
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
    "base": 0.0,
    "on_rem": {
      "F43": 1.8
    },
    "on_cov": {
      "F43": -0.8
    },
    "slot_decay": 0.04,
    "type": "outfit"
  },
  "style_bridge": {
    "addr": {
      "F43": 0.4
    },
    "base": 0.28,
    "on_rem": {
      "F43": 2.0
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
    "base": 0.32,
    "on_rem": {
      "F43": 1.4
    },
    "on_cov": {
      "F43": 0.7
    },
    "slot_decay": 0.05,
    "type": "outfit"
  },
  "return_explainer": {
    "addr": {
      "F46": 0.5
    },
    "base": 0.55,
    "on_rem": {
      "F46": 2.4
    },
    "on_cov": {
      "F46": -1.3
    },
    "slot_decay": 0.07,
    "type": "returns"
  },
  "easy_returns_promise": {
    "addr": {
      "F46": 0.3
    },
    "base": 0.25,
    "on_rem": {
      "F46": 1.2
    },
    "on_cov": {
      "F46": 0.9
    },
    "slot_decay": 0.05,
    "type": "returns"
  },
  "brand_story": {
    "addr": {
      "F33": 0.5
    },
    "base": 0.1,
    "on_rem": {
      "F33": 1.9
    },
    "on_cov": {
      "F33": -1.0,
      "F43": 0.6
    },
    "slot_decay": 0.05,
    "type": "premium"
  },
  "material_deep_dive": {
    "addr": {
      "F33": 0.45
    },
    "base": 0.32,
    "on_rem": {
      "F33": 1.7
    },
    "on_cov": {
      "F33": 0.8
    },
    "slot_decay": 0.07,
    "type": "premium"
  },
  "price_history": {
    "addr": {
      "F45": 0.45
    },
    "base": 0.16,
    "on_rem": {
      "F45": 1.7
    },
    "on_cov": {
      "F45": 0.7
    },
    "slot_decay": 0.06,
    "type": "price"
  },
  "price_drop_notify": {
    "addr": {
      "F51": 0.35,
      "F45": 0.2
    },
    "base": 0.42,
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
    "base": 0.55,
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
    "base": 0.5,
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
    "base": 0.45,
    "on_rem": {
      "F51": 1.4,
      "F33": 0.4
    },
    "on_cov": {
      "F51": 0.6
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
    "base": 0.18,
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
    "base": 0.15,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.18,
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
    "base": 0.22,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1]
  - session 2500: 16 edits — round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2]
  - session 5000: 16 edits — round 5000 draw1 — revive dead widgets (size_guide, occasion_lookbook, personal_recs, trending_now), tame over-firing low-reward widgets, boost confident_repeat/trend_chaser cells, add F32->F46 and F43->F33 synergies  [ensemble-best of 3: draw 1]
  - session 7500: 14 edits — round 7500 draw1 — stabilization: revive truly dead widgets (return_explainer/wishlist_save/price_drop_notify), trim over-firing low r/fire (occasion_lookbook, personal_recs), patch worst cells (confident_repeat shoes/bottoms, size_specific accessories, premium shoes)  [ensemble-best of 3: draw 1]

# Latest report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8251
- mean oracle reward: 2.0225
- mean regret:        0.1975  (9.8% of oracle)
- cum regret (batch): 493.64

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             105    1.9337    2.3312     17.1%
  paralyzed_wishlister     172    2.4744    2.8495     13.2%
  hesitant_first_buyer     336    2.2806    2.6004     12.3%
  size_specific_anxious    114    2.5646    2.9005     11.6%
  premium_silent_browser   177    1.8672    2.1053     11.3%
  returner_from_recent_order   121    2.1841    2.4114      9.4%
  post_return_returner     198    2.5465    2.8039      9.2%
  outfit_event_planner     212    1.7628    1.9123      7.8%
  corporate_uniform_buyer    81    1.3493    1.4618      7.7%
  birthday_rush_gifter     149    2.3138    2.4820      6.8%
  mobile_evening_browser   190    1.0234    1.0955      6.6%
  tabbed_comparison_shopper   240    1.7111    1.8258      6.3%
  bargain_hunter_returning   223    1.1333    1.1832      4.2%
  confident_repeat_buyer   182    0.4989    0.5144      3.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      362    1.4895    1.7287     13.8%
  outerwear        242    2.0904    2.3259     10.1%
  top              575    1.6049    1.7847     10.1%
  dress            441    1.9046    2.1134      9.9%
  bottoms          495    1.9245    2.0960      8.2%
  shoes            385    2.0836    2.2647      8.0%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             28    1.7204    2.2468     23.4%
  corporate_uniform_buyer accessories     14    0.6440    0.8284     22.3%
  premium_silent_browser accessories     24    1.5256    1.9398     21.4%
  hesitant_first_buyer   accessories     55    1.5412    1.9259     20.0%
  size_specific_anxious  accessories     15    1.8195    2.2723     19.9%
  trend_chaser           shoes           11    1.6297    2.0259     19.6%
  paralyzed_wishlister   accessories     20    2.3066    2.8308     18.5%
  post_return_returner   accessories     28    1.7140    2.0918     18.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  easy_returns_promise        11.6      5.18    0.3095
  fit_reassurance             11.0      2.54    0.3486
  style_bridge                 8.9      2.80    0.2995
  return_explainer             8.3      2.97    0.2640
  expert_pick                  8.3      4.02    0.2958
  customers_chose              7.1      3.44    0.3528
  low_return_alts              6.6      3.06    0.3689
  value_breakdown              6.1      2.62    0.3108
  comparison_card              5.5      1.95    0.3099
  size_guide                   5.3      4.77    0.3366
  occasion_lookbook            4.6      4.20    0.2248
  material_deep_dive           4.2      3.99    0.2862
  brand_story                  4.1      3.33    0.2837
  price_drop_notify            3.9      3.18    0.2602
  price_history                3.1      4.35    0.2465
  recently_viewed              1.4      4.80    0.1385
  wishlist_save                0.0      3.60    0.1924
  outfit_completion            0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            style_bridge(105), occasion_lookbook(105), brand_story(95), fit_reassurance(86), price_drop_notify(68)
  paralyzed_wishlister    expert_pick(172), customers_chose(154), fit_reassurance(149), comparison_card(124), style_bridge(124)
  hesitant_first_buyer    fit_reassurance(336), low_return_alts(331), easy_returns_promise(302), value_breakdown(287), size_guide(218)
  size_specific_anxious   fit_reassurance(114), low_return_alts(114), easy_returns_promise(112), customers_chose(92), expert_pick(89)
  premium_silent_browser  easy_returns_promise(177), return_explainer(176), expert_pick(166), material_deep_dive(155), fit_reassurance(138)
  returner_from_recent_order  fit_reassurance(121), easy_returns_promise(118), style_bridge(97), customers_chose(96), return_explainer(76)
  post_return_returner    fit_reassurance(198), easy_returns_promise(198), low_return_alts(196), size_guide(183), customers_chose(163)
  outfit_event_planner    style_bridge(212), customers_chose(190), occasion_lookbook(184), brand_story(180), return_explainer(140)
  corporate_uniform_buyer  fit_reassurance(81), size_guide(81), easy_returns_promise(81), expert_pick(68), return_explainer(53)
  birthday_rush_gifter    fit_reassurance(149), style_bridge(149), customers_chose(117), low_return_alts(115), easy_returns_promise(114)
  mobile_evening_browser  style_bridge(190), occasion_lookbook(189), brand_story(129), return_explainer(97), fit_reassurance(94)
  tabbed_comparison_shopper  return_explainer(240), expert_pick(240), comparison_card(227), price_history(216), price_drop_notify(197)
  bargain_hunter_returning  price_history(206), expert_pick(204), comparison_card(173), return_explainer(153), value_breakdown(131)
  confident_repeat_buyer  easy_returns_promise(176), recently_viewed(142), return_explainer(136), occasion_lookbook(132), style_bridge(118)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1])
  - session 2500: 16 edits (round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2])
  - session 5000: 16 edits (round 5000 draw1 — revive dead widgets (size_guide, occasion_lookbook, personal_recs, trending_now), tame over-firing low-reward widgets, boost confident_repeat/trend_chaser cells, add F32->F46 and F43->F33 synergies  [ensemble-best of 3: draw 1])
  - session 7500: 14 edits (round 7500 draw1 — stabilization: revive truly dead widgets (return_explainer/wishlist_save/price_drop_notify), trim over-firing low r/fire (occasion_lookbook, personal_recs), patch worst cells (confident_repeat shoes/bottoms, size_specific accessories, premium shoes)  [ensemble-best of 3: draw 1])
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `ensemble_state_llm/edits_round_10000_draw3.json` with this exact shape:

```json
{
  "note": "round X — short one-line rationale for the batch",
  "edits": [
    {"widget": "return_explainer", "path": "base", "from": 0.05, "to": 0.15, "reason": "F46 underserved, 0%% activation on returner_anxious"},
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
