"""Page-composition policy.

Defines `pick_page(feat, category) -> list[str]` returning exactly 6 unique
widget names from the catalog, chosen via per-widget scoring based on
context features and category.
"""

CATALOG = [
    "fit_reassurance",
    "size_guide",
    "low_return_alts",
    "comparison_card",
    "customers_chose",
    "value_breakdown",
    "outfit_completion",
    "style_bridge",
    "occasion_lookbook",
    "return_explainer",
    "easy_returns_promise",
    "brand_story",
    "material_deep_dive",
    "price_history",
    "price_drop_notify",
    "recently_viewed",
    "wishlist_save",
    "expert_pick",
    "similar_items",
    "also_bought",
    "trending_now",
    "personal_recs",
]


def _get(feat, key, default=0.5):
    v = feat.get(key, default)
    try:
        v = float(v)
    except (TypeError, ValueError):
        return default
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _category_weights(category):
    # base = (fit_focus, style_focus, price_focus, trust_focus, discovery_focus)
    table = {
        "dress":        {"fit": 0.7, "style": 1.0, "price": 0.6, "trust": 0.6, "discovery": 0.8},
        "top":          {"fit": 0.6, "style": 0.8, "price": 0.7, "trust": 0.5, "discovery": 0.7},
        "bottoms":      {"fit": 1.0, "style": 0.6, "price": 0.6, "trust": 0.7, "discovery": 0.5},
        "shoes":        {"fit": 1.0, "style": 0.6, "price": 0.6, "trust": 0.9, "discovery": 0.5},
        "outerwear":    {"fit": 0.6, "style": 0.9, "price": 0.8, "trust": 0.6, "discovery": 0.6},
        "accessories":  {"fit": 0.2, "style": 1.0, "price": 0.5, "trust": 0.3, "discovery": 0.9},
    }
    return table.get(category, {"fit": 0.6, "style": 0.7, "price": 0.6, "trust": 0.6, "discovery": 0.6})


