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
      "F32": -1.2
    },
    "slot_decay": 0.05,
    "type": "reassurance"
  },
  "size_guide": {
    "addr": {
      "F32": 0.5
    },
    "base": 0.2,
    "on_rem": {
      "F32": 2.0
    },
    "on_cov": {
      "F32": 0.5
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
    "base": 0.18,
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
    "base": 0.05,
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
      "F33": 0.4
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
    "base": 0.2,
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
    "base": 0.3,
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
    "base": 0.22,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.15,
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
    "base": 0.18,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas

# Latest report

```
# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7661
- mean oracle reward: 2.0086
- mean regret:        0.2426  (12.1% of oracle)
- cum regret (batch): 606.39

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  corporate_uniform_buyer   103    1.0609    1.4909     28.8%
  confident_repeat_buyer   204    0.3904    0.5089     23.3%
  size_specific_anxious     92    2.2647    2.8781     21.3%
  premium_silent_browser   170    1.7238    2.1275     19.0%
  returner_from_recent_order   122    1.9454    2.3806     18.3%
  trend_chaser             100    1.9341    2.2730     14.9%
  hesitant_first_buyer     308    2.2551    2.6315     14.3%
  post_return_returner     181    2.3779    2.7693     14.1%
  birthday_rush_gifter     198    2.2507    2.4771      9.1%
  outfit_event_planner     182    1.7325    1.8996      8.8%
  paralyzed_wishlister     194    2.7034    2.8447      5.0%
  bargain_hunter_returning   220    1.1156    1.1720      4.8%
  mobile_evening_browser   161    1.0484    1.0968      4.4%
  tabbed_comparison_shopper   265    1.7717    1.8331      3.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8876    2.2267     15.2%
  outerwear        248    2.0708    2.3830     13.1%
  bottoms          507    1.8041    2.0448     11.8%
  dress            437    1.8015    2.0413     11.7%
  accessories      374    1.5693    1.7635     11.0%
  top              555    1.6169    1.7989     10.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           28    0.4390    0.6914     36.5%
  corporate_uniform_buyer bottoms         19    1.1203    1.7247     35.0%
  corporate_uniform_buyer shoes           13    1.3609    2.0604     34.0%
  corporate_uniform_buyer dress           21    1.0579    1.4908     29.0%
  size_specific_anxious  accessories     15    1.6449    2.2723     27.6%
  premium_silent_browser accessories     29    1.4426    1.9398     25.6%
  corporate_uniform_buyer outerwear        9    1.4659    1.9353     24.3%
  corporate_uniform_buyer top             29    0.9262    1.2187     24.0%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.3      2.13    0.3203
  outfit_completion           13.7      3.34    0.2939
  easy_returns_promise        11.0      5.05    0.3092
  expert_pick                 10.6      2.37    0.3086
  customers_chose              8.0      4.89    0.3282
  low_return_alts              6.6      2.54    0.3307
  fit_reassurance              6.5      2.58    0.3421
  occasion_lookbook            6.1      4.43    0.2083
  value_breakdown              5.8      3.20    0.2669
  similar_items                4.7      5.02    0.1738
  material_deep_dive           4.5      4.15    0.2787
  brand_story                  3.8      3.08    0.3298
  also_bought                  2.0      5.39    0.1191
  size_guide                   1.4      4.89    0.3724
  wishlist_save                0.6      3.87    0.2332
  style_bridge                 0.2      1.00    0.3347
  personal_recs                0.2      5.43    0.0566
  return_explainer             0.0      3.50    0.3227
  trending_now                 0.0      6.00    0.0738
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  corporate_uniform_buyer  comparison_card(103), easy_returns_promise(103), expert_pick(87), similar_items(85), low_return_alts(81)
  confident_repeat_buyer  occasion_lookbook(204), similar_items(202), outfit_completion(192), also_bought(159), material_deep_dive(152)
  size_specific_anxious   comparison_card(92), easy_returns_promise(92), expert_pick(91), fit_reassurance(78), outfit_completion(60)
  premium_silent_browser  comparison_card(170), low_return_alts(146), easy_returns_promise(144), expert_pick(136), outfit_completion(123)
  returner_from_recent_order  low_return_alts(122), outfit_completion(122), comparison_card(122), easy_returns_promise(120), expert_pick(101)
  trend_chaser            occasion_lookbook(96), fit_reassurance(78), brand_story(72), outfit_completion(69), comparison_card(47)
  hesitant_first_buyer    comparison_card(308), outfit_completion(308), easy_returns_promise(308), fit_reassurance(285), customers_chose(250)
  post_return_returner    comparison_card(181), easy_returns_promise(181), expert_pick(157), low_return_alts(151), outfit_completion(107)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), easy_returns_promise(196), fit_reassurance(120), customers_chose(107)
  outfit_event_planner    comparison_card(182), outfit_completion(182), occasion_lookbook(162), expert_pick(122), material_deep_dive(83)
  paralyzed_wishlister    comparison_card(194), expert_pick(194), outfit_completion(194), customers_chose(194), material_deep_dive(98)
  bargain_hunter_returning  comparison_card(220), value_breakdown(220), outfit_completion(217), expert_pick(195), occasion_lookbook(189)
  mobile_evening_browser  outfit_completion(161), occasion_lookbook(161), similar_items(150), expert_pick(96), also_bought(90)
  tabbed_comparison_shopper  comparison_card(265), value_breakdown(263), expert_pick(257), customers_chose(255), low_return_alts(204)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm_rep3/edits_round_5000.json` with this exact shape:

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
