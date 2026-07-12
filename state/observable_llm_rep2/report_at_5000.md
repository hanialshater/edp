# OBSERVABLE EDP CHECKPOINT — actions 2500 → 5000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.6471
- standard deviation: 0.6912

## Reward by observable category
- accessories  n= 395 mean=1.5279
- bottoms      n= 497 mean=1.6554
- dress        n= 438 mean=1.7166
- outerwear    n= 245 mean=1.8387
- shoes        n= 364 mean=1.7129
- top          n= 561 mean=1.5431

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  6.3% n= 943 assoc_page_reward=1.7918
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  9.8% n=1475 assoc_page_reward=1.8963
- comparison_card           act= 13.0% n=1947 assoc_page_reward=1.8290
- customers_chose           act= 11.4% n=1717 assoc_page_reward=1.8788
- value_breakdown           act=  2.9% n= 436 assoc_page_reward=1.4288
- outfit_completion         act= 12.8% n=1919 assoc_page_reward=1.6724
- style_bridge              act=  1.1% n= 169 assoc_page_reward=1.6704
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   0 assoc_page_reward=n/a
- easy_returns_promise      act=  0.1% n=  19 assoc_page_reward=0.6642
- brand_story               act= 13.1% n=1959 assoc_page_reward=1.6835
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.0% n=   2 assoc_page_reward=1.0606
- price_drop_notify         act=  6.3% n= 946 assoc_page_reward=1.6818
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.0% n=   0 assoc_page_reward=n/a
- similar_items             act= 13.9% n=2079 assoc_page_reward=1.4856
- also_bought               act=  6.6% n= 983 assoc_page_reward=1.1044
- trending_now              act=  0.7% n=  98 assoc_page_reward=0.4431
- personal_recs             act=  2.1% n= 308 assoc_page_reward=0.6392

## Observable feature cohorts
- size_conf      high(n=1132)=1.2180 low(n= 491)=2.1308
- price_sens     high(n= 551)=1.5731 low(n= 823)=1.4777
- return_hist    high(n= 258)=2.3031 low(n=1686)=1.4640
- style_stretch  high(n= 285)=1.7116 low(n=1281)=1.5201
- new            high(n= 443)=1.8368 low(n=1725)=1.5830
- mobile         high(n= 869)=1.7263 low(n= 740)=1.5313
- size_chart     high(n= 593)=2.1414 low(n=1399)=1.3726
- tab_switch     high(n= 889)=1.8932 low(n= 761)=1.0726
- zoom           high(n= 387)=1.6702 low(n= 858)=1.1338
- price_dwell    high(n= 693)=1.6286 low(n=1038)=1.4933
- cart_osc       high(n= 335)=2.3980 low(n= 978)=1.3067
- wishlist       high(n= 623)=1.8391 low(n= 876)=1.4262
- return_view    high(n= 781)=2.0349 low(n= 918)=1.2432
- revisit        high(n= 827)=1.8645 low(n= 861)=1.3869
- price_norm     high(n= 215)=1.6965 low(n= 848)=1.6342

## Most common selected sets
- n= 311: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 192: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n= 182: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 147: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  80: also_bought, brand_story, comparison_card, low_return_alts, price_drop_notify, similar_items
- n=  77: also_bought, brand_story, comparison_card, customers_chose, outfit_completion, similar_items
- n=  70: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  65: also_bought, brand_story, comparison_card, outfit_completion, price_drop_notify, similar_items
- n=  63: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, similar_items
- n=  61: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items

## Edit history
- action 2500: 12 edits — Demote generic default widgets with low associated page reward; promote under-activated widgets whose activation or feature cohorts (return_view, return_hist, cart_osc, wishlist) associate with high observed reward.