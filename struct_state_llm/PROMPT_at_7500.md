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
    "base": 0.35,
    "on_rem": {
      "F32": 2.2,
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
    "base": 0.35,
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
    "base": 0.32,
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
    "base": 0.35,
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
  },
  "virtual_try_on": {
    "addr": {
      "F32": 0.45,
      "F46": 0.2,
      "F33": 0.15
    },
    "base": 0.45,
    "on_rem": {
      "F32": 2.4,
      "F46": 1.4,
      "F33": 0.4,
      "F43": 1.2
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

# Latest report

```
# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7628
- mean oracle reward: 1.9790
- mean regret:        0.2162  (10.9% of oracle)
- cum regret (batch): 540.52

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             115    1.7680    2.3060     23.3%
  size_specific_anxious    120    2.2683    2.8656     20.8%
  hesitant_first_buyer     287    2.1521    2.6309     18.2%
  post_return_returner     179    2.2981    2.7828     17.4%
  returner_from_recent_order   108    2.1866    2.4587     11.1%
  paralyzed_wishlister     198    2.5855    2.8502      9.3%
  birthday_rush_gifter     142    2.2817    2.4712      7.7%
  outfit_event_planner     192    1.7628    1.9074      7.6%
  corporate_uniform_buyer   126    1.3484    1.4520      7.1%
  premium_silent_browser   143    2.0422    2.1175      3.6%
  tabbed_comparison_shopper   262    1.7431    1.7976      3.0%
  mobile_evening_browser   187    1.0617    1.0869      2.3%
  confident_repeat_buyer   216    0.5049    0.5145      1.9%
  bargain_hunter_returning   225    1.1811    1.1876      0.5%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  top              538    1.5698    1.7971     12.6%
  accessories      407    1.5260    1.7337     12.0%
  shoes            367    1.9523    2.1928     11.0%
  bottoms          507    1.8050    2.0220     10.7%
  dress            450    1.8131    2.0113      9.9%
  outerwear        231    2.1379    2.3383      8.6%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             30    1.5230    2.2468     32.2%
  size_specific_anxious  top             28    2.0878    2.8041     25.5%
  trend_chaser           shoes           15    1.5480    2.0259     23.6%
  trend_chaser           bottoms         21    1.3373    1.7276     22.6%
  size_specific_anxious  accessories     17    1.7818    2.2751     21.7%
  post_return_returner   top             45    2.1206    2.6843     21.0%
  trend_chaser           accessories     21    2.2774    2.8783     20.9%
  size_specific_anxious  shoes           15    2.5242    3.1786     20.6%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  virtual_try_on              16.7      1.51    0.2938
  return_explainer            16.3      3.33    0.2947
  easy_returns_promise        15.9      4.76    0.2948
  expert_pick                 13.6      3.37    0.2850
  comparison_card             13.4      3.06    0.3231
  material_deep_dive          10.1      4.94    0.2835
  outfit_completion            8.4      3.94    0.3068
  value_breakdown              3.5      4.06    0.2574
  customers_chose              1.0      5.35    0.3078
  occasion_lookbook            1.0      5.01    0.0833
  low_return_alts              0.1      2.00    0.4275
  brand_story                  0.0      1.00    0.3665
  fit_reassurance              0.0      0.00    0.0000
  size_guide                   0.0      0.00    0.0000
  style_bridge                 0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            virtual_try_on(115), outfit_completion(115), expert_pick(115), return_explainer(115), easy_returns_promise(115)
  size_specific_anxious   virtual_try_on(120), easy_returns_promise(120), expert_pick(119), return_explainer(117), comparison_card(117)
  hesitant_first_buyer    virtual_try_on(287), return_explainer(287), easy_returns_promise(287), comparison_card(282), material_deep_dive(270)
  post_return_returner    virtual_try_on(179), comparison_card(179), easy_returns_promise(179), material_deep_dive(176), return_explainer(171)
  returner_from_recent_order  virtual_try_on(108), return_explainer(108), comparison_card(108), easy_returns_promise(108), expert_pick(105)
  paralyzed_wishlister    expert_pick(198), comparison_card(198), virtual_try_on(198), return_explainer(198), easy_returns_promise(173)
  birthday_rush_gifter    virtual_try_on(142), return_explainer(142), easy_returns_promise(142), comparison_card(141), outfit_completion(140)
  outfit_event_planner    virtual_try_on(192), outfit_completion(192), return_explainer(192), expert_pick(191), comparison_card(188)
  corporate_uniform_buyer  virtual_try_on(126), return_explainer(126), easy_returns_promise(126), material_deep_dive(126), comparison_card(126)
  premium_silent_browser  virtual_try_on(143), return_explainer(143), easy_returns_promise(143), expert_pick(142), comparison_card(131)
  tabbed_comparison_shopper  comparison_card(262), virtual_try_on(262), expert_pick(262), return_explainer(262), easy_returns_promise(253)
  mobile_evening_browser  virtual_try_on(187), outfit_completion(187), return_explainer(187), easy_returns_promise(187), material_deep_dive(187)
  confident_repeat_buyer  virtual_try_on(216), return_explainer(216), easy_returns_promise(216), material_deep_dive(216), expert_pick(192)
  bargain_hunter_returning  comparison_card(225), virtual_try_on(225), expert_pick(223), value_breakdown(211), return_explainer(188)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 13 edits (round 5000 — activate virtual_try_on for high-N1_fit personas on shoes/outerwear without crowding fit_reassurance/size_guide)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `struct_state_llm/edits_round_7500.json` with this exact shape:

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
