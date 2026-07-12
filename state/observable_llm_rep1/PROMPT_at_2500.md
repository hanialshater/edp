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
    "base": 0.05,
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
    "base": 0.05,
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
    "base": 0.45,
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
    "base": 0.4,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.03,
    "type": "default"
  },
  "trending_now": {
    "addr": {},
    "base": 0.3,
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
    "base": 0.35,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- none

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 0 → 2500
- feedback items matured since previous checkpoint: 2000
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.5860
- standard deviation: 0.7082

## Reward by observable category
- accessories  n= 296 mean=1.4563
- bottoms      n= 402 mean=1.5785
- dress        n= 368 mean=1.6518
- outerwear    n= 213 mean=1.7502
- shoes        n= 286 mean=1.6471
- top          n= 435 mean=1.5048

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  7.0% n= 840 assoc_page_reward=1.7961
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  7.5% n= 905 assoc_page_reward=1.8804
- comparison_card           act= 12.6% n=1517 assoc_page_reward=1.8111
- customers_chose           act= 12.0% n=1444 assoc_page_reward=1.7693
- value_breakdown           act=  5.3% n= 639 assoc_page_reward=1.3885
- outfit_completion         act= 12.0% n=1435 assoc_page_reward=1.6309
- style_bridge              act=  0.2% n=  25 assoc_page_reward=1.8248
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   2 assoc_page_reward=1.5659
- easy_returns_promise      act=  0.0% n=   0 assoc_page_reward=n/a
- brand_story               act= 10.6% n=1266 assoc_page_reward=1.6791
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.0% n=   0 assoc_page_reward=n/a
- price_drop_notify         act=  1.2% n= 142 assoc_page_reward=2.4126
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.0% n=   2 assoc_page_reward=1.5246
- similar_items             act= 15.4% n=1847 assoc_page_reward=1.4988
- also_bought               act= 10.1% n=1217 assoc_page_reward=1.2448
- trending_now              act=  1.9% n= 232 assoc_page_reward=0.4914
- personal_recs             act=  4.1% n= 487 assoc_page_reward=0.7682

## Observable feature cohorts
- size_conf      high(n= 908)=1.1581 low(n= 405)=2.0686
- price_sens     high(n= 436)=1.5152 low(n= 677)=1.4366
- return_hist    high(n= 210)=2.2978 low(n=1319)=1.3911
- style_stretch  high(n= 233)=1.6832 low(n=1026)=1.4366
- new            high(n= 357)=1.7817 low(n=1358)=1.5230
- mobile         high(n= 707)=1.6716 low(n= 613)=1.4948
- size_chart     high(n= 479)=2.0560 low(n=1110)=1.3083
- tab_switch     high(n= 697)=1.8352 low(n= 618)=0.9939
- zoom           high(n= 278)=1.7148 low(n= 713)=1.0641
- price_dwell    high(n= 551)=1.5716 low(n= 832)=1.4396
- cart_osc       high(n= 263)=2.4105 low(n= 772)=1.2224
- wishlist       high(n= 487)=1.7906 low(n= 741)=1.3191
- return_view    high(n= 603)=1.9659 low(n= 752)=1.1724
- revisit        high(n= 656)=1.8049 low(n= 695)=1.2873
- price_norm     high(n= 168)=1.6153 low(n= 712)=1.5545

## Most common selected sets
- n= 201: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 188: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 140: also_bought, comparison_card, customers_chose, low_return_alts, similar_items, value_breakdown
- n= 116: also_bought, comparison_card, customers_chose, outfit_completion, similar_items, value_breakdown
- n= 108: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, similar_items
- n= 106: also_bought, brand_story, outfit_completion, personal_recs, similar_items, trending_now
- n=  94: also_bought, brand_story, comparison_card, fit_reassurance, outfit_completion, similar_items
- n=  84: also_bought, brand_story, comparison_card, customers_chose, outfit_completion, similar_items
- n=  82: also_bought, comparison_card, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n=  71: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion

## Edit history
- none
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_llm_rep1/edits_round_2500.json` with this shape:

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
