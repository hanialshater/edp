# OBSERVABLE EDP CHECKPOINT — actions 2500 → 5000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.6583
- standard deviation: 0.6934

## Reward by observable category
- accessories  n= 395 mean=1.5229
- bottoms      n= 497 mean=1.6673
- dress        n= 438 mean=1.7314
- outerwear    n= 245 mean=1.8434
- shoes        n= 364 mean=1.7347
- top          n= 561 mean=1.5580

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  8.1% n=1218 assoc_page_reward=1.7982
- size_guide                act=  0.0% n=   0 assoc_page_reward=n/a
- low_return_alts           act=  5.2% n= 777 assoc_page_reward=2.0141
- comparison_card           act= 13.5% n=2030 assoc_page_reward=1.8383
- customers_chose           act= 11.2% n=1673 assoc_page_reward=1.9009
- value_breakdown           act=  2.3% n= 343 assoc_page_reward=1.3560
- outfit_completion         act= 13.3% n=1998 assoc_page_reward=1.6719
- style_bridge              act=  0.2% n=  35 assoc_page_reward=1.9156
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  2.8% n= 424 assoc_page_reward=1.8318
- easy_returns_promise      act=  0.0% n=   2 assoc_page_reward=0.4069
- brand_story               act= 12.7% n=1898 assoc_page_reward=1.6994
- material_deep_dive        act=  0.5% n=  69 assoc_page_reward=1.6650
- price_history             act=  0.3% n=  44 assoc_page_reward=1.4524
- price_drop_notify         act=  6.0% n= 896 assoc_page_reward=1.6805
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.3% n=  42 assoc_page_reward=2.3676
- similar_items             act= 14.0% n=2105 assoc_page_reward=1.5053
- also_bought               act=  6.5% n= 970 assoc_page_reward=1.1288
- trending_now              act=  0.9% n= 133 assoc_page_reward=0.4116
- personal_recs             act=  2.3% n= 343 assoc_page_reward=0.6674

## Observable feature cohorts
- size_conf      high(n=1132)=1.2454 low(n= 491)=2.1028
- price_sens     high(n= 551)=1.5791 low(n= 823)=1.4916
- return_hist    high(n= 258)=2.3224 low(n=1686)=1.4630
- style_stretch  high(n= 285)=1.7099 low(n=1281)=1.5405
- new            high(n= 443)=1.8185 low(n=1725)=1.6030
- mobile         high(n= 869)=1.7138 low(n= 740)=1.5825
- size_chart     high(n= 593)=2.1249 low(n=1399)=1.3925
- tab_switch     high(n= 889)=1.8833 low(n= 761)=1.1101
- zoom           high(n= 387)=1.7053 low(n= 858)=1.1437
- price_dwell    high(n= 693)=1.6290 low(n=1038)=1.4992
- cart_osc       high(n= 335)=2.3819 low(n= 978)=1.3022
- wishlist       high(n= 623)=1.8399 low(n= 876)=1.4446
- return_view    high(n= 781)=2.0230 low(n= 918)=1.2255
- revisit        high(n= 827)=1.8898 low(n= 861)=1.3692
- price_norm     high(n= 215)=1.7060 low(n= 848)=1.6433

## Most common selected sets
- n= 324: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 219: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 118: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  90: also_bought, brand_story, comparison_card, customers_chose, outfit_completion, similar_items
- n=  83: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n=  79: also_bought, brand_story, comparison_card, outfit_completion, price_drop_notify, similar_items
- n=  75: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  75: also_bought, brand_story, outfit_completion, personal_recs, similar_items, trending_now
- n=  73: also_bought, brand_story, fit_reassurance, outfit_completion, personal_recs, similar_items
- n=  67: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, similar_items

## Edit history
- action 2500: 14 edits — Demote low-reward generic defaults that crowd slots; promote never-firing targeted widgets on features whose high cohorts show strong observed reward (cart_osc, return_hist/return_view, size_chart, zoom).