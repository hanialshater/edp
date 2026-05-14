# EDP CHECKPOINT REPORT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.0760
- mean oracle reward: 1.0996
- mean regret:        0.0236  (2.1% of oracle)
- cum regret (batch): 59.02

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  paralyzed                264    1.2939    1.4100      8.2%
  size_anxious_new         435    1.3178    1.3500      2.4%
  returner_anxious         197    1.4506    1.4800      2.0%
  outfit_seeker            289    1.1961    1.2150      1.6%
  browser_lurker           237    0.6340    0.6425      1.3%
  confident_buyer          318    0.5255    0.5275      0.4%
  comparison_shopper       396    1.2393    1.2400      0.1%
  price_sensitive          364    0.9221    0.9225      0.0%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  customers_chose             16.2      4.41    0.1782
  low_return_alts             16.0      2.93    0.1777
  size_guide                  15.6      2.99    0.1774
  outfit_completion           12.8      2.97    0.1818
  brand_story                 12.1      3.40    0.1821
  value_breakdown             11.0      4.15    0.1742
  comparison_card              5.6      2.15    0.1838
  return_explainer             4.7      4.97    0.1845
  occasion_lookbook            4.1      4.80    0.1715
  fit_reassurance              1.2      1.00    0.2223
  expert_pick                  0.4      6.00    0.2269
  material_deep_dive           0.3      4.55    0.1187
  price_drop_notify            0.0      6.00    0.1673
  style_bridge                 0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  paralyzed               customers_chose(264), low_return_alts(260), size_guide(258), brand_story(205), value_breakdown(204)
  size_anxious_new        customers_chose(400), outfit_completion(378), brand_story(373), size_guide(347), low_return_alts(339)
  returner_anxious        low_return_alts(196), return_explainer(189), size_guide(188), customers_chose(172), outfit_completion(161)
  outfit_seeker           outfit_completion(289), size_guide(289), low_return_alts(289), customers_chose(288), brand_story(237)
  browser_lurker          size_guide(237), low_return_alts(237), customers_chose(236), outfit_completion(220), brand_story(178)
  confident_buyer         size_guide(318), low_return_alts(318), customers_chose(318), brand_story(260), value_breakdown(233)
  comparison_shopper      customers_chose(396), comparison_card(394), low_return_alts(393), size_guide(360), brand_story(349)
  price_sensitive         customers_chose(363), low_return_alts(363), value_breakdown(359), size_guide(338), outfit_completion(262)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — boost dead trust/fit widgets for returner_anxious and size_anxious (highest regret), trim over-firing defaults)
  - session 5000: 16 edits (round 5000 — activate dead fit/visual/return widgets for high-regret size_anxious/outfit_seeker/browser_lurker, trim over-firing style_bridge/return_explainer/also_bought)
  - session 7500: 14 edits (round 7500 — stabilize: trim over-firing top-5 defaults, revive size_guide/return_explainer/material_deep_dive for highest-regret personas)