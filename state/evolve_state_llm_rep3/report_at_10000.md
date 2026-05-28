# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.7738
- mean oracle reward: 2.0225
- mean regret:        0.2487  (12.3% of oracle)
- cum regret (batch): 621.71

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   182    0.2524    0.5144     50.9%
  size_specific_anxious    114    2.3370    2.9005     19.4%
  premium_silent_browser   177    1.7309    2.1053     17.8%
  returner_from_recent_order   121    2.0031    2.4114     16.9%
  trend_chaser             105    1.9415    2.3312     16.7%
  hesitant_first_buyer     336    2.1928    2.6004     15.7%
  post_return_returner     198    2.3693    2.8039     15.5%
  birthday_rush_gifter     149    2.1959    2.4820     11.5%
  outfit_event_planner     212    1.7720    1.9123      7.3%
  paralyzed_wishlister     172    2.7157    2.8495      4.7%
  tabbed_comparison_shopper   240    1.7524    1.8258      4.0%
  corporate_uniform_buyer    81    1.4050    1.4618      3.9%
  mobile_evening_browser   190    1.0607    1.0955      3.2%
  bargain_hunter_returning   223    1.1563    1.1832      2.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            385    1.9515    2.2647     13.8%
  accessories      362    1.4976    1.7287     13.4%
  top              575    1.5567    1.7847     12.8%
  outerwear        242    2.0352    2.3259     12.5%
  dress            441    1.8667    2.1134     11.7%
  bottoms          495    1.8794    2.0960     10.3%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           27    0.1960    0.6914     71.7%
  confident_repeat_buyer outerwear       20    0.3272    0.6885     52.5%
  confident_repeat_buyer bottoms         35    0.2241    0.4645     51.8%
  confident_repeat_buyer top             44    0.2177    0.4070     46.5%
  confident_repeat_buyer dress           24    0.2994    0.5304     43.6%
  confident_repeat_buyer accessories     32    0.2967    0.4464     33.5%
  premium_silent_browser accessories     24    1.4042    1.9398     27.6%
  size_specific_anxious  accessories     15    1.6737    2.2723     26.3%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.2      2.37    0.3191
  outfit_completion           11.8      3.24    0.2835
  fit_reassurance              9.4      3.32    0.3259
  wishlist_save                8.7      2.63    0.3015
  expert_pick                  8.0      3.34    0.2761
  brand_story                  7.9      3.69    0.2904
  size_guide                   7.8      5.00    0.3286
  material_deep_dive           6.8      3.43    0.2533
  easy_returns_promise         6.0      5.34    0.3446
  value_breakdown              4.5      3.12    0.2663
  low_return_alts              4.2      2.33    0.3619
  customers_chose              3.1      4.58    0.2687
  return_explainer             2.8      3.57    0.2892
  also_bought                  2.8      5.61    0.1505
  occasion_lookbook            1.0      5.03    0.2913
  recently_viewed              0.8      4.99    0.0642
  price_history                0.2      5.00    0.1312
  personal_recs                0.0      6.00    0.0299
  price_drop_notify            0.0      6.00    0.2756
  style_bridge                 0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  outfit_completion(182), material_deep_dive(177), expert_pick(177), also_bought(154), brand_story(150)
  size_specific_anxious   comparison_card(113), size_guide(111), fit_reassurance(92), easy_returns_promise(76), wishlist_save(74)
  premium_silent_browser  expert_pick(177), comparison_card(171), material_deep_dive(143), return_explainer(129), fit_reassurance(129)
  returner_from_recent_order  comparison_card(119), low_return_alts(104), size_guide(96), outfit_completion(92), brand_story(72)
  trend_chaser            outfit_completion(105), material_deep_dive(94), expert_pick(93), occasion_lookbook(80), fit_reassurance(80)
  hesitant_first_buyer    comparison_card(336), outfit_completion(336), easy_returns_promise(310), fit_reassurance(306), size_guide(253)
  post_return_returner    size_guide(192), comparison_card(188), wishlist_save(157), easy_returns_promise(154), low_return_alts(152)
  birthday_rush_gifter    outfit_completion(148), comparison_card(147), easy_returns_promise(112), fit_reassurance(101), brand_story(93)
  outfit_event_planner    comparison_card(212), outfit_completion(212), material_deep_dive(150), expert_pick(150), brand_story(128)
  paralyzed_wishlister    comparison_card(172), outfit_completion(171), wishlist_save(168), expert_pick(116), low_return_alts(93)
  tabbed_comparison_shopper  comparison_card(240), fit_reassurance(238), return_explainer(235), wishlist_save(232), value_breakdown(217)
  corporate_uniform_buyer  size_guide(81), easy_returns_promise(78), wishlist_save(77), comparison_card(68), brand_story(63)
  mobile_evening_browser  outfit_completion(190), brand_story(165), material_deep_dive(164), expert_pick(162), wishlist_save(116)
  bargain_hunter_returning  comparison_card(223), outfit_completion(222), wishlist_save(219), value_breakdown(219), customers_chose(193)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas)
  - session 5000: 16 edits (round 5000 — boost corporate_uniform/confident_repeat coverage, revive dead price widgets, tame over-firing low-reward widgets)
  - session 7500: 14 edits (round 7500 — stabilize: lift confident_repeat/trend_chaser coverage, revive remaining dead widgets, tame low-r/fire over-firers)