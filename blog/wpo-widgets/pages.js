// =============================================================================
// PAGE REGISTRY — page-based orchestration on top of the existing PDP composer.
// =============================================================================
//
// Today's orchestrator composes ONE page (the PDP) by greedily filling 6 slots
// from a registry of 22 widgets, scored against 7 PDP-stage problems
// (F32–F51). This file extends that model to 7 page types:
//
//   home · search · plp · pdp · cart · checkout · post_purchase
//
// Each page has its own:
//   • slot count            (how many widgets to fit)
//   • problem fingerprint   (which subset of journey problems applies here)
//   • module registry       (widgets that can render on THIS page)
//
// The 14 raw signals + 8 personas stay shared across all pages — that's what
// makes "persona carries through Home → Search → PDP → Cart" feel coherent.
// New problem detectors (F11, F22, F52, etc.) are PWLs built from the same
// 14 signals so a persona's signal vector immediately reads as a fingerprint
// on every page without requiring new instrumentation.
//
// v3 edits stay PDP-only for now — new pages ship as v1 baseline only.

window.PAGES = ['home', 'search', 'plp', 'pdp', 'cart', 'checkout', 'post_purchase'];

window.PAGE_META = {
  home:          { label: 'Home',          slug: '/',                 slots: 8, color: 'blue'    },
  search:        { label: 'Search',        slug: '/search?q=tuxedo',  slots: 6, color: 'sky'     },
  plp:           { label: 'Category',      slug: '/men/suits-tuxedos',slots: 6, color: 'teal'    },
  pdp:           { label: 'Product',       slug: '/p/boss-tuxedo',    slots: 6, color: 'slate'   },
  cart:          { label: 'Cart',          slug: '/bag',              slots: 5, color: 'amber'   },
  checkout:      { label: 'Checkout',      slug: '/checkout',         slots: 4, color: 'emerald' },
  post_purchase: { label: 'Post-purchase', slug: '/orders/94821',     slots: 5, color: 'indigo'  },
};

// -----------------------------------------------------------------------------
// EXTENDED PROBLEM META — adds the journey-catalog codes the new pages need.
// PDP problems (F32–F51) stay defined in the orchestrator HTML; we add the rest.
// -----------------------------------------------------------------------------
window.PROBLEM_META_EXT = {
  // Discover / Explore stages
  F11: { name: 'F11 Category Overwhelm',     color: 'sky',     stage: 'F1' },
  F12: { name: 'F12 Inspiration Gap',        color: 'fuchsia', stage: 'F1' },
  F13: { name: 'F13 Need Translation',       color: 'teal',    stage: 'F1' },
  F21: { name: 'F21 Option Set Stagnation',  color: 'amber',   stage: 'F2' },
  F22: { name: 'F22 Filter Friction',        color: 'orange',  stage: 'F2' },
  F23: { name: 'F23 Discovery Boredom',      color: 'rose',    stage: 'F2' },
  // PDP-adjacent (Narrow)
  F31: { name: 'F31 Detail Anxiety',         color: 'cyan',    stage: 'F3' },
  F35: { name: 'F35 PDP Stagnation',         color: 'indigo',  stage: 'F3' },
  // Commit
  F52: { name: 'F52 Checkout Doubt',         color: 'emerald', stage: 'F5' },
  F53: { name: 'F53 Price Anchoring Block',  color: 'orange',  stage: 'F5' },
  // Post-purchase
  F61: { name: 'F61 Styling Orphan',         color: 'fuchsia', stage: 'F6' },
  F62: { name: 'F62 Care Knowledge Gap',     color: 'teal',    stage: 'F6' },
  F63: { name: 'F63 Wardrobe Drift',         color: 'rose',    stage: 'F6' },
  F64: { name: 'F64 Repeat Trigger',         color: 'indigo',  stage: 'F6' },
};

