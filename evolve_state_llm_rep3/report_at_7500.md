# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7111
- mean oracle reward: 1.9777
- mean regret:        0.2666  (13.5% of oracle)
- cum regret (batch): 666.53

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   216    0.3797    0.5145     26.2%
  trend_chaser             115    1.7285    2.3063     25.1%
  size_specific_anxious    120    2.2228    2.8673     22.5%
  hesitant_first_buyer     287    2.1168    2.6232     19.3%
  post_return_returner     179    2.2655    2.7828     18.6%
  premium_silent_browser   143    1.7276    2.1175     18.4%
  returner_from_recent_order   108    2.0174    2.4577     17.9%
  birthday_rush_gifter     142    2.1671    2.4712     12.3%
  paralyzed_wishlister     198    2.6365    2.8462      7.4%
  corporate_uniform_buyer   126    1.3673    1.4520      5.8%
  outfit_event_planner     192    1.7956    1.9051      5.8%
  tabbed_comparison_shopper   262    1.7182    1.7976      4.4%
  mobile_evening_browser   187    1.0460    1.0869      3.8%
  bargain_hunter_returning   225    1.1543    1.1877      2.8%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  accessories      407    1.4531    1.7337     16.2%
  top              538    1.5246    1.7978     15.2%
  shoes            367    1.8844    2.1880     13.9%
  dress            450    1.7503    2.0100     12.9%
  outerwear        231    2.0483    2.3378     12.4%
  bottoms          507    1.8022    2.0195     10.8%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           33    0.4383    0.6914     36.6%
  size_specific_anxious  accessories     17    1.4543    2.2723     36.0%
  trend_chaser           top             30    1.4784    2.2468     34.2%
  post_return_returner   accessories     29    1.4692    2.0918     29.8%
  confident_repeat_buyer outerwear       16    0.4955    0.6885     28.0%
  premium_silent_browser accessories     23    1.4111    1.9398     27.3%
  trend_chaser           shoes           15    1.4958    2.0259     26.2%
  confident_repeat_buyer bottoms         43    0.3442    0.4645     25.9%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.2      2.32    0.3114
  material_deep_dive           9.7      3.30    0.2790
  fit_reassurance              9.7      3.65    0.3035
  wishlist_save                9.1      3.48    0.2635
  size_guide                   8.2      4.83    0.3046
  easy_returns_promise         8.0      5.28    0.3093
  outfit_completion            7.3      4.04    0.2783
  expert_pick                  5.6      2.30    0.3389
  style_bridge                 5.0      1.58    0.2773
  occasion_lookbook            4.8      4.61    0.1983
  low_return_alts              4.1      2.10    0.3469
  price_history                3.3      3.91    0.1820
  value_breakdown              3.3      2.92    0.2665
  return_explainer             2.9      3.41    0.2829
  customers_chose              2.7      4.79    0.2690
  similar_items                1.2      5.95    0.1155
  price_drop_notify            0.9      2.67    0.2429
  brand_story                  0.0      5.67    0.2429
  recently_viewed              0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  wishlist_save(202), material_deep_dive(198), price_history(185), outfit_completion(179), occasion_lookbook(160)
  trend_chaser            style_bridge(115), occasion_lookbook(115), material_deep_dive(111), wishlist_save(103), fit_reassurance(103)
  size_specific_anxious   size_guide(119), comparison_card(117), easy_returns_promise(101), fit_reassurance(100), expert_pick(94)
  hesitant_first_buyer    comparison_card(287), easy_returns_promise(266), fit_reassurance(264), size_guide(243), outfit_completion(230)
  post_return_returner    size_guide(178), comparison_card(177), easy_returns_promise(173), low_return_alts(147), fit_reassurance(94)
  premium_silent_browser  comparison_card(140), fit_reassurance(105), material_deep_dive(104), return_explainer(104), size_guide(84)
  returner_from_recent_order  comparison_card(108), low_return_alts(92), size_guide(92), easy_returns_promise(92), outfit_completion(76)
  birthday_rush_gifter    comparison_card(142), easy_returns_promise(109), style_bridge(105), material_deep_dive(100), size_guide(88)
  paralyzed_wishlister    comparison_card(198), expert_pick(197), wishlist_save(171), outfit_completion(164), material_deep_dive(127)
  corporate_uniform_buyer  comparison_card(126), size_guide(126), easy_returns_promise(123), wishlist_save(97), material_deep_dive(76)
  outfit_event_planner    comparison_card(192), style_bridge(189), material_deep_dive(173), occasion_lookbook(166), wishlist_save(133)
  tabbed_comparison_shopper  comparison_card(262), return_explainer(261), fit_reassurance(198), value_breakdown(170), customers_chose(147)
  mobile_evening_browser  style_bridge(187), occasion_lookbook(178), wishlist_save(166), material_deep_dive(138), fit_reassurance(107)
  bargain_hunter_returning  comparison_card(225), outfit_completion(225), customers_chose(157), value_breakdown(150), occasion_lookbook(105)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas)
  - session 5000: 16 edits (round 5000 — boost corporate_uniform/confident_repeat coverage, revive dead price widgets, tame over-firing low-reward widgets)