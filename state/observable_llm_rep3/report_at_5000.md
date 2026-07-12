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