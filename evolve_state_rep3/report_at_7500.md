# EDP CHECKPOINT REPORT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.0376
- mean oracle reward: 1.1019
- mean regret:        0.0643  (5.8% of oracle)
- cum regret (batch): 160.72

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  comparison_shopper       381    1.1152    1.2400     10.1%
  price_sensitive          383    0.8317    0.9225      9.8%
  returner_anxious         172    1.3633    1.4800      7.9%
  paralyzed                283    1.3223    1.4100      6.2%
  size_anxious_new         433    1.2889    1.3500      4.5%
  browser_lurker           246    0.6304    0.6425      1.9%
  outfit_seeker            313    1.2029    1.2150      1.0%
  confident_buyer          289    0.5265    0.5275      0.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           16.6      2.50    0.1728
  wishlist_save               15.9      4.08    0.1736
  brand_story                 15.2      3.93    0.1750
  comparison_card             13.6      2.80    0.1752
  easy_returns_promise         9.3      4.61    0.1514
  low_return_alts              8.2      2.26    0.1946
  fit_reassurance              6.6      5.06    0.1644
  price_history                6.1      4.81    0.1616
  size_guide                   4.8      1.96    0.1830
  price_drop_notify            1.9      4.33    0.1887
  value_breakdown              0.9      1.32    0.1416
  return_explainer             0.5      3.12    0.1903
  expert_pick                  0.3      2.17    0.2313
  occasion_lookbook            0.0      6.00    0.1548
  customers_chose              0.0      6.00    0.2269
  style_bridge                 0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  comparison_shopper      comparison_card(381), outfit_completion(375), wishlist_save(372), brand_story(360), easy_returns_promise(248)
  price_sensitive         comparison_card(383), outfit_completion(382), wishlist_save(303), brand_story(255), low_return_alts(236)
  returner_anxious        low_return_alts(172), outfit_completion(172), wishlist_save(170), brand_story(153), comparison_card(134)
  paralyzed               comparison_card(281), outfit_completion(281), wishlist_save(268), brand_story(263), low_return_alts(192)
  size_anxious_new        outfit_completion(433), wishlist_save(432), brand_story(419), low_return_alts(366), size_guide(306)
  browser_lurker          outfit_completion(246), brand_story(244), wishlist_save(241), easy_returns_promise(220), comparison_card(218)
  outfit_seeker           outfit_completion(313), wishlist_save(313), brand_story(306), easy_returns_promise(303), comparison_card(263)
  confident_buyer         outfit_completion(289), easy_returns_promise(289), wishlist_save(288), brand_story(287), fit_reassurance(279)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive returns/size/premium dead widgets and dampen low-reward defaults)
  - session 5000: 16 edits (round 5000 — dial back overfiring style_bridge/return_explainer, revive dead outfit/premium/price/action widgets, boost size_anxious serving)