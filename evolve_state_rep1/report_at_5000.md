# EDP CHECKPOINT REPORT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.0542
- mean oracle reward: 1.1013
- mean regret:        0.0471  (4.3% of oracle)
- cum regret (batch): 117.82

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         413    1.1980    1.3500     11.3%
  paralyzed                253    1.3178    1.4100      6.5%
  browser_lurker           244    0.6249    0.6425      2.7%
  returner_anxious         204    1.4454    1.4800      2.3%
  outfit_seeker            313    1.1868    1.2150      2.3%
  confident_buyer          311    0.5183    0.5275      1.7%
  price_sensitive          343    0.9094    0.9225      1.4%
  comparison_shopper       419    1.2299    1.2400      0.8%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           15.6      3.67    0.1753
  return_explainer            14.3      2.82    0.1780
  comparison_card             13.6      2.78    0.1777
  customers_chose             13.3      4.57    0.1827
  material_deep_dive          13.1      3.17    0.1776
  fit_reassurance             10.1      3.91    0.1751
  size_guide                   6.6      2.20    0.1779
  price_history                3.6      4.76    0.1642
  value_breakdown              3.3      2.39    0.1694
  low_return_alts              2.0      5.08    0.1565
  wishlist_save                1.6      5.43    0.1559
  price_drop_notify            1.3      4.53    0.2020
  similar_items                1.1      5.94    0.1266
  occasion_lookbook            0.3      3.88    0.1115
  also_bought                  0.1      6.00    0.0864
  style_bridge                 0.0      1.00    0.1548
  easy_returns_promise         0.0      5.43    0.1296
  expert_pick                  0.0      1.00    0.2308
  brand_story                  0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        outfit_completion(413), return_explainer(386), material_deep_dive(371), size_guide(365), comparison_card(288)
  paralyzed               return_explainer(237), customers_chose(231), material_deep_dive(219), outfit_completion(216), comparison_card(187)
  browser_lurker          outfit_completion(241), comparison_card(226), material_deep_dive(214), customers_chose(212), return_explainer(190)
  returner_anxious        return_explainer(204), fit_reassurance(199), outfit_completion(197), material_deep_dive(166), customers_chose(163)
  outfit_seeker           outfit_completion(309), material_deep_dive(283), comparison_card(271), customers_chose(267), return_explainer(228)
  confident_buyer         material_deep_dive(294), outfit_completion(279), return_explainer(244), fit_reassurance(238), comparison_card(172)
  price_sensitive         comparison_card(330), outfit_completion(323), customers_chose(315), return_explainer(313), value_breakdown(270)
  comparison_shopper      comparison_card(419), customers_chose(415), outfit_completion(360), material_deep_dive(358), return_explainer(336)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive trust/fit/visual dead widgets for returner_anxious & size_anxious_new; trim defaults that crowd confident_buyer/browser_lurker)