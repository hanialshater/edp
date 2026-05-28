# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7661
- mean oracle reward: 2.0086
- mean regret:        0.2426  (12.1% of oracle)
- cum regret (batch): 606.39

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  corporate_uniform_buyer   103    1.0609    1.4909     28.8%
  confident_repeat_buyer   204    0.3904    0.5089     23.3%
  size_specific_anxious     92    2.2647    2.8781     21.3%
  premium_silent_browser   170    1.7238    2.1275     19.0%
  returner_from_recent_order   122    1.9454    2.3806     18.3%
  trend_chaser             100    1.9341    2.2730     14.9%
  hesitant_first_buyer     308    2.2551    2.6315     14.3%
  post_return_returner     181    2.3779    2.7693     14.1%
  birthday_rush_gifter     198    2.2507    2.4771      9.1%
  outfit_event_planner     182    1.7325    1.8996      8.8%
  paralyzed_wishlister     194    2.7034    2.8447      5.0%
  bargain_hunter_returning   220    1.1156    1.1720      4.8%
  mobile_evening_browser   161    1.0484    1.0968      4.4%
  tabbed_comparison_shopper   265    1.7717    1.8331      3.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8876    2.2267     15.2%
  outerwear        248    2.0708    2.3830     13.1%
  bottoms          507    1.8041    2.0448     11.8%
  dress            437    1.8015    2.0413     11.7%
  accessories      374    1.5693    1.7635     11.0%
  top              555    1.6169    1.7989     10.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           28    0.4390    0.6914     36.5%
  corporate_uniform_buyer bottoms         19    1.1203    1.7247     35.0%
  corporate_uniform_buyer shoes           13    1.3609    2.0604     34.0%
  corporate_uniform_buyer dress           21    1.0579    1.4908     29.0%
  size_specific_anxious  accessories     15    1.6449    2.2723     27.6%
  premium_silent_browser accessories     29    1.4426    1.9398     25.6%
  corporate_uniform_buyer outerwear        9    1.4659    1.9353     24.3%
  corporate_uniform_buyer top             29    0.9262    1.2187     24.0%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             14.3      2.13    0.3203
  outfit_completion           13.7      3.34    0.2939
  easy_returns_promise        11.0      5.05    0.3092
  expert_pick                 10.6      2.37    0.3086
  customers_chose              8.0      4.89    0.3282
  low_return_alts              6.6      2.54    0.3307
  fit_reassurance              6.5      2.58    0.3421
  occasion_lookbook            6.1      4.43    0.2083
  value_breakdown              5.8      3.20    0.2669
  similar_items                4.7      5.02    0.1738
  material_deep_dive           4.5      4.15    0.2787
  brand_story                  3.8      3.08    0.3298
  also_bought                  2.0      5.39    0.1191
  size_guide                   1.4      4.89    0.3724
  wishlist_save                0.6      3.87    0.2332
  style_bridge                 0.2      1.00    0.3347
  personal_recs                0.2      5.43    0.0566
  return_explainer             0.0      3.50    0.3227
  trending_now                 0.0      6.00    0.0738
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  corporate_uniform_buyer  comparison_card(103), easy_returns_promise(103), expert_pick(87), similar_items(85), low_return_alts(81)
  confident_repeat_buyer  occasion_lookbook(204), similar_items(202), outfit_completion(192), also_bought(159), material_deep_dive(152)
  size_specific_anxious   comparison_card(92), easy_returns_promise(92), expert_pick(91), fit_reassurance(78), outfit_completion(60)
  premium_silent_browser  comparison_card(170), low_return_alts(146), easy_returns_promise(144), expert_pick(136), outfit_completion(123)
  returner_from_recent_order  low_return_alts(122), outfit_completion(122), comparison_card(122), easy_returns_promise(120), expert_pick(101)
  trend_chaser            occasion_lookbook(96), fit_reassurance(78), brand_story(72), outfit_completion(69), comparison_card(47)
  hesitant_first_buyer    comparison_card(308), outfit_completion(308), easy_returns_promise(308), fit_reassurance(285), customers_chose(250)
  post_return_returner    comparison_card(181), easy_returns_promise(181), expert_pick(157), low_return_alts(151), outfit_completion(107)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), easy_returns_promise(196), fit_reassurance(120), customers_chose(107)
  outfit_event_planner    comparison_card(182), outfit_completion(182), occasion_lookbook(162), expert_pick(122), material_deep_dive(83)
  paralyzed_wishlister    comparison_card(194), expert_pick(194), outfit_completion(194), customers_chose(194), material_deep_dive(98)
  bargain_hunter_returning  comparison_card(220), value_breakdown(220), outfit_completion(217), expert_pick(195), occasion_lookbook(189)
  mobile_evening_browser  outfit_completion(161), occasion_lookbook(161), similar_items(150), expert_pick(96), also_bought(90)
  tabbed_comparison_shopper  comparison_card(265), value_breakdown(263), expert_pick(257), customers_chose(255), low_return_alts(204)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead widgets, dampen weak defaults, add cov-chain synergies for low-need personas)