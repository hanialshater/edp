# EDP CHECKPOINT REPORT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.0631
- mean oracle reward: 1.1019
- mean regret:        0.0387  (3.5% of oracle)
- cum regret (batch): 96.85

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         433    1.2333    1.3500      8.6%
  outfit_seeker            313    1.1807    1.2150      2.8%
  browser_lurker           246    0.6247    0.6425      2.8%
  price_sensitive          383    0.8977    0.9225      2.7%
  paralyzed                283    1.3817    1.4100      2.0%
  confident_buyer          289    0.5185    0.5275      1.7%
  returner_anxious         172    1.4555    1.4800      1.7%
  comparison_shopper       381    1.2219    1.2400      1.5%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  brand_story                 13.3      2.99    0.1761
  style_bridge                12.7      2.37    0.1758
  comparison_card             11.9      2.42    0.1839
  fit_reassurance             10.7      3.54    0.1886
  customers_chose              9.9      4.85    0.1856
  return_explainer             7.9      3.45    0.1849
  price_history                7.5      3.98    0.1713
  trending_now                 6.7      5.31    0.1477
  occasion_lookbook            5.2      4.70    0.1798
  size_guide                   4.2      2.88    0.1884
  expert_pick                  3.9      2.62    0.2010
  also_bought                  2.2      5.64    0.1004
  wishlist_save                2.0      4.83    0.1649
  value_breakdown              1.6      1.33    0.1613
  material_deep_dive           0.4      5.43    0.1501
  price_drop_notify            0.0      3.50    0.1900
  personal_recs                0.0      6.00    0.0862
  low_return_alts              0.0      0.00    0.0000
  outfit_completion            0.0      0.00    0.0000
  easy_returns_promise         0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        brand_story(420), size_guide(387), style_bridge(369), fit_reassurance(346), return_explainer(268)
  outfit_seeker           style_bridge(313), brand_story(288), comparison_card(230), trending_now(203), customers_chose(179)
  browser_lurker          style_bridge(233), brand_story(228), comparison_card(195), trending_now(172), fit_reassurance(150)
  price_sensitive         comparison_card(382), customers_chose(349), fit_reassurance(250), style_bridge(247), price_history(194)
  paralyzed               expert_pick(281), customers_chose(280), comparison_card(258), fit_reassurance(210), style_bridge(185)
  confident_buyer         brand_story(288), trending_now(288), also_bought(262), style_bridge(210), price_history(193)
  returner_anxious        return_explainer(172), fit_reassurance(156), brand_story(133), style_bridge(132), comparison_card(116)
  comparison_shopper      comparison_card(381), customers_chose(374), brand_story(338), fit_reassurance(240), price_history(224)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead returns/size/material widgets and add synergy chains to attack returner_anxious (27.3%) and size_anxious_new (18.1%) regret)
  - session 5000: 16 edits (round 5000 — revive dead style/visual widgets for browser_lurker/confident_buyer/outfit_seeker; dial back over-firing returns widgets on personas that don't need F46)