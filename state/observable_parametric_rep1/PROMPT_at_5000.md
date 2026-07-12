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
    "base": 0.15,
    "on_rem": {
      "F32": 2.0
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
    "base": 0.15,
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
    "base": 0.1,
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
    "base": 0.12,
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
    "base": 0.15,
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
    "base": 0.14,
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
    "base": 0.12,
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
    "base": 0.36,
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
    "base": 0.25,
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
    "base": 0.18,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- action 2500: 14 edits — Shift slot budget away from low-reward default fillers (trending_now 0.551, personal_recs 0.706, also_bought 0.908 assoc page reward, all below the 1.017 mean) toward targeted widgets that show high associated reward but near-zero activation, and open up never-selected widgets serving cohorts that currently underperform (size_conf-high 0.833).

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 2500 → 5000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.0543
- standard deviation: 0.3961

## Reward by observable category
- accessories  n= 404 mean=0.9618
- bottoms      n= 508 mean=1.1167
- dress        n= 424 mean=1.0822
- outerwear    n= 245 mean=1.1788
- shoes        n= 372 mean=1.0887
- top          n= 547 mean=0.9639

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act= 10.1% n=1514 assoc_page_reward=1.0706
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  6.7% n=1004 assoc_page_reward=1.1484
- comparison_card           act= 12.8% n=1918 assoc_page_reward=1.0932
- customers_chose           act= 13.0% n=1952 assoc_page_reward=1.1034
- value_breakdown           act=  5.9% n= 880 assoc_page_reward=1.0304
- outfit_completion         act= 16.1% n=2421 assoc_page_reward=1.0540
- style_bridge              act=  0.0% n=   7 assoc_page_reward=1.0688
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.1% n=  15 assoc_page_reward=0.9806
- easy_returns_promise      act=  0.0% n=   3 assoc_page_reward=1.0364
- brand_story               act= 10.1% n=1513 assoc_page_reward=1.0822
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.6% n=  83 assoc_page_reward=0.8445
- price_drop_notify         act=  2.7% n= 399 assoc_page_reward=1.1957
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.3% n=  48 assoc_page_reward=1.3356
- similar_items             act= 14.4% n=2161 assoc_page_reward=1.0056
- also_bought               act=  5.5% n= 818 assoc_page_reward=0.8751
- trending_now              act=  0.3% n=  44 assoc_page_reward=0.5404
- personal_recs             act=  1.5% n= 220 assoc_page_reward=0.6592

## Observable feature cohorts
- size_conf      high(n= 621)=0.8779 low(n= 603)=1.1539
- price_sens     high(n= 675)=1.0591 low(n= 446)=0.9585
- return_hist    high(n=  64)=1.1039 low(n=1534)=1.0049
- style_stretch  high(n= 306)=1.1361 low(n= 834)=1.0156
- new            high(n= 545)=1.1220 low(n=1006)=0.9580
- mobile         high(n= 674)=1.0190 low(n= 269)=1.0909
- size_chart     high(n= 346)=1.2404 low(n=1416)=0.9811
- tab_switch     high(n= 503)=1.2221 low(n= 960)=0.9579
- zoom           high(n= 212)=1.2241 low(n= 842)=0.9297
- price_dwell    high(n= 468)=1.0616 low(n= 822)=0.9443
- cart_osc       high(n= 266)=1.3415 low(n=1436)=0.9878
- wishlist       high(n= 435)=1.2539 low(n= 825)=0.9147
- return_view    high(n= 299)=1.1661 low(n=1389)=0.9702
- revisit        high(n= 481)=1.2838 low(n= 815)=0.9331
- price_norm     high(n= 214)=1.0808 low(n= 894)=1.0474

## Most common selected sets
- n= 457: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 214: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n= 200: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 193: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 106: also_bought, brand_story, comparison_card, customers_chose, outfit_completion, similar_items
- n=  82: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  78: also_bought, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n=  76: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, price_drop_notify
- n=  58: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n=  58: also_bought, fit_reassurance, outfit_completion, personal_recs, similar_items, value_breakdown

## Edit history
- action 2500: 14 edits — Shift slot budget away from low-reward default fillers (trending_now 0.551, personal_recs 0.706, also_bought 0.908 assoc page reward, all below the 1.017 mean) toward targeted widgets that show high associated reward but near-zero activation, and open up never-selected widgets serving cohorts that currently underperform (size_conf-high 0.833).
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_parametric_rep1/edits_round_5000.json` with this shape:

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