// -----------------------------------------------------------------------------
// EXTENDED PROBLEM DETECTION SHAPES — reuse the 14 existing signals.
//
// `size_conf` is inverted via the `vals` array when needed (low confidence
// drives a higher detection score). All weights normalize internally.
// -----------------------------------------------------------------------------
window.PROBLEM_SHAPES_EXT = {
  // ── Discover ───────────────────────────────────────────────────────────────
  F11: [ // Category Overwhelm — fresh, low-signal browser
    { signal: 'new',          bps:[0,.3,.7,1], vals:[0,.2,.65,.9],  w: 0.55, title: 'New customer' },
    { signal: 'tab_switch',   bps:[0,.3,.6,1], vals:[0,.15,.45,.7], w: 0.25, title: 'Tab switching (early)' },
    { signal: 'revisit',      bps:[0,.3,.6,1], vals:[.7,.4,.2,.05], w: 0.20, title: 'Low product affinity' },
  ],
  F12: [ // Inspiration Gap — browsing without a goal
    { signal: 'style_stretch',bps:[0,.3,.6,1], vals:[0,.2,.55,.85], w: 0.45, title: 'Style stretch' },
    { signal: 'wishlist',     bps:[0,.2,.5,1], vals:[0,.2,.5,.8],   w: 0.35, title: 'Wishlist depth' },
    { signal: 'new',          bps:[0,.4,.8,1], vals:[.3,.5,.7,.85], w: 0.20, title: 'Newness' },
  ],
  F13: [ // Need Translation — vague intent, broad search
    { signal: 'new',          bps:[0,.3,.7,1], vals:[0,.25,.6,.85], w: 0.45, title: 'New customer' },
    { signal: 'tab_switch',   bps:[0,.3,.6,1], vals:[0,.3,.55,.75], w: 0.30, title: 'Exploring breadth' },
    { signal: 'mobile',       bps:[0,.5,1],    vals:[0,.3,.55],     w: 0.25, title: 'Mobile (small kb)' },
  ],
  // ── Explore ────────────────────────────────────────────────────────────────
  F21: [ // Option Set Stagnation — revisits seeing the same stuff
    { signal: 'revisit',      bps:[0,.3,.6,1], vals:[0,.3,.65,.9],  w: 0.55, title: 'Revisits' },
    { signal: 'wishlist',     bps:[0,.3,.6,1], vals:[0,.15,.4,.65], w: 0.25, title: 'Wishlist depth' },
    { signal: 'cart_osc',     bps:[0,.3,.6,1], vals:[0,.1,.35,.55], w: 0.20, title: 'Browse fatigue' },
  ],
  F22: [ // Filter Friction — toggling filters, hitting empty
    { signal: 'tab_switch',   bps:[0,.3,.6,1], vals:[0,.25,.55,.8], w: 0.40, title: 'Tab/filter switching' },
    { signal: 'price_dwell',  bps:[0,.3,.6,1], vals:[0,.2,.5,.7],   w: 0.30, title: 'Price filter dwell' },
    { signal: 'mobile',       bps:[0,.5,1],    vals:[0,.4,.65],     w: 0.30, title: 'Mobile filters are harder' },
  ],
  F23: [ // Discovery Boredom — seen-it-all
    { signal: 'revisit',      bps:[0,.3,.6,1], vals:[0,.25,.55,.8], w: 0.45, title: 'Revisits' },
    { signal: 'cart_osc',     bps:[0,.3,.6,1], vals:[0,.2,.5,.75],  w: 0.30, title: 'Disengaged' },
    { signal: 'wishlist',     bps:[0,.3,.6,1], vals:[0,.15,.4,.65], w: 0.25, title: 'Wishlist saturation' },
  ],
  // ── PDP-adjacent ───────────────────────────────────────────────────────────
  F31: [ // Detail Anxiety — wants to see everything
    { signal: 'zoom',         bps:[0,.3,.6,1], vals:[0,.25,.6,.9],  w: 0.65, title: 'Image zoom' },
    { signal: 'price_norm',   bps:[0,.5,1],    vals:[0,.3,.55],     w: 0.35, title: 'Premium price' },
  ],
  F35: [ // PDP Stagnation
    { signal: 'revisit',      bps:[0,.3,.6,1], vals:[0,.3,.6,.9],   w: 0.65, title: 'PDP revisits' },
    { signal: 'wishlist',     bps:[0,.3,.6,1], vals:[0,.2,.5,.75],  w: 0.35, title: 'Wishlisted' },
  ],
  // ── Commit ─────────────────────────────────────────────────────────────────
  F52: [ // Checkout Doubt — first-time, mobile, hesitating
    { signal: 'new',          bps:[0,.3,.7,1], vals:[0,.3,.7,.95],  w: 0.50, title: 'New customer (trust)' },
    { signal: 'mobile',       bps:[0,.5,1],    vals:[0,.35,.65],    w: 0.25, title: 'Mobile checkout' },
    { signal: 'cart_osc',     bps:[0,.3,.6,1], vals:[0,.2,.5,.75],  w: 0.25, title: 'Cart hesitation' },
  ],
  F53: [ // Price Anchoring Block — waiting for a sale
    { signal: 'price_sens',   bps:[0,.4,.7,1], vals:[0,.25,.6,.9],  w: 0.45, title: 'Price sensitivity' },
    { signal: 'price_dwell',  bps:[0,.3,.6,1], vals:[0,.2,.5,.8],   w: 0.35, title: 'Price dwell' },
    { signal: 'wishlist',     bps:[0,.3,.6,1], vals:[0,.15,.4,.6],  w: 0.20, title: 'Saved for later' },
  ],
  // ── Post-purchase ──────────────────────────────────────────────────────────
  F61: [ // Styling Orphan — bought something they can't style
    { signal: 'style_stretch',bps:[0,.3,.6,1], vals:[0,.3,.65,.9],  w: 0.65, title: 'Stretched purchase' },
    { signal: 'new',          bps:[0,.4,.8,1], vals:[.2,.4,.6,.8],  w: 0.35, title: 'New customer' },
  ],
  F62: [ // Care Knowledge Gap — premium item, low experience
    { signal: 'price_norm',   bps:[0,.4,.8,1], vals:[0,.2,.55,.85], w: 0.55, title: 'Premium item' },
    { signal: 'new',          bps:[0,.4,.8,1], vals:[.1,.35,.6,.85],w: 0.45, title: 'New to category' },
  ],
  F63: [ // Wardrobe Drift — style has changed
    { signal: 'style_stretch',bps:[0,.3,.6,1], vals:[0,.25,.55,.8], w: 0.55, title: 'Style stretch' },
    { signal: 'revisit',      bps:[0,.3,.6,1], vals:[0,.2,.5,.75],  w: 0.45, title: 'Browse drift' },
  ],
  F64: [ // Repeat Trigger — loved it, wants another
    { signal: 'return_hist',  bps:[0,.2,.5,1], vals:[.9,.6,.3,.05], w: 0.45, title: 'Kept the item (inv)' },
    { signal: 'wishlist',     bps:[0,.3,.6,1], vals:[0,.2,.5,.75],  w: 0.35, title: 'Aware of variants' },
    { signal: 'revisit',      bps:[0,.3,.6,1], vals:[0,.15,.4,.65], w: 0.20, title: 'Coming back' },
  ],
};

