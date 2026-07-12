# OBSERVABLE EDP CHECKPOINT — actions 5000 → 7500
- feedback items matured since previous checkpoint: 2500
- feedback delay: 500 sessions
- observation noise sigma: 0.200

## Aggregate observed reward
- mean: 1.0534
- standard deviation: 0.3891

## Reward by observable category
- accessories  n= 365 mean=0.9614
- bottoms      n= 498 mean=1.0809
- dress        n= 487 mean=1.0819
- outerwear    n= 219 mean=1.1753
- shoes        n= 369 mean=1.0881
- top          n= 562 mean=0.9940

## Widget activation and associated page reward
(Association only: every widget on a page shares the same page reward.)
- fit_reassurance           act=  9.0% n=1357 assoc_page_reward=1.0851
- size_guide                act=  0.3% n=  41 assoc_page_reward=1.0699
- low_return_alts           act=  8.2% n=1225 assoc_page_reward=1.1083
- comparison_card           act= 13.3% n=1994 assoc_page_reward=1.0899
- customers_chose           act= 11.2% n=1674 assoc_page_reward=1.1107
- value_breakdown           act=  4.8% n= 724 assoc_page_reward=0.9914
- outfit_completion         act= 16.4% n=2460 assoc_page_reward=1.0510
- style_bridge              act=  0.1% n=  10 assoc_page_reward=1.2482
- occasion_lookbook         act=  0.0% n=   0 assoc_page_reward=n/a
- return_explainer          act=  0.4% n=  54 assoc_page_reward=0.9953
- easy_returns_promise      act=  0.0% n=   1 assoc_page_reward=1.1845
- brand_story               act=  5.2% n= 777 assoc_page_reward=1.0919
- material_deep_dive        act=  6.5% n= 977 assoc_page_reward=1.0713
- price_history             act=  0.2% n=  25 assoc_page_reward=0.7078
- price_drop_notify         act=  6.5% n= 968 assoc_page_reward=1.1010
- recently_viewed           act=  0.0% n=   0 assoc_page_reward=n/a
- wishlist_save             act=  0.0% n=   0 assoc_page_reward=n/a
- expert_pick               act=  0.1% n=  12 assoc_page_reward=1.3357
- similar_items             act= 13.3% n=1990 assoc_page_reward=0.9824
- also_bought               act=  4.1% n= 611 assoc_page_reward=0.8358
- trending_now              act=  0.0% n=   2 assoc_page_reward=0.5390
- personal_recs             act=  0.7% n=  98 assoc_page_reward=0.6423

## Observable feature cohorts
- size_conf      high(n= 651)=0.8961 low(n= 559)=1.1532
- price_sens     high(n= 669)=1.0470 low(n= 409)=0.9774
- return_hist    high(n=  65)=1.2244 low(n=1533)=0.9958
- style_stretch  high(n= 315)=1.1381 low(n= 830)=1.0141
- new            high(n= 504)=1.1452 low(n=1032)=0.9787
- mobile         high(n= 655)=1.0166 low(n= 285)=1.0993
- size_chart     high(n= 347)=1.2369 low(n=1433)=0.9699
- tab_switch     high(n= 486)=1.2039 low(n= 975)=0.9583
- zoom           high(n= 202)=1.2331 low(n= 841)=0.9352
- price_dwell    high(n= 497)=1.0449 low(n= 843)=0.9582
- cart_osc       high(n= 270)=1.3702 low(n=1403)=0.9883
- wishlist       high(n= 454)=1.2522 low(n= 825)=0.9364
- return_view    high(n= 284)=1.1684 low(n=1411)=0.9731
- revisit        high(n= 458)=1.2891 low(n= 814)=0.9252
- price_norm     high(n= 215)=1.0451 low(n= 849)=1.0357

## Most common selected sets
- n= 188: comparison_card, customers_chose, fit_reassurance, material_deep_dive, outfit_completion, similar_items
- n= 167: comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items, value_breakdown
- n= 164: brand_story, comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items
- n= 113: comparison_card, customers_chose, fit_reassurance, outfit_completion, similar_items, value_breakdown
- n= 103: comparison_card, customers_chose, low_return_alts, material_deep_dive, outfit_completion, similar_items
- n= 100: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, similar_items
- n=  86: brand_story, comparison_card, low_return_alts, outfit_completion, price_drop_notify, similar_items
- n=  72: brand_story, comparison_card, customers_chose, low_return_alts, outfit_completion, price_drop_notify
- n=  71: comparison_card, low_return_alts, material_deep_dive, outfit_completion, price_drop_notify, similar_items
- n=  68: comparison_card, fit_reassurance, material_deep_dive, outfit_completion, price_drop_notify, similar_items

## Edit history
- action 2500: 14 edits — Demote generic defaults with below-mean associated reward; promote starved specialized widgets whose feature cohorts (cart_osc/wishlist/revisit, return_view, zoom, low size_conf) show above-mean observed reward.
- action 5000: 14 edits — Continue demoting the still-below-mean generic widgets and strengthen the specialized widgets whose associated reward and matching high-signal cohorts stay well above the 1.0449 mean but whose activation remains near zero.