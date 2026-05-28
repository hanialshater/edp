# EDP CHECKPOINT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.7934
- mean oracle reward: 2.0225
- mean regret:        0.2291  (11.3% of oracle)
- cum regret (batch): 572.75

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  corporate_uniform_buyer    81    1.0259    1.4618     29.8%
  birthday_rush_gifter     149    1.9560    2.4820     21.2%
  hesitant_first_buyer     336    2.0643    2.6004     20.6%
  returner_from_recent_order   121    2.0417    2.4114     15.3%
  premium_silent_browser   177    1.8231    2.1053     13.4%
  confident_repeat_buyer   182    0.4503    0.5144     12.5%
  trend_chaser             105    2.0511    2.3312     12.0%
  size_specific_anxious    114    2.6434    2.9005      8.9%
  post_return_returner     198    2.5773    2.8039      8.1%
  outfit_event_planner     212    1.8128    1.9123      5.2%
  paralyzed_wishlister     172    2.7042    2.8495      5.1%
  mobile_evening_browser   190    1.0398    1.0955      5.1%
  tabbed_comparison_shopper   240    1.7753    1.8258      2.8%
  bargain_hunter_returning   223    1.1822    1.1832      0.1%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  outerwear        242    1.9820    2.3259     14.8%
  shoes            385    1.9608    2.2647     13.4%
  bottoms          495    1.8607    2.0960     11.2%
  dress            441    1.8848    2.1134     10.8%
  top              575    1.6136    1.7847      9.6%
  accessories      362    1.5716    1.7287      9.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  corporate_uniform_buyer shoes            9    1.2756    2.0604     38.1%
  corporate_uniform_buyer outerwear        9    1.2158    1.9353     37.2%
  corporate_uniform_buyer bottoms         15    1.1747    1.7247     31.9%
  birthday_rush_gifter   outerwear       18    2.0687    2.8620     27.7%
  corporate_uniform_buyer top             21    0.8838    1.2187     27.5%
  confident_repeat_buyer shoes           27    0.5099    0.6914     26.2%
  corporate_uniform_buyer dress           13    1.1152    1.4908     25.2%
  hesitant_first_buyer   shoes           52    2.3375    3.0647     23.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  comparison_card             13.8      2.61    0.3255
  occasion_lookbook           13.7      4.00    0.2979
  brand_story                 11.1      3.21    0.3100
  expert_pick                 10.2      2.63    0.3138
  low_return_alts             10.1      2.49    0.3072
  fit_reassurance              9.4      4.66    0.3254
  customers_chose              8.3      4.74    0.3253
  price_history                5.1      4.63    0.2495
  size_guide                   5.1      1.81    0.2517
  trending_now                 4.3      5.82    0.2152
  outfit_completion            3.2      3.18    0.2746
  return_explainer             2.4      3.38    0.3050
  value_breakdown              2.1      2.89    0.2626
  wishlist_save                0.6      5.51    0.1407
  recently_viewed              0.3      5.98    0.0749
  style_bridge                 0.2      1.00    0.3564
  also_bought                  0.2      6.00    0.1619
  price_drop_notify            0.1      5.40    0.1762
  easy_returns_promise         0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  corporate_uniform_buyer  occasion_lookbook(81), comparison_card(78), expert_pick(76), low_return_alts(72), trending_now(65)
  birthday_rush_gifter    low_return_alts(147), comparison_card(146), occasion_lookbook(120), brand_story(113), customers_chose(103)
  hesitant_first_buyer    low_return_alts(336), occasion_lookbook(335), comparison_card(333), brand_story(316), size_guide(298)
  returner_from_recent_order  low_return_alts(118), comparison_card(116), occasion_lookbook(110), brand_story(108), expert_pick(86)
  premium_silent_browser  occasion_lookbook(175), comparison_card(172), expert_pick(171), brand_story(126), fit_reassurance(119)
  confident_repeat_buyer  occasion_lookbook(182), brand_story(182), size_guide(158), low_return_alts(158), trending_now(150)
  trend_chaser            brand_story(102), expert_pick(85), outfit_completion(78), occasion_lookbook(65), fit_reassurance(62)
  size_specific_anxious   low_return_alts(114), comparison_card(113), fit_reassurance(106), expert_pick(106), brand_story(93)
  post_return_returner    low_return_alts(198), comparison_card(197), fit_reassurance(194), occasion_lookbook(177), expert_pick(158)
  outfit_event_planner    comparison_card(212), brand_story(201), outfit_completion(201), fit_reassurance(178), customers_chose(169)
  paralyzed_wishlister    comparison_card(172), expert_pick(172), customers_chose(172), occasion_lookbook(172), brand_story(115)
  mobile_evening_browser  size_guide(145), low_return_alts(143), occasion_lookbook(138), outfit_completion(137), expert_pick(130)
  tabbed_comparison_shopper  comparison_card(240), fit_reassurance(227), return_explainer(226), expert_pick(203), customers_chose(197)
  bargain_hunter_returning  comparison_card(223), occasion_lookbook(223), fit_reassurance(222), expert_pick(203), customers_chose(179)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 rep2 — revive dead widgets for high-regret personas (confident_repeat, corporate_uniform), tame over-firing similar_items, add cov synergies)
  - session 5000: 16 edits (round 5000 rep2 — boost premium/corporate/trend underperformers, revive dead widgets (brand_story, fit_reassurance, return_explainer, price_drop_notify), curb over-firing easy_returns_promise/personal_recs)
  - session 7500: 13 edits (round 7500 rep2 — stabilization: nudge confident_repeat/returner shoes+bottoms, lift dead widgets gently, trim over-fire)