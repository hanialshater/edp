# OBSERVABLE EDP CHECKPOINT — actions 7500 → 10000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.7720
- standard deviation: 0.7315

## Reward by observable category
- accessories  n= 390 mean=1.5644
- bottoms      n= 486 mean=1.8259
- dress        n= 439 mean=1.8804
- outerwear    n= 231 mean=1.9346
- shoes        n= 369 mean=1.9029
- top          n= 585 mean=1.6375

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  7.6% n=1133 assoc_page_reward=1.9546
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act= 13.1% n=1971 assoc_page_reward=1.9078
- comparison_card           act= 13.5% n=2031 assoc_page_reward=1.9220
- customers_chose           act= 14.8% n=2213 assoc_page_reward=1.8659
- value_breakdown           act=  3.0% n= 448 assoc_page_reward=1.5966
- outfit_completion         act= 15.8% n=2370 assoc_page_reward=1.7630
- style_bridge              act=  0.5% n=  73 assoc_page_reward=1.7710
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   0 assoc_page_reward=n/a
- easy_returns_promise      act=  0.0% n=   0 assoc_page_reward=n/a
- brand_story               act= 13.9% n=2083 assoc_page_reward=1.8114
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.5% n=  77 assoc_page_reward=1.2655
- price_drop_notify         act=  7.0% n=1051 assoc_page_reward=1.6855
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.0% n=   0 assoc_page_reward=n/a
- similar_items             act=  8.1% n=1216 assoc_page_reward=1.3381
- also_bought               act=  2.2% n= 334 assoc_page_reward=0.8390
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.0% n=   0 assoc_page_reward=n/a

## Observable feature cohorts
- size_conf      high(n=1136)=1.2914 low(n= 498)=2.4083
- price_sens     high(n= 543)=1.6231 low(n= 801)=1.6049
- return_hist    high(n= 259)=2.4586 low(n=1677)=1.5768
- style_stretch  high(n= 335)=1.7890 low(n=1307)=1.6492
- new            high(n= 473)=2.1010 low(n=1683)=1.6805
- mobile         high(n= 894)=1.8771 low(n= 751)=1.6257
- size_chart     high(n= 607)=2.3975 low(n=1402)=1.4239
- tab_switch     high(n= 891)=2.0279 low(n= 772)=1.1539
- zoom           high(n= 406)=1.8451 low(n= 848)=1.1893
- price_dwell    high(n= 679)=1.7331 low(n=1008)=1.6012
- cart_osc       high(n= 345)=2.4784 low(n=1011)=1.4761
- wishlist       high(n= 596)=1.8960 low(n= 837)=1.6299
- return_view    high(n= 744)=2.2756 low(n= 934)=1.3101
- revisit        high(n= 805)=1.9342 low(n= 853)=1.5681
- price_norm     high(n= 206)=1.7316 low(n= 834)=1.7609

## Most common selected sets
- n= 517: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n= 407: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 324: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 148: comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify, value_breakdown
- n= 124: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n=  81: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  72: also_bought, brand_story, low_return_alts, outfit_completion, price_drop_notify, similar_items
- n=  64: comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion, value_breakdown
- n=  61: also_bought, brand_story, customers_chose, low_return_alts, outfit_completion, similar_items
- n=  56: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, price_drop_notify

## Edit history
- action 2500: 12 edits — Demote generic default widgets with low associated page reward; promote under-activated widgets whose activation or feature cohorts (return_view, return_hist, cart_osc, wishlist) associate with high observed reward.
- action 5000: 10 edits — Continue demoting low-reward defaults (trending_now, personal_recs, also_bought, similar_items); promote above-mean targeted widgets (customers_chose, low_return_alts, fit_reassurance, comparison_card); partially roll back easy_returns_promise which underperformed when it fired.
- action 7500: 10 edits — Final consolidation: keep demoting below-mean widgets (also_bought, similar_items, price_history, easy_returns_promise, style_bridge), keep promoting consistently above-mean widgets (low_return_alts, customers_chose, comparison_card, fit_reassurance), lightly trim price_drop_notify which drifted below mean.