def _score_widgets(feat, category):
    f_size_conf    = _get(feat, "size_conf")
    f_price_sens   = _get(feat, "price_sens")
    f_return_hist  = _get(feat, "return_hist")
    f_style_str    = _get(feat, "style_stretch")
    f_new          = _get(feat, "new")
    f_mobile       = _get(feat, "mobile")
    f_size_chart   = _get(feat, "size_chart")
    f_tab_switch   = _get(feat, "tab_switch")
    f_zoom         = _get(feat, "zoom")
    f_price_dwell  = _get(feat, "price_dwell")
    f_cart_osc     = _get(feat, "cart_osc")
    f_wishlist     = _get(feat, "wishlist")
    f_return_view  = _get(feat, "return_view")
    f_revisit      = _get(feat, "revisit")
    f_price_norm   = _get(feat, "price_norm")

    cw = _category_weights(category)

    # Composite "archetype" signals
    fit_anxiety   = 0.55 * (1.0 - f_size_conf) + 0.30 * f_size_chart + 0.25 * f_return_hist
    return_anx    = 0.55 * f_return_view + 0.45 * f_return_hist
    indecision    = 0.50 * f_cart_osc + 0.30 * f_revisit + 0.20 * f_tab_switch
    price_focus   = 0.55 * f_price_sens + 0.35 * f_price_dwell + 0.10 * f_tab_switch
    discovery     = 0.60 * f_style_str + 0.30 * f_new + 0.10 * f_wishlist
    detail_examiner = 0.55 * f_zoom + 0.25 * f_tab_switch + 0.20 * f_revisit
    premium_lean  = 0.60 * f_price_norm + 0.20 * (1.0 - f_price_sens) + 0.20 * (1.0 - f_new)
    loyal         = 1.0 - f_new
    save_intent   = 0.55 * f_wishlist + 0.30 * f_cart_osc + 0.15 * f_revisit
    mobile        = f_mobile

    scores = {}

    # FIT cluster
    scores["fit_reassurance"] = (
        1.10 * fit_anxiety * cw["fit"]
        + 0.30 * f_return_hist
        + 0.15
    )
    scores["size_guide"] = (
        1.20 * fit_anxiety * cw["fit"]
        + 0.50 * f_size_chart
        - 0.40 * f_size_conf
        + 0.10
    )
    scores["customers_chose"] = (
        0.80 * fit_anxiety * cw["fit"]
        + 0.40 * (1.0 - f_size_conf)
        + 0.25 * mobile
        + 0.10
    )
    scores["low_return_alts"] = (
        0.90 * return_anx
        + 0.40 * fit_anxiety * cw["fit"]
        + 0.20 * f_return_hist
    )

    # TRUST / RETURNS cluster
    scores["return_explainer"] = (
        1.10 * return_anx * cw["trust"]
        + 0.35 * f_new
        + 0.20 * indecision
    )
    scores["easy_returns_promise"] = (
        0.80 * return_anx
        + 0.50 * f_new * cw["trust"]
        + 0.25 * mobile
        + 0.10
    )

    # PRICE cluster
    scores["comparison_card"] = (
        1.00 * price_focus * cw["price"]
        + 0.45 * f_tab_switch
        + 0.20 * detail_examiner
    )
    scores["value_breakdown"] = (
        0.70 * price_focus * cw["price"]
        + 0.60 * premium_lean
        + 0.25 * f_price_dwell
    )
    scores["price_history"] = (
        0.95 * price_focus
        + 0.40 * f_price_dwell
        + 0.20 * f_revisit
        - 0.20 * f_new
    )
    scores["price_drop_notify"] = (
        0.85 * price_focus
        + 0.50 * save_intent
        + 0.25 * f_revisit
        + 0.20 * indecision
    )

    # STYLING / DISCOVERY cluster
    scores["outfit_completion"] = (
        1.00 * cw["style"]
        + 0.55 * f_wishlist
        + 0.35 * f_style_str
        + 0.20 * (1.0 - f_price_sens)
    )
    scores["style_bridge"] = (
        1.10 * discovery * cw["discovery"]
        + 0.30 * f_wishlist
    )
    scores["occasion_lookbook"] = (
        0.90 * cw["style"]
        + 0.55 * discovery
        + 0.30 * f_zoom
        + 0.20 * premium_lean
    )
    scores["expert_pick"] = (
        0.70 * cw["style"]
        + 0.60 * premium_lean
        + 0.35 * f_new
        + 0.20 * discovery
    )

    # CONTENT / DETAIL cluster
    scores["brand_story"] = (
        0.75 * premium_lean
        + 0.55 * f_new
        + 0.30 * detail_examiner
        - 0.30 * price_focus
    )
    scores["material_deep_dive"] = (
        1.00 * detail_examiner
        + 0.45 * premium_lean
        + 0.30 * f_return_hist
        + 0.20 * cw["fit"]
    )

    # SAVE / RETURN-TO-SITE cluster
    scores["wishlist_save"] = (
        0.95 * save_intent
        + 0.40 * indecision
        + 0.25 * mobile
        + 0.15 * f_price_sens
    )
    scores["recently_viewed"] = (
        0.85 * indecision
        + 0.55 * f_revisit
        + 0.35 * f_tab_switch
        + 0.15 * loyal
    )

    # GENERIC RECS cluster
    scores["similar_items"] = (
        0.55
        + 0.45 * f_tab_switch
        + 0.30 * (1.0 - f_size_conf)
        + 0.20 * price_focus
    )
    scores["also_bought"] = (
        0.60
        + 0.45 * cw["style"]
        + 0.30 * f_wishlist
        + 0.20 * loyal
    )
    scores["trending_now"] = (
        0.70 * f_new
        + 0.55 * discovery
        + 0.35 * mobile
        + 0.20 * cw["discovery"]
    )
    scores["personal_recs"] = (
        0.90 * loyal
        + 0.45 * (1.0 - f_new)
        + 0.30 * f_revisit
        + 0.20 * f_wishlist
    )

    return scores


def pick_page(feat, category):
    """Return a list of exactly 6 unique widget names from the catalog."""
    if not isinstance(feat, dict):
        feat = {}
    scores = _score_widgets(feat, category)

    # Stable deterministic ordering: by (-score, catalog_index)
    catalog_index = {w: i for i, w in enumerate(CATALOG)}
    ranked = sorted(
        CATALOG,
        key=lambda w: (-scores.get(w, 0.0), catalog_index[w]),
    )

    chosen = []
    seen = set()
    for w in ranked:
        if w in seen:
            continue
        seen.add(w)
        chosen.append(w)
        if len(chosen) == 6:
            break

    # Defensive backfill (shouldn't trigger since catalog has 22 items)
    if len(chosen) < 6:
        for w in CATALOG:
            if w not in seen:
                chosen.append(w)
                seen.add(w)
                if len(chosen) == 6:
                    break

    return chosen
