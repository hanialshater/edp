You are editing an Evolvable Decision Program (EDP) for page-module selection.
Your objective is to improve future observed page reward.

You may use only the production-observable evidence below. The report contains
no persona labels, simulator needs, widget provisions, oracle reward, or
counterfactual regret.

# Policy

The policy greedily selects six distinct widgets. At each selection step:

  score = base
        + sum_p on_rem[p] * remaining[p]
        + sum_p on_cov[p] * coverage[p]
        - slot_decay * slot

The seven problem features are F32 size anxiety, F33 quality-signal deficit,
F41 comparison friction, F43 outfit visualization, F45 price-quality confusion,
F46 return hesitation, and F51 decision paralysis.

# Current modules

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
    "base": 0.2,
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
    "base": 0.12,
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
    "base": 0.1,
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
    "base": 0.08,
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
    "base": 0.15,
    "on_rem": {
      "F46": 2.3
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
    "base": 0.1,
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
    "base": 0.05,
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
    "base": 0.16,
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
    "base": 0.16,
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
    "base": 0.1,
    "on_rem": {
      "F51": 1.4,
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
    "slot_decay": 0.03,
    "type": "default"
  },
  "also_bought": {
    "addr": {
      "F41": 0.1,
      "F51": 0.1
    },
    "base": 0.1,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.02,
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

# Prior edits

- action 2500: 12 edits — Demote low-assoc-reward default fillers; surface never-activating widgets targeting underperforming observable cohorts (size_conf-high, return_view-high, cart_osc-high).
- action 5000: 11 edits — Unblock size_guide (coverage penalty too harsh given worst-cohort size_conf gap), revert price_history boost that backfired, keep demoting low-reward defaults, lean into strong return/cart_osc cohorts.

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.7916
- standard deviation: 0.7652

## Reward by observable category
- accessories  n= 385 mean=1.6059
- bottoms      n= 516 mean=1.8196
- dress        n= 452 mean=1.8469
- outerwear    n= 238 mean=2.0570
- shoes        n= 384 mean=1.8807
- top          n= 525 mean=1.6672

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act= 11.4% n=1712 assoc_page_reward=1.8336
- size_guide                act=  0.1% n=  17 assoc_page_reward=1.0689
- low_return_alts           act=  3.9% n= 588 assoc_page_reward=2.1194
- comparison_card           act= 13.9% n=2092 assoc_page_reward=1.9541
- customers_chose           act= 13.3% n=2001 assoc_page_reward=1.9761
- value_breakdown           act=  4.1% n= 614 assoc_page_reward=1.5581
- outfit_completion         act= 15.1% n=2264 assoc_page_reward=1.8016
- style_bridge              act=  2.5% n= 371 assoc_page_reward=1.5791
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  6.0% n= 897 assoc_page_reward=2.1004
- easy_returns_promise      act=  0.0% n=   2 assoc_page_reward=0.5235
- brand_story               act= 13.0% n=1953 assoc_page_reward=1.8484
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.4% n=  66 assoc_page_reward=0.9440
- price_drop_notify         act=  7.0% n=1047 assoc_page_reward=1.6763
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.1% n=  12 assoc_page_reward=1.9501
- similar_items             act=  6.8% n=1017 assoc_page_reward=1.2173
- also_bought               act=  2.1% n= 318 assoc_page_reward=0.7000
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.2% n=  29 assoc_page_reward=0.3563

## Observable feature cohorts
- size_conf      high(n=1140)=1.2985 low(n= 497)=2.4245
- price_sens     high(n= 546)=1.6410 low(n= 811)=1.6215
- return_hist    high(n= 249)=2.5280 low(n=1653)=1.5858
- style_stretch  high(n= 310)=1.7230 low(n=1286)=1.6509
- new            high(n= 442)=2.1245 low(n=1707)=1.6915
- mobile         high(n= 887)=1.9107 low(n= 747)=1.6664
- size_chart     high(n= 582)=2.4245 low(n=1415)=1.4284
- tab_switch     high(n= 916)=2.0672 low(n= 758)=1.1346
- zoom           high(n= 343)=1.9104 low(n= 887)=1.2072
- price_dwell    high(n= 672)=1.7603 low(n=1051)=1.5611
- cart_osc       high(n= 375)=2.5105 low(n=1016)=1.4353
- wishlist       high(n= 618)=1.9130 low(n= 870)=1.6414
- return_view    high(n= 736)=2.3462 low(n= 984)=1.2752
- revisit        high(n= 764)=2.0170 low(n= 870)=1.5485
- price_norm     high(n= 229)=1.6992 low(n= 906)=1.8377

## Most common selected sets
- n= 396: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer
- n= 135: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 120: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, price_drop_notify
- n= 120: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n= 114: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 108: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 108: comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer, value_breakdown
- n=  83: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer
- n=  72: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  65: comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer, value_breakdown

## Edit history
- action 2500: 12 edits — Demote low-assoc-reward default fillers; surface never-activating widgets targeting underperforming observable cohorts (size_conf-high, return_view-high, cart_osc-high).
- action 5000: 11 edits — Unblock size_guide (coverage penalty too harsh given worst-cohort size_conf gap), revert price_history boost that backfired, keep demoting low-reward defaults, lean into strong return/cart_osc cohorts.
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_llm_rep3/edits_round_7500.json` with this shape:

```json
{
  "note": "short rationale",
  "edits": [
    {"widget": "size_guide", "path": "base", "from": 0.05,
      "to": 0.10, "reason": "under-used on high-size_chart sessions"}
  ]
}
```

Allowed paths: `base`, `slot_decay`, `on_rem.<F-code>`, `on_cov.<F-code>`.
Emit only the JSON file.
