# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7628
- mean oracle reward: 1.9790
- mean regret:        0.2162  (10.9% of oracle)
- cum regret (batch): 540.52

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             115    1.7680    2.3060     23.3%
  size_specific_anxious    120    2.2683    2.8656     20.8%
  hesitant_first_buyer     287    2.1521    2.6309     18.2%
  post_return_returner     179    2.2981    2.7828     17.4%
  returner_from_recent_order   108    2.1866    2.4587     11.1%
  paralyzed_wishlister     198    2.5855    2.8502      9.3%
  birthday_rush_gifter     142    2.2817    2.4712      7.7%
  outfit_event_planner     192    1.7628    1.9074      7.6%
  corporate_uniform_buyer   126    1.3484    1.4520      7.1%
  premium_silent_browser   143    2.0422    2.1175      3.6%
  tabbed_comparison_shopper   262    1.7431    1.7976      3.0%
  mobile_evening_browser   187    1.0617    1.0869      2.3%
  confident_repeat_buyer   216    0.5049    0.5145      1.9%
  bargain_hunter_returning   225    1.1811    1.1876      0.5%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  top              538    1.5698    1.7971     12.6%
  accessories      407    1.5260    1.7337     12.0%
  shoes            367    1.9523    2.1928     11.0%
  bottoms          507    1.8050    2.0220     10.7%
  dress            450    1.8131    2.0113      9.9%
  outerwear        231    2.1379    2.3383      8.6%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             30    1.5230    2.2468     32.2%
  size_specific_anxious  top             28    2.0878    2.8041     25.5%
  trend_chaser           shoes           15    1.5480    2.0259     23.6%
  trend_chaser           bottoms         21    1.3373    1.7276     22.6%
  size_specific_anxious  accessories     17    1.7818    2.2751     21.7%
  post_return_returner   top             45    2.1206    2.6843     21.0%
  trend_chaser           accessories     21    2.2774    2.8783     20.9%
  size_specific_anxious  shoes           15    2.5242    3.1786     20.6%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  virtual_try_on              16.7      1.51    0.2938
  return_explainer            16.3      3.33    0.2947
  easy_returns_promise        15.9      4.76    0.2948
  expert_pick                 13.6      3.37    0.2850
  comparison_card             13.4      3.06    0.3231
  material_deep_dive          10.1      4.94    0.2835
  outfit_completion            8.4      3.94    0.3068
  value_breakdown              3.5      4.06    0.2574
  customers_chose              1.0      5.35    0.3078
  occasion_lookbook            1.0      5.01    0.0833
  low_return_alts              0.1      2.00    0.4275
  brand_story                  0.0      1.00    0.3665
  fit_reassurance              0.0      0.00    0.0000
  size_guide                   0.0      0.00    0.0000
  style_bridge                 0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            virtual_try_on(115), outfit_completion(115), expert_pick(115), return_explainer(115), easy_returns_promise(115)
  size_specific_anxious   virtual_try_on(120), easy_returns_promise(120), expert_pick(119), return_explainer(117), comparison_card(117)
  hesitant_first_buyer    virtual_try_on(287), return_explainer(287), easy_returns_promise(287), comparison_card(282), material_deep_dive(270)
  post_return_returner    virtual_try_on(179), comparison_card(179), easy_returns_promise(179), material_deep_dive(176), return_explainer(171)
  returner_from_recent_order  virtual_try_on(108), return_explainer(108), comparison_card(108), easy_returns_promise(108), expert_pick(105)
  paralyzed_wishlister    expert_pick(198), comparison_card(198), virtual_try_on(198), return_explainer(198), easy_returns_promise(173)
  birthday_rush_gifter    virtual_try_on(142), return_explainer(142), easy_returns_promise(142), comparison_card(141), outfit_completion(140)
  outfit_event_planner    virtual_try_on(192), outfit_completion(192), return_explainer(192), expert_pick(191), comparison_card(188)
  corporate_uniform_buyer  virtual_try_on(126), return_explainer(126), easy_returns_promise(126), material_deep_dive(126), comparison_card(126)
  premium_silent_browser  virtual_try_on(143), return_explainer(143), easy_returns_promise(143), expert_pick(142), comparison_card(131)
  tabbed_comparison_shopper  comparison_card(262), virtual_try_on(262), expert_pick(262), return_explainer(262), easy_returns_promise(253)
  mobile_evening_browser  virtual_try_on(187), outfit_completion(187), return_explainer(187), easy_returns_promise(187), material_deep_dive(187)
  confident_repeat_buyer  virtual_try_on(216), return_explainer(216), easy_returns_promise(216), material_deep_dive(216), expert_pick(192)
  bargain_hunter_returning  comparison_card(225), virtual_try_on(225), expert_pick(223), value_breakdown(211), return_explainer(188)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)
  - session 5000: 13 edits (round 5000 — activate virtual_try_on for high-N1_fit personas on shoes/outerwear without crowding fit_reassurance/size_guide)