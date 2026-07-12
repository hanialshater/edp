# OBSERVABLE EDP CHECKPOINT — actions 7500 → 10000
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.7545
- standard deviation: 0.7028

## Reward by observable category
- accessories  n= 390 mean=1.5155
- bottoms      n= 486 mean=1.8172
- dress        n= 439 mean=1.8583
- outerwear    n= 231 mean=1.9456
- shoes        n= 369 mean=1.8893
- top          n= 585 mean=1.6232

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  9.8% n=1476 assoc_page_reward=1.8125
- size_guide                act=  0.1% n=  10 assoc_page_reward=1.4931
- low_return_alts           act=  4.5% n= 678 assoc_page_reward=2.1417
- comparison_card           act= 14.5% n=2179 assoc_page_reward=1.8820
- customers_chose           act= 12.4% n=1862 assoc_page_reward=1.8698
- value_breakdown           act=  0.2% n=  32 assoc_page_reward=0.8285
- outfit_completion         act= 14.7% n=2198 assoc_page_reward=1.7631
- style_bridge              act=  1.0% n= 149 assoc_page_reward=1.6578
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  4.9% n= 735 assoc_page_reward=1.9197
- easy_returns_promise      act=  1.6% n= 237 assoc_page_reward=1.7845
- brand_story               act= 12.0% n=1799 assoc_page_reward=1.7230
- material_deep_dive        act=  0.6% n=  93 assoc_page_reward=1.8007
- price_history             act=  2.7% n= 402 assoc_page_reward=1.6026
- price_drop_notify         act=  4.3% n= 646 assoc_page_reward=1.4538
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  5.1% n= 770 assoc_page_reward=2.0513
- similar_items             act=  8.7% n=1312 assoc_page_reward=1.3830
- also_bought               act=  2.6% n= 389 assoc_page_reward=0.8936
- trending_now              act=  0.0% n=   0 assoc_page_reward=n/a
- personal_recs             act=  0.2% n=  33 assoc_page_reward=0.5320

## Observable feature cohorts
- size_conf      high(n=1136)=1.3227 low(n= 498)=2.3186
- price_sens     high(n= 543)=1.5923 low(n= 801)=1.6203
- return_hist    high(n= 259)=2.3611 low(n=1677)=1.5702
- style_stretch  high(n= 335)=1.7355 low(n=1307)=1.6369
- new            high(n= 473)=2.0208 low(n=1683)=1.6760
- mobile         high(n= 894)=1.8186 low(n= 751)=1.6711
- size_chart     high(n= 607)=2.3061 low(n=1402)=1.4303
- tab_switch     high(n= 891)=1.9687 low(n= 772)=1.2035
- zoom           high(n= 406)=1.8794 low(n= 848)=1.1915
- price_dwell    high(n= 679)=1.7016 low(n=1008)=1.5950
- cart_osc       high(n= 345)=2.3940 low(n=1011)=1.4561
- wishlist       high(n= 596)=1.8455 low(n= 837)=1.6545
- return_view    high(n= 744)=2.2338 low(n= 934)=1.2715
- revisit        high(n= 805)=1.9049 low(n= 853)=1.5341
- price_norm     high(n= 206)=1.7310 low(n= 834)=1.7361

## Most common selected sets
- n= 174: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n= 158: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 136: brand_story, comparison_card, customers_chose, easy_returns_promise, fit_reassurance, outfit_completion
- n= 125: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, return_explainer
- n=  81: comparison_card, customers_chose, expert_pick, fit_reassurance, low_return_alts, outfit_completion
- n=  79: also_bought, brand_story, fit_reassurance, outfit_completion, price_drop_notify, similar_items
- n=  77: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, return_explainer
- n=  71: brand_story, comparison_card, customers_chose, outfit_completion, price_drop_notify, similar_items
- n=  70: brand_story, comparison_card, customers_chose, expert_pick, low_return_alts, outfit_completion
- n=  59: brand_story, comparison_card, customers_chose, fit_reassurance, low_return_alts, outfit_completion

## Edit history
- action 2500: 14 edits — Demote low-reward generic defaults that crowd slots; promote never-firing targeted widgets on features whose high cohorts show strong observed reward (cart_osc, return_hist/return_view, size_chart, zoom).
- action 5000: 13 edits — Continue demoting persistently low-reward defaults; amplify expert_pick (assoc 2.37 at 0.3%), unblock size_guide via smaller coverage penalty, and reinforce returns/outfit widgets that matured well.
- action 7500: 12 edits — Shift share toward the consistently high-reward targeted widgets (low_return_alts, expert_pick, easy_returns_promise, customers_chose); keep squeezing degrading defaults; partially revert the style_bridge boost and rebalance F51 toward expert_pick.