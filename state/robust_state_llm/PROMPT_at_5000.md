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
    "base": 0.1,
    "on_rem": {
      "F32": 2.2,
      "F46": 0.6
    },
    "on_cov": {
      "F32": -1.2,
      "F46": 0.6040394065866245
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.3335393849944239,
    "on_rem": {
      "F32": 2.0
    },
    "on_cov": {
      "F32": -0.8138953737893677
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
      "F46": 1.8
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
    "base": 0.05,
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
    "base": 0.06457928469422505,
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
    "base": 0.30118487128808386,
    "on_rem": {
      "F46": 2.0
    },
    "on_cov": {
      "F46": -1.3,
      "F32": 0.8280331011336839
    },
    "slot_decay": 0.07,
    "type": "returns"
  },
  "easy_returns_promise": {
    "addr": {
      "F46": 0.3
    },
    "base": 0.4143945684741216,
    "on_rem": {
      "F46": 1.2
    },
    "on_cov": {
      "F46": -0.5
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
    "base": 0.5203588373393963,
    "on_rem": {
      "F33": 2.1585841206161436
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
    "base": -0.18447297241472121,
    "on_rem": {
      "F51": 1.718241074193289
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
    "base": 0.2767884627366793,
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
    "base": 0.2996295085294791,
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
    "base": 0.057702547604866566,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.0795128077907968,
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
    "base": 0.378904257369575,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas

# Latest report

```
# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.8661
- mean oracle reward: 2.0086
- mean regret:        0.1425  (7.1% of oracle)
- cum regret (batch): 356.26

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             100    1.7799    2.2730     21.7%
  premium_silent_browser   170    1.8784    2.1275     11.7%
  corporate_uniform_buyer   103    1.3183    1.4909     11.6%
  size_specific_anxious     92    2.5988    2.8781      9.7%
  hesitant_first_buyer     308    2.4021    2.6315      8.7%
  returner_from_recent_order   122    2.1989    2.3806      7.6%
  post_return_returner     181    2.5758    2.7693      7.0%
  paralyzed_wishlister     194    2.6702    2.8447      6.1%
  birthday_rush_gifter     198    2.3471    2.4771      5.2%
  mobile_evening_browser   161    1.0464    1.0968      4.6%
  outfit_event_planner     182    1.8194    1.8996      4.2%
  tabbed_comparison_shopper   265    1.8052    1.8331      1.5%
  bargain_hunter_returning   220    1.1572    1.1720      1.3%
  confident_repeat_buyer   204    0.5070    0.5089      0.4%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  outerwear        248    2.1865    2.3830      8.2%
  shoes            379    2.0442    2.2267      8.2%
  bottoms          507    1.8935    2.0448      7.4%
  dress            437    1.9004    2.0413      6.9%
  accessories      374    1.6468    1.7635      6.6%
  top              555    1.6972    1.7989      5.7%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             18    1.5588    2.2468     30.6%
  trend_chaser           accessories     14    2.2145    2.8803     23.1%
  trend_chaser           dress           21    2.0410    2.5686     20.5%
  trend_chaser           outerwear       10    1.9016    2.3901     20.4%
  premium_silent_browser outerwear       14    2.1811    2.6939     19.0%
  premium_silent_browser accessories     29    1.5747    1.9398     18.8%
  corporate_uniform_buyer bottoms         19    1.4131    1.7247     18.1%
  trend_chaser           bottoms         21    1.4204    1.7276     17.8%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.2      2.49    0.3384
  material_deep_dive          14.0      2.28    0.3191
  fit_reassurance             13.8      3.76    0.3210
  outfit_completion           13.6      3.90    0.3170
  customers_chose             12.2      4.26    0.3461
  return_explainer             8.9      3.16    0.3605
  easy_returns_promise         5.7      4.10    0.2070
  personal_recs                5.5      5.38    0.2171
  value_breakdown              4.4      3.61    0.2764
  expert_pick                  2.8      3.91    0.2834
  similar_items                2.1      5.64    0.1325
  low_return_alts              2.0      1.36    0.3805
  price_drop_notify            0.5      4.56    0.3648
  also_bought                  0.2      6.00    0.0846
  style_bridge                 0.1      1.00    0.2883
  size_guide                   0.1      2.92    0.2262
  occasion_lookbook            0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            material_deep_dive(100), outfit_completion(99), fit_reassurance(89), expert_pick(60), personal_recs(59)
  premium_silent_browser  fit_reassurance(158), material_deep_dive(157), return_explainer(155), comparison_card(145), customers_chose(112)
  corporate_uniform_buyer  comparison_card(103), return_explainer(97), fit_reassurance(97), personal_recs(97), material_deep_dive(73)
  size_specific_anxious   comparison_card(92), material_deep_dive(91), customers_chose(90), fit_reassurance(86), return_explainer(78)
  hesitant_first_buyer    comparison_card(308), outfit_completion(308), fit_reassurance(296), return_explainer(296), material_deep_dive(282)
  returner_from_recent_order  material_deep_dive(122), outfit_completion(122), comparison_card(122), customers_chose(122), fit_reassurance(100)
  post_return_returner    comparison_card(181), customers_chose(181), fit_reassurance(179), material_deep_dive(178), outfit_completion(139)
  paralyzed_wishlister    comparison_card(194), outfit_completion(184), customers_chose(183), material_deep_dive(172), fit_reassurance(156)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), customers_chose(198), material_deep_dive(198), fit_reassurance(159)
  mobile_evening_browser  outfit_completion(161), material_deep_dive(160), easy_returns_promise(152), personal_recs(148), fit_reassurance(120)
  outfit_event_planner    material_deep_dive(182), comparison_card(182), outfit_completion(182), customers_chose(182), fit_reassurance(138)
  tabbed_comparison_shopper  comparison_card(265), customers_chose(261), value_breakdown(248), return_explainer(237), fit_reassurance(233)
  bargain_hunter_returning  comparison_card(220), easy_returns_promise(213), outfit_completion(210), customers_chose(209), value_breakdown(204)
  confident_repeat_buyer  material_deep_dive(204), easy_returns_promise(203), fit_reassurance(202), personal_recs(190), similar_items(177)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `robust_state_llm/edits_round_5000.json` with this exact shape:

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
