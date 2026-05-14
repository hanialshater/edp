# EDP CHECKPOINT REPORT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.0600
- mean oracle reward: 1.0996
- mean regret:        0.0397  (3.6% of oracle)
- cum regret (batch): 99.16

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         435    1.2544    1.3500      7.1%
  browser_lurker           237    0.6101    0.6425      5.0%
  returner_anxious         197    1.4245    1.4800      3.7%
  outfit_seeker            289    1.1720    1.2150      3.5%
  paralyzed                264    1.3778    1.4100      2.3%
  price_sensitive          364    0.9025    0.9225      2.2%
  comparison_shopper       396    1.2194    1.2400      1.7%
  confident_buyer          318    0.5194    0.5275      1.5%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           15.9      3.35    0.1755
  comparison_card             14.5      3.39    0.1813
  brand_story                 10.8      3.08    0.1756
  customers_chose              9.9      4.87    0.1830
  fit_reassurance              9.0      4.33    0.1728
  expert_pick                  8.1      2.19    0.1905
  size_guide                   7.7      2.09    0.1830
  low_return_alts              7.1      4.26    0.1717
  price_drop_notify            5.0      4.45    0.1615
  return_explainer             4.5      2.50    0.1981
  wishlist_save                3.2      4.43    0.1322
  value_breakdown              2.4      2.45    0.1644
  price_history                1.5      5.00    0.1722
  easy_returns_promise         0.5      4.47    0.1101
  occasion_lookbook            0.1      5.36    0.1381
  similar_items                0.0      6.00    0.1014
  style_bridge                 0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        outfit_completion(432), size_guide(429), brand_story(388), comparison_card(344), low_return_alts(335)
  browser_lurker          outfit_completion(237), comparison_card(222), brand_story(179), customers_chose(176), low_return_alts(135)
  returner_anxious        return_explainer(194), outfit_completion(191), comparison_card(169), fit_reassurance(154), expert_pick(133)
  outfit_seeker           outfit_completion(289), comparison_card(267), brand_story(233), customers_chose(215), fit_reassurance(193)
  paralyzed               expert_pick(264), comparison_card(259), outfit_completion(218), customers_chose(210), size_guide(135)
  price_sensitive         comparison_card(364), outfit_completion(334), expert_pick(285), fit_reassurance(273), value_breakdown(236)
  comparison_shopper      comparison_card(396), customers_chose(373), outfit_completion(369), brand_story(251), fit_reassurance(248)
  confident_buyer         outfit_completion(312), brand_story(296), wishlist_save(249), fit_reassurance(219), price_drop_notify(211)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive trust/fit/visual dead widgets for returner_anxious & size_anxious_new; trim defaults that crowd confident_buyer/browser_lurker)
  - session 5000: 16 edits (round 5000 — push fit widgets for size_anxious_new (worst regret), revive expert_pick/wishlist for paralyzed, trim over-firing outfit_completion & material_deep_dive, activate brand_story for browser_lurker)
  - session 7500: 15 edits (round 7500 — stabilize: trim over-firing fit/style/expert defaults, revive dead F43/F33/F51 widgets, rebalance for confident_buyer & outfit_seeker)