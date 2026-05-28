# EDP CHECKPOINT REPORT — sessions 0 → 2500  (N=2500)

## Aggregate performance
- mean reward:        0.9969
- mean oracle reward: 1.1094
- mean regret:        0.1125  (10.1% of oracle)
- cum regret (batch): 281.19

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  returner_anxious         221    1.0765    1.4800     27.3%
  size_anxious_new         463    1.1063    1.3500     18.1%
  browser_lurker           245    0.5832    0.6425      9.2%
  confident_buyer          304    0.4851    0.5275      8.0%
  outfit_seeker            293    1.1380    1.2150      6.3%
  paralyzed                242    1.3665    1.4100      3.1%
  price_sensitive          319    0.9002    0.9225      2.4%
  comparison_shopper       413    1.2121    1.2400      2.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  similar_items               15.7      4.90    0.1625
  outfit_completion           15.1      2.72    0.1654
  customers_chose             12.2      3.51    0.1764
  comparison_card             11.8      1.94    0.1740
  also_bought                  9.5      5.28    0.1512
  fit_reassurance              9.3      2.96    0.1723
  brand_story                  9.0      3.14    0.1723
  value_breakdown              6.4      2.48    0.1623
  low_return_alts              4.9      2.73    0.1839
  personal_recs                3.2      5.36    0.1156
  price_drop_notify            1.5      4.23    0.2160
  trending_now                 1.3      5.79    0.0877
  expert_pick                  0.1      1.75    0.2210
  style_bridge                 0.0      1.00    0.1744
  return_explainer             0.0      3.00    0.2069
  easy_returns_promise         0.0      6.00    0.2037
  size_guide                   0.0      0.00    0.0000
  occasion_lookbook            0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  returner_anxious        low_return_alts(220), similar_items(207), outfit_completion(202), customers_chose(179), comparison_card(133)
  size_anxious_new        outfit_completion(446), similar_items(443), fit_reassurance(442), brand_story(312), comparison_card(274)
  browser_lurker          similar_items(245), outfit_completion(242), comparison_card(184), also_bought(176), fit_reassurance(171)
  confident_buyer         similar_items(304), also_bought(304), personal_recs(263), outfit_completion(261), brand_story(209)
  outfit_seeker           outfit_completion(293), similar_items(293), also_bought(250), customers_chose(230), comparison_card(219)
  paralyzed               customers_chose(240), outfit_completion(208), comparison_card(187), brand_story(175), price_drop_notify(172)
  price_sensitive         similar_items(317), comparison_card(301), value_breakdown(300), customers_chose(299), outfit_completion(285)
  comparison_shopper      comparison_card(413), customers_chose(413), similar_items(405), outfit_completion(321), brand_story(235)

## Edit history applied so far
  (none — this is the baseline run)