# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8166
- mean oracle reward: 2.0225
- mean regret:        0.2059  (10.2% of oracle)
- cum regret (batch): 514.75

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             105    1.8903    2.3312     18.9%
  premium_silent_browser   177    1.7498    2.1053     16.9%
  returner_from_recent_order   121    2.0328    2.4114     15.7%
  corporate_uniform_buyer    81    1.2660    1.4618     13.4%
  size_specific_anxious    114    2.5480    2.9005     12.2%
  hesitant_first_buyer     336    2.3079    2.6004     11.2%
  outfit_event_planner     212    1.7166    1.9123     10.2%
  post_return_returner     198    2.5405    2.8039      9.4%
  paralyzed_wishlister     172    2.6037    2.8495      8.6%
  tabbed_comparison_shopper   240    1.6968    1.8258      7.1%
  mobile_evening_browser   190    1.0317    1.0955      5.8%
  bargain_hunter_returning   223    1.1317    1.1832      4.4%
  birthday_rush_gifter     149    2.3940    2.4820      3.5%
  confident_repeat_buyer   182    0.5044    0.5144      1.9%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      362    1.5146    1.7287     12.4%
  top              575    1.6014    1.7847     10.3%
  dress            441    1.8995    2.1134     10.1%
  bottoms          495    1.8854    2.0960     10.0%
  outerwear        242    2.1016    2.3259      9.6%
  shoes            385    2.0596    2.2647      9.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           accessories     17    2.1360    2.8803     25.8%
  trend_chaser           top             28    1.6925    2.2468     24.7%
  premium_silent_browser accessories     24    1.4854    1.9398     23.4%
  premium_silent_browser dress           27    1.8308    2.3417     21.8%
  returner_from_recent_order top             26    1.6553    2.0668     19.9%
  corporate_uniform_buyer bottoms         15    1.3823    1.7247     19.9%
  returner_from_recent_order bottoms         27    2.1275    2.6170     18.7%
  size_specific_anxious  top             23    2.3068    2.8185     18.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  wishlist_save               12.8      3.49    0.2806
  fit_reassurance             12.1      3.51    0.3014
  value_breakdown             11.6      2.08    0.2795
  easy_returns_promise        10.1      5.51    0.2939
  style_bridge                10.0      3.11    0.2899
  return_explainer             9.5      4.19    0.2816
  customers_chose              9.4      3.11    0.3343
  comparison_card              7.6      3.95    0.3168
  material_deep_dive           5.6      4.45    0.3467
  low_return_alts              4.4      1.70    0.3644
  brand_story                  3.1      3.46    0.2977
  expert_pick                  2.8      3.04    0.3071
  size_guide                   0.9      1.06    0.3769
  outfit_completion            0.1      5.76    0.3417
  price_drop_notify            0.0      1.00    0.3943
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            style_bridge(105), fit_reassurance(101), wishlist_save(87), brand_story(80), expert_pick(77)
  premium_silent_browser  value_breakdown(177), wishlist_save(166), expert_pick(159), easy_returns_promise(136), return_explainer(122)
  returner_from_recent_order  low_return_alts(121), wishlist_save(101), material_deep_dive(98), style_bridge(95), comparison_card(71)
  corporate_uniform_buyer  easy_returns_promise(81), wishlist_save(77), material_deep_dive(77), value_breakdown(55), low_return_alts(54)
  size_specific_anxious   fit_reassurance(114), wishlist_save(108), easy_returns_promise(104), material_deep_dive(102), customers_chose(84)
  hesitant_first_buyer    return_explainer(329), value_breakdown(317), comparison_card(289), fit_reassurance(269), customers_chose(243)
  outfit_event_planner    style_bridge(212), wishlist_save(198), customers_chose(189), fit_reassurance(189), brand_story(149)
  post_return_returner    fit_reassurance(196), easy_returns_promise(192), low_return_alts(185), wishlist_save(169), material_deep_dive(169)
  paralyzed_wishlister    customers_chose(171), wishlist_save(170), value_breakdown(168), style_bridge(164), fit_reassurance(108)
  tabbed_comparison_shopper  value_breakdown(240), customers_chose(240), wishlist_save(240), easy_returns_promise(238), return_explainer(191)
  mobile_evening_browser  style_bridge(190), wishlist_save(190), fit_reassurance(190), return_explainer(188), easy_returns_promise(176)
  bargain_hunter_returning  value_breakdown(223), customers_chose(223), wishlist_save(223), fit_reassurance(217), style_bridge(181)
  birthday_rush_gifter    style_bridge(146), material_deep_dive(141), fit_reassurance(117), return_explainer(113), easy_returns_promise(107)
  confident_repeat_buyer  fit_reassurance(181), return_explainer(172), value_breakdown(166), wishlist_save(164), easy_returns_promise(160)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 16 edits (round 5000 — activate still-dead widgets for trend_chaser/peer-social and size-anxious/fit cells; dial back round-1 over-corrections on material_deep_dive and easy_returns_promise)
  - session 7500: 14 edits (round 7500 — STABILIZATION: revive wishlist_save/expert_pick/value_breakdown for paralyzed_wishlister & premium_silent_browser, dial back brand_story overshoot, trim still-firing defaults)