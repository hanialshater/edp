# EDP CHECKPOINT REPORT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.0661
- mean oracle reward: 1.1019
- mean regret:        0.0358  (3.3% of oracle)
- cum regret (batch): 89.57

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  confident_buyer          289    0.4887    0.5275      7.4%
  outfit_seeker            313    1.1479    1.2150      5.5%
  returner_anxious         172    1.4118    1.4800      4.6%
  browser_lurker           246    0.6147    0.6425      4.3%
  size_anxious_new         433    1.2928    1.3500      4.2%
  price_sensitive          383    0.9100    0.9225      1.4%
  paralyzed                283    1.3936    1.4100      1.2%
  comparison_shopper       381    1.2280    1.2400      1.0%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  style_bridge                16.0      3.39    0.1766
  fit_reassurance             15.2      3.06    0.1748
  expert_pick                 14.3      2.46    0.1782
  comparison_card             14.1      3.12    0.1823
  customers_chose             11.6      5.13    0.1796
  brand_story                  9.6      3.16    0.1855
  easy_returns_promise         5.3      5.50    0.1434
  price_history                4.0      5.02    0.1709
  low_return_alts              2.9      3.72    0.2196
  value_breakdown              2.6      2.52    0.1667
  size_guide                   1.5      1.08    0.2075
  return_explainer             1.2      1.96    0.2145
  personal_recs                1.2      5.77    0.1120
  occasion_lookbook            0.3      5.73    0.1729
  price_drop_notify            0.0      4.57    0.2273
  similar_items                0.0      6.00    0.0692
  wishlist_save                0.0      5.00    0.2291
  outfit_completion            0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  confident_buyer         fit_reassurance(289), style_bridge(288), expert_pick(280), easy_returns_promise(235), brand_story(187)
  outfit_seeker           style_bridge(313), fit_reassurance(313), comparison_card(284), customers_chose(264), expert_pick(256)
  returner_anxious        fit_reassurance(172), style_bridge(163), expert_pick(156), comparison_card(151), return_explainer(100)
  browser_lurker          style_bridge(246), fit_reassurance(231), comparison_card(223), customers_chose(210), brand_story(164)
  size_anxious_new        style_bridge(431), brand_story(361), expert_pick(344), low_return_alts(342), comparison_card(287)
  price_sensitive         comparison_card(383), fit_reassurance(382), expert_pick(359), style_bridge(354), customers_chose(330)
  paralyzed               expert_pick(283), comparison_card(281), fit_reassurance(270), customers_chose(268), style_bridge(243)
  comparison_shopper      comparison_card(381), fit_reassurance(380), customers_chose(367), style_bridge(359), expert_pick(322)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive trust/fit/visual dead widgets for returner_anxious & size_anxious_new; trim defaults that crowd confident_buyer/browser_lurker)
  - session 5000: 16 edits (round 5000 — push fit widgets for size_anxious_new (worst regret), revive expert_pick/wishlist for paralyzed, trim over-firing outfit_completion & material_deep_dive, activate brand_story for browser_lurker)