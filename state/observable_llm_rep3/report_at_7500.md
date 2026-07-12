# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.7916
- standard deviation: 0.7652

## Reward by observable category
- accessories  n= 385 mean=1.6059
- bottoms      n= 516 mean=1.8196
- dress        n= 452 mean=1.8469
- outerwear    n= 238 mean=2.0570
- shoes        n= 384 mean=1.8807
- top          n= 525 mean=1.6672

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act= 11.4% n=1712 assoc_page_reward=1.8336
- size_guide                act=  0.1% n=  17 assoc_page_reward=1.0689
- low_return_alts           act=  3.9% n= 588 assoc_page_reward=2.1194
- comparison_card           act= 13.9% n=2092 assoc_page_reward=1.9541
- customers_chose           act= 13.3% n=2001 assoc_page_reward=1.9761
- value_breakdown           act=  4.1% n= 614 assoc_page_reward=1.5581
- outfit_completion         act= 15.1% n=2264 assoc_page_reward=1.8016
- style_bridge              act=  2.5% n= 371 assoc_page_reward=1.5791
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  6.0% n= 897 assoc_page_reward=2.1004
- easy_returns_promise      act=  0.0% n=   2 assoc_page_reward=0.5235
- brand_story               act= 13.0% n=1953 assoc_page_reward=1.8484
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.4% n=  66 assoc_page_reward=0.9440
- price_drop_notify         act=  7.0% n=1047 assoc_page_reward=1.6763
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.1% n=  12 assoc_page_reward=1.9501
- similar_items             act=  6.8% n=1017 assoc_page_reward=1.2173
- also_bought               act=  2.1% n= 318 assoc_page_reward=0.7000
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.2% n=  29 assoc_page_reward=0.3563

## Observable feature cohorts
- size_conf      high(n=1140)=1.2985 low(n= 497)=2.4245
- price_sens     high(n= 546)=1.6410 low(n= 811)=1.6215
- return_hist    high(n= 249)=2.5280 low(n=1653)=1.5858
- style_stretch  high(n= 310)=1.7230 low(n=1286)=1.6509
- new            high(n= 442)=2.1245 low(n=1707)=1.6915
- mobile         high(n= 887)=1.9107 low(n= 747)=1.6664
- size_chart     high(n= 582)=2.4245 low(n=1415)=1.4284
- tab_switch     high(n= 916)=2.0672 low(n= 758)=1.1346
- zoom           high(n= 343)=1.9104 low(n= 887)=1.2072
- price_dwell    high(n= 672)=1.7603 low(n=1051)=1.5611
- cart_osc       high(n= 375)=2.5105 low(n=1016)=1.4353
- wishlist       high(n= 618)=1.9130 low(n= 870)=1.6414
- return_view    high(n= 736)=2.3462 low(n= 984)=1.2752
- revisit        high(n= 764)=2.0170 low(n= 870)=1.5485
- price_norm     high(n= 229)=1.6992 low(n= 906)=1.8377

## Most common selected sets
- n= 396: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer
- n= 135: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 120: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, price_drop_notify
- n= 120: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n= 114: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 108: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 108: comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer, value_breakdown
- n=  83: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer
- n=  72: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  65: comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer, value_breakdown

## Edit history
- action 2500: 12 edits — Demote low-assoc-reward default fillers; surface never-activating widgets targeting underperforming observable cohorts (size_conf-high, return_view-high, cart_osc-high).
- action 5000: 11 edits — Unblock size_guide (coverage penalty too harsh given worst-cohort size_conf gap), revert price_history boost that backfired, keep demoting low-reward defaults, lean into strong return/cart_osc cohorts.