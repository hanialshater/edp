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
      "F46": 0.95
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.32,
    "on_rem": {
      "F32": 2.0
    },
    "on_cov": {
      "F32": 0.5,
      "F46": 0.5
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
      "F51": -0.3
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
    "base": 0.16,
    "on_rem": {
      "F43": 1.6
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
    "base": 0.04,
    "on_rem": {
      "F43": 1.4
    },
    "on_cov": {
      "F43": 0.4
    },
    "slot_decay": 0.05,
    "type": "outfit"
  },
  "return_explainer": {
    "addr": {
      "F46": 0.5
    },
    "base": 0.18,
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
    "base": 0.22,
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
    "base": 0.24,
    "on_rem": {
      "F33": 1.9
    },
    "on_cov": {
      "F33": -0.4
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
      "F33": 2.1
    },
    "on_cov": {
      "F33": 0.7
    },
    "slot_decay": 0.07,
    "type": "premium"
  },
  "price_history": {
    "addr": {
      "F45": 0.45
    },
    "base": 0.14,
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
    "base": 0.24,
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
    "base": 0.42,
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
    "base": 0.38,
    "on_rem": {
      "F51": 1.9
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
      "F51": 2.0,
      "F33": 0.4
    },
    "on_cov": {
      "F51": -0.7,
      "F33": 0.6
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
    "base": 0.08,
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
    "base": 0.26,
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

  - session 2500: 16 edits — round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas
  - session 5000: 16 edits — round 5000 — boost corporate_uniform/confident_repeat coverage, revive dead price widgets, tame over-firing low-reward widgets
  - session 7500: 14 edits — round 7500 — stabilize: lift confident_repeat/trend_chaser coverage, revive remaining dead widgets, tame low-r/fire over-firers

# Latest report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.7738
- mean oracle reward: 2.0225
- mean regret:        0.2487  (12.3% of oracle)
- cum regret (batch): 621.71

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   182    0.2524    0.5144     50.9%
  size_specific_anxious    114    2.3370    2.9005     19.4%
  premium_silent_browser   177    1.7309    2.1053     17.8%
  returner_from_recent_order   121    2.0031    2.4114     16.9%
  trend_chaser             105    1.9415    2.3312     16.7%
  hesitant_first_buyer     336    2.1928    2.6004     15.7%
  post_return_returner     198    2.3693    2.8039     15.5%
  birthday_rush_gifter     149    2.1959    2.4820     11.5%
  outfit_event_planner     212    1.7720    1.9123      7.3%
  paralyzed_wishlister     172    2.7157    2.8495      4.7%
  tabbed_comparison_shopper   240    1.7524    1.8258      4.0%
  corporate_uniform_buyer    81    1.4050    1.4618      3.9%
  mobile_evening_browser   190    1.0607    1.0955      3.2%
  bargain_hunter_returning   223    1.1563    1.1832      2.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            385    1.9515    2.2647     13.8%
  accessories      362    1.4976    1.7287     13.4%
  top              575    1.5567    1.7847     12.8%
  outerwear        242    2.0352    2.3259     12.5%
  dress            441    1.8667    2.1134     11.7%
  bottoms          495    1.8794    2.0960     10.3%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           27    0.1960    0.6914     71.7%
  confident_repeat_buyer outerwear       20    0.3272    0.6885     52.5%
  confident_repeat_buyer bottoms         35    0.2241    0.4645     51.8%
  confident_repeat_buyer top             44    0.2177    0.4070     46.5%
  confident_repeat_buyer dress           24    0.2994    0.5304     43.6%
  confident_repeat_buyer accessories     32    0.2967    0.4464     33.5%
  premium_silent_browser accessories     24    1.4042    1.9398     27.6%
  size_specific_anxious  accessories     15    1.6737    2.2723     26.3%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.2      2.37    0.3191
  outfit_completion           11.8      3.24    0.2835
  fit_reassurance              9.4      3.32    0.3259
  wishlist_save                8.7      2.63    0.3015
  expert_pick                  8.0      3.34    0.2761
  brand_story                  7.9      3.69    0.2904
  size_guide                   7.8      5.00    0.3286
  material_deep_dive           6.8      3.43    0.2533
  easy_returns_promise         6.0      5.34    0.3446
  value_breakdown              4.5      3.12    0.2663
  low_return_alts              4.2      2.33    0.3619
  customers_chose              3.1      4.58    0.2687
  return_explainer             2.8      3.57    0.2892
  also_bought                  2.8      5.61    0.1505
  occasion_lookbook            1.0      5.03    0.2913
  recently_viewed              0.8      4.99    0.0642
  price_history                0.2      5.00    0.1312
  personal_recs                0.0      6.00    0.0299
  price_drop_notify            0.0      6.00    0.2756
  style_bridge                 0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  outfit_completion(182), material_deep_dive(177), expert_pick(177), also_bought(154), brand_story(150)
  size_specific_anxious   comparison_card(113), size_guide(111), fit_reassurance(92), easy_returns_promise(76), wishlist_save(74)
  premium_silent_browser  expert_pick(177), comparison_card(171), material_deep_dive(143), return_explainer(129), fit_reassurance(129)
  returner_from_recent_order  comparison_card(119), low_return_alts(104), size_guide(96), outfit_completion(92), brand_story(72)
  trend_chaser            outfit_completion(105), material_deep_dive(94), expert_pick(93), occasion_lookbook(80), fit_reassurance(80)
  hesitant_first_buyer    comparison_card(336), outfit_completion(336), easy_returns_promise(310), fit_reassurance(306), size_guide(253)
  post_return_returner    size_guide(192), comparison_card(188), wishlist_save(157), easy_returns_promise(154), low_return_alts(152)
  birthday_rush_gifter    outfit_completion(148), comparison_card(147), easy_returns_promise(112), fit_reassurance(101), brand_story(93)
  outfit_event_planner    comparison_card(212), outfit_completion(212), material_deep_dive(150), expert_pick(150), brand_story(128)
  paralyzed_wishlister    comparison_card(172), outfit_completion(171), wishlist_save(168), expert_pick(116), low_return_alts(93)
  tabbed_comparison_shopper  comparison_card(240), fit_reassurance(238), return_explainer(235), wishlist_save(232), value_breakdown(217)
  corporate_uniform_buyer  size_guide(81), easy_returns_promise(78), wishlist_save(77), comparison_card(68), brand_story(63)
  mobile_evening_browser  outfit_completion(190), brand_story(165), material_deep_dive(164), expert_pick(162), wishlist_save(116)
  bargain_hunter_returning  comparison_card(223), outfit_completion(222), wishlist_save(219), value_breakdown(219), customers_chose(193)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas)
  - session 5000: 16 edits (round 5000 — boost corporate_uniform/confident_repeat coverage, revive dead price widgets, tame over-firing low-reward widgets)
  - session 7500: 14 edits (round 7500 — stabilize: lift confident_repeat/trend_chaser coverage, revive remaining dead widgets, tame low-r/fire over-firers)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm_rep3/edits_round_10000.json` with this exact shape:

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
