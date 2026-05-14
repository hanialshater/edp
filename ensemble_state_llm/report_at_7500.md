# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.7036
- mean oracle reward: 1.9777
- mean regret:        0.2741  (13.9% of oracle)
- cum regret (batch): 685.37

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   216    0.3259    0.5145     36.7%
  size_specific_anxious    120    2.2153    2.8673     22.7%
  hesitant_first_buyer     287    2.1338    2.6232     18.7%
  trend_chaser             115    1.8876    2.3063     18.2%
  post_return_returner     179    2.2981    2.7828     17.4%
  returner_from_recent_order   108    2.0397    2.4577     17.0%
  premium_silent_browser   143    1.7655    2.1175     16.6%
  birthday_rush_gifter     142    2.0789    2.4712     15.9%
  outfit_event_planner     192    1.6709    1.9051     12.3%
  corporate_uniform_buyer   126    1.2918    1.4520     11.0%
  paralyzed_wishlister     198    2.6837    2.8462      5.7%
  bargain_hunter_returning   225    1.1204    1.1877      5.7%
  tabbed_comparison_shopper   262    1.7201    1.7976      4.3%
  mobile_evening_browser   187    1.0490    1.0869      3.5%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.8144    2.1880     17.1%
  outerwear        231    1.9916    2.3378     14.8%
  accessories      407    1.4809    1.7337     14.6%
  top              538    1.5514    1.7978     13.7%
  dress            450    1.7493    2.0100     13.0%
  bottoms          507    1.7917    2.0195     11.3%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           33    0.3401    0.6914     50.8%
  confident_repeat_buyer bottoms         43    0.2693    0.4645     42.0%
  confident_repeat_buyer outerwear       16    0.4265    0.6885     38.0%
  confident_repeat_buyer top             44    0.2586    0.4070     36.5%
  size_specific_anxious  accessories     17    1.4792    2.2723     34.9%
  confident_repeat_buyer dress           44    0.3774    0.5304     28.8%
  premium_silent_browser shoes           26    1.8364    2.4827     26.0%
  post_return_returner   accessories     29    1.5536    2.0918     25.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  occasion_lookbook           14.9      3.47    0.2785
  low_return_alts             14.0      3.06    0.3077
  recently_viewed             12.7      4.00    0.2645
  expert_pick                 11.4      3.28    0.2850
  comparison_card              9.6      2.73    0.3219
  value_breakdown              9.0      2.71    0.2624
  size_guide                   7.9      4.57    0.2995
  fit_reassurance              4.1      1.02    0.3648
  brand_story                  4.0      3.05    0.2753
  price_history                3.6      5.15    0.2485
  personal_recs                3.2      5.89    0.1454
  material_deep_dive           2.6      5.20    0.2589
  easy_returns_promise         1.4      5.60    0.3339
  customers_chose              1.0      3.15    0.2649
  style_bridge                 0.3      1.35    0.3062
  outfit_completion            0.2      5.88    0.2680
  trending_now                 0.1      5.00    0.0728
  return_explainer             0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  occasion_lookbook(216), recently_viewed(216), personal_recs(200), expert_pick(118), value_breakdown(117)
  size_specific_anxious   low_return_alts(120), size_guide(120), expert_pick(115), fit_reassurance(106), comparison_card(89)
  hesitant_first_buyer    low_return_alts(287), occasion_lookbook(287), size_guide(270), value_breakdown(260), fit_reassurance(237)
  trend_chaser            occasion_lookbook(115), recently_viewed(112), low_return_alts(111), brand_story(97), value_breakdown(54)
  post_return_returner    low_return_alts(179), size_guide(178), fit_reassurance(148), expert_pick(140), comparison_card(122)
  returner_from_recent_order  low_return_alts(108), occasion_lookbook(108), expert_pick(92), comparison_card(69), easy_returns_promise(68)
  premium_silent_browser  low_return_alts(143), recently_viewed(143), value_breakdown(139), occasion_lookbook(135), material_deep_dive(118)
  birthday_rush_gifter    low_return_alts(142), occasion_lookbook(142), size_guide(135), recently_viewed(126), brand_story(100)
  outfit_event_planner    occasion_lookbook(192), recently_viewed(191), expert_pick(185), comparison_card(177), low_return_alts(144)
  corporate_uniform_buyer  low_return_alts(126), recently_viewed(126), occasion_lookbook(123), size_guide(110), expert_pick(102)
  paralyzed_wishlister    comparison_card(198), expert_pick(198), occasion_lookbook(198), low_return_alts(197), recently_viewed(189)
  bargain_hunter_returning  comparison_card(225), occasion_lookbook(224), price_history(222), expert_pick(220), value_breakdown(216)
  tabbed_comparison_shopper  comparison_card(262), low_return_alts(262), expert_pick(262), price_history(186), value_breakdown(182)
  mobile_evening_browser  occasion_lookbook(187), recently_viewed(187), personal_recs(165), low_return_alts(155), size_guide(145)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 draw1 — revive dead widgets, boost low-need personas, dampen over-firing defaults  [ensemble-best of 1: draw 1])
  - session 2500: 16 edits (round 2500 draw2 — aggressively trim default widgets that crowd out specialists; raise base for dead widgets serving worst personas (confident_repeat, corporate_uniform); add cross-widget synergies  [ensemble-best of 3: draw 2])
  - session 5000: 16 edits (round 5000 draw1 — revive dead widgets (size_guide, occasion_lookbook, personal_recs, trending_now), tame over-firing low-reward widgets, boost confident_repeat/trend_chaser cells, add F32->F46 and F43->F33 synergies  [ensemble-best of 3: draw 1])