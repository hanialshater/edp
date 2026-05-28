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
    "base": 0.32,
    "on_rem": {
      "F32": 2.2,
      "F46": 0.6
    },
    "on_cov": {
      "F32": -1.6,
      "F46": 0.5
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.45,
    "on_rem": {
      "F32": 2.6
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
    "base": 0.12,
    "on_rem": {
      "F32": 1.4,
      "F46": 1.8
    },
    "on_cov": {
      "F46": -1.0,
      "F32": 0.6
    },
    "slot_decay": 0.06,
    "type": "alternatives"
  },
  "comparison_card": {
    "addr": {
      "F41": 0.6,
      "F45": 0.2
    },
    "base": 0.02,
    "on_rem": {
      "F41": 2.3,
      "F45": 0.7
    },
    "on_cov": {
      "F41": -1.7
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
      "F51": 1.6
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
    "base": 0.45,
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
    "base": 0.28,
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
    "base": 0.24,
    "on_rem": {
      "F46": 1.2
    },
    "on_cov": {
      "F46": -0.4
    },
    "slot_decay": 0.05,
    "type": "returns"
  },
  "brand_story": {
    "addr": {
      "F33": 0.5
    },
    "base": 0.32,
    "on_rem": {
      "F33": 2.3
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
    "base": 0.28,
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
    "base": 0.25,
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
    "base": 0.22,
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
    "base": 0.32,
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
    "base": 0.34,
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
    "base": 0.32,
    "on_rem": {
      "F51": 1.8,
      "F33": 0.7
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
    "base": 0.2,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.32,
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

  - session 2500: 16 edits — round 2500 rep2 — revive dead widgets for high-regret personas (confident_repeat, corporate_uniform), tame over-firing similar_items, add cov synergies
  - session 5000: 16 edits — round 5000 rep2 — boost premium/corporate/trend underperformers, revive dead widgets (brand_story, fit_reassurance, return_explainer, price_drop_notify), curb over-firing easy_returns_promise/personal_recs
  - session 7500: 13 edits — round 7500 rep2 — stabilization: nudge confident_repeat/returner shoes+bottoms, lift dead widgets gently, trim over-fire

# Latest report

```
# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.7934
- mean oracle reward: 2.0225
- mean regret:        0.2291  (11.3% of oracle)
- cum regret (batch): 572.75

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  corporate_uniform_buyer    81    1.0259    1.4618     29.8%
  birthday_rush_gifter     149    1.9560    2.4820     21.2%
  hesitant_first_buyer     336    2.0643    2.6004     20.6%
  returner_from_recent_order   121    2.0417    2.4114     15.3%
  premium_silent_browser   177    1.8231    2.1053     13.4%
  confident_repeat_buyer   182    0.4503    0.5144     12.5%
  trend_chaser             105    2.0511    2.3312     12.0%
  size_specific_anxious    114    2.6434    2.9005      8.9%
  post_return_returner     198    2.5773    2.8039      8.1%
  outfit_event_planner     212    1.8128    1.9123      5.2%
  paralyzed_wishlister     172    2.7042    2.8495      5.1%
  mobile_evening_browser   190    1.0398    1.0955      5.1%
  tabbed_comparison_shopper   240    1.7753    1.8258      2.8%
  bargain_hunter_returning   223    1.1822    1.1832      0.1%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  outerwear        242    1.9820    2.3259     14.8%
  shoes            385    1.9608    2.2647     13.4%
  bottoms          495    1.8607    2.0960     11.2%
  dress            441    1.8848    2.1134     10.8%
  top              575    1.6136    1.7847      9.6%
  accessories      362    1.5716    1.7287      9.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  corporate_uniform_buyer shoes            9    1.2756    2.0604     38.1%
  corporate_uniform_buyer outerwear        9    1.2158    1.9353     37.2%
  corporate_uniform_buyer bottoms         15    1.1747    1.7247     31.9%
  birthday_rush_gifter   outerwear       18    2.0687    2.8620     27.7%
  corporate_uniform_buyer top             21    0.8838    1.2187     27.5%
  confident_repeat_buyer shoes           27    0.5099    0.6914     26.2%
  corporate_uniform_buyer dress           13    1.1152    1.4908     25.2%
  hesitant_first_buyer   shoes           52    2.3375    3.0647     23.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             13.8      2.61    0.3255
  occasion_lookbook           13.7      4.00    0.2979
  brand_story                 11.1      3.21    0.3100
  expert_pick                 10.2      2.63    0.3138
  low_return_alts             10.1      2.49    0.3072
  fit_reassurance              9.4      4.66    0.3254
  customers_chose              8.3      4.74    0.3253
  price_history                5.1      4.63    0.2495
  size_guide                   5.1      1.81    0.2517
  trending_now                 4.3      5.82    0.2152
  outfit_completion            3.2      3.18    0.2746
  return_explainer             2.4      3.38    0.3050
  value_breakdown              2.1      2.89    0.2626
  wishlist_save                0.6      5.51    0.1407
  recently_viewed              0.3      5.98    0.0749
  style_bridge                 0.2      1.00    0.3564
  also_bought                  0.2      6.00    0.1619
  price_drop_notify            0.1      5.40    0.1762
  easy_returns_promise         0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  corporate_uniform_buyer  occasion_lookbook(81), comparison_card(78), expert_pick(76), low_return_alts(72), trending_now(65)
  birthday_rush_gifter    low_return_alts(147), comparison_card(146), occasion_lookbook(120), brand_story(113), customers_chose(103)
  hesitant_first_buyer    low_return_alts(336), occasion_lookbook(335), comparison_card(333), brand_story(316), size_guide(298)
  returner_from_recent_order  low_return_alts(118), comparison_card(116), occasion_lookbook(110), brand_story(108), expert_pick(86)
  premium_silent_browser  occasion_lookbook(175), comparison_card(172), expert_pick(171), brand_story(126), fit_reassurance(119)
  confident_repeat_buyer  occasion_lookbook(182), brand_story(182), size_guide(158), low_return_alts(158), trending_now(150)
  trend_chaser            brand_story(102), expert_pick(85), outfit_completion(78), occasion_lookbook(65), fit_reassurance(62)
  size_specific_anxious   low_return_alts(114), comparison_card(113), fit_reassurance(106), expert_pick(106), brand_story(93)
  post_return_returner    low_return_alts(198), comparison_card(197), fit_reassurance(194), occasion_lookbook(177), expert_pick(158)
  outfit_event_planner    comparison_card(212), brand_story(201), outfit_completion(201), fit_reassurance(178), customers_chose(169)
  paralyzed_wishlister    comparison_card(172), expert_pick(172), customers_chose(172), occasion_lookbook(172), brand_story(115)
  mobile_evening_browser  size_guide(145), low_return_alts(143), occasion_lookbook(138), outfit_completion(137), expert_pick(130)
  tabbed_comparison_shopper  comparison_card(240), fit_reassurance(227), return_explainer(226), expert_pick(203), customers_chose(197)
  bargain_hunter_returning  comparison_card(223), occasion_lookbook(223), fit_reassurance(222), expert_pick(203), customers_chose(179)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 rep2 — revive dead widgets for high-regret personas (confident_repeat, corporate_uniform), tame over-firing similar_items, add cov synergies)
  - session 5000: 16 edits (round 5000 rep2 — boost premium/corporate/trend underperformers, revive dead widgets (brand_story, fit_reassurance, return_explainer, price_drop_notify), curb over-firing easy_returns_promise/personal_recs)
  - session 7500: 13 edits (round 7500 rep2 — stabilization: nudge confident_repeat/returner shoes+bottoms, lift dead widgets gently, trim over-fire)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm_rep2/edits_round_10000.json` with this exact shape:

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
