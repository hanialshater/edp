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
      "F46": 0.6
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
    "base": 0.16,
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
    "base": 0.1,
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
    "base": 0.1,
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
      "F33": 0.4
    },
    "slot_decay": 0.07,
    "type": "premium"
  },
  "price_history": {
    "addr": {
      "F45": 0.45
    },
    "base": 0.22,
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
    "base": 0.26,
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
    "base": 0.3,
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
    "base": 0.12,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.06,
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
    "base": 0.07,
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

# Latest report

```
# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7111
- mean oracle reward: 1.9777
- mean regret:        0.2666  (13.5% of oracle)
- cum regret (batch): 666.53

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   216    0.3797    0.5145     26.2%
  trend_chaser             115    1.7285    2.3063     25.1%
  size_specific_anxious    120    2.2228    2.8673     22.5%
  hesitant_first_buyer     287    2.1168    2.6232     19.3%
  post_return_returner     179    2.2655    2.7828     18.6%
  premium_silent_browser   143    1.7276    2.1175     18.4%
  returner_from_recent_order   108    2.0174    2.4577     17.9%
  birthday_rush_gifter     142    2.1671    2.4712     12.3%
  paralyzed_wishlister     198    2.6365    2.8462      7.4%
  corporate_uniform_buyer   126    1.3673    1.4520      5.8%
  outfit_event_planner     192    1.7956    1.9051      5.8%
  tabbed_comparison_shopper   262    1.7182    1.7976      4.4%
  mobile_evening_browser   187    1.0460    1.0869      3.8%
  bargain_hunter_returning   225    1.1543    1.1877      2.8%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      407    1.4531    1.7337     16.2%
  top              538    1.5246    1.7978     15.2%
  shoes            367    1.8844    2.1880     13.9%
  dress            450    1.7503    2.0100     12.9%
  outerwear        231    2.0483    2.3378     12.4%
  bottoms          507    1.8022    2.0195     10.8%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           33    0.4383    0.6914     36.6%
  size_specific_anxious  accessories     17    1.4543    2.2723     36.0%
  trend_chaser           top             30    1.4784    2.2468     34.2%
  post_return_returner   accessories     29    1.4692    2.0918     29.8%
  confident_repeat_buyer outerwear       16    0.4955    0.6885     28.0%
  premium_silent_browser accessories     23    1.4111    1.9398     27.3%
  trend_chaser           shoes           15    1.4958    2.0259     26.2%
  confident_repeat_buyer bottoms         43    0.3442    0.4645     25.9%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.2      2.32    0.3114
  material_deep_dive           9.7      3.30    0.2790
  fit_reassurance              9.7      3.65    0.3035
  wishlist_save                9.1      3.48    0.2635
  size_guide                   8.2      4.83    0.3046
  easy_returns_promise         8.0      5.28    0.3093
  outfit_completion            7.3      4.04    0.2783
  expert_pick                  5.6      2.30    0.3389
  style_bridge                 5.0      1.58    0.2773
  occasion_lookbook            4.8      4.61    0.1983
  low_return_alts              4.1      2.10    0.3469
  price_history                3.3      3.91    0.1820
  value_breakdown              3.3      2.92    0.2665
  return_explainer             2.9      3.41    0.2829
  customers_chose              2.7      4.79    0.2690
  similar_items                1.2      5.95    0.1155
  price_drop_notify            0.9      2.67    0.2429
  brand_story                  0.0      5.67    0.2429
  recently_viewed              0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  wishlist_save(202), material_deep_dive(198), price_history(185), outfit_completion(179), occasion_lookbook(160)
  trend_chaser            style_bridge(115), occasion_lookbook(115), material_deep_dive(111), wishlist_save(103), fit_reassurance(103)
  size_specific_anxious   size_guide(119), comparison_card(117), easy_returns_promise(101), fit_reassurance(100), expert_pick(94)
  hesitant_first_buyer    comparison_card(287), easy_returns_promise(266), fit_reassurance(264), size_guide(243), outfit_completion(230)
  post_return_returner    size_guide(178), comparison_card(177), easy_returns_promise(173), low_return_alts(147), fit_reassurance(94)
  premium_silent_browser  comparison_card(140), fit_reassurance(105), material_deep_dive(104), return_explainer(104), size_guide(84)
  returner_from_recent_order  comparison_card(108), low_return_alts(92), size_guide(92), easy_returns_promise(92), outfit_completion(76)
  birthday_rush_gifter    comparison_card(142), easy_returns_promise(109), style_bridge(105), material_deep_dive(100), size_guide(88)
  paralyzed_wishlister    comparison_card(198), expert_pick(197), wishlist_save(171), outfit_completion(164), material_deep_dive(127)
  corporate_uniform_buyer  comparison_card(126), size_guide(126), easy_returns_promise(123), wishlist_save(97), material_deep_dive(76)
  outfit_event_planner    comparison_card(192), style_bridge(189), material_deep_dive(173), occasion_lookbook(166), wishlist_save(133)
  tabbed_comparison_shopper  comparison_card(262), return_explainer(261), fit_reassurance(198), value_breakdown(170), customers_chose(147)
  mobile_evening_browser  style_bridge(187), occasion_lookbook(178), wishlist_save(166), material_deep_dive(138), fit_reassurance(107)
  bargain_hunter_returning  comparison_card(225), outfit_completion(225), customers_chose(157), value_breakdown(150), occasion_lookbook(105)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas)
  - session 5000: 16 edits (round 5000 — boost corporate_uniform/confident_repeat coverage, revive dead price widgets, tame over-firing low-reward widgets)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm_rep3/edits_round_7500.json` with this exact shape:

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
