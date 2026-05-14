# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7711
- mean oracle reward: 1.9777
- mean regret:        0.2066  (10.4% of oracle)
- cum regret (batch): 516.45

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  corporate_uniform_buyer   126    0.9754    1.4520     32.8%
  premium_silent_browser   143    1.6803    2.1175     20.6%
  returner_from_recent_order   108    1.9800    2.4577     19.4%
  confident_repeat_buyer   216    0.4270    0.5145     17.0%
  trend_chaser             115    1.9267    2.3063     16.5%
  hesitant_first_buyer     287    2.3024    2.6232     12.2%
  birthday_rush_gifter     142    2.2053    2.4712     10.8%
  size_specific_anxious    120    2.5726    2.8673     10.3%
  post_return_returner     179    2.5332    2.7828      9.0%
  outfit_event_planner     192    1.7635    1.9051      7.4%
  mobile_evening_browser   187    1.0434    1.0869      4.0%
  paralyzed_wishlister     198    2.7511    2.8462      3.3%
  tabbed_comparison_shopper   262    1.7494    1.7976      2.7%
  bargain_hunter_returning   225    1.1740    1.1877      1.2%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.8765    2.1880     14.2%
  outerwear        231    2.0335    2.3378     13.0%
  bottoms          507    1.8187    2.0195      9.9%
  dress            450    1.8151    2.0100      9.7%
  top              538    1.6411    1.7978      8.7%
  accessories      407    1.5913    1.7337      8.2%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  corporate_uniform_buyer bottoms         15    1.0079    1.7247     41.6%
  corporate_uniform_buyer outerwear       13    1.1991    1.9353     38.0%
  corporate_uniform_buyer shoes           19    1.2917    2.0604     37.3%
  confident_repeat_buyer shoes           33    0.4719    0.6914     31.8%
  corporate_uniform_buyer dress           23    1.0363    1.4908     30.5%
  corporate_uniform_buyer top             31    0.8830    1.2187     27.5%
  premium_silent_browser shoes           26    1.8058    2.4827     27.3%
  returner_from_recent_order bottoms         26    1.9793    2.6170     24.4%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           15.5      3.60    0.2918
  comparison_card             14.2      2.12    0.3224
  customers_chose             11.5      4.14    0.3321
  fit_reassurance             10.1      2.69    0.3326
  also_bought                  9.3      5.08    0.2274
  material_deep_dive           6.5      2.26    0.3080
  value_breakdown              6.4      3.44    0.2438
  low_return_alts              5.8      2.87    0.3357
  expert_pick                  4.5      2.94    0.3011
  return_explainer             3.5      4.01    0.3218
  brand_story                  3.4      4.95    0.3528
  wishlist_save                3.1      4.80    0.2971
  similar_items                2.5      5.54    0.1296
  easy_returns_promise         2.1      5.64    0.1980
  size_guide                   1.2      2.34    0.1127
  style_bridge                 0.2      1.00    0.3070
  price_drop_notify            0.2      4.70    0.4379
  personal_recs                0.2      6.00    0.1500
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  corporate_uniform_buyer  comparison_card(126), also_bought(125), outfit_completion(111), low_return_alts(80), expert_pick(78)
  premium_silent_browser  comparison_card(143), outfit_completion(134), material_deep_dive(108), low_return_alts(92), also_bought(82)
  returner_from_recent_order  comparison_card(108), outfit_completion(108), low_return_alts(99), customers_chose(83), material_deep_dive(73)
  confident_repeat_buyer  outfit_completion(216), also_bought(216), similar_items(162), value_breakdown(135), easy_returns_promise(119)
  trend_chaser            outfit_completion(115), material_deep_dive(114), fit_reassurance(106), also_bought(102), expert_pick(61)
  hesitant_first_buyer    comparison_card(287), outfit_completion(287), fit_reassurance(275), customers_chose(252), material_deep_dive(144)
  birthday_rush_gifter    outfit_completion(142), comparison_card(142), customers_chose(141), fit_reassurance(105), material_deep_dive(77)
  size_specific_anxious   comparison_card(119), fit_reassurance(118), outfit_completion(93), low_return_alts(92), customers_chose(86)
  post_return_returner    comparison_card(179), fit_reassurance(178), outfit_completion(139), customers_chose(136), low_return_alts(126)
  outfit_event_planner    outfit_completion(192), comparison_card(192), also_bought(181), customers_chose(180), material_deep_dive(164)
  mobile_evening_browser  outfit_completion(187), also_bought(187), similar_items(139), expert_pick(128), fit_reassurance(114)
  paralyzed_wishlister    comparison_card(198), outfit_completion(198), customers_chose(198), fit_reassurance(148), expert_pick(122)
  tabbed_comparison_shopper  comparison_card(262), customers_chose(261), value_breakdown(260), wishlist_save(201), outfit_completion(171)
  bargain_hunter_returning  comparison_card(225), outfit_completion(225), value_breakdown(223), customers_chose(220), also_bought(152)

## Edit history applied so far
  - session 2500: 14 edits (round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser)
  - session 5000: 14 edits (round 5000 — kill bad defaults for confident_repeat_buyer, fix material_deep_dive miscalibration, revive size_guide for corporate_uniform_buyer, dampen F41 over-detection on premium_silent_browser)