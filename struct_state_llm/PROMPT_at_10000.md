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
- virtual_try_on: N1_fit=0.65, N2_visual=0.45, N6_trust=0.20

# Current modules config

```json
{
  "fit_reassurance": {
    "addr": {
      "F32": 0.55,
      "F46": 0.2
    },
    "base": 0.95,
    "on_rem": {
      "F32": 2.7,
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
    "base": 0.85,
    "on_rem": {
      "F32": 2.7
    },
    "on_cov": {
      "F32": -1.6
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
      "F46": -1.0,
      "F32": 0.5
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
    "base": 0.55,
    "on_rem": {
      "F41": 1.6,
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
    "base": 0.75,
    "on_rem": {
      "F43": 2.0
    },
    "on_cov": {
      "F43": 0.4
    },
    "slot_decay": 0.06,
    "type": "outfit"
  },
  "occasion_lookbook": {
    "addr": {
      "F43": 0.3
    },
    "base": 0.05,
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
      "F32": 1.2
    },
    "slot_decay": 0.07,
    "type": "returns"
  },
  "easy_returns_promise": {
    "addr": {
      "F46": 0.3
    },
    "base": 0.1,
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
    "base": 0.1,
    "on_rem": {
      "F33": 1.9
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
    "base": 0.05,
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
    "base": 0.2,
    "on_rem": {
      "F51": 2.2,
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
    "base": 0.45,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.18,
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
    "base": 0.45,
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
  },
  "virtual_try_on": {
    "addr": {
      "F32": 0.45,
      "F46": 0.2,
      "F33": 0.15
    },
    "base": 0.2,
    "on_rem": {
      "F32": 2.4,
      "F46": 1.4,
      "F33": 0.4,
      "F43": 0.3
    },
    "on_cov": {
      "F32": -1.1,
      "F46": 0.6
    },
    "slot_decay": 0.04,
    "type": "premium-fit"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer
  - session 5000: 13 edits — round 5000 — activate virtual_try_on for high-N1_fit personas on shoes/outerwear without crowding fit_reassurance/size_guide
  - session 7500: 13 edits — round 7500 — tame virtual_try_on over-fire, revive fit_reassurance/size_guide/style_bridge for size_anxious & trend_chaser, boost peer widgets for trend_chaser

# Latest report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8688
- mean oracle reward: 2.0241
- mean regret:        0.1554  (7.7% of oracle)
- cum regret (batch): 388.42

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  paralyzed_wishlister     172    2.4422    2.8561     14.5%
  trend_chaser             105    2.0467    2.3309     12.2%
  size_specific_anxious    114    2.5801    2.8997     11.0%
  outfit_event_planner     212    1.7300    1.9150      9.7%
  bargain_hunter_returning   223    1.0696    1.1832      9.6%
  returner_from_recent_order   121    2.1861    2.4116      9.4%
  post_return_returner     198    2.5527    2.8038      9.0%
  tabbed_comparison_shopper   240    1.6736    1.8258      8.3%
  corporate_uniform_buyer    81    1.3546    1.4618      7.3%
  hesitant_first_buyer     336    2.4770    2.6077      5.0%
  premium_silent_browser   177    2.0135    2.1053      4.4%
  birthday_rush_gifter     149    2.4548    2.4820      1.1%
  mobile_evening_browser   190    1.0955    1.0955      0.0%
  confident_repeat_buyer   182    0.5144    0.5144      0.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  bottoms          495    1.8909    2.0990      9.9%
  outerwear        242    2.1460    2.3272      7.8%
  accessories      362    1.5997    1.7287      7.5%
  shoes            385    2.1082    2.2700      7.1%
  top              575    1.6576    1.7841      7.1%
  dress            441    1.9789    2.1146      6.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  paralyzed_wishlister   bottoms         40    2.2989    2.9255     21.4%
  trend_chaser           accessories     17    2.3201    2.8783     19.4%
  paralyzed_wishlister   outerwear       15    2.6828    3.1770     15.6%
  returner_from_recent_order bottoms         27    2.2157    2.6170     15.3%
  bargain_hunter_returning outerwear       20    1.2135    1.4171     14.4%
  corporate_uniform_buyer bottoms         15    1.4797    1.7247     14.2%
  bargain_hunter_returning bottoms         45    1.2369    1.4325     13.7%
  size_specific_anxious  top             23    2.4306    2.8041     13.3%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  fit_reassurance             16.6      1.80    0.3112
  return_explainer            16.5      3.84    0.3116
  customers_chose             16.4      2.93    0.3106
  style_bridge                15.9      3.24    0.3094
  material_deep_dive          12.8      4.20    0.3252
  easy_returns_promise        12.6      5.76    0.2983
  value_breakdown              4.3      2.78    0.2738
  comparison_card              3.4      3.42    0.3335
  expert_pick                  0.8      5.54    0.3988
  virtual_try_on               0.5      4.22    0.4190
  brand_story                  0.2      2.65    0.3100
  size_guide                   0.0      0.00    0.0000
  low_return_alts              0.0      0.00    0.0000
  outfit_completion            0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  paralyzed_wishlister    customers_chose(172), fit_reassurance(172), style_bridge(172), return_explainer(164), expert_pick(112)
  trend_chaser            style_bridge(105), fit_reassurance(105), material_deep_dive(105), return_explainer(105), customers_chose(105)
  size_specific_anxious   fit_reassurance(114), customers_chose(114), return_explainer(114), easy_returns_promise(114), material_deep_dive(113)
  outfit_event_planner    style_bridge(212), customers_chose(212), fit_reassurance(212), return_explainer(212), easy_returns_promise(212)
  bargain_hunter_returning  customers_chose(223), value_breakdown(223), fit_reassurance(223), style_bridge(223), return_explainer(209)
  returner_from_recent_order  return_explainer(121), customers_chose(121), style_bridge(121), material_deep_dive(121), fit_reassurance(108)
  post_return_returner    fit_reassurance(198), return_explainer(198), material_deep_dive(198), customers_chose(198), easy_returns_promise(198)
  tabbed_comparison_shopper  customers_chose(240), value_breakdown(240), fit_reassurance(240), return_explainer(240), style_bridge(179)
  corporate_uniform_buyer  fit_reassurance(81), return_explainer(81), material_deep_dive(81), customers_chose(81), style_bridge(81)
  hesitant_first_buyer    fit_reassurance(336), return_explainer(336), style_bridge(336), material_deep_dive(335), customers_chose(299)
  premium_silent_browser  fit_reassurance(177), customers_chose(177), return_explainer(177), style_bridge(176), material_deep_dive(167)
  birthday_rush_gifter    fit_reassurance(149), customers_chose(149), return_explainer(149), material_deep_dive(149), style_bridge(149)
  mobile_evening_browser  style_bridge(190), fit_reassurance(190), customers_chose(190), return_explainer(190), easy_returns_promise(190)
  confident_repeat_buyer  fit_reassurance(182), style_bridge(182), return_explainer(182), material_deep_dive(182), easy_returns_promise(182)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 13 edits (round 5000 — activate virtual_try_on for high-N1_fit personas on shoes/outerwear without crowding fit_reassurance/size_guide)
  - session 7500: 13 edits (round 7500 — tame virtual_try_on over-fire, revive fit_reassurance/size_guide/style_bridge for size_anxious & trend_chaser, boost peer widgets for trend_chaser)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `struct_state_llm/edits_round_10000.json` with this exact shape:

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
