# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.8192
- mean oracle reward: 2.0225
- mean regret:        0.2033  (10.1% of oracle)
- cum regret (batch): 508.20

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   182    0.3479    0.5144     32.4%
  corporate_uniform_buyer    81    1.0171    1.4618     30.4%
  returner_from_recent_order   121    1.9471    2.4114     19.3%
  premium_silent_browser   177    1.7003    2.1053     19.2%
  trend_chaser             105    1.9750    2.3312     15.3%
  size_specific_anxious    114    2.5426    2.9005     12.3%
  post_return_returner     198    2.5038    2.8039     10.7%
  hesitant_first_buyer     336    2.3704    2.6004      8.8%
  birthday_rush_gifter     149    2.2711    2.4820      8.5%
  outfit_event_planner     212    1.7762    1.9123      7.1%
  paralyzed_wishlister     172    2.7139    2.8495      4.8%
  tabbed_comparison_shopper   240    1.7816    1.8258      2.4%
  mobile_evening_browser   190    1.0711    1.0955      2.2%
  bargain_hunter_returning   223    1.1819    1.1832      0.1%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  outerwear        242    2.0373    2.3259     12.4%
  shoes            385    2.0017    2.2647     11.6%
  dress            441    1.9052    2.1134      9.9%
  bottoms          495    1.8947    2.0960      9.6%
  accessories      362    1.5641    1.7287      9.5%
  top              575    1.6350    1.7847      8.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           27    0.3713    0.6914     46.3%
  corporate_uniform_buyer shoes            9    1.2371    2.0604     40.0%
  confident_repeat_buyer outerwear       20    0.4356    0.6885     36.7%
  confident_repeat_buyer bottoms         35    0.3077    0.4645     33.8%
  corporate_uniform_buyer bottoms         15    1.1688    1.7247     32.2%
  corporate_uniform_buyer outerwear        9    1.3331    1.9353     31.1%
  corporate_uniform_buyer dress           13    1.0399    1.4908     30.2%
  confident_repeat_buyer top             44    0.2923    0.4070     28.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           15.8      3.64    0.2996
  comparison_card             13.7      2.36    0.3335
  fit_reassurance             13.5      2.60    0.3115
  customers_chose              9.2      5.07    0.3343
  expert_pick                  9.0      2.92    0.2945
  value_breakdown              7.9      3.65    0.2500
  also_bought                  6.8      5.32    0.2269
  material_deep_dive           6.0      2.12    0.3157
  low_return_alts              5.0      3.34    0.3464
  return_explainer             4.6      4.43    0.3482
  wishlist_save                3.3      3.01    0.2976
  brand_story                  2.9      5.16    0.3692
  similar_items                1.8      5.81    0.1244
  personal_recs                0.3      6.00    0.1023
  style_bridge                 0.2      1.00    0.3291
  size_guide                   0.1      1.00    0.0821
  occasion_lookbook            0.1      5.89    0.2437
  easy_returns_promise         0.0      6.00    0.2235
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  outfit_completion(182), also_bought(182), fit_reassurance(168), value_breakdown(150), similar_items(130)
  corporate_uniform_buyer  comparison_card(77), also_bought(77), outfit_completion(76), expert_pick(70), low_return_alts(45)
  returner_from_recent_order  comparison_card(121), outfit_completion(121), low_return_alts(83), expert_pick(74), fit_reassurance(71)
  premium_silent_browser  comparison_card(174), outfit_completion(169), expert_pick(142), material_deep_dive(123), value_breakdown(115)
  trend_chaser            outfit_completion(105), fit_reassurance(105), material_deep_dive(101), also_bought(89), expert_pick(81)
  size_specific_anxious   fit_reassurance(114), comparison_card(113), expert_pick(93), low_return_alts(90), outfit_completion(75)
  post_return_returner    fit_reassurance(198), comparison_card(193), outfit_completion(165), expert_pick(159), low_return_alts(136)
  hesitant_first_buyer    comparison_card(336), outfit_completion(336), fit_reassurance(335), customers_chose(294), material_deep_dive(194)
  birthday_rush_gifter    comparison_card(149), outfit_completion(149), fit_reassurance(131), customers_chose(89), return_explainer(83)
  outfit_event_planner    comparison_card(212), outfit_completion(212), fit_reassurance(209), also_bought(172), material_deep_dive(163)
  paralyzed_wishlister    comparison_card(172), customers_chose(171), fit_reassurance(170), outfit_completion(170), expert_pick(125)
  tabbed_comparison_shopper  comparison_card(240), value_breakdown(240), customers_chose(239), outfit_completion(193), return_explainer(152)
  mobile_evening_browser  outfit_completion(190), fit_reassurance(190), also_bought(190), expert_pick(184), value_breakdown(153)
  bargain_hunter_returning  comparison_card(223), value_breakdown(223), outfit_completion(223), fit_reassurance(217), customers_chose(185)

## Edit history applied so far
  - session 2500: 14 edits (round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser)
  - session 5000: 14 edits (round 5000 — kill bad defaults for confident_repeat_buyer, fix material_deep_dive miscalibration, revive size_guide for corporate_uniform_buyer, dampen F41 over-detection on premium_silent_browser)
  - session 7500: 11 edits (round 7500 — stabilize: trim defaults still over-firing on confident_repeat_buyer, fix comparison_card universal-firing, pull back size_guide over-correction, address corporate_uniform_buyer F32 gap)