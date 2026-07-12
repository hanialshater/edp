# OBSERVABLE EDP CHECKPOINT — actions 7500 → 10000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.8367
- standard deviation: 0.7436

## Reward by observable category
- accessories  n= 390 mean=1.5859
- bottoms      n= 486 mean=1.8908
- dress        n= 439 mean=1.9418
- outerwear    n= 231 mean=2.0493
- shoes        n= 369 mean=2.0069
- top          n= 585 mean=1.6887

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act= 12.4% n=1861 assoc_page_reward=1.8636
- size_guide                act=  0.2% n=  29 assoc_page_reward=1.1123
- low_return_alts           act=  4.0% n= 594 assoc_page_reward=2.0527
- comparison_card           act= 15.0% n=2256 assoc_page_reward=1.9182
- customers_chose           act= 13.7% n=2051 assoc_page_reward=1.9819
- value_breakdown           act=  4.2% n= 636 assoc_page_reward=1.5774
- outfit_completion         act= 16.2% n=2425 assoc_page_reward=1.8327
- style_bridge              act=  0.7% n= 100 assoc_page_reward=1.7078
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  7.0% n=1056 assoc_page_reward=2.1130
- easy_returns_promise      act=  0.0% n=   0 assoc_page_reward=n/a
- brand_story               act= 12.9% n=1939 assoc_page_reward=1.9154
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.0% n=   1 assoc_page_reward=0.8725
- price_drop_notify         act=  7.1% n=1058 assoc_page_reward=1.6093
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.1% n=  22 assoc_page_reward=1.7553
- expert_pick               act=  0.4% n=  61 assoc_page_reward=1.7015
- similar_items             act=  5.2% n= 780 assoc_page_reward=1.2139
- also_bought               act=  0.9% n= 131 assoc_page_reward=0.6213
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.0% n=   0 assoc_page_reward=n/a

## Observable feature cohorts
- size_conf      high(n=1136)=1.3515 low(n= 498)=2.4630
- price_sens     high(n= 543)=1.6492 low(n= 801)=1.6674
- return_hist    high(n= 259)=2.4631 low(n=1677)=1.6415
- style_stretch  high(n= 335)=1.7591 low(n=1307)=1.7089
- new            high(n= 473)=2.1947 low(n=1683)=1.7322
- mobile         high(n= 894)=1.9452 low(n= 751)=1.7186
- size_chart     high(n= 607)=2.4435 low(n=1402)=1.4625
- tab_switch     high(n= 891)=2.0549 low(n= 772)=1.2326
- zoom           high(n= 406)=1.9184 low(n= 848)=1.2383
- price_dwell    high(n= 679)=1.7724 low(n=1008)=1.6399
- cart_osc       high(n= 345)=2.4798 low(n=1011)=1.5367
- wishlist       high(n= 596)=1.9040 low(n= 837)=1.7481
- return_view    high(n= 744)=2.3594 low(n= 934)=1.2974
- revisit        high(n= 805)=1.9770 low(n= 853)=1.6354
- price_norm     high(n= 206)=1.7858 low(n= 834)=1.8371

## Most common selected sets
- n= 561: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer
- n= 140: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 138: brand_story, comparison_card, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n= 137: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, price_drop_notify
- n= 135: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 129: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n= 115: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 107: comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer, value_breakdown
- n=  87: comparison_card, customers_chose, fit_reassurance, outfit_completion, price_drop_notify, value_breakdown
- n=  85: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer

## Edit history
- action 2500: 12 edits — Demote low-assoc-reward default fillers; surface never-activating widgets targeting underperforming observable cohorts (size_conf-high, return_view-high, cart_osc-high).
- action 5000: 11 edits — Unblock size_guide (coverage penalty too harsh given worst-cohort size_conf gap), revert price_history boost that backfired, keep demoting low-reward defaults, lean into strong return/cart_osc cohorts.
- action 7500: 11 edits — Consolidate: further demote persistently low-assoc defaults, revert style_bridge boost that underperformed, lean into top-assoc return widgets and above-mean expert_pick, keep pushing F32 response for worst cohort (size_conf-high 1.30 vs 2.42).