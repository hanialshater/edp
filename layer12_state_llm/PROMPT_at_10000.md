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
        0.25,
        0.45,
        0.75,
        0.95
      ],
      "weight": 0.55
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
        0.75,
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
        0.05,
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
      "weight": 0.1
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
    "base": 0.18,
    "on_rem": {
      "F32": 2.2,
      "F46": 1.0
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
    "base": 0.22,
    "on_rem": {
      "F32": 2.4
    },
    "on_cov": {
      "F32": -0.6
    },
    "slot_decay": 0.1,
    "type": "guide"
  },
  "low_return_alts": {
    "addr": {
      "F32": 0.3,
      "F46": 0.45
    },
    "base": 0.15,
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
    "base": -0.05,
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
    "base": 0.12,
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
    "base": 0.08,
    "on_rem": {
      "F33": 2.1
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
      "F51": 2.0
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
    "base": 0.26,
    "on_rem": {
      "F51": 1.7,
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
    "base": 0.2,
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
    "base": 0.24,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.08,
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
    "base": 0.1,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 14 edits (11 module + 3 shape) — round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser
  - session 5000: 14 edits (11 module + 3 shape) — round 5000 — kill bad defaults for confident_repeat_buyer, fix material_deep_dive miscalibration, revive size_guide for corporate_uniform_buyer, dampen F41 over-detection on premium_silent_browser
  - session 7500: 11 edits (9 module + 2 shape) — round 7500 — stabilize: trim defaults still over-firing on confident_repeat_buyer, fix comparison_card universal-firing, pull back size_guide over-correction, address corporate_uniform_buyer F32 gap

# Latest checkpoint report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8192
- mean oracle reward: 2.0225
- mean regret:        0.2033  (10.1% of oracle)
- cum regret (batch): 508.20

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   182    0.3479    0.5144     32.4%
  corporate_uniform_buyer    81    1.0171    1.4618     30.4%
  returner_from_recent_order   121    1.9471    2.4114     19.3%
  premium_silent_browser   177    1.7003    2.1053     19.2%
  trend_chaser             105    1.9750    2.3312     15.3%
  size_specific_anxious    114    2.5426    2.9005     12.3%
  post_return_returner     198    2.5038    2.8039     10.7%
  hesitant_first_buyer     336    2.3704    2.6004      8.8%
  birthday_rush_gifter     149    2.2711    2.4820      8.5%
  outfit_event_planner     212    1.7762    1.9123      7.1%
  paralyzed_wishlister     172    2.7139    2.8495      4.8%
  tabbed_comparison_shopper   240    1.7816    1.8258      2.4%
  mobile_evening_browser   190    1.0711    1.0955      2.2%
  bargain_hunter_returning   223    1.1819    1.1832      0.1%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  outerwear        242    2.0373    2.3259     12.4%
  shoes            385    2.0017    2.2647     11.6%
  dress            441    1.9052    2.1134      9.9%
  bottoms          495    1.8947    2.0960      9.6%
  accessories      362    1.5641    1.7287      9.5%
  top              575    1.6350    1.7847      8.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           27    0.3713    0.6914     46.3%
  corporate_uniform_buyer shoes            9    1.2371    2.0604     40.0%
  confident_repeat_buyer outerwear       20    0.4356    0.6885     36.7%
  confident_repeat_buyer bottoms         35    0.3077    0.4645     33.8%
  corporate_uniform_buyer bottoms         15    1.1688    1.7247     32.2%
  corporate_uniform_buyer outerwear        9    1.3331    1.9353     31.1%
  corporate_uniform_buyer dress           13    1.0399    1.4908     30.2%
  confident_repeat_buyer top             44    0.2923    0.4070     28.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           15.8      3.64    0.2996
  comparison_card             13.7      2.36    0.3335
  fit_reassurance             13.5      2.60    0.3115
  customers_chose              9.2      5.07    0.3343
  expert_pick                  9.0      2.92    0.2945
  value_breakdown              7.9      3.65    0.2500
  also_bought                  6.8      5.32    0.2269
  material_deep_dive           6.0      2.12    0.3157
  low_return_alts              5.0      3.34    0.3464
  return_explainer             4.6      4.43    0.3482
  wishlist_save                3.3      3.01    0.2976
  brand_story                  2.9      5.16    0.3692
  similar_items                1.8      5.81    0.1244
  personal_recs                0.3      6.00    0.1023
  style_bridge                 0.2      1.00    0.3291
  size_guide                   0.1      1.00    0.0821
  occasion_lookbook            0.1      5.89    0.2437
  easy_returns_promise         0.0      6.00    0.2235
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  outfit_completion(182), also_bought(182), fit_reassurance(168), value_breakdown(150), similar_items(130)
  corporate_uniform_buyer  comparison_card(77), also_bought(77), outfit_completion(76), expert_pick(70), low_return_alts(45)
  returner_from_recent_order  comparison_card(121), outfit_completion(121), low_return_alts(83), expert_pick(74), fit_reassurance(71)
  premium_silent_browser  comparison_card(174), outfit_completion(169), expert_pick(142), material_deep_dive(123), value_breakdown(115)
  trend_chaser            outfit_completion(105), fit_reassurance(105), material_deep_dive(101), also_bought(89), expert_pick(81)
  size_specific_anxious   fit_reassurance(114), comparison_card(113), expert_pick(93), low_return_alts(90), outfit_completion(75)
  post_return_returner    fit_reassurance(198), comparison_card(193), outfit_completion(165), expert_pick(159), low_return_alts(136)
  hesitant_first_buyer    comparison_card(336), outfit_completion(336), fit_reassurance(335), customers_chose(294), material_deep_dive(194)
  birthday_rush_gifter    comparison_card(149), outfit_completion(149), fit_reassurance(131), customers_chose(89), return_explainer(83)
  outfit_event_planner    comparison_card(212), outfit_completion(212), fit_reassurance(209), also_bought(172), material_deep_dive(163)
  paralyzed_wishlister    comparison_card(172), customers_chose(171), fit_reassurance(170), outfit_completion(170), expert_pick(125)
  tabbed_comparison_shopper  comparison_card(240), value_breakdown(240), customers_chose(239), outfit_completion(193), return_explainer(152)
  mobile_evening_browser  outfit_completion(190), fit_reassurance(190), also_bought(190), expert_pick(184), value_breakdown(153)
  bargain_hunter_returning  comparison_card(223), value_breakdown(223), outfit_completion(223), fit_reassurance(217), customers_chose(185)

## Edit history applied so far
  - session 2500: 14 edits (round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser)
  - session 5000: 14 edits (round 5000 — kill bad defaults for confident_repeat_buyer, fix material_deep_dive miscalibration, revive size_guide for corporate_uniform_buyer, dampen F41 over-detection on premium_silent_browser)
  - session 7500: 11 edits (round 7500 — stabilize: trim defaults still over-firing on confident_repeat_buyer, fix comparison_card universal-firing, pull back size_guide over-correction, address corporate_uniform_buyer F32 gap)
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

Write a JSON file at `layer12_state_llm/edits_round_10000.json` with this shape:

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
