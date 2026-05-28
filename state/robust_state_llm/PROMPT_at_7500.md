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
    "base": 0.7598593846733062,
    "on_rem": {
      "F32": 2.298427861819732
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
    "base": 0.4719107037322973,
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
    "base": 0.19862349735531015,
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
    "base": 0.5339840661116153,
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
    "base": 0.5203588373393963,
    "on_rem": {
      "F33": 2.1585841206161436
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
    "base": 0.5443110406560565,
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
    "base": 0.380687119293019,
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

# Latest report

```
# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7476
- mean oracle reward: 1.9777
- mean regret:        0.2301  (11.6% of oracle)
- cum regret (batch): 575.37

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             115    1.8281    2.3063     20.7%
  size_specific_anxious    120    2.2831    2.8673     20.4%
  hesitant_first_buyer     287    2.1527    2.6232     17.9%
  premium_silent_browser   143    1.7650    2.1175     16.6%
  returner_from_recent_order   108    2.0612    2.4577     16.1%
  post_return_returner     179    2.3420    2.7828     15.8%
  corporate_uniform_buyer   126    1.2309    1.4520     15.2%
  birthday_rush_gifter     142    2.2660    2.4712      8.3%
  paralyzed_wishlister     198    2.6165    2.8462      8.1%
  outfit_event_planner     192    1.7620    1.9051      7.5%
  mobile_evening_browser   187    1.0505    1.0869      3.3%
  bargain_hunter_returning   225    1.1718    1.1877      1.3%
  tabbed_comparison_shopper   262    1.7871    1.7976      0.6%
  confident_repeat_buyer   216    0.5144    0.5145      0.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.8765    2.1880     14.2%
  bottoms          507    1.7766    2.0195     12.0%
  outerwear        231    2.0618    2.3378     11.8%
  top              538    1.5965    1.7978     11.2%
  dress            450    1.7923    2.0100     10.8%
  accessories      407    1.5670    1.7337      9.6%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  premium_silent_browser accessories     23    1.3795    1.9398     28.9%
  trend_chaser           accessories     21    2.1522    2.8803     25.3%
  size_specific_anxious  top             28    2.1180    2.8185     24.9%
  hesitant_first_buyer   shoes           48    2.3075    3.0647     24.7%
  trend_chaser           top             30    1.6929    2.2468     24.7%
  corporate_uniform_buyer bottoms         15    1.3247    1.7247     23.2%
  returner_from_recent_order shoes           19    2.2103    2.8524     22.5%
  corporate_uniform_buyer shoes           19    1.6154    2.0604     21.6%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  brand_story                 16.5      2.80    0.2918
  size_guide                  16.2      2.78    0.2920
  return_explainer            16.1      3.22    0.2948
  comparison_card             13.2      2.94    0.3228
  occasion_lookbook            7.9      5.13    0.2898
  price_history                7.7      4.25    0.2383
  customers_chose              6.2      4.63    0.3046
  wishlist_save                5.5      4.23    0.3274
  style_bridge                 5.3      2.51    0.2989
  trending_now                 4.6      5.59    0.2002
  fit_reassurance              0.4      6.00    0.4296
  value_breakdown              0.1      1.06    0.1997
  personal_recs                0.1      6.00    0.0812
  low_return_alts              0.0      1.00    0.3108
  material_deep_dive           0.0      5.50    0.3204
  expert_pick                  0.0      5.00    0.3073
  outfit_completion            0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            brand_story(115), style_bridge(115), size_guide(115), return_explainer(115), occasion_lookbook(76)
  size_specific_anxious   size_guide(120), return_explainer(120), brand_story(120), comparison_card(115), occasion_lookbook(91)
  hesitant_first_buyer    size_guide(287), return_explainer(287), comparison_card(287), brand_story(287), occasion_lookbook(209)
  premium_silent_browser  return_explainer(143), brand_story(142), size_guide(141), comparison_card(129), wishlist_save(109)
  returner_from_recent_order  brand_story(108), return_explainer(105), size_guide(104), comparison_card(104), occasion_lookbook(58)
  post_return_returner    size_guide(179), return_explainer(179), brand_story(179), comparison_card(173), occasion_lookbook(137)
  corporate_uniform_buyer  size_guide(126), return_explainer(126), brand_story(126), comparison_card(121), trending_now(104)
  birthday_rush_gifter    size_guide(142), return_explainer(142), brand_story(142), comparison_card(142), style_bridge(110)
  paralyzed_wishlister    comparison_card(198), wishlist_save(198), size_guide(198), return_explainer(198), brand_story(196)
  outfit_event_planner    style_bridge(192), size_guide(192), brand_story(192), return_explainer(192), comparison_card(192)
  mobile_evening_browser  size_guide(187), return_explainer(187), brand_story(187), style_bridge(185), trending_now(137)
  bargain_hunter_returning  comparison_card(225), price_history(210), brand_story(210), size_guide(204), customers_chose(187)
  tabbed_comparison_shopper  comparison_card(262), return_explainer(262), brand_story(262), price_history(260), size_guide(225)
  confident_repeat_buyer  brand_story(216), size_guide(216), return_explainer(216), trending_now(216), occasion_lookbook(213)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas)
  - session 5000: 16 edits (round 5000 — revive trend/visual widgets for trend_chaser & premium personas, lift size_guide for bottoms/shoes fit, dampen over-firing low-r defaults; robust to noise)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `robust_state_llm/edits_round_7500.json` with this exact shape:

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
