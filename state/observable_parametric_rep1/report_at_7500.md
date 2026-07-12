# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.0721
- standard deviation: 0.3889

## Reward by observable category
- accessories  n= 365 mean=0.9731
- bottoms      n= 498 mean=1.1046
- dress        n= 487 mean=1.0981
- outerwear    n= 219 mean=1.1872
- shoes        n= 369 mean=1.1101
- top          n= 562 mean=1.0154

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  7.7% n=1155 assoc_page_reward=1.1119
- size_guide                act=  1.4% n= 210 assoc_page_reward=1.1685
- low_return_alts           act=  9.8% n=1477 assoc_page_reward=1.1040
- comparison_card           act= 13.9% n=2085 assoc_page_reward=1.1045
- customers_chose           act= 12.8% n=1927 assoc_page_reward=1.0956
- value_breakdown           act=  6.5% n= 979 assoc_page_reward=1.0459
- outfit_completion         act= 16.5% n=2473 assoc_page_reward=1.0702
- style_bridge              act=  0.1% n=  10 assoc_page_reward=1.2545
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.1% n=  12 assoc_page_reward=0.9096
- easy_returns_promise      act=  0.0% n=   4 assoc_page_reward=1.3465
- brand_story               act=  9.3% n=1395 assoc_page_reward=1.0744
- material_deep_dive        act=  0.0% n=   0 assoc_page_reward=n/a
- price_history             act=  0.1% n=  14 assoc_page_reward=0.8762
- price_drop_notify         act=  2.1% n= 319 assoc_page_reward=1.0390
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  3.5% n= 527 assoc_page_reward=1.1959
- similar_items             act= 13.0% n=1952 assoc_page_reward=1.0105
- also_bought               act=  2.8% n= 423 assoc_page_reward=0.8008
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.3% n=  38 assoc_page_reward=0.6416

## Observable feature cohorts
- size_conf      high(n= 651)=0.9036 low(n= 559)=1.1918
- price_sens     high(n= 669)=1.0735 low(n= 409)=0.9900
- return_hist    high(n=  65)=1.2575 low(n=1533)=1.0073
- style_stretch  high(n= 315)=1.1452 low(n= 830)=1.0401
- new            high(n= 504)=1.1974 low(n=1032)=0.9898
- mobile         high(n= 655)=1.0426 low(n= 285)=1.1097
- size_chart     high(n= 347)=1.2815 low(n=1433)=0.9807
- tab_switch     high(n= 486)=1.2272 low(n= 975)=0.9803
- zoom           high(n= 202)=1.2644 low(n= 841)=0.9454
- price_dwell    high(n= 497)=1.0672 low(n= 843)=0.9766
- cart_osc       high(n= 270)=1.3583 low(n=1403)=1.0059
- wishlist       high(n= 454)=1.2564 low(n= 825)=0.9580
- return_view    high(n= 284)=1.1821 low(n=1411)=0.9879
- revisit        high(n= 458)=1.2870 low(n= 814)=0.9450
- price_norm     high(n= 215)=1.0657 low(n= 849)=1.0531

## Most common selected sets
- n= 324: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 279: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 252: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 151: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n=  91: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion
- n=  85: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, size_guide
- n=  79: comparison_card, customers_chose, expert_pick, fit_reassurance, outfit_completion, similar_items
- n=  77: comparison_card, customers_chose, expert_pick, low_return_alts, outfit_completion, similar_items
- n=  50: comparison_card, customers_chose, expert_pick, low_return_alts, outfit_completion, value_breakdown
- n=  47: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items

## Edit history
- action 2500: 14 edits — Shift slot budget away from low-reward default fillers (trending_now 0.551, personal_recs 0.706, also_bought 0.908 assoc page reward, all below the 1.017 mean) toward targeted widgets that show high associated reward but near-zero activation, and open up never-selected widgets serving cohorts that currently underperform (size_conf-high 0.833).
- action 5000: 14 edits — Continue draining low-reward defaults (trending_now 0.540, personal_recs 0.659, also_bought 0.875), revert the price_history boost that landed at 0.845 assoc reward, and push harder on high-reward under-activated widgets (expert_pick 1.336, low_return_alts 1.148, price_drop_notify 1.196). size_guide still never fires while the size_conf-high cohort trails 0.878 vs 1.154, so raise its remaining-weight and soften its coverage penalty so it can co-appear with fit_reassurance.