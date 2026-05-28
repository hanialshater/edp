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
      "F32": 2.8,
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
    "base": 0.55,
    "on_rem": {
      "F32": 2.0
    },
    "on_cov": {
      "F32": 0.6
    },
    "slot_decay": 0.1,
    "type": "guide"
  },
  "low_return_alts": {
    "addr": {
      "F32": 0.3,
      "F46": 0.45
    },
    "base": 0.35,
    "on_rem": {
      "F32": 1.0,
      "F46": 1.8
    },
    "on_cov": {
      "F46": -1.0,
      "F32": 0.8
    },
    "slot_decay": 0.06,
    "type": "alternatives"
  },
  "comparison_card": {
    "addr": {
      "F41": 0.6,
      "F45": 0.2
    },
    "base": -0.15,
    "on_rem": {
      "F41": 2.3,
      "F45": 0.7
    },
    "on_cov": {
      "F41": -1.3
    },
    "slot_decay": 0.07,
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
    "base": 0.3,
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
    "base": 0.0,
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
    "base": 0.5,
    "on_rem": {
      "F43": 1.4
    },
    "on_cov": {
      "F43": 0.7
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
    "base": 0.0,
    "on_rem": {
      "F46": 1.2
    },
    "on_cov": {
      "F46": 0.9
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
      "F33": -1.0,
      "F43": 0.6
    },
    "slot_decay": 0.05,
    "type": "premium"
  },
  "material_deep_dive": {
    "addr": {
      "F33": 0.45
    },
    "base": 0.16,
    "on_rem": {
      "F33": 1.7
    },
    "on_cov": {
      "F33": 0.8
    },
    "slot_decay": 0.07,
    "type": "premium"
  },
  "price_history": {
    "addr": {
      "F45": 0.45
    },
    "base": 0.16,
    "on_rem": {
      "F45": 1.7
    },
    "on_cov": {
      "F45": 0.7
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
    "base": 0.7,
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
    "base": 0.22,
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
    "base": 0.45,
    "on_rem": {
      "F51": 1.4,
      "F33": 0.4
    },
    "on_cov": {
      "F51": 0.6
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
    "base": 0.15,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.4,
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
    "base": 0.45,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1]
  - session 2500: 16 edits — round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2]
  - session 5000: 16 edits — round 5000 draw1 — revive dead widgets (size_guide, occasion_lookbook, personal_recs, trending_now), tame over-firing low-reward widgets, boost confident_repeat/trend_chaser cells, add F32->F46 and F43->F33 synergies  [ensemble-best of 3: draw 1]

# Latest report

```
# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7036
- mean oracle reward: 1.9777
- mean regret:        0.2741  (13.9% of oracle)
- cum regret (batch): 685.37

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   216    0.3259    0.5145     36.7%
  size_specific_anxious    120    2.2153    2.8673     22.7%
  hesitant_first_buyer     287    2.1338    2.6232     18.7%
  trend_chaser             115    1.8876    2.3063     18.2%
  post_return_returner     179    2.2981    2.7828     17.4%
  returner_from_recent_order   108    2.0397    2.4577     17.0%
  premium_silent_browser   143    1.7655    2.1175     16.6%
  birthday_rush_gifter     142    2.0789    2.4712     15.9%
  outfit_event_planner     192    1.6709    1.9051     12.3%
  corporate_uniform_buyer   126    1.2918    1.4520     11.0%
  paralyzed_wishlister     198    2.6837    2.8462      5.7%
  bargain_hunter_returning   225    1.1204    1.1877      5.7%
  tabbed_comparison_shopper   262    1.7201    1.7976      4.3%
  mobile_evening_browser   187    1.0490    1.0869      3.5%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.8144    2.1880     17.1%
  outerwear        231    1.9916    2.3378     14.8%
  accessories      407    1.4809    1.7337     14.6%
  top              538    1.5514    1.7978     13.7%
  dress            450    1.7493    2.0100     13.0%
  bottoms          507    1.7917    2.0195     11.3%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           33    0.3401    0.6914     50.8%
  confident_repeat_buyer bottoms         43    0.2693    0.4645     42.0%
  confident_repeat_buyer outerwear       16    0.4265    0.6885     38.0%
  confident_repeat_buyer top             44    0.2586    0.4070     36.5%
  size_specific_anxious  accessories     17    1.4792    2.2723     34.9%
  confident_repeat_buyer dress           44    0.3774    0.5304     28.8%
  premium_silent_browser shoes           26    1.8364    2.4827     26.0%
  post_return_returner   accessories     29    1.5536    2.0918     25.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  occasion_lookbook           14.9      3.47    0.2785
  low_return_alts             14.0      3.06    0.3077
  recently_viewed             12.7      4.00    0.2645
  expert_pick                 11.4      3.28    0.2850
  comparison_card              9.6      2.73    0.3219
  value_breakdown              9.0      2.71    0.2624
  size_guide                   7.9      4.57    0.2995
  fit_reassurance              4.1      1.02    0.3648
  brand_story                  4.0      3.05    0.2753
  price_history                3.6      5.15    0.2485
  personal_recs                3.2      5.89    0.1454
  material_deep_dive           2.6      5.20    0.2589
  easy_returns_promise         1.4      5.60    0.3339
  customers_chose              1.0      3.15    0.2649
  style_bridge                 0.3      1.35    0.3062
  outfit_completion            0.2      5.88    0.2680
  trending_now                 0.1      5.00    0.0728
  return_explainer             0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  occasion_lookbook(216), recently_viewed(216), personal_recs(200), expert_pick(118), value_breakdown(117)
  size_specific_anxious   low_return_alts(120), size_guide(120), expert_pick(115), fit_reassurance(106), comparison_card(89)
  hesitant_first_buyer    low_return_alts(287), occasion_lookbook(287), size_guide(270), value_breakdown(260), fit_reassurance(237)
  trend_chaser            occasion_lookbook(115), recently_viewed(112), low_return_alts(111), brand_story(97), value_breakdown(54)
  post_return_returner    low_return_alts(179), size_guide(178), fit_reassurance(148), expert_pick(140), comparison_card(122)
  returner_from_recent_order  low_return_alts(108), occasion_lookbook(108), expert_pick(92), comparison_card(69), easy_returns_promise(68)
  premium_silent_browser  low_return_alts(143), recently_viewed(143), value_breakdown(139), occasion_lookbook(135), material_deep_dive(118)
  birthday_rush_gifter    low_return_alts(142), occasion_lookbook(142), size_guide(135), recently_viewed(126), brand_story(100)
  outfit_event_planner    occasion_lookbook(192), recently_viewed(191), expert_pick(185), comparison_card(177), low_return_alts(144)
  corporate_uniform_buyer  low_return_alts(126), recently_viewed(126), occasion_lookbook(123), size_guide(110), expert_pick(102)
  paralyzed_wishlister    comparison_card(198), expert_pick(198), occasion_lookbook(198), low_return_alts(197), recently_viewed(189)
  bargain_hunter_returning  comparison_card(225), occasion_lookbook(224), price_history(222), expert_pick(220), value_breakdown(216)
  tabbed_comparison_shopper  comparison_card(262), low_return_alts(262), expert_pick(262), price_history(186), value_breakdown(182)
  mobile_evening_browser  occasion_lookbook(187), recently_viewed(187), personal_recs(165), low_return_alts(155), size_guide(145)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1])
  - session 2500: 16 edits (round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2])
  - session 5000: 16 edits (round 5000 draw1 — revive dead widgets (size_guide, occasion_lookbook, personal_recs, trending_now), tame over-firing low-reward widgets, boost confident_repeat/trend_chaser cells, add F32->F46 and F43->F33 synergies  [ensemble-best of 3: draw 1])
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `ensemble_state_llm/edits_round_7500_draw2.json` with this exact shape:

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
