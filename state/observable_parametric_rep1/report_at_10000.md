# OBSERVABLE EDP CHECKPOINT — actions 7500 → 10000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.0805
- standard deviation: 0.3862

## Reward by observable category
- accessories  n= 371 mean=0.9657
- bottoms      n= 482 mean=1.1111
- dress        n= 464 mean=1.0830
- outerwear    n= 263 mean=1.2338
- shoes        n= 374 mean=1.1698
- top          n= 546 mean=0.9944

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  6.1% n= 916 assoc_page_reward=1.1183
- size_guide                act=  2.3% n= 347 assoc_page_reward=1.1496
- low_return_alts           act= 11.8% n=1769 assoc_page_reward=1.1047
- comparison_card           act= 15.0% n=2251 assoc_page_reward=1.1026
- customers_chose           act= 13.3% n=1989 assoc_page_reward=1.0881
- value_breakdown           act=  7.4% n=1108 assoc_page_reward=1.0599
- outfit_completion         act= 14.4% n=2162 assoc_page_reward=1.0870
- style_bridge              act=  2.8% n= 427 assoc_page_reward=1.0669
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.0% n=   1 assoc_page_reward=0.8213
- easy_returns_promise      act=  0.0% n=   1 assoc_page_reward=1.3972
- brand_story               act=  8.1% n=1221 assoc_page_reward=1.0760
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.0% n=   0 assoc_page_reward=n/a
- price_drop_notify         act=  0.8% n= 113 assoc_page_reward=1.0095
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  6.2% n= 933 assoc_page_reward=1.1620
- similar_items             act= 10.6% n=1588 assoc_page_reward=0.9866
- also_bought               act=  1.1% n= 172 assoc_page_reward=0.7049
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.0% n=   2 assoc_page_reward=0.9647

## Observable feature cohorts
- size_conf      high(n= 649)=0.8860 low(n= 564)=1.2452
- price_sens     high(n= 695)=1.0769 low(n= 426)=0.9428
- return_hist    high(n=  80)=1.1984 low(n=1521)=1.0103
- style_stretch  high(n= 282)=1.1580 low(n= 923)=1.0701
- new            high(n= 496)=1.2225 low(n=1008)=0.9898
- mobile         high(n= 690)=1.0541 low(n= 274)=1.1398
- size_chart     high(n= 340)=1.2959 low(n=1413)=0.9799
- tab_switch     high(n= 508)=1.2191 low(n= 962)=0.9849
- zoom           high(n= 220)=1.2589 low(n= 845)=0.9378
- price_dwell    high(n= 498)=1.0690 low(n= 786)=0.9641
- cart_osc       high(n= 282)=1.3605 low(n=1387)=1.0138
- wishlist       high(n= 484)=1.2406 low(n= 762)=0.9576
- return_view    high(n= 293)=1.1829 low(n=1353)=0.9917
- revisit        high(n= 512)=1.2851 low(n= 807)=0.9515
- price_norm     high(n= 205)=1.0814 low(n= 895)=1.0734

## Most common selected sets
- n= 224: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 220: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 142: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 139: comparison_card, customers_chose, expert_pick, low_return_alts, outfit_completion, value_breakdown
- n= 124: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n= 117: comparison_card, customers_chose, expert_pick, low_return_alts, outfit_completion, similar_items
- n= 112: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, size_guide
- n=  81: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  80: brand_story, comparison_card, customers_chose, expert_pick, low_return_alts, outfit_completion
- n=  68: brand_story, comparison_card, customers_chose, low_return_alts, similar_items, style_bridge

## Edit history
- action 2500: 14 edits — Shift slot budget away from low-reward default fillers (trending_now 0.551, personal_recs 0.706, also_bought 0.908 assoc page reward, all below the 1.017 mean) toward targeted widgets that show high associated reward but near-zero activation, and open up never-selected widgets serving cohorts that currently underperform (size_conf-high 0.833).
- action 5000: 14 edits — Continue draining low-reward defaults (trending_now 0.540, personal_recs 0.659, also_bought 0.875), revert the price_history boost that landed at 0.845 assoc reward, and push harder on high-reward under-activated widgets (expert_pick 1.336, low_return_alts 1.148, price_drop_notify 1.196). size_guide still never fires while the size_conf-high cohort trails 0.878 vs 1.154, so raise its remaining-weight and soften its coverage penalty so it can co-appear with fit_reassurance.
- action 7500: 13 edits — Consolidate: keep cutting below-mean fillers (also_bought 0.801, personal_recs 0.642, similar_items 1.010 vs mean 1.072), roll back boosts that landed below mean (return_explainer 0.910, price_history 0.876, price_drop_notify 1.039), and reinforce what worked: size_guide now activates at 1.4% with 1.169 assoc reward while size_conf-high still trails (0.904 vs 1.192), expert_pick scaled to 3.5% at 1.196, style_bridge shows 1.255 on early activations.