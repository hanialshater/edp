# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8251
- mean oracle reward: 2.0225
- mean regret:        0.1975  (9.8% of oracle)
- cum regret (batch): 493.64

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             105    1.9337    2.3312     17.1%
  paralyzed_wishlister     172    2.4744    2.8495     13.2%
  hesitant_first_buyer     336    2.2806    2.6004     12.3%
  size_specific_anxious    114    2.5646    2.9005     11.6%
  premium_silent_browser   177    1.8672    2.1053     11.3%
  returner_from_recent_order   121    2.1841    2.4114      9.4%
  post_return_returner     198    2.5465    2.8039      9.2%
  outfit_event_planner     212    1.7628    1.9123      7.8%
  corporate_uniform_buyer    81    1.3493    1.4618      7.7%
  birthday_rush_gifter     149    2.3138    2.4820      6.8%
  mobile_evening_browser   190    1.0234    1.0955      6.6%
  tabbed_comparison_shopper   240    1.7111    1.8258      6.3%
  bargain_hunter_returning   223    1.1333    1.1832      4.2%
  confident_repeat_buyer   182    0.4989    0.5144      3.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      362    1.4895    1.7287     13.8%
  outerwear        242    2.0904    2.3259     10.1%
  top              575    1.6049    1.7847     10.1%
  dress            441    1.9046    2.1134      9.9%
  bottoms          495    1.9245    2.0960      8.2%
  shoes            385    2.0836    2.2647      8.0%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             28    1.7204    2.2468     23.4%
  corporate_uniform_buyer accessories     14    0.6440    0.8284     22.3%
  premium_silent_browser accessories     24    1.5256    1.9398     21.4%
  hesitant_first_buyer   accessories     55    1.5412    1.9259     20.0%
  size_specific_anxious  accessories     15    1.8195    2.2723     19.9%
  trend_chaser           shoes           11    1.6297    2.0259     19.6%
  paralyzed_wishlister   accessories     20    2.3066    2.8308     18.5%
  post_return_returner   accessories     28    1.7140    2.0918     18.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  easy_returns_promise        11.6      5.18    0.3095
  fit_reassurance             11.0      2.54    0.3486
  style_bridge                 8.9      2.80    0.2995
  return_explainer             8.3      2.97    0.2640
  expert_pick                  8.3      4.02    0.2958
  customers_chose              7.1      3.44    0.3528
  low_return_alts              6.6      3.06    0.3689
  value_breakdown              6.1      2.62    0.3108
  comparison_card              5.5      1.95    0.3099
  size_guide                   5.3      4.77    0.3366
  occasion_lookbook            4.6      4.20    0.2248
  material_deep_dive           4.2      3.99    0.2862
  brand_story                  4.1      3.33    0.2837
  price_drop_notify            3.9      3.18    0.2602
  price_history                3.1      4.35    0.2465
  recently_viewed              1.4      4.80    0.1385
  wishlist_save                0.0      3.60    0.1924
  outfit_completion            0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            style_bridge(105), occasion_lookbook(105), brand_story(95), fit_reassurance(86), price_drop_notify(68)
  paralyzed_wishlister    expert_pick(172), customers_chose(154), fit_reassurance(149), comparison_card(124), style_bridge(124)
  hesitant_first_buyer    fit_reassurance(336), low_return_alts(331), easy_returns_promise(302), value_breakdown(287), size_guide(218)
  size_specific_anxious   fit_reassurance(114), low_return_alts(114), easy_returns_promise(112), customers_chose(92), expert_pick(89)
  premium_silent_browser  easy_returns_promise(177), return_explainer(176), expert_pick(166), material_deep_dive(155), fit_reassurance(138)
  returner_from_recent_order  fit_reassurance(121), easy_returns_promise(118), style_bridge(97), customers_chose(96), return_explainer(76)
  post_return_returner    fit_reassurance(198), easy_returns_promise(198), low_return_alts(196), size_guide(183), customers_chose(163)
  outfit_event_planner    style_bridge(212), customers_chose(190), occasion_lookbook(184), brand_story(180), return_explainer(140)
  corporate_uniform_buyer  fit_reassurance(81), size_guide(81), easy_returns_promise(81), expert_pick(68), return_explainer(53)
  birthday_rush_gifter    fit_reassurance(149), style_bridge(149), customers_chose(117), low_return_alts(115), easy_returns_promise(114)
  mobile_evening_browser  style_bridge(190), occasion_lookbook(189), brand_story(129), return_explainer(97), fit_reassurance(94)
  tabbed_comparison_shopper  return_explainer(240), expert_pick(240), comparison_card(227), price_history(216), price_drop_notify(197)
  bargain_hunter_returning  price_history(206), expert_pick(204), comparison_card(173), return_explainer(153), value_breakdown(131)
  confident_repeat_buyer  easy_returns_promise(176), recently_viewed(142), return_explainer(136), occasion_lookbook(132), style_bridge(118)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1])
  - session 2500: 16 edits (round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2])
  - session 5000: 16 edits (round 5000 draw1 — revive dead widgets (size_guide, occasion_lookbook, personal_recs, trending_now), tame over-firing low-reward widgets, boost confident_repeat/trend_chaser cells, add F32->F46 and F43->F33 synergies  [ensemble-best of 3: draw 1])
  - session 7500: 14 edits (round 7500 draw1 — stabilization: revive truly dead widgets (return_explainer/wishlist_save/price_drop_notify), trim over-firing low r/fire (occasion_lookbook, personal_recs), patch worst cells (confident_repeat shoes/bottoms, size_specific accessories, premium shoes)  [ensemble-best of 3: draw 1])