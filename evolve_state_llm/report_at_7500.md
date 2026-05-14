# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.8627
- mean oracle reward: 1.9777
- mean regret:        0.1150  (5.8% of oracle)
- cum regret (batch): 287.51

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  premium_silent_browser   143    1.7906    2.1175     15.4%
  paralyzed_wishlister     198    2.5484    2.8462     10.5%
  trend_chaser             115    2.0857    2.3063      9.6%
  size_specific_anxious    120    2.6105    2.8673      9.0%
  returner_from_recent_order   108    2.2790    2.4577      7.3%
  hesitant_first_buyer     287    2.4757    2.6232      5.6%
  outfit_event_planner     192    1.8220    1.9051      4.4%
  corporate_uniform_buyer   126    1.3925    1.4520      4.1%
  post_return_returner     179    2.6714    2.7828      4.0%
  birthday_rush_gifter     142    2.3931    2.4712      3.2%
  tabbed_comparison_shopper   262    1.7710    1.7976      1.5%
  mobile_evening_browser   187    1.0800    1.0869      0.6%
  bargain_hunter_returning   225    1.1833    1.1877      0.4%
  confident_repeat_buyer   216    0.5131    0.5145      0.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      407    1.5993    1.7337      7.8%
  outerwear        231    2.1835    2.3378      6.6%
  bottoms          507    1.9047    2.0195      5.7%
  top              538    1.6968    1.7978      5.6%
  shoes            367    2.0732    2.1880      5.2%
  dress            450    1.9155    2.0100      4.7%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  premium_silent_browser accessories     23    1.4929    1.9398     23.0%
  premium_silent_browser dress           24    1.8610    2.3417     20.5%
  premium_silent_browser outerwear       10    2.2431    2.6939     16.7%
  paralyzed_wishlister   outerwear       17    2.6891    3.2235     16.6%
  trend_chaser           accessories     21    2.4222    2.8803     15.9%
  size_specific_anxious  top             28    2.4249    2.8185     14.0%
  premium_silent_browser top             28    1.5159    1.7578     13.8%
  trend_chaser           outerwear        7    2.0741    2.3901     13.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  customers_chose             14.9      2.68    0.3250
  fit_reassurance             13.8      3.11    0.3096
  easy_returns_promise        13.3      5.33    0.3096
  return_explainer            11.5      4.12    0.2864
  material_deep_dive           9.3      4.27    0.3464
  brand_story                  9.0      2.91    0.2574
  price_drop_notify            7.9      3.13    0.2937
  outfit_completion            7.4      3.69    0.3185
  comparison_card              6.6      2.31    0.3222
  low_return_alts              4.2      1.52    0.3813
  occasion_lookbook            1.1      4.46    0.1482
  wishlist_save                0.7      5.68    0.4218
  style_bridge                 0.2      1.00    0.3470
  value_breakdown              0.0      5.00    0.2820
  size_guide                   0.0      1.00    0.4018
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  expert_pick                  0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  premium_silent_browser  customers_chose(142), easy_returns_promise(130), brand_story(119), price_drop_notify(116), return_explainer(102)
  paralyzed_wishlister    customers_chose(198), price_drop_notify(188), outfit_completion(155), fit_reassurance(152), brand_story(135)
  trend_chaser            brand_story(113), fit_reassurance(111), return_explainer(108), customers_chose(101), easy_returns_promise(85)
  size_specific_anxious   fit_reassurance(120), material_deep_dive(120), easy_returns_promise(120), customers_chose(114), low_return_alts(70)
  returner_from_recent_order  low_return_alts(108), material_deep_dive(108), easy_returns_promise(108), customers_chose(107), outfit_completion(83)
  hesitant_first_buyer    fit_reassurance(286), return_explainer(284), easy_returns_promise(256), comparison_card(251), customers_chose(247)
  outfit_event_planner    customers_chose(192), outfit_completion(192), fit_reassurance(183), return_explainer(177), brand_story(170)
  corporate_uniform_buyer  easy_returns_promise(126), brand_story(122), material_deep_dive(121), customers_chose(120), fit_reassurance(117)
  post_return_returner    fit_reassurance(179), material_deep_dive(179), easy_returns_promise(179), low_return_alts(172), customers_chose(164)
  birthday_rush_gifter    customers_chose(142), outfit_completion(140), easy_returns_promise(139), material_deep_dive(131), fit_reassurance(130)
  tabbed_comparison_shopper  price_drop_notify(262), customers_chose(262), comparison_card(261), easy_returns_promise(259), material_deep_dive(243)
  mobile_evening_browser  outfit_completion(187), fit_reassurance(187), return_explainer(187), easy_returns_promise(187), brand_story(140)
  bargain_hunter_returning  price_drop_notify(225), comparison_card(225), customers_chose(225), fit_reassurance(225), brand_story(204)
  confident_repeat_buyer  fit_reassurance(216), return_explainer(216), easy_returns_promise(216), brand_story(208), occasion_lookbook(111)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 16 edits (round 5000 — activate still-dead widgets for trend_chaser/peer-social and size-anxious/fit cells; dial back round-1 over-corrections on material_deep_dive and easy_returns_promise)