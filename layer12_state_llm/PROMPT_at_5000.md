You are an EDP evolution agent. You can edit BOTH layers of the EDP policy.

# Architecture (recap)

EDP composes a 6-slot page by greedy submodular selection over 22 widgets.
Two layers process each session:

**Layer 1 — PWL problem detection.** 14 raw signals → 7-d problem
fingerprint. Each problem `F` is a weighted average of piecewise-linear
shape functions over its relevant signals:

  problem_F = sum_sig (weight_F_sig · pwl(feat_sig, bps, vals)) / sum_weight

You can edit:
- `weight` (the signal's contribution weight to the problem)
- `vals.<i>` (i-th breakpoint value, in [0, 1])
- `bps.<i>` (i-th breakpoint position, must stay monotonic in [0, 1])

You may NOT delete signals or add new ones.

**Layer 2 — module GAM + greedy composition.** Per-widget score:

  score(widget, slot) = base
                      + sum_p on_rem[p] * remaining[p]
                      + sum_p on_cov[p] * coverage[p]
                      - slot_decay * slot

You can edit `base`, `slot_decay`, `on_rem.<problem>`, `on_cov.<problem>`.
You may NOT change `addr` (a fixed content property).

# Reference data

Problems: F32 Size Anxiety, F33 Quality Signal Deficit, F41 Comparison
Friction, F43 Outfit Visualization, F45 Price-Quality Confusion,
F46 Return Hesitation, F51 Decision Paralysis.

Persona base-need vectors:
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

Fashion-category need multipliers (each session is a (persona, category)
pair; effective need = persona_need * category_multiplier):
- dress: N5_styling×1.30, N2_visual×1.10, N1_fit×1.00
- top: N3_peer×1.20, N4_compare×1.00, N5_styling×1.00
- bottoms: N1_fit×1.30, N4_compare×1.20, N6_trust×1.00
- shoes: N1_fit×1.40, N6_trust×1.30, N3_peer×1.00
- outerwear: N2_visual×1.30, N6_trust×1.20, N1_fit×1.10
- accessories: N2_visual×1.30, N5_styling×1.30, N3_peer×1.10

Widget true provisions (use as priors):
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

# Current Layer-1 PWL shapes (editable)

```json
{
  "F32": {
    "size_chart": {
      "bps": [
        0,
        0.2,
        0.5,
        0.8,
        1
      ],
      "vals": [
        0,
        0.1,
        0.45,
        0.75,
        0.95
      ],
      "weight": 0.45
    },
    "size_conf_inv": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0.95,
        0.6,
        0.25,
        0.05
      ],
      "weight": 0.3
    },
    "return_hist": {
      "bps": [
        0,
        0.2,
        0.5,
        1
      ],
      "vals": [
        0,
        0.1,
        0.4,
        0.7
      ],
      "weight": 0.25
    }
  },
  "F33": {
    "zoom": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.15,
        0.6,
        0.95
      ],
      "weight": 0.55
    },
    "price_norm": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.2,
        0.5,
        0.8
      ],
      "weight": 0.45
    }
  },
  "F41": {
    "tab_switch": {
      "bps": [
        0,
        0.2,
        0.5,
        0.8,
        1
      ],
      "vals": [
        0,
        0.1,
        0.5,
        0.85,
        0.95
      ],
      "weight": 0.55
    },
    "revisit": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.2,
        0.55,
        0.8
      ],
      "weight": 0.25
    },
    "price_dwell": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.1,
        0.35,
        0.55
      ],
      "weight": 0.2
    }
  },
  "F43": {
    "style_stretch": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.2,
        0.6,
        0.95
      ],
      "weight": 0.65
    },
    "mobile": {
      "bps": [
        0,
        0.5,
        1
      ],
      "vals": [
        0,
        0.3,
        0.55
      ],
      "weight": 0.35
    }
  },
  "F45": {
    "price_dwell": {
      "bps": [
        0,
        0.3,
        0.6,
        0.9,
        1
      ],
      "vals": [
        0,
        0.15,
        0.5,
        0.8,
        0.95
      ],
      "weight": 0.5
    },
    "price_sens": {
      "bps": [
        0,
        0.4,
        0.7,
        1
      ],
      "vals": [
        0,
        0.2,
        0.55,
        0.85
      ],
      "weight": 0.5
    }
  },
  "F46": {
    "return_view": {
      "bps": [
        0,
        0.2,
        0.5,
        1
      ],
      "vals": [
        0,
        0.15,
        0.7,
        0.9
      ],
      "weight": 0.55
    },
    "return_hist": {
      "bps": [
        0,
        0.2,
        0.5,
        1
      ],
      "vals": [
        0,
        0.15,
        0.5,
        0.8
      ],
      "weight": 0.45
    }
  },
  "F51": {
    "cart_osc": {
      "bps": [
        0,
        0.2,
        0.5,
        1
      ],
      "vals": [
        0,
        0.15,
        0.55,
        0.9
      ],
      "weight": 0.45
    },
    "wishlist": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.1,
        0.4,
        0.7
      ],
      "weight": 0.3
    },
    "revisit": {
      "bps": [
        0,
        0.3,
        0.6,
        1
      ],
      "vals": [
        0,
        0.1,
        0.4,
        0.65
      ],
      "weight": 0.25
    }
  }
}
```

# Current Layer-2 modules (editable)

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
      "F32": -1.2
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.18,
    "on_rem": {
      "F32": 2.0
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
    "base": 0.2,
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
    "base": 0.22,
    "on_rem": {
      "F46": 2.0
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
    "base": 0.2,
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
    "base": 0.18,
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
    "base": 0.18,
    "on_rem": {
      "F51": 1.7
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
    "base": 0.18,
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
    "base": 0.45,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.06,
    "type": "default"
  },
  "also_bought": {
    "addr": {
      "F41": 0.1,
      "F51": 0.1
    },
    "base": 0.4,
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

  - session 2500: 14 edits (11 module + 3 shape) — round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser

# Latest checkpoint report

```
# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7292
- mean oracle reward: 2.0086
- mean regret:        0.2794  (13.9% of oracle)
- cum regret (batch): 698.57

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   204    0.3718    0.5089     26.9%
  corporate_uniform_buyer   103    1.1122    1.4909     25.4%
  premium_silent_browser   170    1.6232    2.1275     23.7%
  returner_from_recent_order   122    1.8506    2.3806     22.3%
  hesitant_first_buyer     308    2.0750    2.6315     21.1%
  birthday_rush_gifter     198    2.0375    2.4771     17.7%
  trend_chaser             100    1.8907    2.2730     16.8%
  size_specific_anxious     92    2.4620    2.8781     14.5%
  outfit_event_planner     182    1.6847    1.8996     11.3%
  post_return_returner     181    2.4997    2.7693      9.7%
  mobile_evening_browser   161    1.0194    1.0968      7.1%
  bargain_hunter_returning   220    1.1200    1.1720      4.4%
  paralyzed_wishlister     194    2.7426    2.8447      3.6%
  tabbed_comparison_shopper   265    1.7778    1.8331      3.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8398    2.2267     17.4%
  outerwear        248    1.9770    2.3830     17.0%
  bottoms          507    1.7355    2.0448     15.1%
  dress            437    1.7621    2.0413     13.7%
  accessories      374    1.5688    1.7635     11.0%
  top              555    1.6194    1.7989     10.0%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer bottoms         39    0.2978    0.4645     35.9%
  corporate_uniform_buyer shoes           13    1.3518    2.0604     34.4%
  confident_repeat_buyer shoes           28    0.4596    0.6914     33.5%
  corporate_uniform_buyer outerwear        9    1.3180    1.9353     31.9%
  premium_silent_browser outerwear       14    1.8756    2.6939     30.4%
  corporate_uniform_buyer bottoms         19    1.2016    1.7247     30.3%
  confident_repeat_buyer outerwear       16    0.4822    0.6885     30.0%
  returner_from_recent_order shoes           17    2.0218    2.8524     29.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           13.9      3.35    0.2880
  comparison_card             13.8      2.01    0.3180
  also_bought                 13.3      5.10    0.2582
  customers_chose             10.9      3.76    0.3185
  brand_story                  9.7      3.59    0.3292
  fit_reassurance              7.5      3.17    0.3237
  value_breakdown              5.7      3.14    0.2505
  return_explainer             5.2      3.27    0.3057
  similar_items                5.1      4.67    0.1752
  low_return_alts              4.5      1.77    0.3566
  wishlist_save                4.3      3.64    0.3097
  personal_recs                2.0      5.59    0.1147
  easy_returns_promise         1.3      5.76    0.2292
  material_deep_dive           1.3      1.73    0.0930
  expert_pick                  0.5      2.45    0.3521
  trending_now                 0.3      5.76    0.0670
  price_drop_notify            0.2      3.67    0.3366
  style_bridge                 0.2      1.00    0.3284
  size_guide                   0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  also_bought(204), similar_items(203), outfit_completion(180), personal_recs(168), material_deep_dive(137)
  corporate_uniform_buyer  comparison_card(103), also_bought(103), fit_reassurance(72), brand_story(71), similar_items(58)
  premium_silent_browser  comparison_card(169), return_explainer(150), also_bought(128), outfit_completion(127), brand_story(120)
  returner_from_recent_order  comparison_card(122), outfit_completion(121), brand_story(118), customers_chose(112), low_return_alts(103)
  hesitant_first_buyer    comparison_card(308), outfit_completion(308), also_bought(305), fit_reassurance(256), brand_story(208)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), customers_chose(197), brand_story(171), also_bought(153)
  trend_chaser            outfit_completion(100), also_bought(95), brand_story(94), fit_reassurance(76), wishlist_save(57)
  size_specific_anxious   comparison_card(91), brand_story(82), customers_chose(74), fit_reassurance(72), low_return_alts(70)
  outfit_event_planner    brand_story(182), comparison_card(182), outfit_completion(182), customers_chose(180), also_bought(174)
  post_return_returner    comparison_card(181), customers_chose(171), low_return_alts(165), fit_reassurance(159), brand_story(157)
  mobile_evening_browser  outfit_completion(161), also_bought(161), similar_items(160), personal_recs(117), fit_reassurance(108)
  bargain_hunter_returning  comparison_card(220), also_bought(217), outfit_completion(213), customers_chose(211), value_breakdown(211)
  paralyzed_wishlister    comparison_card(194), outfit_completion(194), customers_chose(193), brand_story(163), wishlist_save(142)
  tabbed_comparison_shopper  comparison_card(265), return_explainer(265), customers_chose(261), value_breakdown(258), also_bought(227)

## Edit history applied so far
  - session 2500: 14 edits (round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser)
```

# Your task

Propose two batches of atomic edits in ONE JSON file. Both batches are
optional — you can emit only Layer-2 edits if Layer-1 looks fine, or
only Layer-1 edits if the issue is mis-detection rather than mis-routing.

Layer-1 edits are appropriate when the report shows a persona with high
regret AND the persona's true needs (above) include dimensions that
should map to a problem the current PWL is under-detecting. Examples:

- A persona who heavily uses size_chart but isn't getting size-relevant
  widgets → maybe F32's `size_chart.weight` is too low or `vals` rises
  too slowly.
- A premium-product session not getting quality content → maybe F33's
  `zoom.vals` saturates too low.
- An indecisive persona not getting decision-support → maybe F51's
  `cart_osc.vals` needs a steeper curve.

Layer-2 edits are appropriate for: dead widgets, over-firing defaults,
synergy chains, slot-decay tuning. (See prior agent guidance.)

Aim for 8–14 total edits across both layers. Heuristic: 70/30 split with
Layer-2 carrying most of the batch unless you specifically diagnose a
Layer-1 mis-detection.

# Output format

Write a JSON file at `layer12_state_llm/edits_round_5000.json` with this shape:

```json
{
  "note": "round X — short one-line rationale",
  "edits": [
    {"widget": "return_explainer", "path": "base", "from": 0.05, "to": 0.15, "reason": "..."},
    {"widget": "easy_returns_promise", "path": "on_cov.F46", "from": 0.0, "to": 1.0, "reason": "..."}
  ],
  "shape_edits": [
    {"problem": "F32", "signal": "size_chart", "path": "weight", "from": 0.45, "to": 0.55, "reason": "size_anxious_new under-detected"},
    {"problem": "F32", "signal": "size_chart", "path": "vals.2", "from": 0.45, "to": 0.55, "reason": "steeper rise at mid-range"}
  ]
}
```

Constraints:
- ONLY write that one JSON file.
- Layer-2 paths: `base`, `slot_decay`, `on_rem.<F-code>`, `on_cov.<F-code>`. Range -1.5 to 2.8.
- Layer-1 paths: `weight` (≥ 0, typical 0.1-0.7), `vals.<i>` (∈ [0, 1]), `bps.<i>` (∈ [0, 1], monotonic).
- One-sentence `reason` on each edit.
- Final message in chat (under 80 words): which Layer-1 mis-detection (if any) you targeted, plus your top-3 most-impactful Layer-2 edits.
