# Task — write a page-composition policy in Python

You are designing a recommender page-composition policy for a fashion retail
site. Each user session is described by 14 numeric **context features** plus
a **product category**. Your policy must select 6 widgets (no repeats) from a
fixed catalogue of 22 for each session.

You will write a single Python function:

```python
def pick_page(feat: dict, category: str) -> list[str]:
    """Return a list of exactly 6 unique widget names from the catalog."""
    ...
```

The function must:
- Be self-contained Python (use only built-ins + the standard library).
- Return a list of exactly **6** widget names from the catalog (see below).
- Never repeat a widget within one returned list.
- Use the context features (`feat`) and category to personalise the page.
- Be deterministic: same input → same output. No randomness, no I/O.

## Context features available in `feat` (each in [0, 1])

- `size_conf`: how confident the user is in their size for this product right now
- `price_sens`: how price-driven this session is (1 = highly price-sensitive)
- `return_hist`: historical return rate (0 = new buyer, 1 = heavy returner)
- `style_stretch`: openness to discovery / unfamiliar styles
- `new`: how new this user is to the brand (0 = loyal, 1 = first visit)
- `mobile`: mobile vs desktop (1 = mobile)
- `size_chart`: time spent engaging the size chart this session
- `tab_switch`: how often they tab-switched (compare across retailers / pages)
- `zoom`: image-zoom engagement (proxy for examining details)
- `price_dwell`: time spent dwelling on price information
- `cart_osc`: add/remove-from-cart oscillation (proxy for indecision)
- `wishlist`: wishlist activity this session
- `return_view`: time spent on the returns-policy block
- `revisit`: how many times they revisited this product

(There is also `feat['price_norm']` in [0, 1] indicating how premium the
priced item is — 0 = budget, 1 = luxury. You may use it.)

## Category options

`category` is one of: `dress`, `top`, `bottoms`, `shoes`, `outerwear`, `accessories`

Different categories may have different needs (e.g. shoes have higher fit
anxiety than accessories; outerwear is more about visual presentation).

## Widget catalog with descriptions

- `fit_reassurance`: Reassurance content about the fit of this product (typical fit, model heights, fit reviews).
- `size_guide`: Detailed size chart for this product category with measurement guidance.
- `low_return_alts`: Alternative items in this product family that have low return rates.
- `comparison_card`: Side-by-side comparison vs similar products on price, material, ratings.
- `customers_chose`: Statistics like 'X% of customers picked this size' and similar social proof.
- `value_breakdown`: Breakdown of cost-per-wear, durability, and price-vs-quality positioning.
- `outfit_completion`: Suggested items that complete an outfit around this product.
- `style_bridge`: Adjacent style suggestions — 'pairs well with' for users open to discovery.
- `occasion_lookbook`: Lookbook of how this product is worn for specific occasions.
- `return_explainer`: Detailed return-policy walkthrough: deadlines, free returns, exchange options.
- `easy_returns_promise`: Banner emphasizing the no-hassle returns guarantee.
- `brand_story`: Brand story content — heritage, craftsmanship, designer notes.
- `material_deep_dive`: Material composition, sourcing, technical fabric details, care.
- `price_history`: Historical price chart for this item across recent months.
- `price_drop_notify`: Subscribe to be notified if the price drops on this item.
- `recently_viewed`: Items the user recently viewed; encourages cross-comparison.
- `wishlist_save`: Prompt to save this item for later; reduces purchase pressure.
- `expert_pick`: Stylist or buyer's pick highlighting the item with curator commentary.
- `similar_items`: Generic 'you might also like' grid of similar products.
- `also_bought`: Items frequently purchased together with this one.
- `trending_now`: Currently trending items in this category.
- `personal_recs`: Algorithmic personal recommendations based on user history.

## Guidance for your policy

You may reason however you like — if/else thresholds, scoring, weighted
ranking, a small decision tree. Aim for an interpretable rule set that:

- Personalises by context features (not the same page for every session).
- Recognises common shopper archetypes from the features (e.g. high
  `return_view` + high `return_hist` → consider return-trust widgets).
- Considers category effects (shoes & bottoms care more about fit; dress &
  accessories care more about styling).
- Uses 4–6 "personalised slot" picks plus 0–2 sensible defaults if needed.

## Output

Write your Python function to `data/llm_policy_fn.py`. Only define
`pick_page` (you may add helper functions). Do NOT include print statements
or top-level code that runs on import.

After writing, in under 100 words describe the structure of your policy
(thresholds you used, archetypes you defined, etc.). Do not paste the code.
