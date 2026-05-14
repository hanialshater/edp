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
      "F32": 2.5,
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
    "base": 0.18,
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
      "F33": -1.0
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
    "base": 0.28,
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
    "base": 0.18,
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

  - session 2500: 16 edits — round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1]
  - session 2500: 16 edits — round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2]

# Latest report

```
# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7802
- mean oracle reward: 2.0086
- mean regret:        0.2284  (11.4% of oracle)
- cum regret (batch): 571.02

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   204    0.3735    0.5089     26.6%
  trend_chaser             100    1.8878    2.2730     16.9%
  corporate_uniform_buyer   103    1.2422    1.4909     16.7%
  returner_from_recent_order   122    1.9899    2.3806     16.4%
  hesitant_first_buyer     308    2.2057    2.6315     16.2%
  premium_silent_browser   170    1.8189    2.1275     14.5%
  size_specific_anxious     92    2.4815    2.8781     13.8%
  post_return_returner     181    2.4749    2.7693     10.6%
  birthday_rush_gifter     198    2.2723    2.4771      8.3%
  outfit_event_planner     182    1.7509    1.8996      7.8%
  paralyzed_wishlister     194    2.6255    2.8447      7.7%
  mobile_evening_browser   161    1.0305    1.0968      6.0%
  tabbed_comparison_shopper   265    1.7239    1.8331      6.0%
  bargain_hunter_returning   220    1.1336    1.1720      3.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8946    2.2267     14.9%
  outerwear        248    2.0824    2.3830     12.6%
  bottoms          507    1.7904    2.0448     12.4%
  dress            437    1.8207    2.0413     10.8%
  accessories      374    1.6002    1.7635      9.3%
  top              555    1.6472    1.7989      8.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer bottoms         39    0.2981    0.4645     35.8%
  confident_repeat_buyer shoes           28    0.4494    0.6914     35.0%
  confident_repeat_buyer dress           38    0.3743    0.5304     29.4%
  trend_chaser           top             18    1.6596    2.2468     26.1%
  returner_from_recent_order shoes           17    2.1808    2.8524     23.5%
  corporate_uniform_buyer bottoms         19    1.3326    1.7247     22.7%
  hesitant_first_buyer   shoes           44    2.3793    3.0647     22.4%
  returner_from_recent_order bottoms         32    2.0397    2.6170     22.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             13.1      2.05    0.3288
  outfit_completion           12.8      3.27    0.2924
  easy_returns_promise        12.2      4.77    0.3096
  customers_chose             11.3      3.92    0.3268
  fit_reassurance             10.3      2.68    0.3248
  brand_story                  8.7      3.85    0.3253
  price_history                7.8      3.51    0.2567
  expert_pick                  6.6      3.94    0.2893
  material_deep_dive           5.4      4.24    0.2481
  return_explainer             4.0      3.28    0.2791
  recently_viewed              1.9      4.33    0.1162
  low_return_alts              1.8      1.99    0.3648
  similar_items                1.6      5.53    0.1222
  value_breakdown              1.3      1.77    0.2467
  also_bought                  0.6      5.95    0.0728
  price_drop_notify            0.3      4.10    0.3032
  style_bridge                 0.2      1.00    0.3146
  wishlist_save                0.1      3.85    0.2103
  size_guide                   0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  outfit_completion(204), recently_viewed(186), material_deep_dive(161), price_history(149), easy_returns_promise(123)
  trend_chaser            outfit_completion(100), fit_reassurance(98), brand_story(91), material_deep_dive(90), easy_returns_promise(70)
  corporate_uniform_buyer  easy_returns_promise(103), comparison_card(85), fit_reassurance(82), customers_chose(75), expert_pick(61)
  returner_from_recent_order  easy_returns_promise(120), comparison_card(118), customers_chose(114), outfit_completion(113), brand_story(111)
  hesitant_first_buyer    outfit_completion(308), easy_returns_promise(308), comparison_card(306), fit_reassurance(305), brand_story(274)
  premium_silent_browser  easy_returns_promise(168), return_explainer(148), material_deep_dive(109), comparison_card(103), value_breakdown(97)
  size_specific_anxious   fit_reassurance(92), easy_returns_promise(92), comparison_card(85), customers_chose(82), brand_story(58)
  post_return_returner    easy_returns_promise(181), fit_reassurance(180), comparison_card(171), customers_chose(169), brand_story(119)
  birthday_rush_gifter    outfit_completion(198), easy_returns_promise(198), comparison_card(197), brand_story(188), customers_chose(185)
  outfit_event_planner    comparison_card(182), outfit_completion(182), customers_chose(181), brand_story(168), material_deep_dive(126)
  paralyzed_wishlister    comparison_card(194), expert_pick(194), outfit_completion(192), customers_chose(191), fit_reassurance(152)
  mobile_evening_browser  outfit_completion(161), fit_reassurance(121), easy_returns_promise(116), price_history(114), similar_items(84)
  tabbed_comparison_shopper  comparison_card(265), price_history(265), return_explainer(265), customers_chose(264), easy_returns_promise(259)
  bargain_hunter_returning  comparison_card(220), price_history(220), customers_chose(220), outfit_completion(213), expert_pick(172)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1])
  - session 2500: 16 edits (round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2])
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `ensemble_state_llm/edits_round_5000_draw2.json` with this exact shape:

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
