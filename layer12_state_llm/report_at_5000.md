# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7292
- mean oracle reward: 2.0086
- mean regret:        0.2794  (13.9% of oracle)
- cum regret (batch): 698.57

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   204    0.3718    0.5089     26.9%
  corporate_uniform_buyer   103    1.1122    1.4909     25.4%
  premium_silent_browser   170    1.6232    2.1275     23.7%
  returner_from_recent_order   122    1.8506    2.3806     22.3%
  hesitant_first_buyer     308    2.0750    2.6315     21.1%
  birthday_rush_gifter     198    2.0375    2.4771     17.7%
  trend_chaser             100    1.8907    2.2730     16.8%
  size_specific_anxious     92    2.4620    2.8781     14.5%
  outfit_event_planner     182    1.6847    1.8996     11.3%
  post_return_returner     181    2.4997    2.7693      9.7%
  mobile_evening_browser   161    1.0194    1.0968      7.1%
  bargain_hunter_returning   220    1.1200    1.1720      4.4%
  paralyzed_wishlister     194    2.7426    2.8447      3.6%
  tabbed_comparison_shopper   265    1.7778    1.8331      3.0%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8398    2.2267     17.4%
  outerwear        248    1.9770    2.3830     17.0%
  bottoms          507    1.7355    2.0448     15.1%
  dress            437    1.7621    2.0413     13.7%
  accessories      374    1.5688    1.7635     11.0%
  top              555    1.6194    1.7989     10.0%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer bottoms         39    0.2978    0.4645     35.9%
  corporate_uniform_buyer shoes           13    1.3518    2.0604     34.4%
  confident_repeat_buyer shoes           28    0.4596    0.6914     33.5%
  corporate_uniform_buyer outerwear        9    1.3180    1.9353     31.9%
  premium_silent_browser outerwear       14    1.8756    2.6939     30.4%
  corporate_uniform_buyer bottoms         19    1.2016    1.7247     30.3%
  confident_repeat_buyer outerwear       16    0.4822    0.6885     30.0%
  returner_from_recent_order shoes           17    2.0218    2.8524     29.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           13.9      3.35    0.2880
  comparison_card             13.8      2.01    0.3180
  also_bought                 13.3      5.10    0.2582
  customers_chose             10.9      3.76    0.3185
  brand_story                  9.7      3.59    0.3292
  fit_reassurance              7.5      3.17    0.3237
  value_breakdown              5.7      3.14    0.2505
  return_explainer             5.2      3.27    0.3057
  similar_items                5.1      4.67    0.1752
  low_return_alts              4.5      1.77    0.3566
  wishlist_save                4.3      3.64    0.3097
  personal_recs                2.0      5.59    0.1147
  easy_returns_promise         1.3      5.76    0.2292
  material_deep_dive           1.3      1.73    0.0930
  expert_pick                  0.5      2.45    0.3521
  trending_now                 0.3      5.76    0.0670
  price_drop_notify            0.2      3.67    0.3366
  style_bridge                 0.2      1.00    0.3284
  size_guide                   0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  also_bought(204), similar_items(203), outfit_completion(180), personal_recs(168), material_deep_dive(137)
  corporate_uniform_buyer  comparison_card(103), also_bought(103), fit_reassurance(72), brand_story(71), similar_items(58)
  premium_silent_browser  comparison_card(169), return_explainer(150), also_bought(128), outfit_completion(127), brand_story(120)
  returner_from_recent_order  comparison_card(122), outfit_completion(121), brand_story(118), customers_chose(112), low_return_alts(103)
  hesitant_first_buyer    comparison_card(308), outfit_completion(308), also_bought(305), fit_reassurance(256), brand_story(208)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), customers_chose(197), brand_story(171), also_bought(153)
  trend_chaser            outfit_completion(100), also_bought(95), brand_story(94), fit_reassurance(76), wishlist_save(57)
  size_specific_anxious   comparison_card(91), brand_story(82), customers_chose(74), fit_reassurance(72), low_return_alts(70)
  outfit_event_planner    brand_story(182), comparison_card(182), outfit_completion(182), customers_chose(180), also_bought(174)
  post_return_returner    comparison_card(181), customers_chose(171), low_return_alts(165), fit_reassurance(159), brand_story(157)
  mobile_evening_browser  outfit_completion(161), also_bought(161), similar_items(160), personal_recs(117), fit_reassurance(108)
  bargain_hunter_returning  comparison_card(220), also_bought(217), outfit_completion(213), customers_chose(211), value_breakdown(211)
  paralyzed_wishlister    comparison_card(194), outfit_completion(194), customers_chose(193), brand_story(163), wishlist_save(142)
  tabbed_comparison_shopper  comparison_card(265), return_explainer(265), customers_chose(261), value_breakdown(258), also_bought(227)

## Edit history applied so far
  - session 2500: 14 edits (round 2500 — revive dead F46/F33/F51 widgets, sharpen F33 detection for premium_silent_browser)