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
      "F32": -1.6
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
    "base": 0.05,
    "on_rem": {
      "F32": 1.0,
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
    "base": -0.05,
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
    "base": 0.18,
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
    "base": 0.42,
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
    "base": 0.25,
    "on_rem": {
      "F51": 1.8,
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
    "base": 0.2,
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
    "base": 0.32,
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

# Latest report

```
# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.8009
- mean oracle reward: 1.9777
- mean regret:        0.1768  (8.9% of oracle)
- cum regret (batch): 441.97

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   216    0.4199    0.5145     18.4%
  returner_from_recent_order   108    2.0723    2.4577     15.7%
  hesitant_first_buyer     287    2.2505    2.6232     14.2%
  trend_chaser             115    1.9820    2.3063     14.1%
  premium_silent_browser   143    1.8233    2.1175     13.9%
  birthday_rush_gifter     142    2.1487    2.4712     13.1%
  corporate_uniform_buyer   126    1.2867    1.4520     11.4%
  paralyzed_wishlister     198    2.6562    2.8462      6.7%
  outfit_event_planner     192    1.7811    1.9051      6.5%
  size_specific_anxious    120    2.6911    2.8673      6.1%
  post_return_returner     179    2.6160    2.7828      6.0%
  mobile_evening_browser   187    1.0610    1.0869      2.4%
  tabbed_comparison_shopper   262    1.7693    1.7976      1.6%
  bargain_hunter_returning   225    1.1775    1.1877      0.9%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.9135    2.1880     12.5%
  outerwear        231    2.0577    2.3378     12.0%
  bottoms          507    1.8410    2.0195      8.8%
  dress            450    1.8356    2.0100      8.7%
  accessories      407    1.6193    1.7337      6.6%
  top              538    1.6845    1.7978      6.3%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           33    0.4662    0.6914     32.6%
  confident_repeat_buyer outerwear       16    0.5165    0.6885     25.0%
  trend_chaser           accessories     21    2.2904    2.8803     20.5%
  returner_from_recent_order bottoms         26    2.0916    2.6170     20.1%
  premium_silent_browser shoes           26    1.9930    2.4827     19.7%
  returner_from_recent_order shoes           19    2.3073    2.8524     19.1%
  confident_repeat_buyer bottoms         43    0.3771    0.4645     18.8%
  hesitant_first_buyer   shoes           48    2.5036    3.0647     18.3%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  occasion_lookbook           14.9      3.85    0.3001
  fit_reassurance             14.0      2.96    0.3037
  brand_story                 13.2      2.83    0.3095
  comparison_card             11.4      2.44    0.3263
  customers_chose             10.2      3.58    0.3431
  low_return_alts              6.2      4.02    0.3754
  wishlist_save                6.1      4.50    0.2288
  trending_now                 5.9      5.52    0.2112
  price_history                4.8      4.76    0.2592
  expert_pick                  2.9      2.68    0.3261
  return_explainer             2.8      3.04    0.2944
  outfit_completion            2.6      3.03    0.2765
  value_breakdown              2.5      2.82    0.2570
  personal_recs                0.9      5.97    0.1161
  price_drop_notify            0.9      4.20    0.3718
  size_guide                   0.5      1.40    0.2988
  style_bridge                 0.2      1.00    0.3251
  easy_returns_promise         0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  brand_story(216), occasion_lookbook(216), wishlist_save(216), trending_now(216), fit_reassurance(214)
  returner_from_recent_order  brand_story(104), customers_chose(93), occasion_lookbook(89), low_return_alts(88), fit_reassurance(72)
  hesitant_first_buyer    occasion_lookbook(287), low_return_alts(283), comparison_card(276), brand_story(272), fit_reassurance(248)
  trend_chaser            brand_story(115), fit_reassurance(115), trending_now(94), outfit_completion(84), wishlist_save(69)
  premium_silent_browser  occasion_lookbook(142), brand_story(124), comparison_card(119), return_explainer(102), fit_reassurance(96)
  birthday_rush_gifter    brand_story(141), low_return_alts(140), fit_reassurance(138), customers_chose(136), occasion_lookbook(135)
  corporate_uniform_buyer  occasion_lookbook(126), comparison_card(113), fit_reassurance(95), trending_now(76), expert_pick(74)
  paralyzed_wishlister    occasion_lookbook(198), customers_chose(198), fit_reassurance(197), comparison_card(171), brand_story(169)
  outfit_event_planner    brand_story(189), customers_chose(187), fit_reassurance(184), outfit_completion(166), comparison_card(161)
  size_specific_anxious   fit_reassurance(120), low_return_alts(120), occasion_lookbook(110), brand_story(107), customers_chose(95)
  post_return_returner    fit_reassurance(179), low_return_alts(179), occasion_lookbook(175), brand_story(169), customers_chose(163)
  mobile_evening_browser  fit_reassurance(187), wishlist_save(180), brand_story(178), trending_now(169), occasion_lookbook(141)
  tabbed_comparison_shopper  comparison_card(262), customers_chose(250), return_explainer(246), occasion_lookbook(243), value_breakdown(161)
  bargain_hunter_returning  comparison_card(225), occasion_lookbook(225), customers_chose(207), fit_reassurance(189), value_breakdown(158)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 rep2 — revive dead widgets for high-regret personas (confident_repeat, corporate_uniform), tame over-firing similar_items, add cov synergies)
  - session 5000: 16 edits (round 5000 rep2 — boost premium/corporate/trend underperformers, revive dead widgets (brand_story, fit_reassurance, return_explainer, price_drop_notify), curb over-firing easy_returns_promise/personal_recs)
```

# Your task

Write up to 16 atomic edits as JSON. Each edit changes ONE field. Focus on:
- Personas with high regret %% (top of the per-persona table)
- Categories with high regret %%
- Dead widgets (activation 0%%) that should fire for those (persona, category) cells
- Over-firing widgets with low reward/fire (consider lowering `base`)
- New `on_cov.<problem>` synergy terms to chain widgets after a related one fires

# Output format

Write a JSON file at `evolve_state_llm_rep2/edits_round_7500.json` with this exact shape:

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
