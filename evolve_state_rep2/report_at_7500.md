# EDP CHECKPOINT REPORT — sessions 5000 → 7500  (N=2500)

## Aggregate performance
- mean reward:        1.0587
- mean oracle reward: 1.1019
- mean regret:        0.0432  (3.9% of oracle)
- cum regret (batch): 107.92

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  size_anxious_new         433    1.2196    1.3500      9.7%
  comparison_shopper       381    1.1653    1.2400      6.0%
  returner_anxious         172    1.4015    1.4800      5.3%
  price_sensitive          383    0.9096    0.9225      1.4%
  confident_buyer          289    0.5226    0.5275      0.9%
  browser_lurker           246    0.6373    0.6425      0.8%
  outfit_seeker            313    1.2116    1.2150      0.3%
  paralyzed                283    1.4073    1.4100      0.2%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  outfit_completion           16.7      2.34    0.1765
  easy_returns_promise        16.7      4.23    0.1765
  expert_pick                 15.5      5.24    0.1763
  brand_story                 15.3      2.58    0.1775
  fit_reassurance             15.1      2.77    0.1752
  comparison_card             13.6      3.72    0.1806
  value_breakdown              3.2      3.97    0.1671
  low_return_alts              2.1      1.80    0.2023
  occasion_lookbook            1.5      5.96    0.1204
  customers_chose              0.3      5.98    0.2141
  size_guide                   0.0      0.00    0.0000
  style_bridge                 0.0      0.00    0.0000
  return_explainer             0.0      0.00    0.0000
  material_deep_dive           0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  also_bought                  0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  size_anxious_new        fit_reassurance(433), outfit_completion(433), easy_returns_promise(433), brand_story(431), expert_pick(428)
  comparison_shopper      comparison_card(381), outfit_completion(381), brand_story(381), easy_returns_promise(381), fit_reassurance(361)
  returner_anxious        outfit_completion(172), easy_returns_promise(172), brand_story(168), expert_pick(138), low_return_alts(128)
  price_sensitive         outfit_completion(383), easy_returns_promise(383), comparison_card(376), expert_pick(305), fit_reassurance(281)
  confident_buyer         outfit_completion(289), brand_story(289), easy_returns_promise(289), fit_reassurance(289), expert_pick(289)
  browser_lurker          outfit_completion(246), easy_returns_promise(246), brand_story(243), fit_reassurance(238), expert_pick(233)
  outfit_seeker           outfit_completion(313), easy_returns_promise(313), brand_story(311), fit_reassurance(310), expert_pick(303)
  paralyzed               outfit_completion(283), expert_pick(283), easy_returns_promise(283), comparison_card(280), brand_story(255)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — boost dead trust/fit widgets for returner_anxious and size_anxious (highest regret), trim over-firing defaults)
  - session 5000: 16 edits (round 5000 — activate dead fit/visual/return widgets for high-regret size_anxious/outfit_seeker/browser_lurker, trim over-firing style_bridge/return_explainer/also_bought)