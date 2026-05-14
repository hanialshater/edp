# EDP CHECKPOINT REPORT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.0333
- mean oracle reward: 1.1013
- mean regret:        0.0680  (6.2% of oracle)
- cum regret (batch): 170.00

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  browser_lurker           244    0.5625    0.6425     12.5%
  size_anxious_new         413    1.2289    1.3500      9.0%
  confident_buyer          311    0.4856    0.5275      7.9%
  outfit_seeker            313    1.1318    1.2150      6.8%
  returner_anxious         204    1.3909    1.4800      6.0%
  paralyzed                253    1.3253    1.4100      6.0%
  price_sensitive          343    0.8879    0.9225      3.8%
  comparison_shopper       419    1.2164    1.2400      1.9%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           13.4      3.15    0.1691
  easy_returns_promise        12.1      4.74    0.1723
  comparison_card             11.8      2.38    0.1776
  return_explainer            11.6      2.71    0.1684
  material_deep_dive          10.4      3.42    0.1758
  customers_chose             10.3      4.02    0.1828
  fit_reassurance             10.0      3.49    0.1894
  size_guide                   6.6      2.73    0.1674
  also_bought                  5.8      5.50    0.1456
  value_breakdown              5.2      2.85    0.1705
  price_drop_notify            1.2      4.34    0.1981
  similar_items                1.2      5.62    0.0891
  personal_recs                0.4      5.79    0.0824
  expert_pick                  0.0      1.25    0.2215
  wishlist_save                0.0      5.00    0.2207
  brand_story                  0.0      6.00    0.2067
  low_return_alts              0.0      0.00    0.0000
  style_bridge                 0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  browser_lurker          outfit_completion(235), comparison_card(199), return_explainer(183), easy_returns_promise(172), customers_chose(143)
  size_anxious_new        easy_returns_promise(385), size_guide(356), outfit_completion(356), fit_reassurance(331), material_deep_dive(320)
  confident_buyer         also_bought(291), outfit_completion(274), material_deep_dive(246), return_explainer(243), easy_returns_promise(242)
  outfit_seeker           outfit_completion(313), comparison_card(241), material_deep_dive(233), customers_chose(231), return_explainer(185)
  returner_anxious        return_explainer(204), easy_returns_promise(203), fit_reassurance(180), outfit_completion(163), comparison_card(125)
  paralyzed               customers_chose(224), fit_reassurance(191), comparison_card(183), material_deep_dive(183), return_explainer(180)
  price_sensitive         comparison_card(330), value_breakdown(307), customers_chose(293), return_explainer(243), outfit_completion(225)
  comparison_shopper      comparison_card(419), customers_chose(412), material_deep_dive(277), outfit_completion(273), fit_reassurance(260)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead returns/size/material widgets and add synergy chains to attack returner_anxious (27.3%) and size_anxious_new (18.1%) regret)