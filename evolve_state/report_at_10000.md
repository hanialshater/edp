# EDP CHECKPOINT REPORT — sessions 7500 → 10000  (N=2500)

## Aggregate performance
- mean reward:        1.0121
- mean oracle reward: 1.0996
- mean regret:        0.0875  (8.0% of oracle)
- cum regret (batch): 218.84

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         435    1.1467    1.3500     15.1%
  browser_lurker           237    0.5634    0.6425     12.3%
  confident_buyer          318    0.4713    0.5275     10.7%
  outfit_seeker            289    1.1142    1.2150      8.3%
  returner_anxious         197    1.3576    1.4800      8.3%
  comparison_shopper       396    1.1928    1.2400      3.8%
  price_sensitive          364    0.8897    0.9225      3.6%
  paralyzed                264    1.3726    1.4100      2.7%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           16.0      3.06    0.1676
  comparison_card             12.7      2.75    0.1757
  size_guide                  12.1      2.44    0.1684
  expert_pick                 11.8      3.42    0.1715
  return_explainer            11.5      3.34    0.1758
  customers_chose             10.1      5.27    0.1787
  price_history                7.9      3.86    0.1574
  brand_story                  6.8      3.42    0.1712
  fit_reassurance              5.8      4.92    0.1571
  value_breakdown              2.0      1.72    0.1637
  material_deep_dive           1.3      5.30    0.1386
  trending_now                 1.0      5.88    0.0983
  wishlist_save                0.9      5.84    0.1285
  easy_returns_promise         0.3      5.85    0.2241
  personal_recs                0.1      6.00    0.0773
  low_return_alts              0.0      4.00    0.2158
  style_bridge                 0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        size_guide(435), return_explainer(433), outfit_completion(432), brand_story(307), comparison_card(251)
  browser_lurker          outfit_completion(237), comparison_card(205), size_guide(203), return_explainer(176), customers_chose(170)
  confident_buyer         outfit_completion(315), price_history(260), size_guide(259), brand_story(194), fit_reassurance(185)
  outfit_seeker           outfit_completion(289), comparison_card(228), expert_pick(205), customers_chose(195), size_guide(181)
  returner_anxious        size_guide(197), return_explainer(197), outfit_completion(189), expert_pick(162), comparison_card(147)
  comparison_shopper      comparison_card(396), customers_chose(370), outfit_completion(360), expert_pick(291), price_history(251)
  price_sensitive         comparison_card(363), outfit_completion(336), expert_pick(329), customers_chose(243), return_explainer(229)
  paralyzed               expert_pick(264), customers_chose(254), comparison_card(239), outfit_completion(237), return_explainer(216)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead returns/size/material widgets and add synergy chains to attack returner_anxious (27.3%) and size_anxious_new (18.1%) regret)
  - session 5000: 16 edits (round 5000 — revive dead style/visual widgets for browser_lurker/confident_buyer/outfit_seeker; dial back over-firing returns widgets on personas that don't need F46)
  - session 7500: 12 edits (round 7500 — stabilize: pull back over-firing brand_story/style_bridge/occasion_lookbook, revive outfit_completion/easy_returns_promise/similar_items, fix size_anxious_new composition)