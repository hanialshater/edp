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
- virtual_try_on: N1_fit=0.65, N2_visual=0.45, N6_trust=0.20

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
    "base": 0.35,
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
    "base": 0.4,
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
    "base": 0.05,
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
    "base": 0.35,
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
    "base": 0.45,
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
  },
  "virtual_try_on": {
    "addr": {
      "F32": 0.45,
      "F46": 0.2,
      "F33": 0.15
    },
    "base": 0.05,
    "on_rem": {
      "F32": 1.6,
      "F46": 0.5,
      "F33": 0.4
    },
    "on_cov": {
      "F32": -0.6
    },
    "slot_decay": 0.06,
    "type": "premium-fit"
  }
}
```

# Edit history so far

  - session 2500: 16 edits — round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer

# Latest report

```
# STRUCTURAL CHANGE — `virtual_try_on` added to the catalog at session 5000

A new widget has been added to the catalog with provisions {'N1_fit': 0.65, 'N2_visual': 0.45, 'N6_trust': 0.2}. The widget appears in the modules JSON below with default values; it will show 0% activation in this batch because no edits have targeted it yet. Please consider whether this widget should fire for any (persona, category) cells (its provisions strongly favour personas with high N1_fit / N2_visual / N6_trust needs, e.g. size_anxious_new, returner_anxious, post_return_returner, hesitant_first_buyer, and the `shoes` / `outerwear` categories).

---

# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7739
- mean oracle reward: 2.0086
- mean regret:        0.2347  (11.7% of oracle)
- cum regret (batch): 586.87

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             100    1.7318    2.2730     23.8%
  size_specific_anxious     92    2.2343    2.8781     22.4%
  corporate_uniform_buyer   103    1.1749    1.4909     21.2%
  returner_from_recent_order   122    1.9216    2.3806     19.3%
  hesitant_first_buyer     308    2.1671    2.6315     17.6%
  post_return_returner     181    2.3331    2.7693     15.8%
  premium_silent_browser   170    1.9202    2.1275      9.7%
  paralyzed_wishlister     194    2.5904    2.8447      8.9%
  birthday_rush_gifter     198    2.2878    2.4771      7.6%
  outfit_event_planner     182    1.7901    1.8996      5.8%
  confident_repeat_buyer   204    0.4955    0.5089      2.6%
  tabbed_comparison_shopper   265    1.7924    1.8331      2.2%
  bargain_hunter_returning   220    1.1488    1.1720      2.0%
  mobile_evening_browser   161    1.0817    1.0968      1.4%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.9278    2.2267     13.4%
  top              555    1.5777    1.7989     12.3%
  bottoms          507    1.7967    2.0448     12.1%
  accessories      374    1.5707    1.7635     10.9%
  dress            437    1.8280    2.0413     10.4%
  outerwear        248    2.1419    2.3830     10.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             18    1.5457    2.2468     31.2%
  corporate_uniform_buyer bottoms         19    1.2273    1.7247     28.8%
  trend_chaser           accessories     14    2.0808    2.8803     27.8%
  size_specific_anxious  top             22    2.0554    2.8185     27.1%
  returner_from_recent_order shoes           17    2.1053    2.8524     26.2%
  corporate_uniform_buyer shoes           13    1.5212    2.0604     26.2%
  size_specific_anxious  accessories     15    1.7025    2.2723     25.1%
  returner_from_recent_order bottoms         32    2.0037    2.6170     23.4%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  easy_returns_promise        15.8      4.60    0.2988
  comparison_card             15.1      3.16    0.3077
  material_deep_dive          14.5      3.54    0.3026
  expert_pick                 14.2      2.90    0.2865
  return_explainer            11.2      3.32    0.2690
  outfit_completion            8.8      3.82    0.3223
  low_return_alts              5.5      1.34    0.3505
  size_guide                   4.7      3.10    0.3368
  value_breakdown              3.9      3.73    0.2577
  occasion_lookbook            3.4      4.32    0.1869
  customers_chose              2.3      5.32    0.2865
  also_bought                  0.4      6.00    0.0815
  style_bridge                 0.2      1.00    0.3086
  fit_reassurance              0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000
  virtual_try_on               0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            expert_pick(100), material_deep_dive(100), easy_returns_promise(98), return_explainer(80), outfit_completion(69)
  size_specific_anxious   low_return_alts(92), expert_pick(92), easy_returns_promise(92), material_deep_dive(92), comparison_card(91)
  corporate_uniform_buyer  material_deep_dive(103), easy_returns_promise(103), comparison_card(103), expert_pick(101), low_return_alts(84)
  returner_from_recent_order  low_return_alts(122), easy_returns_promise(122), material_deep_dive(122), comparison_card(122), expert_pick(121)
  hesitant_first_buyer    comparison_card(308), material_deep_dive(308), easy_returns_promise(306), outfit_completion(272), size_guide(255)
  post_return_returner    low_return_alts(181), easy_returns_promise(181), material_deep_dive(181), expert_pick(180), comparison_card(180)
  premium_silent_browser  expert_pick(170), easy_returns_promise(170), material_deep_dive(160), comparison_card(159), return_explainer(139)
  paralyzed_wishlister    comparison_card(194), expert_pick(194), easy_returns_promise(190), material_deep_dive(182), outfit_completion(147)
  birthday_rush_gifter    comparison_card(197), outfit_completion(196), material_deep_dive(177), easy_returns_promise(176), expert_pick(129)
  outfit_event_planner    comparison_card(182), outfit_completion(182), expert_pick(182), material_deep_dive(181), easy_returns_promise(180)
  confident_repeat_buyer  material_deep_dive(204), return_explainer(204), easy_returns_promise(204), occasion_lookbook(190), expert_pick(189)
  tabbed_comparison_shopper  comparison_card(265), expert_pick(265), easy_returns_promise(265), return_explainer(259), value_breakdown(245)
  bargain_hunter_returning  comparison_card(220), expert_pick(220), value_breakdown(218), return_explainer(218), easy_returns_promise(128)
  mobile_evening_browser  outfit_completion(161), material_deep_dive(161), return_explainer(161), easy_returns_promise(161), expert_pick(149)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `struct_state_llm/edits_round_5000.json` with this exact shape:

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
