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
    "base": 0.14,
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
    "base": 0.16,
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
      "F41": 2.5,
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
    "base": 0.14,
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
      "F45": 1.8,
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
    "base": 0.12,
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
    "base": 0.2,
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
    "base": 0.1,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- action 2500: 12 edits — Demote generic default widgets with low associated page reward; promote under-activated widgets whose activation or feature cohorts (return_view, return_hist, cart_osc, wishlist) associate with high observed reward.
- action 5000: 10 edits — Continue demoting low-reward defaults (trending_now, personal_recs, also_bought, similar_items); promote above-mean targeted widgets (customers_chose, low_return_alts, fit_reassurance, comparison_card); partially roll back easy_returns_promise which underperformed when it fired.

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.7023
- standard deviation: 0.7385

## Reward by observable category
- accessories  n= 385 mean=1.5585
- bottoms      n= 516 mean=1.7355
- dress        n= 452 mean=1.7518
- outerwear    n= 238 mean=1.9141
- shoes        n= 384 mean=1.7420
- top          n= 525 mean=1.6076

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  7.4% n=1116 assoc_page_reward=1.8004
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act= 10.9% n=1636 assoc_page_reward=1.9484
- comparison_card           act= 13.4% n=2005 assoc_page_reward=1.9012
- customers_chose           act= 12.5% n=1880 assoc_page_reward=1.9173
- value_breakdown           act=  1.1% n= 164 assoc_page_reward=1.7103
- outfit_completion         act= 14.4% n=2153 assoc_page_reward=1.7055
- style_bridge              act=  1.4% n= 207 assoc_page_reward=1.5995
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   0 assoc_page_reward=n/a
- easy_returns_promise      act=  0.1% n=  12 assoc_page_reward=0.3669
- brand_story               act= 14.4% n=2158 assoc_page_reward=1.7067
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  1.1% n= 165 assoc_page_reward=1.1863
- price_drop_notify         act=  8.1% n=1213 assoc_page_reward=1.6376
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.0% n=   0 assoc_page_reward=n/a
- similar_items             act= 10.6% n=1595 assoc_page_reward=1.3678
- also_bought               act=  4.2% n= 627 assoc_page_reward=0.8877
- trending_now              act=  0.1% n=  14 assoc_page_reward=0.3112
- personal_recs             act=  0.4% n=  55 assoc_page_reward=0.4726

## Observable feature cohorts
- size_conf      high(n=1140)=1.2350 low(n= 497)=2.3131
- price_sens     high(n= 546)=1.6032 low(n= 811)=1.5456
- return_hist    high(n= 249)=2.5020 low(n=1653)=1.4939
- style_stretch  high(n= 310)=1.7017 low(n=1286)=1.5739
- new            high(n= 442)=1.9379 low(n=1707)=1.6319
- mobile         high(n= 887)=1.7933 low(n= 747)=1.5741
- size_chart     high(n= 582)=2.3199 low(n=1415)=1.3790
- tab_switch     high(n= 916)=2.0132 low(n= 758)=1.0416
- zoom           high(n= 343)=1.8095 low(n= 887)=1.1545
- price_dwell    high(n= 672)=1.6928 low(n=1051)=1.5046
- cart_osc       high(n= 375)=2.5016 low(n=1016)=1.3421
- wishlist       high(n= 618)=1.8942 low(n= 870)=1.4870
- return_view    high(n= 736)=2.2024 low(n= 984)=1.2683
- revisit        high(n= 764)=1.9708 low(n= 870)=1.4238
- price_norm     high(n= 229)=1.6137 low(n= 906)=1.7332

## Most common selected sets
- n= 316: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 313: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 297: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n= 160: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 145: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  68: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, price_drop_notify
- n=  61: comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify, similar_items
- n=  56: also_bought, brand_story, comparison_card, outfit_completion, price_drop_notify, similar_items
- n=  56: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items
- n=  49: brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items, style_bridge

## Edit history
- action 2500: 12 edits — Demote generic default widgets with low associated page reward; promote under-activated widgets whose activation or feature cohorts (return_view, return_hist, cart_osc, wishlist) associate with high observed reward.
- action 5000: 10 edits — Continue demoting low-reward defaults (trending_now, personal_recs, also_bought, similar_items); promote above-mean targeted widgets (customers_chose, low_return_alts, fit_reassurance, comparison_card); partially roll back easy_returns_promise which underperformed when it fired.
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_llm_rep2/edits_round_7500.json` with this shape:

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
