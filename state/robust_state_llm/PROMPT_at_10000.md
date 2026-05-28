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
    "base": 0.4411388160655064,
    "on_rem": {
      "F32": 2.6047715125359114,
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
    "base": 0.7598593846733062,
    "on_rem": {
      "F32": 2.298427861819732
    },
    "on_cov": {
      "F32": -0.8138953737893677,
      "F46": 0.38091657949698354
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
      "F41": -1.3,
      "F51": 0.6439190236675489
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
    "base": 0.297779671664525,
    "on_rem": {
      "F43": 1.9089823622343673
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
    "base": 0.27758234561426265,
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
    "base": 0.1394099247427078,
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
      "F32": 0.8280331011336839,
      "F33": 0.3964018044039136
    },
    "slot_decay": 0.07,
    "type": "returns"
  },
  "easy_returns_promise": {
    "addr": {
      "F46": 0.3
    },
    "base": 0.2613464920680541,
    "on_rem": {
      "F46": 1.5110775634524811
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
    "base": 0.35263466014200745,
    "on_rem": {
      "F33": 2.4481434211628184
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
    "base": 0.6460647875512283,
    "on_rem": {
      "F33": 2.445047682376226
    },
    "on_cov": {
      "F33": -0.9,
      "F43": 0.0648235514623608
    },
    "slot_decay": 0.07,
    "type": "premium"
  },
  "price_history": {
    "addr": {
      "F45": 0.45
    },
    "base": 0.3947055606017039,
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
    "base": 0.22570058266924747,
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
    "base": 0.5118774612496566,
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
    "base": 0.22746724976108249,
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
    "base": -0.1496665048297091,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.2993468805800291,
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
    "base": 0.1268054313475613,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas
  - session 5000: 16 edits — round 5000 — revive trend/visual widgets for trend_chaser & premium personas, lift size_guide for bottoms/shoes fit, dampen over-firing low-r defaults; robust to noise
  - session 7500: 14 edits — round 7500 — stabilization: pull back overshoots on brand_story/style_bridge, revive silenced widgets (fit_reassurance, material_deep_dive, outfit_completion, easy_returns_promise) for high-regret cells

# Latest report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8549
- mean oracle reward: 2.0225
- mean regret:        0.1676  (8.3% of oracle)
- cum regret (batch): 419.08

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             105    1.7930    2.3312     23.1%
  size_specific_anxious    114    2.4905    2.9005     14.1%
  hesitant_first_buyer     336    2.3023    2.6004     11.5%
  premium_silent_browser   177    1.8739    2.1053     11.0%
  post_return_returner     198    2.5006    2.8039     10.8%
  paralyzed_wishlister     172    2.5680    2.8495      9.9%
  corporate_uniform_buyer    81    1.3512    1.4618      7.6%
  returner_from_recent_order   121    2.2397    2.4114      7.1%
  outfit_event_planner     212    1.8462    1.9123      3.5%
  tabbed_comparison_shopper   240    1.7717    1.8258      3.0%
  mobile_evening_browser   190    1.0810    1.0955      1.3%
  bargain_hunter_returning   223    1.1701    1.1832      1.1%
  birthday_rush_gifter     149    2.4563    2.4820      1.0%
  confident_repeat_buyer   182    0.5144    0.5144      0.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      362    1.5488    1.7287     10.4%
  top              575    1.6180    1.7847      9.3%
  dress            441    1.9422    2.1134      8.1%
  shoes            385    2.0910    2.2647      7.7%
  bottoms          495    1.9395    2.0960      7.5%
  outerwear        242    2.1678    2.3259      6.8%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             28    1.5846    2.2468     29.5%
  trend_chaser           accessories     17    2.1719    2.8803     24.6%
  trend_chaser           shoes           11    1.5836    2.0259     21.8%
  size_specific_anxious  accessories     15    1.7785    2.2723     21.7%
  trend_chaser           bottoms         16    1.3581    1.7276     21.4%
  premium_silent_browser accessories     24    1.5598    1.9398     19.6%
  size_specific_anxious  top             23    2.2726    2.8185     19.4%
  trend_chaser           dress           23    2.0881    2.5686     18.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  return_explainer            16.4      3.78    0.3088
  expert_pick                 15.0      4.33    0.3047
  comparison_card             14.1      3.08    0.3337
  material_deep_dive          14.1      2.25    0.3149
  outfit_completion           10.7      5.00    0.3152
  fit_reassurance              9.9      2.14    0.3713
  size_guide                   7.9      3.70    0.2482
  price_history                7.2      4.33    0.2508
  style_bridge                 3.3      1.51    0.2696
  customers_chose              1.3      5.93    0.3147
  value_breakdown              0.1      1.12    0.2002
  trending_now                 0.0      6.00    0.2175
  low_return_alts              0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            style_bridge(105), material_deep_dive(105), return_explainer(104), expert_pick(104), size_guide(81)
  size_specific_anxious   fit_reassurance(114), return_explainer(114), expert_pick(114), material_deep_dive(112), comparison_card(109)
  hesitant_first_buyer    fit_reassurance(336), comparison_card(336), return_explainer(336), material_deep_dive(336), outfit_completion(335)
  premium_silent_browser  return_explainer(177), expert_pick(177), material_deep_dive(175), comparison_card(174), outfit_completion(131)
  post_return_returner    fit_reassurance(198), return_explainer(198), expert_pick(196), material_deep_dive(185), comparison_card(183)
  paralyzed_wishlister    comparison_card(172), expert_pick(172), outfit_completion(163), fit_reassurance(151), return_explainer(149)
  corporate_uniform_buyer  material_deep_dive(81), return_explainer(81), expert_pick(81), comparison_card(81), outfit_completion(72)
  returner_from_recent_order  material_deep_dive(121), return_explainer(121), comparison_card(119), expert_pick(119), outfit_completion(113)
  outfit_event_planner    material_deep_dive(212), comparison_card(212), expert_pick(212), return_explainer(212), style_bridge(162)
  tabbed_comparison_shopper  comparison_card(240), return_explainer(239), price_history(238), expert_pick(237), fit_reassurance(175)
  mobile_evening_browser  size_guide(190), return_explainer(190), material_deep_dive(190), style_bridge(181), expert_pick(162)
  bargain_hunter_returning  comparison_card(223), expert_pick(223), size_guide(219), price_history(217), return_explainer(201)
  birthday_rush_gifter    return_explainer(149), expert_pick(149), comparison_card(149), material_deep_dive(147), fit_reassurance(138)
  confident_repeat_buyer  material_deep_dive(182), size_guide(182), return_explainer(182), expert_pick(182), outfit_completion(182)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas)
  - session 5000: 16 edits (round 5000 — revive trend/visual widgets for trend_chaser & premium personas, lift size_guide for bottoms/shoes fit, dampen over-firing low-r defaults; robust to noise)
  - session 7500: 14 edits (round 7500 — stabilization: pull back overshoots on brand_story/style_bridge, revive silenced widgets (fit_reassurance, material_deep_dive, outfit_completion, easy_returns_promise) for high-regret cells)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `robust_state_llm/edits_round_10000.json` with this exact shape:

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
