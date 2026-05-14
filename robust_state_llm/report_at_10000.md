# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8549
- mean oracle reward: 2.0225
- mean regret:        0.1676  (8.3% of oracle)
- cum regret (batch): 419.08

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             105    1.7930    2.3312     23.1%
  size_specific_anxious    114    2.4905    2.9005     14.1%
  hesitant_first_buyer     336    2.3023    2.6004     11.5%
  premium_silent_browser   177    1.8739    2.1053     11.0%
  post_return_returner     198    2.5006    2.8039     10.8%
  paralyzed_wishlister     172    2.5680    2.8495      9.9%
  corporate_uniform_buyer    81    1.3512    1.4618      7.6%
  returner_from_recent_order   121    2.2397    2.4114      7.1%
  outfit_event_planner     212    1.8462    1.9123      3.5%
  tabbed_comparison_shopper   240    1.7717    1.8258      3.0%
  mobile_evening_browser   190    1.0810    1.0955      1.3%
  bargain_hunter_returning   223    1.1701    1.1832      1.1%
  birthday_rush_gifter     149    2.4563    2.4820      1.0%
  confident_repeat_buyer   182    0.5144    0.5144      0.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      362    1.5488    1.7287     10.4%
  top              575    1.6180    1.7847      9.3%
  dress            441    1.9422    2.1134      8.1%
  shoes            385    2.0910    2.2647      7.7%
  bottoms          495    1.9395    2.0960      7.5%
  outerwear        242    2.1678    2.3259      6.8%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             28    1.5846    2.2468     29.5%
  trend_chaser           accessories     17    2.1719    2.8803     24.6%
  trend_chaser           shoes           11    1.5836    2.0259     21.8%
  size_specific_anxious  accessories     15    1.7785    2.2723     21.7%
  trend_chaser           bottoms         16    1.3581    1.7276     21.4%
  premium_silent_browser accessories     24    1.5598    1.9398     19.6%
  size_specific_anxious  top             23    2.2726    2.8185     19.4%
  trend_chaser           dress           23    2.0881    2.5686     18.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  return_explainer            16.4      3.78    0.3088
  expert_pick                 15.0      4.33    0.3047
  comparison_card             14.1      3.08    0.3337
  material_deep_dive          14.1      2.25    0.3149
  outfit_completion           10.7      5.00    0.3152
  fit_reassurance              9.9      2.14    0.3713
  size_guide                   7.9      3.70    0.2482
  price_history                7.2      4.33    0.2508
  style_bridge                 3.3      1.51    0.2696
  customers_chose              1.3      5.93    0.3147
  value_breakdown              0.1      1.12    0.2002
  trending_now                 0.0      6.00    0.2175
  low_return_alts              0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            style_bridge(105), material_deep_dive(105), return_explainer(104), expert_pick(104), size_guide(81)
  size_specific_anxious   fit_reassurance(114), return_explainer(114), expert_pick(114), material_deep_dive(112), comparison_card(109)
  hesitant_first_buyer    fit_reassurance(336), comparison_card(336), return_explainer(336), material_deep_dive(336), outfit_completion(335)
  premium_silent_browser  return_explainer(177), expert_pick(177), material_deep_dive(175), comparison_card(174), outfit_completion(131)
  post_return_returner    fit_reassurance(198), return_explainer(198), expert_pick(196), material_deep_dive(185), comparison_card(183)
  paralyzed_wishlister    comparison_card(172), expert_pick(172), outfit_completion(163), fit_reassurance(151), return_explainer(149)
  corporate_uniform_buyer  material_deep_dive(81), return_explainer(81), expert_pick(81), comparison_card(81), outfit_completion(72)
  returner_from_recent_order  material_deep_dive(121), return_explainer(121), comparison_card(119), expert_pick(119), outfit_completion(113)
  outfit_event_planner    material_deep_dive(212), comparison_card(212), expert_pick(212), return_explainer(212), style_bridge(162)
  tabbed_comparison_shopper  comparison_card(240), return_explainer(239), price_history(238), expert_pick(237), fit_reassurance(175)
  mobile_evening_browser  size_guide(190), return_explainer(190), material_deep_dive(190), style_bridge(181), expert_pick(162)
  bargain_hunter_returning  comparison_card(223), expert_pick(223), size_guide(219), price_history(217), return_explainer(201)
  birthday_rush_gifter    return_explainer(149), expert_pick(149), comparison_card(149), material_deep_dive(147), fit_reassurance(138)
  confident_repeat_buyer  material_deep_dive(182), size_guide(182), return_explainer(182), expert_pick(182), outfit_completion(182)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas)
  - session 5000: 16 edits (round 5000 — revive trend/visual widgets for trend_chaser & premium personas, lift size_guide for bottoms/shoes fit, dampen over-firing low-r defaults; robust to noise)
  - session 7500: 14 edits (round 7500 — stabilization: pull back overshoots on brand_story/style_bridge, revive silenced widgets (fit_reassurance, material_deep_dive, outfit_completion, easy_returns_promise) for high-regret cells)