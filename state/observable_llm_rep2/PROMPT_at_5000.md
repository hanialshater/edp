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
      "F51": 1.5
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
    "base": 0.02,
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
    "base": 0.08,
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
    "base": 0.16,
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
    "base": 0.18,
    "on_rem": {
      "F51": 1.6,
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
    "base": 0.1,
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
    "base": 0.38,
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
    "base": 0.3,
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
    "base": 0.2,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- action 2500: 12 edits — Demote generic default widgets with low associated page reward; promote under-activated widgets whose activation or feature cohorts (return_view, return_hist, cart_osc, wishlist) associate with high observed reward.

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 2500 → 5000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.6471
- standard deviation: 0.6912

## Reward by observable category
- accessories  n= 395 mean=1.5279
- bottoms      n= 497 mean=1.6554
- dress        n= 438 mean=1.7166
- outerwear    n= 245 mean=1.8387
- shoes        n= 364 mean=1.7129
- top          n= 561 mean=1.5431

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  6.3% n= 943 assoc_page_reward=1.7918
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  9.8% n=1475 assoc_page_reward=1.8963
- comparison_card           act= 13.0% n=1947 assoc_page_reward=1.8290
- customers_chose           act= 11.4% n=1717 assoc_page_reward=1.8788
- value_breakdown           act=  2.9% n= 436 assoc_page_reward=1.4288
- outfit_completion         act= 12.8% n=1919 assoc_page_reward=1.6724
- style_bridge              act=  1.1% n= 169 assoc_page_reward=1.6704
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   0 assoc_page_reward=n/a
- easy_returns_promise      act=  0.1% n=  19 assoc_page_reward=0.6642
- brand_story               act= 13.1% n=1959 assoc_page_reward=1.6835
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.0% n=   2 assoc_page_reward=1.0606
- price_drop_notify         act=  6.3% n= 946 assoc_page_reward=1.6818
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.0% n=   0 assoc_page_reward=n/a
- similar_items             act= 13.9% n=2079 assoc_page_reward=1.4856
- also_bought               act=  6.6% n= 983 assoc_page_reward=1.1044
- trending_now              act=  0.7% n=  98 assoc_page_reward=0.4431
- personal_recs             act=  2.1% n= 308 assoc_page_reward=0.6392

## Observable feature cohorts
- size_conf      high(n=1132)=1.2180 low(n= 491)=2.1308
- price_sens     high(n= 551)=1.5731 low(n= 823)=1.4777
- return_hist    high(n= 258)=2.3031 low(n=1686)=1.4640
- style_stretch  high(n= 285)=1.7116 low(n=1281)=1.5201
- new            high(n= 443)=1.8368 low(n=1725)=1.5830
- mobile         high(n= 869)=1.7263 low(n= 740)=1.5313
- size_chart     high(n= 593)=2.1414 low(n=1399)=1.3726
- tab_switch     high(n= 889)=1.8932 low(n= 761)=1.0726
- zoom           high(n= 387)=1.6702 low(n= 858)=1.1338
- price_dwell    high(n= 693)=1.6286 low(n=1038)=1.4933
- cart_osc       high(n= 335)=2.3980 low(n= 978)=1.3067
- wishlist       high(n= 623)=1.8391 low(n= 876)=1.4262
- return_view    high(n= 781)=2.0349 low(n= 918)=1.2432
- revisit        high(n= 827)=1.8645 low(n= 861)=1.3869
- price_norm     high(n= 215)=1.6965 low(n= 848)=1.6342

## Most common selected sets
- n= 311: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 192: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 182: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 147: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  80: also_bought, brand_story, comparison_card, low_return_alts, price_drop_notify, similar_items
- n=  77: also_bought, brand_story, comparison_card, customers_chose, outfit_completion, similar_items
- n=  70: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  65: also_bought, brand_story, comparison_card, outfit_completion, price_drop_notify, similar_items
- n=  63: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, similar_items
- n=  61: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items

## Edit history
- action 2500: 12 edits — Demote generic default widgets with low associated page reward; promote under-activated widgets whose activation or feature cohorts (return_view, return_hist, cart_osc, wishlist) associate with high observed reward.
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_llm_rep2/edits_round_5000.json` with this shape:

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
