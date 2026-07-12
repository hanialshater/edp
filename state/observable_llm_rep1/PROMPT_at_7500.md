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
    "base": 0.16,
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
      "F45": 1.7,
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
      "F43": 2.2
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
    "base": 0.13,
    "on_rem": {
      "F46": 1.4
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
    "base": 0.14,
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
      "F51": 1.5
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
    "base": 0.1,
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
    "base": 0.14,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- action 2500: 14 edits — Demote low-reward generic defaults that crowd slots; promote never-firing targeted widgets on features whose high cohorts show strong observed reward (cart_osc, return_hist/return_view, size_chart, zoom).
- action 5000: 13 edits — Continue demoting persistently low-reward defaults; amplify expert_pick (assoc 2.37 at 0.3%), unblock size_guide via smaller coverage penalty, and reinforce returns/outfit widgets that matured well.

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.6897
- standard deviation: 0.7164

## Reward by observable category
- accessories  n= 385 mean=1.5105
- bottoms      n= 516 mean=1.7245
- dress        n= 452 mean=1.7320
- outerwear    n= 238 mean=1.9322
- shoes        n= 384 mean=1.7596
- top          n= 525 mean=1.5896

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  9.7% n=1462 assoc_page_reward=1.7497
- size_guide                act=  0.0% n=   4 assoc_page_reward=1.2355
- low_return_alts           act=  4.0% n= 594 assoc_page_reward=2.1120
- comparison_card           act= 13.8% n=2072 assoc_page_reward=1.8703
- customers_chose           act= 10.5% n=1578 assoc_page_reward=1.9452
- value_breakdown           act=  1.3% n= 191 assoc_page_reward=1.1197
- outfit_completion         act= 12.0% n=1794 assoc_page_reward=1.7035
- style_bridge              act=  3.4% n= 509 assoc_page_reward=1.6336
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  3.9% n= 589 assoc_page_reward=1.9064
- easy_returns_promise      act=  0.7% n= 109 assoc_page_reward=2.0070
- brand_story               act= 12.1% n=1815 assoc_page_reward=1.6569
- material_deep_dive        act=  0.5% n=  72 assoc_page_reward=1.7534
- price_history             act=  0.9% n= 131 assoc_page_reward=1.5817
- price_drop_notify         act=  6.0% n= 903 assoc_page_reward=1.5506
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  3.0% n= 447 assoc_page_reward=2.1746
- similar_items             act= 12.0% n=1806 assoc_page_reward=1.4625
- also_bought               act=  4.8% n= 714 assoc_page_reward=0.9647
- trending_now              act=  0.1% n=  22 assoc_page_reward=0.2247
- personal_recs             act=  1.3% n= 188 assoc_page_reward=0.4951

## Observable feature cohorts
- size_conf      high(n=1140)=1.2571 low(n= 497)=2.2082
- price_sens     high(n= 546)=1.5821 low(n= 811)=1.5456
- return_hist    high(n= 249)=2.3872 low(n=1653)=1.4852
- style_stretch  high(n= 310)=1.6645 low(n=1286)=1.5586
- new            high(n= 442)=1.9015 low(n=1707)=1.6235
- mobile         high(n= 887)=1.7624 low(n= 747)=1.6129
- size_chart     high(n= 582)=2.2163 low(n=1415)=1.3875
- tab_switch     high(n= 916)=1.9505 low(n= 758)=1.0977
- zoom           high(n= 343)=1.8341 low(n= 887)=1.1537
- price_dwell    high(n= 672)=1.6643 low(n=1051)=1.4896
- cart_osc       high(n= 375)=2.4230 low(n=1016)=1.3244
- wishlist       high(n= 618)=1.8526 low(n= 870)=1.4997
- return_view    high(n= 736)=2.1416 low(n= 984)=1.2315
- revisit        high(n= 764)=1.9491 low(n= 870)=1.4049
- price_norm     high(n= 229)=1.6315 low(n= 906)=1.7141

## Most common selected sets
- n= 184: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 111: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n=  89: also_bought, brand_story, fit_reassurance, outfit_completion, personal_recs, similar_items
- n=  89: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer
- n=  87: also_bought, brand_story, comparison_card, outfit_completion, price_drop_notify, similar_items
- n=  86: also_bought, brand_story, fit_reassurance, price_drop_notify, similar_items, style_bridge
- n=  76: brand_story, comparison_card, customers_chose, fit_reassurance, similar_items, style_bridge
- n=  72: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer
- n=  54: brand_story, comparison_card, customers_chose, price_drop_notify, return_explainer, similar_items
- n=  49: also_bought, brand_story, fit_reassurance, outfit_completion, similar_items, value_breakdown

## Edit history
- action 2500: 14 edits — Demote low-reward generic defaults that crowd slots; promote never-firing targeted widgets on features whose high cohorts show strong observed reward (cart_osc, return_hist/return_view, size_chart, zoom).
- action 5000: 13 edits — Continue demoting persistently low-reward defaults; amplify expert_pick (assoc 2.37 at 0.3%), unblock size_guide via smaller coverage penalty, and reinforce returns/outfit widgets that matured well.
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_llm_rep1/edits_round_7500.json` with this shape:

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
