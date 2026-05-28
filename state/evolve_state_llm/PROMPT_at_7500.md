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
    "base": 0.45,
    "on_rem": {
      "F32": 2.2,
      "F46": 0.6
    },
    "on_cov": {
      "F32": 0.3
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
      "F46": 2.4
    },
    "on_cov": {
      "F46": -1.0
    },
    "slot_decay": 0.03,
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
    "base": 0.4,
    "on_rem": {
      "F41": 0.8,
      "F51": 2.0
    },
    "on_cov": {
      "F41": 1.0,
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
      "F32": 0.9
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
    "base": 0.4,
    "on_rem": {
      "F33": 1.9
    },
    "on_cov": {
      "F33": 0.4
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
    "base": 0.3,
    "on_rem": {
      "F51": 1.3,
      "F45": 1.6
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
    "base": 0.35,
    "on_rem": {
      "F51": 2.3
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
    "base": 0.22,
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
    "base": 0.05,
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
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer
  - session 5000: 16 edits — round 5000 — activate still-dead widgets for trend_chaser/peer-social and size-anxious/fit cells; dial back round-1 over-corrections on material_deep_dive and easy_returns_promise

# Latest report

```
# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.8627
- mean oracle reward: 1.9777
- mean regret:        0.1150  (5.8% of oracle)
- cum regret (batch): 287.51

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  premium_silent_browser   143    1.7906    2.1175     15.4%
  paralyzed_wishlister     198    2.5484    2.8462     10.5%
  trend_chaser             115    2.0857    2.3063      9.6%
  size_specific_anxious    120    2.6105    2.8673      9.0%
  returner_from_recent_order   108    2.2790    2.4577      7.3%
  hesitant_first_buyer     287    2.4757    2.6232      5.6%
  outfit_event_planner     192    1.8220    1.9051      4.4%
  corporate_uniform_buyer   126    1.3925    1.4520      4.1%
  post_return_returner     179    2.6714    2.7828      4.0%
  birthday_rush_gifter     142    2.3931    2.4712      3.2%
  tabbed_comparison_shopper   262    1.7710    1.7976      1.5%
  mobile_evening_browser   187    1.0800    1.0869      0.6%
  bargain_hunter_returning   225    1.1833    1.1877      0.4%
  confident_repeat_buyer   216    0.5131    0.5145      0.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      407    1.5993    1.7337      7.8%
  outerwear        231    2.1835    2.3378      6.6%
  bottoms          507    1.9047    2.0195      5.7%
  top              538    1.6968    1.7978      5.6%
  shoes            367    2.0732    2.1880      5.2%
  dress            450    1.9155    2.0100      4.7%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  premium_silent_browser accessories     23    1.4929    1.9398     23.0%
  premium_silent_browser dress           24    1.8610    2.3417     20.5%
  premium_silent_browser outerwear       10    2.2431    2.6939     16.7%
  paralyzed_wishlister   outerwear       17    2.6891    3.2235     16.6%
  trend_chaser           accessories     21    2.4222    2.8803     15.9%
  size_specific_anxious  top             28    2.4249    2.8185     14.0%
  premium_silent_browser top             28    1.5159    1.7578     13.8%
  trend_chaser           outerwear        7    2.0741    2.3901     13.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  customers_chose             14.9      2.68    0.3250
  fit_reassurance             13.8      3.11    0.3096
  easy_returns_promise        13.3      5.33    0.3096
  return_explainer            11.5      4.12    0.2864
  material_deep_dive           9.3      4.27    0.3464
  brand_story                  9.0      2.91    0.2574
  price_drop_notify            7.9      3.13    0.2937
  outfit_completion            7.4      3.69    0.3185
  comparison_card              6.6      2.31    0.3222
  low_return_alts              4.2      1.52    0.3813
  occasion_lookbook            1.1      4.46    0.1482
  wishlist_save                0.7      5.68    0.4218
  style_bridge                 0.2      1.00    0.3470
  value_breakdown              0.0      5.00    0.2820
  size_guide                   0.0      1.00    0.4018
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  expert_pick                  0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  premium_silent_browser  customers_chose(142), easy_returns_promise(130), brand_story(119), price_drop_notify(116), return_explainer(102)
  paralyzed_wishlister    customers_chose(198), price_drop_notify(188), outfit_completion(155), fit_reassurance(152), brand_story(135)
  trend_chaser            brand_story(113), fit_reassurance(111), return_explainer(108), customers_chose(101), easy_returns_promise(85)
  size_specific_anxious   fit_reassurance(120), material_deep_dive(120), easy_returns_promise(120), customers_chose(114), low_return_alts(70)
  returner_from_recent_order  low_return_alts(108), material_deep_dive(108), easy_returns_promise(108), customers_chose(107), outfit_completion(83)
  hesitant_first_buyer    fit_reassurance(286), return_explainer(284), easy_returns_promise(256), comparison_card(251), customers_chose(247)
  outfit_event_planner    customers_chose(192), outfit_completion(192), fit_reassurance(183), return_explainer(177), brand_story(170)
  corporate_uniform_buyer  easy_returns_promise(126), brand_story(122), material_deep_dive(121), customers_chose(120), fit_reassurance(117)
  post_return_returner    fit_reassurance(179), material_deep_dive(179), easy_returns_promise(179), low_return_alts(172), customers_chose(164)
  birthday_rush_gifter    customers_chose(142), outfit_completion(140), easy_returns_promise(139), material_deep_dive(131), fit_reassurance(130)
  tabbed_comparison_shopper  price_drop_notify(262), customers_chose(262), comparison_card(261), easy_returns_promise(259), material_deep_dive(243)
  mobile_evening_browser  outfit_completion(187), fit_reassurance(187), return_explainer(187), easy_returns_promise(187), brand_story(140)
  bargain_hunter_returning  price_drop_notify(225), comparison_card(225), customers_chose(225), fit_reassurance(225), brand_story(204)
  confident_repeat_buyer  fit_reassurance(216), return_explainer(216), easy_returns_promise(216), brand_story(208), occasion_lookbook(111)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 16 edits (round 5000 — activate still-dead widgets for trend_chaser/peer-social and size-anxious/fit cells; dial back round-1 over-corrections on material_deep_dive and easy_returns_promise)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm/edits_round_7500.json` with this exact shape:

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
