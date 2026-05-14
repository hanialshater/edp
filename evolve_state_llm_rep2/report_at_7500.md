# EDP CHECKPOINT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.8009
- mean oracle reward: 1.9777
- mean regret:        0.1768  (8.9% of oracle)
- cum regret (batch): 441.97

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_repeat_buyer   216    0.4199    0.5145     18.4%
  returner_from_recent_order   108    2.0723    2.4577     15.7%
  hesitant_first_buyer     287    2.2505    2.6232     14.2%
  trend_chaser             115    1.9820    2.3063     14.1%
  premium_silent_browser   143    1.8233    2.1175     13.9%
  birthday_rush_gifter     142    2.1487    2.4712     13.1%
  corporate_uniform_buyer   126    1.2867    1.4520     11.4%
  paralyzed_wishlister     198    2.6562    2.8462      6.7%
  outfit_event_planner     192    1.7811    1.9051      6.5%
  size_specific_anxious    120    2.6911    2.8673      6.1%
  post_return_returner     179    2.6160    2.7828      6.0%
  mobile_evening_browser   187    1.0610    1.0869      2.4%
  tabbed_comparison_shopper   262    1.7693    1.7976      1.6%
  bargain_hunter_returning   225    1.1775    1.1877      0.9%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            367    1.9135    2.1880     12.5%
  outerwear        231    2.0577    2.3378     12.0%
  bottoms          507    1.8410    2.0195      8.8%
  dress            450    1.8356    2.0100      8.7%
  accessories      407    1.6193    1.7337      6.6%
  top              538    1.6845    1.7978      6.3%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  confident_repeat_buyer shoes           33    0.4662    0.6914     32.6%
  confident_repeat_buyer outerwear       16    0.5165    0.6885     25.0%
  trend_chaser           accessories     21    2.2904    2.8803     20.5%
  returner_from_recent_order bottoms         26    2.0916    2.6170     20.1%
  premium_silent_browser shoes           26    1.9930    2.4827     19.7%
  returner_from_recent_order shoes           19    2.3073    2.8524     19.1%
  confident_repeat_buyer bottoms         43    0.3771    0.4645     18.8%
  hesitant_first_buyer   shoes           48    2.5036    3.0647     18.3%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  occasion_lookbook           14.9      3.85    0.3001
  fit_reassurance             14.0      2.96    0.3037
  brand_story                 13.2      2.83    0.3095
  comparison_card             11.4      2.44    0.3263
  customers_chose             10.2      3.58    0.3431
  low_return_alts              6.2      4.02    0.3754
  wishlist_save                6.1      4.50    0.2288
  trending_now                 5.9      5.52    0.2112
  price_history                4.8      4.76    0.2592
  expert_pick                  2.9      2.68    0.3261
  return_explainer             2.8      3.04    0.2944
  outfit_completion            2.6      3.03    0.2765
  value_breakdown              2.5      2.82    0.2570
  personal_recs                0.9      5.97    0.1161
  price_drop_notify            0.9      4.20    0.3718
  size_guide                   0.5      1.40    0.2988
  style_bridge                 0.2      1.00    0.3251
  easy_returns_promise         0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_repeat_buyer  brand_story(216), occasion_lookbook(216), wishlist_save(216), trending_now(216), fit_reassurance(214)
  returner_from_recent_order  brand_story(104), customers_chose(93), occasion_lookbook(89), low_return_alts(88), fit_reassurance(72)
  hesitant_first_buyer    occasion_lookbook(287), low_return_alts(283), comparison_card(276), brand_story(272), fit_reassurance(248)
  trend_chaser            brand_story(115), fit_reassurance(115), trending_now(94), outfit_completion(84), wishlist_save(69)
  premium_silent_browser  occasion_lookbook(142), brand_story(124), comparison_card(119), return_explainer(102), fit_reassurance(96)
  birthday_rush_gifter    brand_story(141), low_return_alts(140), fit_reassurance(138), customers_chose(136), occasion_lookbook(135)
  corporate_uniform_buyer  occasion_lookbook(126), comparison_card(113), fit_reassurance(95), trending_now(76), expert_pick(74)
  paralyzed_wishlister    occasion_lookbook(198), customers_chose(198), fit_reassurance(197), comparison_card(171), brand_story(169)
  outfit_event_planner    brand_story(189), customers_chose(187), fit_reassurance(184), outfit_completion(166), comparison_card(161)
  size_specific_anxious   fit_reassurance(120), low_return_alts(120), occasion_lookbook(110), brand_story(107), customers_chose(95)
  post_return_returner    fit_reassurance(179), low_return_alts(179), occasion_lookbook(175), brand_story(169), customers_chose(163)
  mobile_evening_browser  fit_reassurance(187), wishlist_save(180), brand_story(178), trending_now(169), occasion_lookbook(141)
  tabbed_comparison_shopper  comparison_card(262), customers_chose(250), return_explainer(246), occasion_lookbook(243), value_breakdown(161)
  bargain_hunter_returning  comparison_card(225), occasion_lookbook(225), customers_chose(207), fit_reassurance(189), value_breakdown(158)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 rep2 — revive dead widgets for high-regret personas (confident_repeat, corporate_uniform), tame over-firing similar_items, add cov synergies)
  - session 5000: 16 edits (round 5000 rep2 — boost premium/corporate/trend underperformers, revive dead widgets (brand_story, fit_reassurance, return_explainer, price_drop_notify), curb over-firing easy_returns_promise/personal_recs)