# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8688
- mean oracle reward: 2.0241
- mean regret:        0.1554  (7.7% of oracle)
- cum regret (batch): 388.42

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  paralyzed_wishlister     172    2.4422    2.8561     14.5%
  trend_chaser             105    2.0467    2.3309     12.2%
  size_specific_anxious    114    2.5801    2.8997     11.0%
  outfit_event_planner     212    1.7300    1.9150      9.7%
  bargain_hunter_returning   223    1.0696    1.1832      9.6%
  returner_from_recent_order   121    2.1861    2.4116      9.4%
  post_return_returner     198    2.5527    2.8038      9.0%
  tabbed_comparison_shopper   240    1.6736    1.8258      8.3%
  corporate_uniform_buyer    81    1.3546    1.4618      7.3%
  hesitant_first_buyer     336    2.4770    2.6077      5.0%
  premium_silent_browser   177    2.0135    2.1053      4.4%
  birthday_rush_gifter     149    2.4548    2.4820      1.1%
  mobile_evening_browser   190    1.0955    1.0955      0.0%
  confident_repeat_buyer   182    0.5144    0.5144      0.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  bottoms          495    1.8909    2.0990      9.9%
  outerwear        242    2.1460    2.3272      7.8%
  accessories      362    1.5997    1.7287      7.5%
  shoes            385    2.1082    2.2700      7.1%
  top              575    1.6576    1.7841      7.1%
  dress            441    1.9789    2.1146      6.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  paralyzed_wishlister   bottoms         40    2.2989    2.9255     21.4%
  trend_chaser           accessories     17    2.3201    2.8783     19.4%
  paralyzed_wishlister   outerwear       15    2.6828    3.1770     15.6%
  returner_from_recent_order bottoms         27    2.2157    2.6170     15.3%
  bargain_hunter_returning outerwear       20    1.2135    1.4171     14.4%
  corporate_uniform_buyer bottoms         15    1.4797    1.7247     14.2%
  bargain_hunter_returning bottoms         45    1.2369    1.4325     13.7%
  size_specific_anxious  top             23    2.4306    2.8041     13.3%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  fit_reassurance             16.6      1.80    0.3112
  return_explainer            16.5      3.84    0.3116
  customers_chose             16.4      2.93    0.3106
  style_bridge                15.9      3.24    0.3094
  material_deep_dive          12.8      4.20    0.3252
  easy_returns_promise        12.6      5.76    0.2983
  value_breakdown              4.3      2.78    0.2738
  comparison_card              3.4      3.42    0.3335
  expert_pick                  0.8      5.54    0.3988
  virtual_try_on               0.5      4.22    0.4190
  brand_story                  0.2      2.65    0.3100
  size_guide                   0.0      0.00    0.0000
  low_return_alts              0.0      0.00    0.0000
  outfit_completion            0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  paralyzed_wishlister    customers_chose(172), fit_reassurance(172), style_bridge(172), return_explainer(164), expert_pick(112)
  trend_chaser            style_bridge(105), fit_reassurance(105), material_deep_dive(105), return_explainer(105), customers_chose(105)
  size_specific_anxious   fit_reassurance(114), customers_chose(114), return_explainer(114), easy_returns_promise(114), material_deep_dive(113)
  outfit_event_planner    style_bridge(212), customers_chose(212), fit_reassurance(212), return_explainer(212), easy_returns_promise(212)
  bargain_hunter_returning  customers_chose(223), value_breakdown(223), fit_reassurance(223), style_bridge(223), return_explainer(209)
  returner_from_recent_order  return_explainer(121), customers_chose(121), style_bridge(121), material_deep_dive(121), fit_reassurance(108)
  post_return_returner    fit_reassurance(198), return_explainer(198), material_deep_dive(198), customers_chose(198), easy_returns_promise(198)
  tabbed_comparison_shopper  customers_chose(240), value_breakdown(240), fit_reassurance(240), return_explainer(240), style_bridge(179)
  corporate_uniform_buyer  fit_reassurance(81), return_explainer(81), material_deep_dive(81), customers_chose(81), style_bridge(81)
  hesitant_first_buyer    fit_reassurance(336), return_explainer(336), style_bridge(336), material_deep_dive(335), customers_chose(299)
  premium_silent_browser  fit_reassurance(177), customers_chose(177), return_explainer(177), style_bridge(176), material_deep_dive(167)
  birthday_rush_gifter    fit_reassurance(149), customers_chose(149), return_explainer(149), material_deep_dive(149), style_bridge(149)
  mobile_evening_browser  style_bridge(190), fit_reassurance(190), customers_chose(190), return_explainer(190), easy_returns_promise(190)
  confident_repeat_buyer  fit_reassurance(182), style_bridge(182), return_explainer(182), material_deep_dive(182), easy_returns_promise(182)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 13 edits (round 5000 — activate virtual_try_on for high-N1_fit personas on shoes/outerwear without crowding fit_reassurance/size_guide)
  - session 7500: 13 edits (round 7500 — tame virtual_try_on over-fire, revive fit_reassurance/size_guide/style_bridge for size_anxious & trend_chaser, boost peer widgets for trend_chaser)