// -----------------------------------------------------------------------------
// PROBLEM FINGERPRINT PER PAGE — which problems "exist" on each page.
// -----------------------------------------------------------------------------
window.PAGE_PROBLEMS = {
  home:          ['F11', 'F12', 'F21', 'F35', 'F51'],
  search:        ['F13', 'F21', 'F22', 'F23', 'F11'],
  plp:           ['F11', 'F22', 'F23', 'F21', 'F31'],
  pdp:           ['F32', 'F33', 'F41', 'F43', 'F45', 'F46', 'F51'], // unchanged
  cart:          ['F51', 'F46', 'F45', 'F52', 'F53'],
  checkout:      ['F52', 'F46', 'F53'],
  post_purchase: ['F61', 'F62', 'F63', 'F64', 'F12'],
};

// -----------------------------------------------------------------------------
// PER-PAGE WIDGET REGISTRIES
//
// Each entry mirrors the PDP module schema:
//   { type, color, addr, base, on_rem, on_cov, slot_decay }
//
// `addr`: per-problem addressing strength
// `base`: floor utility (the widget is OK even with no detected problem)
// `on_rem`: bonus = sum(on_rem[p] · remaining[p]) — fires when problem is hot
// `on_cov`: synergy = sum(on_cov[p] · coverage[p]) — fires AFTER another widget
//           has already partially addressed the problem (great for chained
//           explainer/promise pairs)
// `slot_decay`: penalty per later slot — keeps the strongest pick up top
// -----------------------------------------------------------------------------

