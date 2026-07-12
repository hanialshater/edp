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
      "F32": 2.4
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
    "base": 0.15,
    "on_rem": {},
    "on_cov": {},
    "slot_decay": 0.04,
    "type": "default"
  }
}
```

# Prior edits

- action 2500: 12 edits — Demote low-assoc-reward default fillers; surface never-activating widgets targeting underperforming observable cohorts (size_conf-high, return_view-high, cart_osc-high).

# Observable delayed-feedback report

```
# OBSERVABLE EDP CHECKPOINT — actions 2500 → 5000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.6912
- standard deviation: 0.7055

## Reward by observable category
- accessories  n= 395 mean=1.5530
- bottoms      n= 497 mean=1.7035
- dress        n= 438 mean=1.7618
- outerwear    n= 245 mean=1.9052
- shoes        n= 364 mean=1.7729
- top          n= 561 mean=1.5761

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  8.9% n=1329 assoc_page_reward=1.7973
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  5.7% n= 856 assoc_page_reward=2.0475
- comparison_card           act= 13.1% n=1960 assoc_page_reward=1.8765
- customers_chose           act= 12.9% n=1935 assoc_page_reward=1.8876
- value_breakdown           act=  3.7% n= 557 assoc_page_reward=1.5299
- outfit_completion         act= 13.4% n=2015 assoc_page_reward=1.7279
- style_bridge              act=  1.8% n= 275 assoc_page_reward=1.6160
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  2.8% n= 413 assoc_page_reward=1.8507
- easy_returns_promise      act=  0.0% n=   0 assoc_page_reward=n/a
- brand_story               act= 12.6% n=1895 assoc_page_reward=1.7505
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  1.2% n= 174 assoc_page_reward=0.9232
- price_drop_notify         act=  5.0% n= 748 assoc_page_reward=1.7675
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.1% n=  15 assoc_page_reward=1.4934
- similar_items             act= 11.8% n=1773 assoc_page_reward=1.4398
- also_bought               act=  5.2% n= 777 assoc_page_reward=1.0545
- trending_now              act=  0.5% n=  72 assoc_page_reward=0.5235
- personal_recs             act=  1.4% n= 206 assoc_page_reward=0.5908

## Observable feature cohorts
- size_conf      high(n=1132)=1.2614 low(n= 491)=2.1885
- price_sens     high(n= 551)=1.6017 low(n= 823)=1.5273
- return_hist    high(n= 258)=2.3461 low(n=1686)=1.5062
- style_stretch  high(n= 285)=1.7354 low(n=1281)=1.5662
- new            high(n= 443)=1.8773 low(n=1725)=1.6187
- mobile         high(n= 869)=1.7699 low(n= 740)=1.5841
- size_chart     high(n= 593)=2.2027 low(n=1399)=1.4099
- tab_switch     high(n= 889)=1.9228 low(n= 761)=1.1257
- zoom           high(n= 387)=1.7493 low(n= 858)=1.1677
- price_dwell    high(n= 693)=1.6673 low(n=1038)=1.5296
- cart_osc       high(n= 335)=2.4153 low(n= 978)=1.3293
- wishlist       high(n= 623)=1.8620 low(n= 876)=1.4790
- return_view    high(n= 781)=2.0893 low(n= 918)=1.2491
- revisit        high(n= 827)=1.9063 low(n= 861)=1.4307
- price_norm     high(n= 215)=1.7323 low(n= 848)=1.6863

## Most common selected sets
- n= 221: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 221: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 217: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  85: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n=  77: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, price_drop_notify
- n=  65: brand_story, comparison_card, customers_chose, fit_reassurance, similar_items, style_bridge
- n=  59: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  58: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n=  58: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer
- n=  55: also_bought, comparison_card, customers_chose, outfit_completion, similar_items, value_breakdown

## Edit history
- action 2500: 12 edits — Demote low-assoc-reward default fillers; surface never-activating widgets targeting underperforming observable cohorts (size_conf-high, return_view-high, cart_osc-high).
```

# Task

Propose at most 16 conservative scalar edits. Each edit changes one field and
must be justified by an observable pattern in the report. Do not claim to know
latent personas, true needs, provisions, oracle pages, or regret.

Write JSON to `state/observable_llm_rep3/edits_round_5000.json` with this shape:

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
