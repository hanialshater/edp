# STRUCTURAL CHANGE — `virtual_try_on` added to the catalog at session 5000

A new widget has been added to the catalog with provisions {'N1_fit': 0.65, 'N2_visual': 0.45, 'N6_trust': 0.2}. The widget appears in the modules JSON below with default values; it will show 0% activation in this batch because no edits have targeted it yet. Please consider whether this widget should fire for any (persona, category) cells (its provisions strongly favour personas with high N1_fit / N2_visual / N6_trust needs, e.g. size_anxious_new, returner_anxious, post_return_returner, hesitant_first_buyer, and the `shoes` / `outerwear` categories).

---

# EDP CHECKPOINT — sessions 2500 → 5000  (N=2500)

## Aggregate performance
- mean reward:        1.7739
- mean oracle reward: 2.0086
- mean regret:        0.2347  (11.7% of oracle)
- cum regret (batch): 586.87

## Per-persona performance (sorted by regret %, worst first)
  persona                    N    reward    oracle   regret%
  trend_chaser             100    1.7318    2.2730     23.8%
  size_specific_anxious     92    2.2343    2.8781     22.4%
  corporate_uniform_buyer   103    1.1749    1.4909     21.2%
  returner_from_recent_order   122    1.9216    2.3806     19.3%
  hesitant_first_buyer     308    2.1671    2.6315     17.6%
  post_return_returner     181    2.3331    2.7693     15.8%
  premium_silent_browser   170    1.9202    2.1275      9.7%
  paralyzed_wishlister     194    2.5904    2.8447      8.9%
  birthday_rush_gifter     198    2.2878    2.4771      7.6%
  outfit_event_planner     182    1.7901    1.8996      5.8%
  confident_repeat_buyer   204    0.4955    0.5089      2.6%
  tabbed_comparison_shopper   265    1.7924    1.8331      2.2%
  bargain_hunter_returning   220    1.1488    1.1720      2.0%
  mobile_evening_browser   161    1.0817    1.0968      1.4%

## Per-category performance (sorted by regret %, worst first)
  category           N    reward    oracle   regret%
  shoes            379    1.9278    2.2267     13.4%
  top              555    1.5777    1.7989     12.3%
  bottoms          507    1.7967    2.0448     12.1%
  accessories      374    1.5707    1.7635     10.9%
  dress            437    1.8280    2.0413     10.4%
  outerwear        248    2.1419    2.3830     10.1%

## Worst 8 (persona, category) cells by regret %
  persona                category         N    reward    oracle   regret%
  trend_chaser           top             18    1.5457    2.2468     31.2%
  corporate_uniform_buyer bottoms         19    1.2273    1.7247     28.8%
  trend_chaser           accessories     14    2.0808    2.8803     27.8%
  size_specific_anxious  top             22    2.0554    2.8185     27.1%
  returner_from_recent_order shoes           17    2.1053    2.8524     26.2%
  corporate_uniform_buyer shoes           13    1.5212    2.0604     26.2%
  size_specific_anxious  accessories     15    1.7025    2.2723     25.1%
  returner_from_recent_order bottoms         32    2.0037    2.6170     23.4%

## Widget activation rate (% of all slots filled) and avg-slot-reward
  widget                      act%  avg_slot    r/fire
  easy_returns_promise        15.8      4.60    0.2988
  comparison_card             15.1      3.16    0.3077
  material_deep_dive          14.5      3.54    0.3026
  expert_pick                 14.2      2.90    0.2865
  return_explainer            11.2      3.32    0.2690
  outfit_completion            8.8      3.82    0.3223
  low_return_alts              5.5      1.34    0.3505
  size_guide                   4.7      3.10    0.3368
  value_breakdown              3.9      3.73    0.2577
  occasion_lookbook            3.4      4.32    0.1869
  customers_chose              2.3      5.32    0.2865
  also_bought                  0.4      6.00    0.0815
  style_bridge                 0.2      1.00    0.3086
  fit_reassurance              0.0      0.00    0.0000
  brand_story                  0.0      0.00    0.0000
  price_history                0.0      0.00    0.0000
  price_drop_notify            0.0      0.00    0.0000
  recently_viewed              0.0      0.00    0.0000
  wishlist_save                0.0      0.00    0.0000
  similar_items                0.0      0.00    0.0000
  trending_now                 0.0      0.00    0.0000
  personal_recs                0.0      0.00    0.0000
  virtual_try_on               0.0      0.00    0.0000

## Top 5 widgets per persona (composition signature)
  trend_chaser            expert_pick(100), material_deep_dive(100), easy_returns_promise(98), return_explainer(80), outfit_completion(69)
  size_specific_anxious   low_return_alts(92), expert_pick(92), easy_returns_promise(92), material_deep_dive(92), comparison_card(91)
  corporate_uniform_buyer  material_deep_dive(103), easy_returns_promise(103), comparison_card(103), expert_pick(101), low_return_alts(84)
  returner_from_recent_order  low_return_alts(122), easy_returns_promise(122), material_deep_dive(122), comparison_card(122), expert_pick(121)
  hesitant_first_buyer    comparison_card(308), material_deep_dive(308), easy_returns_promise(306), outfit_completion(272), size_guide(255)
  post_return_returner    low_return_alts(181), easy_returns_promise(181), material_deep_dive(181), expert_pick(180), comparison_card(180)
  premium_silent_browser  expert_pick(170), easy_returns_promise(170), material_deep_dive(160), comparison_card(159), return_explainer(139)
  paralyzed_wishlister    comparison_card(194), expert_pick(194), easy_returns_promise(190), material_deep_dive(182), outfit_completion(147)
  birthday_rush_gifter    comparison_card(197), outfit_completion(196), material_deep_dive(177), easy_returns_promise(176), expert_pick(129)
  outfit_event_planner    comparison_card(182), outfit_completion(182), expert_pick(182), material_deep_dive(181), easy_returns_promise(180)
  confident_repeat_buyer  material_deep_dive(204), return_explainer(204), easy_returns_promise(204), occasion_lookbook(190), expert_pick(189)
  tabbed_comparison_shopper  comparison_card(265), expert_pick(265), easy_returns_promise(265), return_explainer(259), value_breakdown(245)
  bargain_hunter_returning  comparison_card(220), expert_pick(220), value_breakdown(218), return_explainer(218), easy_returns_promise(128)
  mobile_evening_browser  outfit_completion(161), material_deep_dive(161), return_explainer(161), easy_returns_promise(161), expert_pick(149)

## Edit history applied so far
  - session 2500: 16 edits (round 2500 — revive dead trust/fit/visual widgets for shoes/outerwear/bottoms; suppress weak defaults dominating confident_repeat_buyer)