window.PAGE_MODULES = {
  // ───────────────────────────── HOME ──────────────────────────────────────
  home: {
    inspiration_hero:     { type: 'hero',      color: 'fuchsia',
      addr: { F12: 0.55, F11: 0.25 }, base: 0.35,
      on_rem: { F12: 1.8, F11: 0.8 }, on_cov: { F12: -0.8 }, slot_decay: 0.02 },
    continue_browsing:    { type: 'continuity',color: 'indigo',
      addr: { F35: 0.55, F51: 0.20 }, base: 0.15,
      on_rem: { F35: 2.0, F51: 0.7 }, on_cov: { F35: -1.2 }, slot_decay: 0.06 },
    shopping_mission:     { type: 'guidance',  color: 'sky',
      addr: { F11: 0.55, F12: 0.20 }, base: 0.10,
      on_rem: { F11: 1.9, F12: 0.6 }, on_cov: { F11: -1.1 }, slot_decay: 0.05 },
    editorial_collections:{ type: 'editorial', color: 'fuchsia',
      addr: { F12: 0.45, F21: 0.20 }, base: 0.25,
      on_rem: { F12: 1.4, F21: 0.7 }, on_cov: { F12: -0.5 }, slot_decay: 0.05 },
    new_arrivals:         { type: 'feed',      color: 'amber',
      addr: { F21: 0.40, F12: 0.10 }, base: 0.25,
      on_rem: { F21: 1.6 }, on_cov: { F21: -0.8 }, slot_decay: 0.04 },
    trending_now_home:    { type: 'feed',      color: 'rose',
      addr: { F21: 0.30, F12: 0.10 }, base: 0.30,
      on_rem: { F21: 1.0 }, on_cov: { F21: 0.5 }, slot_decay: 0.05 },
    personal_picks_home:  { type: 'personal',  color: 'indigo',
      addr: { F35: 0.20, F51: 0.15 }, base: 0.35,
      on_rem: { F35: 0.6, F51: 0.7 }, on_cov: { F35: 0.4 }, slot_decay: 0.04 },
    shop_the_look_home:   { type: 'editorial', color: 'fuchsia',
      addr: { F12: 0.30 }, base: 0.20,
      on_rem: { F12: 1.0 }, on_cov: { F12: 0.6 }, slot_decay: 0.06 },
    seasonal_picks:       { type: 'feed',      color: 'teal',
      addr: {}, base: 0.30, on_rem: {}, on_cov: {}, slot_decay: 0.04 },
    last_chance:          { type: 'feed',      color: 'orange',
      addr: { F51: 0.10 }, base: 0.20, on_rem: { F51: 0.5 }, on_cov: {}, slot_decay: 0.05 },
  },

  // ───────────────────────────── SEARCH ────────────────────────────────────
  search: {
    query_interpretation: { type: 'query',     color: 'teal',
      addr: { F13: 0.65 }, base: 0.40,
      on_rem: { F13: 1.8 }, on_cov: {}, slot_decay: 0.02 },
    smart_facets:         { type: 'filter',    color: 'orange',
      addr: { F22: 0.55, F11: 0.20 }, base: 0.20,
      on_rem: { F22: 2.0, F11: 0.8 }, on_cov: { F22: -1.0 }, slot_decay: 0.05 },
    visual_swatches:      { type: 'filter',    color: 'sky',
      addr: { F22: 0.30, F13: 0.20 }, base: 0.15,
      on_rem: { F22: 1.2, F13: 0.8 }, on_cov: { F22: 0.5 }, slot_decay: 0.06 },
    did_you_mean:         { type: 'query',     color: 'teal',
      addr: { F13: 0.40 }, base: 0.10,
      on_rem: { F13: 1.6 }, on_cov: { F13: -0.9 }, slot_decay: 0.07 },
    results_grid:         { type: 'results',   color: 'slate',
      addr: { F11: 0.10 }, base: 0.65, on_rem: {}, on_cov: {}, slot_decay: 0.01 },
    fresh_picks_search:   { type: 'results',   color: 'amber',
      addr: { F21: 0.50, F23: 0.30 }, base: 0.10,
      on_rem: { F21: 1.8, F23: 1.2 }, on_cov: { F21: -1.0 }, slot_decay: 0.06 },
    related_searches:     { type: 'query',     color: 'rose',
      addr: { F13: 0.20, F23: 0.20 }, base: 0.15,
      on_rem: { F13: 0.7, F23: 0.9 }, on_cov: {}, slot_decay: 0.05 },
    featured_brands:      { type: 'editorial', color: 'fuchsia',
      addr: { F11: 0.15, F23: 0.15 }, base: 0.20, on_rem: {}, on_cov: {}, slot_decay: 0.05 },
  },

  // ───────────────────────────── PLP ───────────────────────────────────────
  plp: {
    category_hero:        { type: 'hero',      color: 'teal',
      addr: { F11: 0.45 }, base: 0.30,
      on_rem: { F11: 1.4 }, on_cov: { F11: -0.6 }, slot_decay: 0.02 },
    facet_rail:           { type: 'filter',    color: 'orange',
      addr: { F22: 0.55, F11: 0.20 }, base: 0.25,
      on_rem: { F22: 2.0 }, on_cov: { F22: -1.0 }, slot_decay: 0.04 },
    size_predictor:       { type: 'filter',    color: 'cyan',
      addr: { F22: 0.30, F31: 0.15 }, base: 0.10,
      on_rem: { F22: 1.4 }, on_cov: { F22: 0.6 }, slot_decay: 0.06 },
    fresh_picks_plp:      { type: 'results',   color: 'amber',
      addr: { F21: 0.55, F23: 0.30 }, base: 0.10,
      on_rem: { F21: 1.9, F23: 1.3 }, on_cov: { F21: -0.9 }, slot_decay: 0.06 },
    plp_grid:             { type: 'results',   color: 'slate',
      addr: { F11: 0.10 }, base: 0.65, on_rem: {}, on_cov: {}, slot_decay: 0.01 },
    collection_callout:   { type: 'editorial', color: 'fuchsia',
      addr: { F23: 0.30, F12: 0.15 }, base: 0.20,
      on_rem: { F23: 1.0 }, on_cov: {}, slot_decay: 0.05 },
    visual_browse:        { type: 'editorial', color: 'rose',
      addr: { F23: 0.45, F12: 0.20 }, base: 0.10,
      on_rem: { F23: 1.6, F12: 0.7 }, on_cov: { F23: -0.8 }, slot_decay: 0.06 },
    editor_picks_plp:     { type: 'editorial', color: 'indigo',
      addr: { F23: 0.20, F31: 0.10 }, base: 0.20, on_rem: {}, on_cov: {}, slot_decay: 0.05 },
  },

  // ───────────────────────────── PDP ───────────────────────────────────────
  // pdp uses the existing 22-widget registry from the orchestrator; no entry
  // is needed here — the composer will fall back to modulesV1 / modulesV3 for
  // the 'pdp' page type.
  pdp: null,

  // ───────────────────────────── CART ──────────────────────────────────────
  cart: {
    cart_summary:         { type: 'core',      color: 'slate',
      addr: {}, base: 0.95, on_rem: {}, on_cov: {}, slot_decay: 0.0 },
    shipping_threshold:   { type: 'incentive', color: 'emerald',
      addr: { F45: 0.25, F51: 0.20 }, base: 0.35,
      on_rem: { F45: 0.8, F51: 0.9 }, on_cov: {}, slot_decay: 0.04 },
    complete_outfit_cart: { type: 'upsell',    color: 'fuchsia',
      addr: { F12: 0.25, F51: 0.15 }, base: 0.25,
      on_rem: { F12: 0.8, F51: 0.5 }, on_cov: {}, slot_decay: 0.05 },
    return_assurance_cart:{ type: 'trust',     color: 'rose',
      addr: { F46: 0.55, F52: 0.20 }, base: 0.20,
      on_rem: { F46: 2.0, F52: 0.7 }, on_cov: { F46: -1.0 }, slot_decay: 0.05 },
    decision_help_cart:   { type: 'decision',  color: 'indigo',
      addr: { F51: 0.55 }, base: 0.10,
      on_rem: { F51: 2.1 }, on_cov: { F51: -1.0 }, slot_decay: 0.05 },
    price_freeze:         { type: 'price',     color: 'orange',
      addr: { F53: 0.55, F51: 0.20 }, base: 0.10,
      on_rem: { F53: 2.0, F51: 0.6 }, on_cov: { F53: -1.0 }, slot_decay: 0.05 },
    gift_options:         { type: 'incentive', color: 'amber',
      addr: {}, base: 0.20, on_rem: {}, on_cov: {}, slot_decay: 0.05 },
    saved_for_later:      { type: 'continuity',color: 'indigo',
      addr: { F51: 0.20, F53: 0.15 }, base: 0.15,
      on_rem: { F51: 0.7, F53: 0.6 }, on_cov: {}, slot_decay: 0.04 },
  },

  // ───────────────────────────── CHECKOUT ──────────────────────────────────
  checkout: {
    order_summary:        { type: 'core',      color: 'slate',
      addr: {}, base: 0.95, on_rem: {}, on_cov: {}, slot_decay: 0.0 },
    express_payment:      { type: 'speed',     color: 'emerald',
      addr: { F52: 0.30 }, base: 0.55,
      on_rem: { F52: 0.7 }, on_cov: {}, slot_decay: 0.03 },
    trust_signals:        { type: 'trust',     color: 'emerald',
      addr: { F52: 0.60 }, base: 0.15,
      on_rem: { F52: 2.0 }, on_cov: { F52: -1.0 }, slot_decay: 0.06 },
    shipping_options:     { type: 'core',      color: 'slate',
      addr: { F52: 0.15 }, base: 0.55, on_rem: {}, on_cov: {}, slot_decay: 0.02 },
    return_micro:         { type: 'trust',     color: 'rose',
      addr: { F46: 0.45 }, base: 0.20,
      on_rem: { F46: 1.6 }, on_cov: { F46: -0.8 }, slot_decay: 0.06 },
    price_lock_assurance: { type: 'price',     color: 'orange',
      addr: { F53: 0.40, F52: 0.15 }, base: 0.10,
      on_rem: { F53: 1.5 }, on_cov: { F53: -0.7 }, slot_decay: 0.06 },
  },

  // ───────────────────────────── POST-PURCHASE ─────────────────────────────
  post_purchase: {
    order_status:         { type: 'core',      color: 'slate',
      addr: {}, base: 0.95, on_rem: {}, on_cov: {}, slot_decay: 0.0 },
    care_guide:           { type: 'guidance',  color: 'teal',
      addr: { F62: 0.55 }, base: 0.20,
      on_rem: { F62: 2.0 }, on_cov: { F62: -1.0 }, slot_decay: 0.05 },
    style_companion:      { type: 'editorial', color: 'fuchsia',
      addr: { F61: 0.55, F12: 0.15 }, base: 0.15,
      on_rem: { F61: 2.0, F12: 0.6 }, on_cov: { F61: -1.0 }, slot_decay: 0.06 },
    repeat_in_color:      { type: 'upsell',    color: 'indigo',
      addr: { F64: 0.55 }, base: 0.15,
      on_rem: { F64: 1.9 }, on_cov: { F64: -1.0 }, slot_decay: 0.06 },
    wardrobe_check:       { type: 'guidance',  color: 'rose',
      addr: { F63: 0.50, F12: 0.15 }, base: 0.10,
      on_rem: { F63: 1.8 }, on_cov: { F63: -0.9 }, slot_decay: 0.06 },
    review_prompt:        { type: 'engagement',color: 'amber',
      addr: {}, base: 0.30, on_rem: {}, on_cov: {}, slot_decay: 0.05 },
    referral_thanks:      { type: 'engagement',color: 'emerald',
      addr: {}, base: 0.25, on_rem: {}, on_cov: {}, slot_decay: 0.05 },
    coordinate_recent:    { type: 'upsell',    color: 'fuchsia',
      addr: { F61: 0.25, F64: 0.20 }, base: 0.20,
      on_rem: { F61: 0.8, F64: 0.7 }, on_cov: {}, slot_decay: 0.05 },
  },
};

