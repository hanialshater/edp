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
    "base": 0.45,
    "on_rem": {
      "F32": 2.2,
      "F46": 0.6
    },
    "on_cov": {
      "F32": 0.3
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.45,
    "on_rem": {
      "F32": 2.7
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
    "base": 0.05,
    "on_rem": {
      "F32": 1.0,
      "F46": 2.4
    },
    "on_cov": {
      "F46": -1.0
    },
    "slot_decay": 0.03,
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
    "base": 0.3,
    "on_rem": {
      "F41": 0.8,
      "F51": 2.0
    },
    "on_cov": {
      "F41": 1.0,
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
    "base": 0.4,
    "on_rem": {
      "F45": 2.6,
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
    "base": 0.2,
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
    "base": 0.35,
    "on_rem": {
      "F43": 2.0
    },
    "on_cov": {
      "F43": 0.5
    },
    "slot_decay": 0.06,
    "type": "outfit"
  },
  "occasion_lookbook": {
    "addr": {
      "F43": 0.3
    },
    "base": 0.18,
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
    "base": 0.45,
    "on_rem": {
      "F46": 2.0
    },
    "on_cov": {
      "F46": -1.3,
      "F32": 0.9
    },
    "slot_decay": 0.07,
    "type": "returns"
  },
  "easy_returns_promise": {
    "addr": {
      "F46": 0.3
    },
    "base": 0.22,
    "on_rem": {
      "F46": 1.2
    },
    "on_cov": {
      "F46": 1.1
    },
    "slot_decay": 0.05,
    "type": "returns"
  },
  "brand_story": {
    "addr": {
      "F33": 0.5
    },
    "base": 0.25,
    "on_rem": {
      "F33": 1.9
    },
    "on_cov": {
      "F33": 0.4
    },
    "slot_decay": 0.05,
    "type": "premium"
  },
  "material_deep_dive": {
    "addr": {
      "F33": 0.45
    },
    "base": 0.25,
    "on_rem": {
      "F33": 1.7
    },
    "on_cov": {
      "F33": -0.9,
      "F46": 0.8
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
    "base": 0.3,
    "on_rem": {
      "F51": 1.3,
      "F45": 1.6
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
    "base": 0.55,
    "on_rem": {
      "F51": 2.3
    },
    "on_cov": {
      "F51": 0.4
    },
    "slot_decay": 0.06,
    "type": "action"
  },
  "expert_pick": {
    "addr": {
      "F51": 0.3,
      "F33": 0.15
    },
    "base": 0.4,
    "on_rem": {
      "F51": 2.2,
      "F33": 0.4
    },
    "on_cov": {
      "F51": -0.7,
      "F33": 0.5
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
    "base": 0.05,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.22,
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

  - session 2500: 16 edits — round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer
  - session 5000: 16 edits — round 5000 — activate still-dead widgets for trend_chaser/peer-social and size-anxious/fit cells; dial back round-1 over-corrections on material_deep_dive and easy_returns_promise
  - session 7500: 14 edits — round 7500 — STABILIZATION: revive wishlist_save/expert_pick/value_breakdown for paralyzed_wishlister & premium_silent_browser, dial back brand_story overshoot, trim still-firing defaults

# Latest report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8166
- mean oracle reward: 2.0225
- mean regret:        0.2059  (10.2% of oracle)
- cum regret (batch): 514.75

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             105    1.8903    2.3312     18.9%
  premium_silent_browser   177    1.7498    2.1053     16.9%
  returner_from_recent_order   121    2.0328    2.4114     15.7%
  corporate_uniform_buyer    81    1.2660    1.4618     13.4%
  size_specific_anxious    114    2.5480    2.9005     12.2%
  hesitant_first_buyer     336    2.3079    2.6004     11.2%
  outfit_event_planner     212    1.7166    1.9123     10.2%
  post_return_returner     198    2.5405    2.8039      9.4%
  paralyzed_wishlister     172    2.6037    2.8495      8.6%
  tabbed_comparison_shopper   240    1.6968    1.8258      7.1%
  mobile_evening_browser   190    1.0317    1.0955      5.8%
  bargain_hunter_returning   223    1.1317    1.1832      4.4%
  birthday_rush_gifter     149    2.3940    2.4820      3.5%
  confident_repeat_buyer   182    0.5044    0.5144      1.9%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      362    1.5146    1.7287     12.4%
  top              575    1.6014    1.7847     10.3%
  dress            441    1.8995    2.1134     10.1%
  bottoms          495    1.8854    2.0960     10.0%
  outerwear        242    2.1016    2.3259      9.6%
  shoes            385    2.0596    2.2647      9.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           accessories     17    2.1360    2.8803     25.8%
  trend_chaser           top             28    1.6925    2.2468     24.7%
  premium_silent_browser accessories     24    1.4854    1.9398     23.4%
  premium_silent_browser dress           27    1.8308    2.3417     21.8%
  returner_from_recent_order top             26    1.6553    2.0668     19.9%
  corporate_uniform_buyer bottoms         15    1.3823    1.7247     19.9%
  returner_from_recent_order bottoms         27    2.1275    2.6170     18.7%
  size_specific_anxious  top             23    2.3068    2.8185     18.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  wishlist_save               12.8      3.49    0.2806
  fit_reassurance             12.1      3.51    0.3014
  value_breakdown             11.6      2.08    0.2795
  easy_returns_promise        10.1      5.51    0.2939
  style_bridge                10.0      3.11    0.2899
  return_explainer             9.5      4.19    0.2816
  customers_chose              9.4      3.11    0.3343
  comparison_card              7.6      3.95    0.3168
  material_deep_dive           5.6      4.45    0.3467
  low_return_alts              4.4      1.70    0.3644
  brand_story                  3.1      3.46    0.2977
  expert_pick                  2.8      3.04    0.3071
  size_guide                   0.9      1.06    0.3769
  outfit_completion            0.1      5.76    0.3417
  price_drop_notify            0.0      1.00    0.3943
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            style_bridge(105), fit_reassurance(101), wishlist_save(87), brand_story(80), expert_pick(77)
  premium_silent_browser  value_breakdown(177), wishlist_save(166), expert_pick(159), easy_returns_promise(136), return_explainer(122)
  returner_from_recent_order  low_return_alts(121), wishlist_save(101), material_deep_dive(98), style_bridge(95), comparison_card(71)
  corporate_uniform_buyer  easy_returns_promise(81), wishlist_save(77), material_deep_dive(77), value_breakdown(55), low_return_alts(54)
  size_specific_anxious   fit_reassurance(114), wishlist_save(108), easy_returns_promise(104), material_deep_dive(102), customers_chose(84)
  hesitant_first_buyer    return_explainer(329), value_breakdown(317), comparison_card(289), fit_reassurance(269), customers_chose(243)
  outfit_event_planner    style_bridge(212), wishlist_save(198), customers_chose(189), fit_reassurance(189), brand_story(149)
  post_return_returner    fit_reassurance(196), easy_returns_promise(192), low_return_alts(185), wishlist_save(169), material_deep_dive(169)
  paralyzed_wishlister    customers_chose(171), wishlist_save(170), value_breakdown(168), style_bridge(164), fit_reassurance(108)
  tabbed_comparison_shopper  value_breakdown(240), customers_chose(240), wishlist_save(240), easy_returns_promise(238), return_explainer(191)
  mobile_evening_browser  style_bridge(190), wishlist_save(190), fit_reassurance(190), return_explainer(188), easy_returns_promise(176)
  bargain_hunter_returning  value_breakdown(223), customers_chose(223), wishlist_save(223), fit_reassurance(217), style_bridge(181)
  birthday_rush_gifter    style_bridge(146), material_deep_dive(141), fit_reassurance(117), return_explainer(113), easy_returns_promise(107)
  confident_repeat_buyer  fit_reassurance(181), return_explainer(172), value_breakdown(166), wishlist_save(164), easy_returns_promise(160)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 16 edits (round 5000 — activate still-dead widgets for trend_chaser/peer-social and size-anxious/fit cells; dial back round-1 over-corrections on material_deep_dive and easy_returns_promise)
  - session 7500: 14 edits (round 7500 — STABILIZATION: revive wishlist_save/expert_pick/value_breakdown for paralyzed_wishlister & premium_silent_browser, dial back brand_story overshoot, trim still-firing defaults)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm/edits_round_10000.json` with this exact shape:

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
