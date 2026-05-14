# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7476
- mean oracle reward: 1.9777
- mean regret:        0.2301  (11.6% of oracle)
- cum regret (batch): 575.37

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             115    1.8281    2.3063     20.7%
  size_specific_anxious    120    2.2831    2.8673     20.4%
  hesitant_first_buyer     287    2.1527    2.6232     17.9%
  premium_silent_browser   143    1.7650    2.1175     16.6%
  returner_from_recent_order   108    2.0612    2.4577     16.1%
  post_return_returner     179    2.3420    2.7828     15.8%
  corporate_uniform_buyer   126    1.2309    1.4520     15.2%
  birthday_rush_gifter     142    2.2660    2.4712      8.3%
  paralyzed_wishlister     198    2.6165    2.8462      8.1%
  outfit_event_planner     192    1.7620    1.9051      7.5%
  mobile_evening_browser   187    1.0505    1.0869      3.3%
  bargain_hunter_returning   225    1.1718    1.1877      1.3%
  tabbed_comparison_shopper   262    1.7871    1.7976      0.6%
  confident_repeat_buyer   216    0.5144    0.5145      0.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.8765    2.1880     14.2%
  bottoms          507    1.7766    2.0195     12.0%
  outerwear        231    2.0618    2.3378     11.8%
  top              538    1.5965    1.7978     11.2%
  dress            450    1.7923    2.0100     10.8%
  accessories      407    1.5670    1.7337      9.6%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  premium_silent_browser accessories     23    1.3795    1.9398     28.9%
  trend_chaser           accessories     21    2.1522    2.8803     25.3%
  size_specific_anxious  top             28    2.1180    2.8185     24.9%
  hesitant_first_buyer   shoes           48    2.3075    3.0647     24.7%
  trend_chaser           top             30    1.6929    2.2468     24.7%
  corporate_uniform_buyer bottoms         15    1.3247    1.7247     23.2%
  returner_from_recent_order shoes           19    2.2103    2.8524     22.5%
  corporate_uniform_buyer shoes           19    1.6154    2.0604     21.6%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  brand_story                 16.5      2.80    0.2918
  size_guide                  16.2      2.78    0.2920
  return_explainer            16.1      3.22    0.2948
  comparison_card             13.2      2.94    0.3228
  occasion_lookbook            7.9      5.13    0.2898
  price_history                7.7      4.25    0.2383
  customers_chose              6.2      4.63    0.3046
  wishlist_save                5.5      4.23    0.3274
  style_bridge                 5.3      2.51    0.2989
  trending_now                 4.6      5.59    0.2002
  fit_reassurance              0.4      6.00    0.4296
  value_breakdown              0.1      1.06    0.1997
  personal_recs                0.1      6.00    0.0812
  low_return_alts              0.0      1.00    0.3108
  material_deep_dive           0.0      5.50    0.3204
  expert_pick                  0.0      5.00    0.3073
  outfit_completion            0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            brand_story(115), style_bridge(115), size_guide(115), return_explainer(115), occasion_lookbook(76)
  size_specific_anxious   size_guide(120), return_explainer(120), brand_story(120), comparison_card(115), occasion_lookbook(91)
  hesitant_first_buyer    size_guide(287), return_explainer(287), comparison_card(287), brand_story(287), occasion_lookbook(209)
  premium_silent_browser  return_explainer(143), brand_story(142), size_guide(141), comparison_card(129), wishlist_save(109)
  returner_from_recent_order  brand_story(108), return_explainer(105), size_guide(104), comparison_card(104), occasion_lookbook(58)
  post_return_returner    size_guide(179), return_explainer(179), brand_story(179), comparison_card(173), occasion_lookbook(137)
  corporate_uniform_buyer  size_guide(126), return_explainer(126), brand_story(126), comparison_card(121), trending_now(104)
  birthday_rush_gifter    size_guide(142), return_explainer(142), brand_story(142), comparison_card(142), style_bridge(110)
  paralyzed_wishlister    comparison_card(198), wishlist_save(198), size_guide(198), return_explainer(198), brand_story(196)
  outfit_event_planner    style_bridge(192), size_guide(192), brand_story(192), return_explainer(192), comparison_card(192)
  mobile_evening_browser  size_guide(187), return_explainer(187), brand_story(187), style_bridge(185), trending_now(137)
  bargain_hunter_returning  comparison_card(225), price_history(210), brand_story(210), size_guide(204), customers_chose(187)
  tabbed_comparison_shopper  comparison_card(262), return_explainer(262), brand_story(262), price_history(260), size_guide(225)
  confident_repeat_buyer  brand_story(216), size_guide(216), return_explainer(216), trending_now(216), occasion_lookbook(213)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas)
  - session 5000: 16 edits (round 5000 — revive trend/visual widgets for trend_chaser & premium personas, lift size_guide for bottoms/shoes fit, dampen over-firing low-r defaults; robust to noise)