// -----------------------------------------------------------------------------
// Page-scoped compose() — uses the PDP composer for 'pdp', otherwise builds
// against this page's problems + modules + slot count.
// -----------------------------------------------------------------------------
window.composePage = function (pageId, feat) {
  const meta = window.PAGE_META[pageId];
  if (!meta) throw new Error('Unknown page: ' + pageId);

  // PDP falls through to the original orchestrator state (v1/v3 toggle still
  // honored automatically by activeModules()).
  if (pageId === 'pdp') {
    const modules = window.useV3 ? window.modulesV3 : window.modulesV1;
    return { ...window.compose(feat, modules, meta.slots), modules };
  }

  const modules = window.PAGE_MODULES[pageId];
  const problems = window.PAGE_PROBLEMS[pageId];

  // Build merged problem-shape map: PDP shapes + extended shapes.
  const mergedShapes = { ...(window.EDITED_SHAPES || window.PROBLEM_SHAPES) };
  for (const code in window.PROBLEM_SHAPES_EXT) {
    if (!mergedShapes[code]) mergedShapes[code] = window.PROBLEM_SHAPES_EXT[code];
  }

  // Score only the problems this page cares about.
  const problemScores = {};
  for (const p of problems) {
    let s = 0, wsum = 0;
    for (const cfg of mergedShapes[p]) {
      const x = feat[cfg.signal];
      s += cfg.w * window.pwl(x, cfg.bps, cfg.vals);
      wsum += cfg.w;
    }
    problemScores[p] = Math.max(0, Math.min(1, s / Math.max(wsum, 1e-9)));
  }

  // Greedy compose against this page's slot budget.
  const remaining = { ...problemScores };
  const coverage = Object.fromEntries(problems.map(p => [p, 0]));
  const page = [];
  const used = new Set();

  for (let slot = 0; slot < meta.slots; slot++) {
    let bestName = null, bestScore = -1e9;
    const scores = {};
    for (const name in modules) {
      if (used.has(name)) continue;
      const sc = window.scoreModule(modules[name], remaining, coverage, slot);
      scores[name] = sc;
      if (sc > bestScore) { bestScore = sc; bestName = name; }
    }
    if (bestName == null) break; // ran out of widgets
    page.push({ slot, name: bestName, score: bestScore, scores });
    used.add(bestName);
    const mod = modules[bestName];
    for (const p in (mod.addr || {})) {
      if (remaining[p] != null) {
        remaining[p] = Math.max(0, remaining[p] - mod.addr[p]);
        coverage[p]  = Math.min(1, (coverage[p] || 0) + mod.addr[p]);
      }
    }
  }

  return { page, problems: problemScores, remaining, coverage, modules };
};
