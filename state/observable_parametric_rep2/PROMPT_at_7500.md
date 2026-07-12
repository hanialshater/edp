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
    "base": 0.18,
    "on_rem": {
      "F32": 2.3
    },
    "on_cov": {
      "F32": -1.0
    },
    "slot_decay": 0.1,
    "type": "guide"
  },
  "low_return_alts": {
    "addr": {
      "F32": 0.3,
      "F46": 0.45
    },
    "base": 0.1,
    "on_rem": {
      "F32": 1.0,
      "F46": 2.0
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
      "F51": 1.4
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
    "base": 0.12,
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
    "base": 0.14,
    "on_rem": {
      "F33": 2.0
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
    "base": 0.1,
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
    "base": 0.2,
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
    "base": 0.12,
    "on_rem": {
      "F51": 1.6
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
    "base": 0.32,
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
    "base": 0.05,
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
    "base": 0.12,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- action 2500: 14 edits — Demote generic defaults with below-mean associated reward; promote starved specialized widgets whose feature cohorts (cart_osc/wishlist/revisit, return_view, zoom, low size_conf) show above-mean observed reward.
- action 5000: 14 edits — Continue demoting the still-below-mean generic widgets and strengthen the specialized widgets whose associated reward and matching high-signal cohorts stay well above the 1.0449 mean but whose activation remains near zero.

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.0534
- standard deviation: 0.3891

## Reward by observable category
- accessories  n= 365 mean=0.9614
- bottoms      n= 498 mean=1.0809
- dress        n= 487 mean=1.0819
- outerwear    n= 219 mean=1.1753
- shoes        n= 369 mean=1.0881
- top          n= 562 mean=0.9940

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  9.0% n=1357 assoc_page_reward=1.0851
- size_guide                act=  0.3% n=  41 assoc_page_reward=1.0699
- low_return_alts           act=  8.2% n=1225 assoc_page_reward=1.1083
- comparison_card           act= 13.3% n=1994 assoc_page_reward=1.0899
- customers_chose           act= 11.2% n=1674 assoc_page_reward=1.1107
- value_breakdown           act=  4.8% n= 724 assoc_page_reward=0.9914
- outfit_completion         act= 16.4% n=2460 assoc_page_reward=1.0510
- style_bridge              act=  0.1% n=  10 assoc_page_reward=1.2482
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.4% n=  54 assoc_page_reward=0.9953
- easy_returns_promise      act=  0.0% n=   1 assoc_page_reward=1.1845
- brand_story               act=  5.2% n= 777 assoc_page_reward=1.0919
- material_deep_dive        act=  6.5% n= 977 assoc_page_reward=1.0713
- price_history             act=  0.2% n=  25 assoc_page_reward=0.7078
- price_drop_notify         act=  6.5% n= 968 assoc_page_reward=1.1010
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.1% n=  12 assoc_page_reward=1.3357
- similar_items             act= 13.3% n=1990 assoc_page_reward=0.9824
- also_bought               act=  4.1% n= 611 assoc_page_reward=0.8358
- trending_now              act=  0.0% n=   2 assoc_page_reward=0.5390
- personal_recs             act=  0.7% n=  98 assoc_page_reward=0.6423

## Observable feature cohorts
- size_conf      high(n= 651)=0.8961 low(n= 559)=1.1532
- price_sens     high(n= 669)=1.0470 low(n= 409)=0.9774
- return_hist    high(n=  65)=1.2244 low(n=1533)=0.9958
- style_stretch  high(n= 315)=1.1381 low(n= 830)=1.0141
- new            high(n= 504)=1.1452 low(n=1032)=0.9787
- mobile         high(n= 655)=1.0166 low(n= 285)=1.0993
- size_chart     high(n= 347)=1.2369 low(n=1433)=0.9699
- tab_switch     high(n= 486)=1.2039 low(n= 975)=0.9583
- zoom           high(n= 202)=1.2331 low(n= 841)=0.9352
- price_dwell    high(n= 497)=1.0449 low(n= 843)=0.9582
- cart_osc       high(n= 270)=1.3702 low(n=1403)=0.9883
- wishlist       high(n= 454)=1.2522 low(n= 825)=0.9364
- return_view    high(n= 284)=1.1684 low(n=1411)=0.9731
- revisit        high(n= 458)=1.2891 low(n= 814)=0.9252
- price_norm     high(n= 215)=1.0451 low(n= 849)=1.0357

## Most common selected sets
- n= 188: comparison_card, customers_chose, fit_reassurance, material_deep_dive, outfit_completion, similar_items
- n= 167: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 164: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 113: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n= 103: comparison_card, customers_chose, low_return_alts, material_deep_dive, outfit_completion, similar_items
- n= 100: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n=  86: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items
- n=  72: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n=  71: comparison_card, low_return_alts, material_deep_dive, outfit_completion, price_drop_notify, similar_items
- n=  68: comparison_card, fit_reassurance, material_deep_dive, outfit_completion, price_drop_notify, similar_items

## Edit history
- action 2500: 14 edits — Demote generic defaults with below-mean associated reward; promote starved specialized widgets whose feature cohorts (cart_osc/wishlist/revisit, return_view, zoom, low size_conf) show above-mean observed reward.
- action 5000: 14 edits — Continue demoting the still-below-mean generic widgets and strengthen the specialized widgets whose associated reward and matching high-signal cohorts stay well above the 1.0449 mean but whose activation remains near zero.
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_parametric_rep2/edits_round_7500.json` with this shape:

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
