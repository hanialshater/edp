# EDP CHECKPOINT REPORT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.0506
- mean oracle reward: 1.1013
- mean regret:        0.0507  (4.6% of oracle)
- cum regret (batch): 126.68

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         413    1.1974    1.3500     11.3%
  returner_anxious         204    1.3935    1.4800      5.8%
  outfit_seeker            313    1.1492    1.2150      5.4%
  browser_lurker           244    0.6276    0.6425      2.3%
  comparison_shopper       419    1.2141    1.2400      2.1%
  paralyzed                253    1.3877    1.4100      1.6%
  confident_buyer          311    0.5200    0.5275      1.4%
  price_sensitive          343    0.9138    0.9225      0.9%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  return_explainer            16.4      2.64    0.1745
  style_bridge                15.3      3.08    0.1739
  comparison_card             14.7      3.16    0.1788
  expert_pick                 10.0      3.81    0.1797
  material_deep_dive           8.8      3.43    0.1675
  fit_reassurance              8.5      4.42    0.1666
  size_guide                   8.2      2.04    0.1842
  customers_chose              7.9      5.61    0.1796
  value_breakdown              5.6      3.69    0.1726
  occasion_lookbook            2.4      5.63    0.1818
  similar_items                1.6      5.98    0.1309
  easy_returns_promise         0.3      5.98    0.2319
  low_return_alts              0.2      1.00    0.2228
  also_bought                  0.0      6.00    0.0739
  price_drop_notify            0.0      4.50    0.1271
  wishlist_save                0.0      6.00    0.2312
  outfit_completion            0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        style_bridge(405), size_guide(401), return_explainer(401), comparison_card(324), material_deep_dive(319)
  returner_anxious        comparison_card(187), return_explainer(187), style_bridge(186), expert_pick(153), size_guide(128)
  outfit_seeker           style_bridge(313), return_explainer(308), comparison_card(272), fit_reassurance(227), material_deep_dive(198)
  browser_lurker          style_bridge(242), return_explainer(241), comparison_card(228), material_deep_dive(167), customers_chose(156)
  comparison_shopper      comparison_card(419), return_explainer(417), style_bridge(342), fit_reassurance(258), customers_chose(242)
  paralyzed               expert_pick(253), comparison_card(252), return_explainer(251), style_bridge(218), customers_chose(184)
  confident_buyer         return_explainer(311), style_bridge(291), material_deep_dive(276), fit_reassurance(262), expert_pick(198)
  price_sensitive         comparison_card(343), return_explainer(342), value_breakdown(335), style_bridge(294), fit_reassurance(223)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive returns/size/premium dead widgets and dampen low-reward defaults)