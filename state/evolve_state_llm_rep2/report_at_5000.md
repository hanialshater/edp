# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7175
- mean oracle reward: 2.0086
- mean regret:        0.2911  (14.5% of oracle)
- cum regret (batch): 727.69

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  corporate_uniform_buyer   103    1.0327    1.4909     30.7%
  premium_silent_browser   170    1.5703    2.1275     26.2%
  trend_chaser             100    1.7052    2.2730     25.0%
  size_specific_anxious     92    2.3342    2.8781     18.9%
  returner_from_recent_order   122    1.9328    2.3806     18.8%
  hesitant_first_buyer     308    2.1582    2.6315     18.0%
  confident_repeat_buyer   204    0.4274    0.5089     16.0%
  outfit_event_planner     182    1.6252    1.8996     14.4%
  post_return_returner     181    2.4383    2.7693     12.0%
  birthday_rush_gifter     198    2.2213    2.4771     10.3%
  paralyzed_wishlister     194    2.5637    2.8447      9.9%
  mobile_evening_browser   161    1.0266    1.0968      6.4%
  bargain_hunter_returning   220    1.1151    1.1720      4.9%
  tabbed_comparison_shopper   265    1.7459    1.8331      4.8%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.8572    2.2267     16.6%
  accessories      374    1.4755    1.7635     16.3%
  outerwear        248    2.0239    2.3830     15.1%
  dress            437    1.7437    2.0413     14.6%
  top              555    1.5669    1.7989     12.9%
  bottoms          507    1.7842    2.0448     12.7%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  corporate_uniform_buyer bottoms         19    1.0998    1.7247     36.2%
  corporate_uniform_buyer dress           21    1.0068    1.4908     32.5%
  premium_silent_browser accessories     29    1.3112    1.9398     32.4%
  confident_repeat_buyer shoes           28    0.4673    0.6914     32.4%
  premium_silent_browser outerwear       14    1.8472    2.6939     31.4%
  trend_chaser           accessories     14    2.0155    2.8803     30.0%
  corporate_uniform_buyer shoes           13    1.4431    2.0604     30.0%
  premium_silent_browser dress           27    1.6473    2.3417     29.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             13.9      2.39    0.3135
  easy_returns_promise        13.7      4.57    0.2954
  outfit_completion           10.2      3.43    0.3078
  trending_now                10.2      4.48    0.2327
  customers_chose              8.7      3.85    0.3108
  material_deep_dive           8.2      3.40    0.2754
  personal_recs                6.8      4.95    0.1924
  size_guide                   6.6      1.52    0.3508
  low_return_alts              6.6      2.41    0.3376
  value_breakdown              3.4      2.68    0.2670
  price_history                3.3      4.38    0.1722
  expert_pick                  3.3      3.18    0.3132
  return_explainer             2.4      3.20    0.3523
  occasion_lookbook            0.9      2.79    0.1228
  also_bought                  0.5      6.00    0.0765
  price_drop_notify            0.4      4.46    0.3640
  fit_reassurance              0.2      5.49    0.3133
  recently_viewed              0.2      5.43    0.1449
  style_bridge                 0.2      1.00    0.3002
  brand_story                  0.1      5.07    0.3938
  wishlist_save                0.1      5.11    0.2190
  similar_items                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  corporate_uniform_buyer  easy_returns_promise(103), comparison_card(102), trending_now(93), low_return_alts(72), personal_recs(66)
  premium_silent_browser  easy_returns_promise(170), comparison_card(163), trending_now(126), low_return_alts(112), material_deep_dive(98)
  trend_chaser            material_deep_dive(93), trending_now(79), size_guide(74), outfit_completion(69), easy_returns_promise(57)
  size_specific_anxious   size_guide(92), easy_returns_promise(92), comparison_card(89), low_return_alts(64), customers_chose(51)
  returner_from_recent_order  easy_returns_promise(122), comparison_card(122), low_return_alts(121), outfit_completion(111), customers_chose(79)
  hesitant_first_buyer    comparison_card(308), outfit_completion(307), easy_returns_promise(307), size_guide(304), material_deep_dive(196)
  confident_repeat_buyer  trending_now(204), personal_recs(204), material_deep_dive(196), easy_returns_promise(195), price_history(190)
  outfit_event_planner    comparison_card(182), outfit_completion(182), customers_chose(165), material_deep_dive(147), trending_now(145)
  post_return_returner    easy_returns_promise(181), comparison_card(179), size_guide(173), low_return_alts(142), customers_chose(119)
  birthday_rush_gifter    comparison_card(198), outfit_completion(198), easy_returns_promise(198), size_guide(146), low_return_alts(113)
  paralyzed_wishlister    comparison_card(194), outfit_completion(188), customers_chose(174), easy_returns_promise(134), expert_pick(128)
  mobile_evening_browser  outfit_completion(161), trending_now(161), personal_recs(159), easy_returns_promise(118), material_deep_dive(114)
  bargain_hunter_returning  comparison_card(220), trending_now(220), personal_recs(213), customers_chose(211), value_breakdown(160)
  tabbed_comparison_shopper  comparison_card(265), easy_returns_promise(265), customers_chose(247), trending_now(233), value_breakdown(188)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 rep2 — revive dead widgets for high-regret personas (confident_repeat, corporate_uniform), tame over-firing similar_items, add cov synergies)