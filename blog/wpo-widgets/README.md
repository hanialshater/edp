# WPO widget codebase — UX reference

The polished whole-page-optimization product-page UI that the blog's EDP
composer (posts **6 `05-edp`** and **7 `06-edp-adapts`**) renders. Provided as
the source of truth for the *look*; the posts inline a self-contained vanilla
port of it (per the blog's offline single-file rule).

## The 1:1 mapping (why this matters)

`widget-renderers.js` defines exactly the **22 renderers keyed by the same
module names as the EDP policy** (`POLICY.modules` in `../05-edp/index.html`):

```
fit_reassurance  size_guide        low_return_alts   comparison_card
customers_chose  value_breakdown   outfit_completion style_bridge
occasion_lookbook return_explainer easy_returns_promise brand_story
material_deep_dive price_history    price_drop_notify recently_viewed
wishlist_save    expert_pick       similar_items     also_bought
trending_now     personal_recs
```

So the composer's output (an ordered list of 6 module names) maps directly onto
real widget cards — no translation layer. Each renderer is
`name: () => widgetChrome(accent, title, eyebrow, bodyHTML)`, sharing one
retail/PDP visual language (the `.lp-*` / `.fit-*` / `.cmp-*` classes live in
`live-page.css`).

## Files

| File | Role |
|---|---|
| `orchestrator.html` | Runnable bundle: loads the modules below + Tailwind/IBM-Plex from CDN. Open with a network connection. |
| `widget-renderers.js` | The 22 module renderers (`const R = { fit_reassurance: …, … }`) + SVG garment atoms. **The port source.** |
| `page-widgets.js` | Higher-level page widgets/sections. |
| `live-page.css`, `page-styles.css` | The retail PDP styling the renderers assume. |
| `products.jsx` | Product fixtures (BOSS tuxedo demo product). |
| `policies.js`, `pages.js`, `page-router.js`, `page-shells.js`, `page-extensions.js`, `journey-catalog.js`, `design-canvas.jsx` | The orchestrator app (routing, journeys, the design canvas). |

## Offline note

The blog **posts** are strictly offline/single-file. This reference folder is
*not* a post: `orchestrator.html` pulls Tailwind + Google Fonts from a CDN, so it
needs a network connection to look right. The in-post composer
(`../components/wpo/product-page.html`, inlined into 05-edp and 06-edp-adapts)
re-creates the same look with **zero external assets** — inline CSS, SVG/emoji
placeholders instead of remote images, no fonts beyond the system stack.

## Provenance

Uploaded by the author as "good UX for WPO." Kept as the design reference the
interactive posts are ported from; the large standalone export and binary
assets (PDF, screenshots) were omitted to keep the repo lean.
</content>
