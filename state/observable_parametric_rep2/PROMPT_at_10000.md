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
    "base": 0.24,
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
      "F45": 1.9,
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
    "base": 0.09,
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
    "base": 0.14,
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
    "base": 0.18,
    "on_rem": {
      "F51": 1.8
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
    "base": 0.24,
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
    "base": 0.26,
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
    "base": 0.14,
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
    "base": 0.06,
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
- action 7500: 13 edits — Prune remaining below-mean widgets (incl. reverting the price_history boost that showed assoc 0.7078), and keep promoting above-mean but starved specialists: size_guide, expert_pick, style_bridge, wishlist_save, easy_returns_promise.

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 7500 → 10000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.0593
- standard deviation: 0.3882

## Reward by observable category
- accessories  n= 371 mean=0.9459
- bottoms      n= 482 mean=1.0873
- dress        n= 464 mean=1.0661
- outerwear    n= 263 mean=1.2281
- shoes        n= 374 mean=1.1460
- top          n= 546 mean=0.9652

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  8.0% n=1196 assoc_page_reward=1.0901
- size_guide                act=  1.2% n= 177 assoc_page_reward=1.0013
- low_return_alts           act=  9.7% n=1462 assoc_page_reward=1.1100
- comparison_card           act= 14.2% n=2126 assoc_page_reward=1.0849
- customers_chose           act= 10.5% n=1579 assoc_page_reward=1.1291
- value_breakdown           act=  3.1% n= 462 assoc_page_reward=1.0011
- outfit_completion         act= 15.4% n=2306 assoc_page_reward=1.0565
- style_bridge              act=  1.7% n= 260 assoc_page_reward=1.1069
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.2% n=  32 assoc_page_reward=0.8934
- easy_returns_promise      act=  0.1% n=  21 assoc_page_reward=0.8079
- brand_story               act=  4.6% n= 683 assoc_page_reward=1.0849
- material_deep_dive        act=  8.7% n=1298 assoc_page_reward=1.0755
- price_history             act=  0.3% n=  41 assoc_page_reward=1.0400
- price_drop_notify         act=  8.4% n=1254 assoc_page_reward=1.0581
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.3% n=  52 assoc_page_reward=1.2577
- expert_pick               act=  0.2% n=  28 assoc_page_reward=0.9353
- similar_items             act= 11.4% n=1708 assoc_page_reward=0.9601
- also_bought               act=  2.0% n= 304 assoc_page_reward=0.7252
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.1% n=  11 assoc_page_reward=0.5003

## Observable feature cohorts
- size_conf      high(n= 649)=0.8870 low(n= 564)=1.1870
- price_sens     high(n= 695)=1.0376 low(n= 426)=0.9305
- return_hist    high(n=  80)=1.2193 low(n=1521)=0.9961
- style_stretch  high(n= 282)=1.1494 low(n= 923)=1.0456
- new            high(n= 496)=1.1506 low(n=1008)=0.9848
- mobile         high(n= 690)=1.0245 low(n= 274)=1.1254
- size_chart     high(n= 340)=1.2595 low(n=1413)=0.9701
- tab_switch     high(n= 508)=1.1963 low(n= 962)=0.9594
- zoom           high(n= 220)=1.2097 low(n= 845)=0.9302
- price_dwell    high(n= 498)=1.0345 low(n= 786)=0.9477
- cart_osc       high(n= 282)=1.3706 low(n=1387)=0.9913
- wishlist       high(n= 484)=1.2307 low(n= 762)=0.9343
- return_view    high(n= 293)=1.1701 low(n=1353)=0.9809
- revisit        high(n= 512)=1.2853 low(n= 807)=0.9299
- price_norm     high(n= 205)=1.0461 low(n= 895)=1.0546

## Most common selected sets
- n= 166: comparison_card, customers_chose, fit_reassurance, material_deep_dive, outfit_completion, similar_items
- n= 128: comparison_card, customers_chose, low_return_alts, material_deep_dive, outfit_completion, similar_items
- n= 114: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items
- n= 114: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 108: comparison_card, customers_chose, low_return_alts, material_deep_dive, outfit_completion, price_drop_notify
- n=  95: comparison_card, low_return_alts, material_deep_dive, outfit_completion, price_drop_notify, similar_items
- n=  91: comparison_card, fit_reassurance, material_deep_dive, outfit_completion, price_drop_notify, similar_items
- n=  86: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n=  84: comparison_card, customers_chose, fit_reassurance, low_return_alts, material_deep_dive, outfit_completion
- n=  82: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items

## Edit history
- action 2500: 14 edits — Demote generic defaults with below-mean associated reward; promote starved specialized widgets whose feature cohorts (cart_osc/wishlist/revisit, return_view, zoom, low size_conf) show above-mean observed reward.
- action 5000: 14 edits — Continue demoting the still-below-mean generic widgets and strengthen the specialized widgets whose associated reward and matching high-signal cohorts stay well above the 1.0449 mean but whose activation remains near zero.
- action 7500: 13 edits — Prune remaining below-mean widgets (incl. reverting the price_history boost that showed assoc 0.7078), and keep promoting above-mean but starved specialists: size_guide, expert_pick, style_bridge, wishlist_save, easy_returns_promise.
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_parametric_rep2/edits_round_10000.json` with this shape:

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
