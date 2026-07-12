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