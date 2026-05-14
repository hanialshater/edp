# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7802
- mean oracle reward: 2.0086
- mean regret:        0.2284  (11.4% of oracle)
- cum regret (batch): 571.02

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   204    0.3735    0.5089     26.6%
  trend_chaser             100    1.8878    2.2730     16.9%
  corporate_uniform_buyer   103    1.2422    1.4909     16.7%
  returner_from_recent_order   122    1.9899    2.3806     16.4%
  hesitant_first_buyer     308    2.2057    2.6315     16.2%
  premium_silent_browser   170    1.8189    2.1275     14.5%
  size_specific_anxious     92    2.4815    2.8781     13.8%
  post_return_returner     181    2.4749    2.7693     10.6%
  birthday_rush_gifter     198    2.2723    2.4771      8.3%
  outfit_event_planner     182    1.7509    1.8996      7.8%
  paralyzed_wishlister     194    2.6255    2.8447      7.7%
  mobile_evening_browser   161    1.0305    1.0968      6.0%
  tabbed_comparison_shopper   265    1.7239    1.8331      6.0%
  bargain_hunter_returning   220    1.1336    1.1720      3.3%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8946    2.2267     14.9%
  outerwear        248    2.0824    2.3830     12.6%
  bottoms          507    1.7904    2.0448     12.4%
  dress            437    1.8207    2.0413     10.8%
  accessories      374    1.6002    1.7635      9.3%
  top              555    1.6472    1.7989      8.4%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer bottoms         39    0.2981    0.4645     35.8%
  confident_repeat_buyer shoes           28    0.4494    0.6914     35.0%
  confident_repeat_buyer dress           38    0.3743    0.5304     29.4%
  trend_chaser           top             18    1.6596    2.2468     26.1%
  returner_from_recent_order shoes           17    2.1808    2.8524     23.5%
  corporate_uniform_buyer bottoms         19    1.3326    1.7247     22.7%
  hesitant_first_buyer   shoes           44    2.3793    3.0647     22.4%
  returner_from_recent_order bottoms         32    2.0397    2.6170     22.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             13.1      2.05    0.3288
  outfit_completion           12.8      3.27    0.2924
  easy_returns_promise        12.2      4.77    0.3096
  customers_chose             11.3      3.92    0.3268
  fit_reassurance             10.3      2.68    0.3248
  brand_story                  8.7      3.85    0.3253
  price_history                7.8      3.51    0.2567
  expert_pick                  6.6      3.94    0.2893
  material_deep_dive           5.4      4.24    0.2481
  return_explainer             4.0      3.28    0.2791
  recently_viewed              1.9      4.33    0.1162
  low_return_alts              1.8      1.99    0.3648
  similar_items                1.6      5.53    0.1222
  value_breakdown              1.3      1.77    0.2467
  also_bought                  0.6      5.95    0.0728
  price_drop_notify            0.3      4.10    0.3032
  style_bridge                 0.2      1.00    0.3146
  wishlist_save                0.1      3.85    0.2103
  size_guide                   0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  outfit_completion(204), recently_viewed(186), material_deep_dive(161), price_history(149), easy_returns_promise(123)
  trend_chaser            outfit_completion(100), fit_reassurance(98), brand_story(91), material_deep_dive(90), easy_returns_promise(70)
  corporate_uniform_buyer  easy_returns_promise(103), comparison_card(85), fit_reassurance(82), customers_chose(75), expert_pick(61)
  returner_from_recent_order  easy_returns_promise(120), comparison_card(118), customers_chose(114), outfit_completion(113), brand_story(111)
  hesitant_first_buyer    outfit_completion(308), easy_returns_promise(308), comparison_card(306), fit_reassurance(305), brand_story(274)
  premium_silent_browser  easy_returns_promise(168), return_explainer(148), material_deep_dive(109), comparison_card(103), value_breakdown(97)
  size_specific_anxious   fit_reassurance(92), easy_returns_promise(92), comparison_card(85), customers_chose(82), brand_story(58)
  post_return_returner    easy_returns_promise(181), fit_reassurance(180), comparison_card(171), customers_chose(169), brand_story(119)
  birthday_rush_gifter    outfit_completion(198), easy_returns_promise(198), comparison_card(197), brand_story(188), customers_chose(185)
  outfit_event_planner    comparison_card(182), outfit_completion(182), customers_chose(181), brand_story(168), material_deep_dive(126)
  paralyzed_wishlister    comparison_card(194), expert_pick(194), outfit_completion(192), customers_chose(191), fit_reassurance(152)
  mobile_evening_browser  outfit_completion(161), fit_reassurance(121), easy_returns_promise(116), price_history(114), similar_items(84)
  tabbed_comparison_shopper  comparison_card(265), price_history(265), return_explainer(265), customers_chose(264), easy_returns_promise(259)
  bargain_hunter_returning  comparison_card(220), price_history(220), customers_chose(220), outfit_completion(213), expert_pick(172)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1])
  - session 2500: 16 edits (round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2])