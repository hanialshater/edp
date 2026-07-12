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
- mean: 1.0172
- standard deviation: 0.3817

## Reward by observable category
- accessories  n= 295 mean=0.9226
- bottoms      n= 388 mean=1.0776
- dress        n= 350 mean=1.0221
- outerwear    n= 207 mean=1.1382
- shoes        n= 317 mean=1.0436
- top          n= 443 mean=0.9479

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  9.3% n=1118 assoc_page_reward=1.0646
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  5.0% n= 605 assoc_page_reward=1.1125
- comparison_card           act= 11.8% n=1413 assoc_page_reward=1.0678
- customers_chose           act= 11.9% n=1430 assoc_page_reward=1.0848
- value_breakdown           act=  6.5% n= 783 assoc_page_reward=0.9971
- outfit_completion         act= 15.2% n=1822 assoc_page_reward=1.0167
- style_bridge              act=  0.0% n=   5 assoc_page_reward=1.0400
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   1 assoc_page_reward=1.3899
- easy_returns_promise      act=  0.0% n=   0 assoc_page_reward=n/a
- brand_story               act=  8.6% n=1037 assoc_page_reward=1.0633
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.0% n=   0 assoc_page_reward=n/a
- price_drop_notify         act=  1.5% n= 181 assoc_page_reward=1.3076
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.1% n=  15 assoc_page_reward=1.3565
- similar_items             act= 15.8% n=1893 assoc_page_reward=0.9961
- also_bought               act=  9.3% n=1117 assoc_page_reward=0.9080
- trending_now              act=  1.4% n= 169 assoc_page_reward=0.5510
- personal_recs             act=  3.4% n= 411 assoc_page_reward=0.7059

## Observable feature cohorts
- size_conf      high(n= 533)=0.8326 low(n= 483)=1.1139
- price_sens     high(n= 538)=1.0462 low(n= 347)=0.9061
- return_hist    high(n=  55)=1.1360 low(n=1228)=0.9614
- style_stretch  high(n= 230)=1.1065 low(n= 696)=0.9922
- new            high(n= 418)=1.0821 low(n= 789)=0.9361
- mobile         high(n= 584)=0.9713 low(n= 210)=1.0916
- size_chart     high(n= 272)=1.1738 low(n=1122)=0.9295
- tab_switch     high(n= 436)=1.1666 low(n= 779)=0.9143
- zoom           high(n= 159)=1.1986 low(n= 695)=0.8806
- price_dwell    high(n= 400)=1.0281 low(n= 656)=0.9008
- cart_osc       high(n= 208)=1.3365 low(n=1165)=0.9315
- wishlist       high(n= 387)=1.2337 low(n= 672)=0.8806
- return_view    high(n= 223)=1.1368 low(n=1078)=0.9375
- revisit        high(n= 367)=1.2481 low(n= 675)=0.8764
- price_norm     high(n= 159)=1.0655 low(n= 733)=0.9880

## Most common selected sets
- n= 231: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 152: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n= 151: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 146: also_bought, brand_story, comparison_card, customers_chose, outfit_completion, similar_items
- n= 109: also_bought, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 103: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n=  89: also_bought, fit_reassurance, outfit_completion, personal_recs, similar_items, value_breakdown
- n=  70: also_bought, brand_story, outfit_completion, personal_recs, similar_items, trending_now
- n=  56: also_bought, brand_story, fit_reassurance, outfit_completion, personal_recs, similar_items
- n=  55: also_bought, brand_story, comparison_card, fit_reassurance, outfit_completion, similar_items

## Edit history
- none
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_parametric_rep2/edits_round_2500.json` with this shape:

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
