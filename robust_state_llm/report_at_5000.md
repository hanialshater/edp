# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.8661
- mean oracle reward: 2.0086
- mean regret:        0.1425  (7.1% of oracle)
- cum regret (batch): 356.26

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             100    1.7799    2.2730     21.7%
  premium_silent_browser   170    1.8784    2.1275     11.7%
  corporate_uniform_buyer   103    1.3183    1.4909     11.6%
  size_specific_anxious     92    2.5988    2.8781      9.7%
  hesitant_first_buyer     308    2.4021    2.6315      8.7%
  returner_from_recent_order   122    2.1989    2.3806      7.6%
  post_return_returner     181    2.5758    2.7693      7.0%
  paralyzed_wishlister     194    2.6702    2.8447      6.1%
  birthday_rush_gifter     198    2.3471    2.4771      5.2%
  mobile_evening_browser   161    1.0464    1.0968      4.6%
  outfit_event_planner     182    1.8194    1.8996      4.2%
  tabbed_comparison_shopper   265    1.8052    1.8331      1.5%
  bargain_hunter_returning   220    1.1572    1.1720      1.3%
  confident_repeat_buyer   204    0.5070    0.5089      0.4%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  outerwear        248    2.1865    2.3830      8.2%
  shoes            379    2.0442    2.2267      8.2%
  bottoms          507    1.8935    2.0448      7.4%
  dress            437    1.9004    2.0413      6.9%
  accessories      374    1.6468    1.7635      6.6%
  top              555    1.6972    1.7989      5.7%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             18    1.5588    2.2468     30.6%
  trend_chaser           accessories     14    2.2145    2.8803     23.1%
  trend_chaser           dress           21    2.0410    2.5686     20.5%
  trend_chaser           outerwear       10    1.9016    2.3901     20.4%
  premium_silent_browser outerwear       14    2.1811    2.6939     19.0%
  premium_silent_browser accessories     29    1.5747    1.9398     18.8%
  corporate_uniform_buyer bottoms         19    1.4131    1.7247     18.1%
  trend_chaser           bottoms         21    1.4204    1.7276     17.8%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.2      2.49    0.3384
  material_deep_dive          14.0      2.28    0.3191
  fit_reassurance             13.8      3.76    0.3210
  outfit_completion           13.6      3.90    0.3170
  customers_chose             12.2      4.26    0.3461
  return_explainer             8.9      3.16    0.3605
  easy_returns_promise         5.7      4.10    0.2070
  personal_recs                5.5      5.38    0.2171
  value_breakdown              4.4      3.61    0.2764
  expert_pick                  2.8      3.91    0.2834
  similar_items                2.1      5.64    0.1325
  low_return_alts              2.0      1.36    0.3805
  price_drop_notify            0.5      4.56    0.3648
  also_bought                  0.2      6.00    0.0846
  style_bridge                 0.1      1.00    0.2883
  size_guide                   0.1      2.92    0.2262
  occasion_lookbook            0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            material_deep_dive(100), outfit_completion(99), fit_reassurance(89), expert_pick(60), personal_recs(59)
  premium_silent_browser  fit_reassurance(158), material_deep_dive(157), return_explainer(155), comparison_card(145), customers_chose(112)
  corporate_uniform_buyer  comparison_card(103), return_explainer(97), fit_reassurance(97), personal_recs(97), material_deep_dive(73)
  size_specific_anxious   comparison_card(92), material_deep_dive(91), customers_chose(90), fit_reassurance(86), return_explainer(78)
  hesitant_first_buyer    comparison_card(308), outfit_completion(308), fit_reassurance(296), return_explainer(296), material_deep_dive(282)
  returner_from_recent_order  material_deep_dive(122), outfit_completion(122), comparison_card(122), customers_chose(122), fit_reassurance(100)
  post_return_returner    comparison_card(181), customers_chose(181), fit_reassurance(179), material_deep_dive(178), outfit_completion(139)
  paralyzed_wishlister    comparison_card(194), outfit_completion(184), customers_chose(183), material_deep_dive(172), fit_reassurance(156)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), customers_chose(198), material_deep_dive(198), fit_reassurance(159)
  mobile_evening_browser  outfit_completion(161), material_deep_dive(160), easy_returns_promise(152), personal_recs(148), fit_reassurance(120)
  outfit_event_planner    material_deep_dive(182), comparison_card(182), outfit_completion(182), customers_chose(182), fit_reassurance(138)
  tabbed_comparison_shopper  comparison_card(265), customers_chose(261), value_breakdown(248), return_explainer(237), fit_reassurance(233)
  bargain_hunter_returning  comparison_card(220), easy_returns_promise(213), outfit_completion(210), customers_chose(209), value_breakdown(204)
  confident_repeat_buyer  material_deep_dive(204), easy_returns_promise(203), fit_reassurance(202), personal_recs(190), similar_items(177)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen low-r/fire defaults, add cross-problem synergies for worst personas)