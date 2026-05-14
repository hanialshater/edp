# EDP CHECKPOINT — sessions 0 → 2500  (N=2500)

## Aggregate performance
- mean reward:        1.5868
- mean oracle reward: 1.9831
- mean regret:        0.3963  (20.0% of oracle)
- cum regret (batch): 990.83

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   211    0.2444    0.5166     52.7%
  corporate_uniform_buyer   126    0.8481    1.4828     42.8%
  hesitant_first_buyer     290    1.7417    2.6105     33.3%
  premium_silent_browser   157    1.4047    2.0908     32.8%
  returner_from_recent_order   137    1.7138    2.3672     27.6%
  birthday_rush_gifter     176    1.8309    2.5072     27.0%
  trend_chaser             108    1.8651    2.2381     16.7%
  mobile_evening_browser   155    0.9324    1.0904     14.5%
  size_specific_anxious    100    2.4859    2.8922     14.0%
  post_return_returner     179    2.4160    2.7510     12.2%
  outfit_event_planner     209    1.7040    1.9068     10.6%
  paralyzed_wishlister     181    2.6590    2.8576      6.9%
  tabbed_comparison_shopper   236    1.7131    1.8233      6.0%
  bargain_hunter_returning   235    1.0944    1.1605      5.7%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            353    1.6206    2.1672     25.2%
  outerwear        258    1.7423    2.3058     24.4%
  bottoms          496    1.5939    2.0095     20.7%
  dress            456    1.6616    2.0843     20.3%
  top              551    1.5068    1.7946     16.0%
  accessories      386    1.4687    1.7149     14.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           28    0.2157    0.6914     68.8%
  confident_repeat_buyer outerwear       27    0.3042    0.6885     55.8%
  confident_repeat_buyer bottoms         41    0.2174    0.4645     53.2%
  confident_repeat_buyer top             47    0.1948    0.4070     52.1%
  corporate_uniform_buyer shoes           12    1.0099    2.0604     51.0%
  corporate_uniform_buyer bottoms         27    0.8668    1.7247     49.7%
  confident_repeat_buyer dress           30    0.2747    0.5304     48.2%
  corporate_uniform_buyer outerwear       10    1.0084    1.9353     47.9%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  similar_items               15.4      4.74    0.2499
  comparison_card             12.6      1.73    0.3020
  customers_chose             12.0      3.25    0.2953
  outfit_completion           12.0      2.92    0.2723
  brand_story                 10.6      3.55    0.2794
  also_bought                 10.1      5.15    0.2061
  low_return_alts              7.5      2.57    0.3134
  fit_reassurance              7.0      2.82    0.3024
  value_breakdown              5.3      2.76    0.2321
  personal_recs                4.0      5.15    0.1278
  trending_now                 2.0      5.52    0.0845
  price_drop_notify            1.2      4.69    0.3948
  style_bridge                 0.2      1.00    0.3097
  return_explainer             0.0      4.00    0.2679
  expert_pick                  0.0      2.00    0.2361
  size_guide                   0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  similar_items(211), also_bought(211), personal_recs(209), brand_story(182), trending_now(179)
  corporate_uniform_buyer  customers_chose(126), similar_items(126), also_bought(126), low_return_alts(102), personal_recs(97)
  hesitant_first_buyer    comparison_card(290), outfit_completion(290), similar_items(290), fit_reassurance(267), also_bought(214)
  premium_silent_browser  similar_items(156), low_return_alts(143), customers_chose(143), also_bought(130), brand_story(114)
  returner_from_recent_order  low_return_alts(137), comparison_card(137), customers_chose(137), brand_story(127), outfit_completion(125)
  birthday_rush_gifter    outfit_completion(176), comparison_card(175), similar_items(175), customers_chose(169), brand_story(152)
  trend_chaser            outfit_completion(108), similar_items(108), brand_story(101), also_bought(84), fit_reassurance(76)
  mobile_evening_browser  outfit_completion(155), similar_items(155), also_bought(155), personal_recs(149), trending_now(93)
  size_specific_anxious   customers_chose(98), comparison_card(94), low_return_alts(90), brand_story(87), fit_reassurance(86)
  post_return_returner    low_return_alts(178), comparison_card(178), customers_chose(177), fit_reassurance(152), similar_items(143)
  outfit_event_planner    outfit_completion(209), comparison_card(209), customers_chose(209), similar_items(209), brand_story(202)
  paralyzed_wishlister    comparison_card(181), customers_chose(181), outfit_completion(181), brand_story(142), price_drop_notify(125)
  tabbed_comparison_shopper  comparison_card(236), customers_chose(234), similar_items(234), value_breakdown(231), low_return_alts(223)
  bargain_hunter_returning  comparison_card(235), similar_items(235), customers_chose(228), value_breakdown(226), also_bought(218)

## Edit history applied so far
  (none — this is the baseline run)