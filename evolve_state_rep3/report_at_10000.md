# EDP CHECKPOINT REPORT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.0749
- mean oracle reward: 1.0996
- mean regret:        0.0247  (2.2% of oracle)
- cum regret (batch): 61.85

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  returner_anxious         197    1.3789    1.4800      6.8%
  size_anxious_new         435    1.2982    1.3500      3.8%
  outfit_seeker            289    1.1725    1.2150      3.5%
  paralyzed                264    1.3938    1.4100      1.1%
  confident_buyer          318    0.5234    0.5275      0.8%
  browser_lurker           237    0.6397    0.6425      0.4%
  price_sensitive          364    0.9213    0.9225      0.1%
  comparison_shopper       396    1.2388    1.2400      0.1%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  customers_chose             14.0      3.76    0.1844
  comparison_card             13.1      2.53    0.1773
  occasion_lookbook           12.8      3.38    0.1748
  material_deep_dive          11.2      3.65    0.1790
  easy_returns_promise        10.6      4.64    0.1629
  low_return_alts              8.2      2.29    0.2010
  fit_reassurance              7.5      4.88    0.1679
  value_breakdown              5.6      3.02    0.1798
  expert_pick                  4.7      4.77    0.1716
  size_guide                   4.7      2.09    0.1926
  outfit_completion            4.4      2.12    0.1889
  price_history                2.1      5.60    0.1669
  price_drop_notify            0.8      5.52    0.2148
  return_explainer             0.4      2.95    0.2039
  wishlist_save                0.1      6.00    0.1438
  style_bridge                 0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  returner_anxious        low_return_alts(197), fit_reassurance(165), customers_chose(160), occasion_lookbook(154), comparison_card(123)
  size_anxious_new        low_return_alts(370), material_deep_dive(354), customers_chose(320), occasion_lookbook(313), size_guide(305)
  outfit_seeker           easy_returns_promise(278), material_deep_dive(244), customers_chose(242), outfit_completion(239), comparison_card(234)
  paralyzed               customers_chose(264), occasion_lookbook(191), low_return_alts(181), expert_pick(163), comparison_card(154)
  confident_buyer         easy_returns_promise(318), occasion_lookbook(313), fit_reassurance(304), material_deep_dive(266), comparison_card(209)
  browser_lurker          comparison_card(218), easy_returns_promise(209), customers_chose(202), material_deep_dive(196), occasion_lookbook(157)
  price_sensitive         customers_chose(362), value_breakdown(357), occasion_lookbook(330), comparison_card(325), easy_returns_promise(237)
  comparison_shopper      comparison_card(396), customers_chose(396), occasion_lookbook(376), material_deep_dive(306), easy_returns_promise(295)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive returns/size/premium dead widgets and dampen low-reward defaults)
  - session 5000: 16 edits (round 5000 — dial back overfiring style_bridge/return_explainer, revive dead outfit/premium/price/action widgets, boost size_anxious serving)
  - session 7500: 14 edits (round 7500 — stabilization: dampen overfiring outfit/brand/wishlist, revive silent style_bridge/material/customers_chose/occasion, soften default trim)