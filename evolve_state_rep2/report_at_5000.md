# EDP CHECKPOINT REPORT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.0392
- mean oracle reward: 1.1013
- mean regret:        0.0621  (5.6% of oracle)
- cum regret (batch): 155.27

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         413    1.1842    1.3500     12.3%
  outfit_seeker            313    1.1020    1.2150      9.3%
  returner_anxious         204    1.3733    1.4800      7.2%
  browser_lurker           244    0.6043    0.6425      6.0%
  paralyzed                253    1.3727    1.4100      2.6%
  confident_buyer          311    0.5174    0.5275      1.9%
  price_sensitive          343    0.9094    0.9225      1.4%
  comparison_shopper       419    1.2322    1.2400      0.6%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  return_explainer            16.5      2.52    0.1731
  style_bridge                16.3      3.12    0.1727
  size_guide                  15.5      3.04    0.1735
  comparison_card             12.2      2.58    0.1792
  customers_chose             12.1      4.64    0.1838
  material_deep_dive          10.3      3.93    0.1763
  also_bought                  6.9      5.55    0.1504
  value_breakdown              5.7      3.46    0.1696
  similar_items                1.6      5.99    0.1030
  price_drop_notify            1.3      4.59    0.2008
  outfit_completion            1.0      5.50    0.1761
  wishlist_save                0.3      5.33    0.1977
  easy_returns_promise         0.2      5.84    0.2233
  fit_reassurance              0.1      5.62    0.2280
  brand_story                  0.0      6.00    0.2350
  expert_pick                  0.0      2.00    0.2329
  low_return_alts              0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        size_guide(413), return_explainer(413), style_bridge(413), material_deep_dive(319), comparison_card(243)
  outfit_seeker           style_bridge(313), return_explainer(308), customers_chose(242), comparison_card(241), size_guide(238)
  returner_anxious        return_explainer(204), size_guide(204), style_bridge(201), customers_chose(156), comparison_card(126)
  browser_lurker          style_bridge(244), return_explainer(242), size_guide(235), comparison_card(204), customers_chose(178)
  paralyzed               return_explainer(250), size_guide(245), style_bridge(240), customers_chose(228), material_deep_dive(190)
  confident_buyer         return_explainer(311), style_bridge(308), also_bought(294), size_guide(285), material_deep_dive(261)
  price_sensitive         return_explainer(339), style_bridge(338), comparison_card(331), size_guide(323), customers_chose(314)
  comparison_shopper      comparison_card(419), customers_chose(418), return_explainer(412), style_bridge(394), size_guide(381)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — boost dead trust/fit widgets for returner_anxious and size_anxious (highest regret), trim over-firing defaults)