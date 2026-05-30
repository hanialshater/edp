// =============================================================================
// PAGE EXTENSIONS — makes Widget Gallery + GAM Curves page-aware, and adds
// per-page v3 edits so the v1↔v3 toggle is meaningful on every page (not just
// the PDP). Loaded after page-router.js, before the orchestrator's boot calls
// have re-rendered the views.
// =============================================================================

(function () {

  // ──────────────────────────────────────────────────────────────────────────
  // 1) Per-page v3 edits.
  //
  // Same edit-tuple format as EDITS_V3 in the orchestrator HTML:
  //   [widget, "path", fromValue, toValue, reasoning]
  // path can be 'base', 'on_rem.F##', 'on_cov.F##'. NEW synergies set on_cov
  // to non-zero. (Reasoning is informational — picked up by the gallery diff.)
  // ──────────────────────────────────────────────────────────────────────────
  window.PAGE_EDITS_V3 = {
    home: [
      ['continue_browsing',    'base',         0.15, 0.22, 'Round-2: returners exited too early — primary continuity surface.'],
      ['continue_browsing',    'on_cov.F35',   0.0, -0.6, 'Saturate F35 faster after first re-engagement card.'],
      ['shopping_mission',     'on_cov.F11',   0.0,  1.0, 'NEW synergy: complements editorial_collections on F11.'],
      ['shop_the_look_home',   'base',         0.20, 0.28, 'Strengthen outfit-build surface for paralyzed/outfit-seeker.'],
      ['shop_the_look_home',   'on_cov.F12',   0.6,  1.2, 'Lift after editorial_collections fires.'],
      ['personal_picks_home',  'on_cov.F51',   0.0,  0.9, 'NEW synergy: helps decision paralysis after continue_browsing.'],
      ['last_chance',          'base',         0.20, 0.10, 'Was over-firing on home — drop unless F51 detected.'],
      ['inspiration_hero',     'on_rem.F11',   0.8,  1.2, 'Better entry for first-visit category-overwhelmed shoppers.'],
    ],

    search: [
      ['smart_facets',         'on_rem.F22',   2.0,  2.4, 'Filter friction is the dominant search problem; sharpen.'],
      ['smart_facets',         'on_cov.F22',  -1.0, -1.4, 'Stronger saturation — one facet widget is enough.'],
      ['visual_swatches',      'on_cov.F22',   0.5,  1.1, 'NEW-ish: rises after smart_facets has fired.'],
      ['did_you_mean',         'base',         0.10, 0.16, 'Was firing only on extreme F13; bump baseline.'],
      ['fresh_picks_search',   'on_cov.F21',  -1.0, -1.4, 'Tighter saturation so it does not crowd out related_searches.'],
      ['related_searches',     'on_cov.F23',   0.0,  0.9, 'NEW synergy: complements fresh_picks_search on boredom.'],
      ['featured_brands',      'base',         0.20, 0.12, 'Was over-firing on bored shoppers; depend more on detected need.'],
    ],

    plp: [
      ['facet_rail',           'on_rem.F22',   2.0,  2.4, 'PLP filter friction is the central problem.'],
      ['size_predictor',       'base',         0.10, 0.18, 'Helpful for ANY size-aware shopper, not just F22.'],
      ['size_predictor',       'on_cov.F22',   0.6,  1.2, 'Stronger synergy after facet_rail narrows the set.'],
      ['fresh_picks_plp',      'on_cov.F21',  -0.9, -1.3, 'Saturate so collection_callout gets room.'],
      ['collection_callout',   'on_cov.F23',   0.0,  1.0, 'NEW synergy: lifts after visual_browse fires.'],
      ['visual_browse',        'on_rem.F23',   1.6,  1.9, 'Discovery boredom — visual browse is its primary cure.'],
      ['editor_picks_plp',     'base',         0.20, 0.13, 'Was over-firing on undetected sessions.'],
      ['editor_picks_plp',     'on_cov.F23',   0.0,  0.8, 'NEW synergy: rises with discovery-boredom signal.'],
    ],

    cart: [
      ['return_assurance_cart','on_rem.F46',   2.0,  2.5, 'Round-1 PDP: F46 is the strongest cart-stage worry.'],
      ['return_assurance_cart','on_cov.F46',  -1.0, -1.4, 'Tighter saturation.'],
      ['decision_help_cart',   'base',         0.10, 0.16, 'Always-useful nudge; bump baseline.'],
      ['decision_help_cart',   'on_cov.F51',  -1.0, -1.4, 'Avoid stacking with price_freeze on paralyzed personas.'],
      ['price_freeze',         'on_cov.F53',   0.0, -0.7, 'NEW: saturate F53 quickly after first lock.'],
      ['complete_outfit_cart', 'base',         0.25, 0.32, 'Strong AOV lift surface; lift baseline.'],
      ['shipping_threshold',   'on_rem.F45',   0.8,  1.2, 'Stronger pull on price-sensitive shoppers.'],
      ['saved_for_later',      'on_cov.F51',   0.0,  0.8, 'NEW synergy: nudges paralyzed shoppers to keep momentum.'],
    ],

    checkout: [
      ['trust_signals',        'on_rem.F52',   2.0,  2.6, 'Round-1: checkout doubt is the dominant exit reason.'],
      ['trust_signals',        'on_cov.F52',  -1.0, -1.5, 'Tighter saturation — once trust is addressed, move on.'],
      ['express_payment',      'base',         0.55, 0.62, 'Universally lifts conversion; bump.'],
      ['return_micro',         'on_cov.F46',   0.0, -0.8, 'NEW: saturate F46 quickly inside checkout.'],
      ['price_lock_assurance', 'base',         0.10, 0.16, 'Even price-confident shoppers value the guarantee.'],
      ['price_lock_assurance', 'on_cov.F53',  -0.7, -1.1, 'Tighter saturation.'],
    ],

    post_purchase: [
      ['care_guide',           'on_rem.F62',   2.0,  2.4, 'Premium item + new customer = need clear care guidance.'],
      ['style_companion',      'on_rem.F61',   2.0,  2.4, 'F61 styling-orphan is the #1 post-purchase regret driver.'],
      ['style_companion',      'on_cov.F61',  -1.0, -1.4, 'Tighter saturation.'],
      ['coordinate_recent',    'on_cov.F61',   0.0,  0.9, 'NEW synergy: rises after style_companion seeds the look.'],
      ['repeat_in_color',      'base',         0.15, 0.22, 'F64 is the highest-LTV signal in post-purchase.'],
      ['wardrobe_check',       'on_cov.F63',  -0.9, -1.3, 'Saturate quickly — never ask twice.'],
      ['review_prompt',        'base',         0.30, 0.20, 'Was over-firing on every persona; rely on detection.'],
      ['referral_thanks',      'base',         0.25, 0.16, 'Same as above — was always firing in slot 4.'],
    ],
  };

  // Apply edits to clone of v1 modules. Same logic as applyEdits() in the
  // orchestrator, but isolated so we can build per-page maps.
  function applyEdits(modules, edits) {
    const m = JSON.parse(JSON.stringify(modules));
    for (const [widget, path, _from, to] of edits) {
      if (!m[widget]) continue;
      const parts = path.split('.');
      if (parts.length === 1) {
        m[widget][parts[0]] = to;
      } else {
        const [section, key] = parts;
        if (!m[widget][section]) m[widget][section] = {};
        m[widget][section][key] = to;
      }
    }
    return m;
  }

  // Build PAGE_MODULES_V3 — page-specific evolved registries.
  window.PAGE_MODULES_V3 = {};
  for (const pageId in window.PAGE_MODULES) {
    if (pageId === 'pdp') continue; // pdp uses orchestrator's modulesV3
    const v1 = window.PAGE_MODULES[pageId];
    if (!v1) continue;
    const edits = window.PAGE_EDITS_V3[pageId] || [];
    window.PAGE_MODULES_V3[pageId] = applyEdits(v1, edits);
  }

  // Replace composePage so it picks v1 vs v3 modules per page based on useV3.
  const origCompose = window.composePage;
  window.composePage = function (pageId, feat) {
    if (pageId === 'pdp') return origCompose(pageId, feat);
    const meta = window.PAGE_META[pageId];
    const modules = (window.useV3 && window.PAGE_MODULES_V3[pageId])
      ? window.PAGE_MODULES_V3[pageId]
      : window.PAGE_MODULES[pageId];
    if (!modules) return origCompose(pageId, feat);
    // Temporarily swap PAGE_MODULES[pageId] for the call, then restore.
    const saved = window.PAGE_MODULES[pageId];
    window.PAGE_MODULES[pageId] = modules;
    const out = origCompose(pageId, feat);
    window.PAGE_MODULES[pageId] = saved;
    return out;
  };

  // ──────────────────────────────────────────────────────────────────────────
  // 2) Page picker bar — used by both Gallery and GAM Curves.
  // ──────────────────────────────────────────────────────────────────────────
  let galleryPage = 'pdp';
  let curvesPage  = 'pdp';
  window.galleryPage = () => galleryPage;
  window.curvesPage  = () => curvesPage;

  function pagePickerBar(activeId, onPick) {
    const pages = window.PAGES;
    const meta = window.PAGE_META;
    return `
      <div class="pgx-picker">
        <span class="pgx-picker__lab">PAGE</span>
        ${pages.map(id => `
          <button class="pgx-picker__btn ${id === activeId ? 'pgx-picker__btn--on' : ''}" data-pick="${id}">
            ${meta[id].label}
            <span class="pgx-picker__count">${id === 'pdp' ? Object.keys(window.modulesV1).length : Object.keys(window.PAGE_MODULES[id] || {}).length} widgets</span>
          </button>`).join('')}
      </div>`;
  }

  function wirePagePicker(rootEl, onPick) {
    rootEl.querySelectorAll('[data-pick]').forEach(b => {
      b.addEventListener('click', () => onPick(b.dataset.pick));
    });
  }

  // ──────────────────────────────────────────────────────────────────────────
  // 3) Page-aware Widget Gallery.
  // ──────────────────────────────────────────────────────────────────────────

  // PDP type metadata + non-PDP type metadata (covers all types used in
  // PAGE_MODULES). Colors are CSS hex for the left bar.
  const TYPE_META = {
    // PDP types
    size:     { color: '#06b6d4', desc: 'Fit confidence, size guidance, low-return alternatives.' },
    compare:  { color: '#10b981', desc: 'Side-by-side, vs cards, value breakdowns.' },
    outfit:   { color: '#e879f9', desc: 'Style completion, occasion lookbooks, theme switching.' },
    returns:  { color: '#fb7185', desc: 'Return policy clarity, easy-returns promise.' },
    premium:  { color: '#fbbf24', desc: 'Brand story, material deep dive.' },
    price:    { color: '#f97316', desc: 'Price history, price-drop alerts, freezes, locks.' },
    decision: { color: '#818cf8', desc: 'Wishlist, recently viewed, expert picks — nudges out of paralysis.' },
    default:  { color: '#94a3b8', desc: 'Always-on fallbacks: similar, also bought, trending, personal.' },
    // Non-PDP page types
    hero:        { color: '#f472b6', desc: 'Top-of-page editorial / inspiration surfaces.' },
    continuity:  { color: '#818cf8', desc: 'Pick up where the customer left off.' },
    guidance:    { color: '#38bdf8', desc: 'Direct shopper into the right path: missions, care, wardrobe checks.' },
    editorial:   { color: '#e879f9', desc: 'Curated collections, lookbooks, editor picks.' },
    feed:        { color: '#fbbf24', desc: 'Algorithmic product feeds: new, trending, seasonal, last-chance.' },
    personal:    { color: '#818cf8', desc: 'Personalized recommendations and history.' },
    query:       { color: '#2dd4bf', desc: 'Query interpretation: did-you-mean, related, intent rewrite.' },
    filter:      { color: '#f97316', desc: 'Facets, swatches, size predictors — narrow the result set.' },
    results:     { color: '#94a3b8', desc: 'The canonical product grid for this page.' },
    core:        { color: '#94a3b8', desc: 'Always-on backbone of the page (cart summary, order summary).' },
    incentive:   { color: '#10b981', desc: 'Free-shipping bars, gift options, threshold nudges.' },
    upsell:      { color: '#e879f9', desc: 'Cross-sell, AOV-lifters.' },
    trust:       { color: '#10b981', desc: 'Trust badges, return assurance, buyer protection.' },
    speed:       { color: '#10b981', desc: 'Express pay, one-click flows.' },
    engagement:  { color: '#fbbf24', desc: 'Reviews, referrals, ongoing relationship moves.' },
  };
  const TYPE_LABEL = {
    size:'Size · Fit', compare:'Comparison', outfit:'Outfit', returns:'Returns',
    premium:'Premium · Quality', price:'Price', decision:'Decision', default:'Defaults',
    hero:'Hero', continuity:'Continuity', guidance:'Guidance', editorial:'Editorial',
    feed:'Feed', personal:'Personal', query:'Query', filter:'Filter', results:'Results',
    core:'Core', incentive:'Incentive', upsell:'Upsell', trust:'Trust', speed:'Speed',
    engagement:'Engagement',
  };
  const COLOR_TINT = {
    cyan:'#e8f6f9', amber:'#fbf2dd', emerald:'#e3f3ea', fuchsia:'#f7e7f4',
    orange:'#fbeadc', rose:'#fbe3e6', indigo:'#e8e9f7', slate:'#f1f2f4',
    sky:'#e0f2fe', teal:'#dff5f0', blue:'#e0e8f7',
  };
  const COLOR_TXT = {
    cyan:'#0c5a66', amber:'#7a4e0a', emerald:'#0c5234', fuchsia:'#7a1f6a',
    orange:'#7a3c0d', rose:'#7a1c2a', indigo:'#26307a', slate:'#3a3f4a',
    sky:'#0c4a6e', teal:'#0c4c46', blue:'#1e3a8a',
  };

  function modulesForGalleryPage(pageId) {
    if (pageId === 'pdp') return window.useV3 ? window.modulesV3 : window.modulesV1;
    return (window.useV3 && window.PAGE_MODULES_V3[pageId])
      ? window.PAGE_MODULES_V3[pageId]
      : window.PAGE_MODULES[pageId];
  }
  function renderersForGalleryPage(pageId) {
    return pageId === 'pdp' ? window.WidgetRenderers : (window.PageWidgets[pageId] || {});
  }

  function renderGalleryPaged() {
    const pageId = galleryPage;
    const modules = modulesForGalleryPage(pageId);
    const renderers = renderersForGalleryPage(pageId);
    const meta = window.PAGE_META[pageId];

    // Group widgets by type, preserving registry order within each group.
    const grouped = {};
    for (const name in modules) {
      const t = modules[name].type;
      if (!grouped[t]) grouped[t] = [];
      grouped[t].push(name);
    }
    const typeOrder = Object.keys(grouped).sort((a, b) => {
      // Stable display order: types that exist in our pre-defined order come
      // first, others alphabetic.
      const all = ['hero','continuity','guidance','editorial','feed','personal',
                   'query','filter','results','core','incentive','upsell','trust',
                   'speed','engagement','size','compare','outfit','returns',
                   'premium','price','decision','default'];
      const ai = all.indexOf(a), bi = all.indexOf(b);
      if (ai === -1 && bi === -1) return a.localeCompare(b);
      if (ai === -1) return 1;
      if (bi === -1) return -1;
      return ai - bi;
    });

    const total = Object.keys(modules).length;

    // Count synergies introduced by v3 for the active page (only non-zero
    // on_cov entries that differ from v1).
    let v3SynergyCount = 0;
    if (window.useV3) {
      const v1 = pageId === 'pdp' ? window.modulesV1 : window.PAGE_MODULES[pageId];
      for (const name in modules) {
        const v1m = v1[name] || {};
        const v3m = modules[name];
        const v1cov = v1m.on_cov || {};
        const v3cov = v3m.on_cov || {};
        for (const p in v3cov) {
          if ((v1cov[p] || 0) === 0 && v3cov[p] !== 0) v3SynergyCount++;
        }
      }
    }

    let html = `
      <div class="gal-shell">
        ${pagePickerBar(pageId)}
        <header class="gal-header">
          <div>
            <h1 class="gal-title">Widget Registry · ${meta.label}</h1>
            <p class="gal-sub">${total} widgets registered for <b>${meta.label}</b>. Showing version <b>${window.useV3 ? 'v3 evolved' : 'v1 baseline'}</b>${window.useV3 && v3SynergyCount > 0 ? ` · <b>${v3SynergyCount} new synergies</b> on this page` : ''}. Switch page above to see what's eligible there; toggle v1↔v3 in the header to see addressing and synergy rewires.</p>
          </div>
          <div class="gal-stats">
            <div><span class="gal-stats__big">${total}</span><span class="gal-stats__lab">WIDGETS</span></div>
            <div><span class="gal-stats__big">${typeOrder.length}</span><span class="gal-stats__lab">TYPES</span></div>
            <div><span class="gal-stats__big">${(window.PAGE_PROBLEMS[pageId] || window.PROBLEMS).length}</span><span class="gal-stats__lab">PROBLEMS</span></div>
            <div><span class="gal-stats__big">${meta.slots}</span><span class="gal-stats__lab">SLOTS / PAGE</span></div>
          </div>
        </header>
    `;

    for (const t of typeOrder) {
      const tm = TYPE_META[t] || { color: '#94a3b8', desc: '' };
      const label = TYPE_LABEL[t] || t;
      html += `
        <section class="gal-group">
          <div class="gal-group__head">
            <div class="gal-group__bar" style="background:${tm.color};"></div>
            <div>
              <h2 class="gal-group__title">${label} <span class="gal-group__count">(${grouped[t].length})</span></h2>
              <p class="gal-group__desc">${tm.desc}</p>
            </div>
          </div>
          <table class="gal-tbl">
            <thead>
              <tr>
                <th style="width:24px;"></th>
                <th style="width:200px;">Widget</th>
                <th style="width:170px;">Addresses</th>
                <th style="width:90px;">Base</th>
                <th style="width:120px;">Synergies (cov)</th>
                <th>Preview</th>
              </tr>
            </thead>
            <tbody>
      `;

      grouped[t].forEach((name, idx) => {
        const mod = modules[name];
        const tint = COLOR_TINT[mod.color] || '#f1f2f4';
        const txt  = COLOR_TXT[mod.color]  || '#3a3f4a';
        const addrChips = Object.entries(mod.addr || {})
          .sort((a, b) => b[1] - a[1])
          .map(([p, v]) => `<span class="gal-chip" data-problem="${p}" style="background:${tint};color:${txt};">${p} · ${v.toFixed(2)}</span>`)
          .join('') || '<span class="gal-chip gal-chip--muted">—</span>';
        const covChips = Object.entries(mod.on_cov || {})
          .filter(([, v]) => v !== 0)
          .map(([p, v]) => `<span class="gal-chip gal-chip--cov" data-problem="${p}">${p}: ${v > 0 ? '+' : ''}${v.toFixed(2)}</span>`)
          .join('') || '<span class="gal-chip gal-chip--muted">—</span>';

        const renderer = renderers[name];
        let preview = renderer
          ? renderer({ entry: { name, score: 0 }, mod, slotIdx: 0, problems: {}, coverage: {} })
          : '<div class="gal-noprev">no renderer</div>';
        preview = window.pCodes ? window.pCodes(preview) : preview;

        html += `
          <tr class="gal-row">
            <td class="gal-num">${String(idx + 1).padStart(2, '0')}</td>
            <td>
              <div class="gal-name">${name}</div>
              <div class="gal-meta"><code>type=${mod.type}</code> · decay <b>${(mod.slot_decay || 0).toFixed(2)}</b></div>
            </td>
            <td>${addrChips}</td>
            <td><span class="gal-base">${mod.base.toFixed(2)}</span></td>
            <td>${covChips}</td>
            <td><div class="gal-preview">${preview}</div></td>
          </tr>
        `;
      });

      html += `</tbody></table></section>`;
    }
    html += '</div>';
    const cont = document.getElementById('gallery-cont');
    cont.innerHTML = html;
    wirePagePicker(cont, (id) => { galleryPage = id; renderGalleryPaged(); });
  }
  window.renderGallery = renderGalleryPaged;

  // ──────────────────────────────────────────────────────────────────────────
  // 4) Page-aware GAM Curves.
  //
  // L1 — render only the problem shapes that the active page actually scores.
  // L2 — pick widgets from the active page's registry. Re-uses the existing
  // gamL2Widget global so existing handlers still work.
  // ──────────────────────────────────────────────────────────────────────────

  // Snapshot of the orchestrator's existing curve helpers (they live in the
  // root <script> as local lexical names but `gamSetView` / `gamResetCurve` /
  // `gamResetAll` / `gamStartDrag` / `gamHasEdits` / `ensureEditedShapes` are
  // declared as `function` so they're on window).

  function activeProblemsForCurves() {
    const pageId = curvesPage;
    return (window.PAGE_PROBLEMS[pageId] || window.PROBLEMS).slice();
  }
  function problemMetaFor(p) {
    if (window.PROBLEM_META && window.PROBLEM_META[p]) return window.PROBLEM_META[p];
    return (window.PROBLEM_META_EXT && window.PROBLEM_META_EXT[p]) || { name: p, color: 'slate' };
  }
  // The orchestrator's EDITED_SHAPES only covers F32–F51. For Layer 1 we need
  // the merged map: edited (when present) ∪ extended page shapes.
  function mergedShapes() {
    const base = { ...(window.PROBLEM_SHAPES || {}), ...(window.PROBLEM_SHAPES_EXT || {}) };
    if (window.EDITED_SHAPES) {
      for (const p in window.EDITED_SHAPES) base[p] = window.EDITED_SHAPES[p];
    }
    return base;
  }

  // Score one problem against current featState using the merged shape map.
  function scoreOneProblem(p, shapes) {
    if (!shapes[p]) return 0;
    let s = 0, wsum = 0;
    for (const cfg of shapes[p]) {
      const x = window.featState[cfg.signal];
      s += cfg.w * window.pwl(x, cfg.bps, cfg.vals);
      wsum += cfg.w;
    }
    return Math.max(0, Math.min(1, s / Math.max(wsum, 1e-9)));
  }

  function renderCurvesPaged() {
    const cont = document.getElementById('curves-cont');
    if (!cont) return;
    cont.innerHTML = '';

    // Subtab bar + global edit actions + page picker.
    const header = document.createElement('div');
    header.className = 'col-span-full';
    const pickerHtml = pagePickerBar(curvesPage);
    header.innerHTML = `
      ${pickerHtml}
      <div class="gam-subtabs">
        <button class="gam-subtab ${window.gamView === 'l1' ? 'gam-subtab--on' : ''}" onclick="gamSetView('l1')">Layer 1 · Signals → Problems</button>
        <button class="gam-subtab ${window.gamView === 'l2' ? 'gam-subtab--on' : ''}" onclick="gamSetView('l2')">Layer 2 · Problems → Widget Score</button>
      </div>
      ${window.gamView === 'l1' ? `
        <div class="gam-global-actions">
          <span>DRAG ANY DOT ON THE CURVE TO RESHAPE PROBLEM DETECTION · only PDP-problem curves (F32–F51) are editable</span>
          ${window.gamHasEdits && window.gamHasEdits() ? '<span class="gam-edited-badge">EDITED</span>' : ''}
          <button onclick="gamResetAll()" ${(window.gamHasEdits && window.gamHasEdits()) ? '' : 'disabled style="opacity:0.4;cursor:not-allowed;"'}>RESET ALL CURVES</button>
        </div>
      ` : ''}
    `;
    cont.appendChild(header);
    wirePagePicker(header, (id) => { curvesPage = id; renderCurvesPaged(); });

    if (window.gamView === 'l1') return renderCurvesL1Paged(cont);
    return renderCurvesL2Paged(cont);
  }

  function renderCurvesL1Paged(cont) {
    const SHAPES = mergedShapes();
    const problemsForPage = activeProblemsForCurves();
    const colorRGBMap = {
      cyan: '34,211,238', amber: '251,191,36', emerald: '16,185,129',
      fuchsia: '232,121,249', orange: '249,115,22', rose: '251,113,133',
      indigo: '129,140,248', sky: '125,211,252', teal: '94,234,212',
      slate: '148,163,184',
    };

    for (const p of problemsForPage) {
      if (!SHAPES[p]) continue;
      const meta = problemMetaFor(p);
      const isPdpProblem = !!(window.PROBLEM_SHAPES && window.PROBLEM_SHAPES[p]);
      const groupDiv = document.createElement('div');
      // Tailwind safelist trick — use inline color when possible.
      groupDiv.className = `rounded-lg p-3 border bg-slate-900/40`;
      groupDiv.style.borderColor = `rgba(${colorRGBMap[meta.color] || '148,163,184'}, 0.35)`;
      const score = scoreOneProblem(p, SHAPES);
      let html = `
        <div class="flex justify-between items-end pb-2 mb-3" style="border-bottom: 1px solid rgba(${colorRGBMap[meta.color] || '148,163,184'}, 0.3);">
          <h3 class="text-sm font-bold" data-problem="${p}" style="cursor:help;color:rgb(${colorRGBMap[meta.color] || '148,163,184'});">${meta.name}</h3>
          <div class="text-right">
            <span class="text-[9px] text-slate-500 uppercase tracking-widest block">Aggregate</span>
            <span class="mono text-xl font-bold text-white">${score.toFixed(2)}</span>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-${SHAPES[p].length} gap-2">
      `;
      SHAPES[p].forEach((cfg, ci) => {
        const origCfg = (window.PROBLEM_SHAPES && window.PROBLEM_SHAPES[p]) ? window.PROBLEM_SHAPES[p][ci] : null;
        const x = window.featState[cfg.signal];
        const y = window.pwl(x, cfg.bps, cfg.vals);
        const xRange = cfg.bps[cfg.bps.length - 1] - cfg.bps[0];
        const rgb = colorRGBMap[meta.color] || '148,163,184';
        let pathD = '';
        cfg.bps.forEach((bp, i) => {
          const px = 30 + ((bp - cfg.bps[0]) / xRange) * 230;
          const py = 100 - cfg.vals[i] * 80;
          pathD += (i === 0 ? 'M' : 'L') + ` ${px} ${py} `;
        });
        const handles = cfg.bps.map((bp, i) => {
          const px = 30 + ((bp - cfg.bps[0]) / xRange) * 230;
          const py = 100 - cfg.vals[i] * 80;
          // Only PDP-problem curves are editable (the orchestrator's
          // EDITED_SHAPES storage and gamStartDrag are PDP-scoped).
          const drag = isPdpProblem ? `onmousedown="gamStartDrag(event, '${p}', ${ci}, ${i})"` : 'style="cursor:not-allowed;"';
          return `<circle class="gam-handle" cx="${px}" cy="${py}" r="${isPdpProblem ? 5 : 4}" fill="rgb(${rgb})" stroke="#0f172a" stroke-width="1.5" ${drag}/>`;
        }).join('');
        const curPx = 30 + ((x - cfg.bps[0]) / xRange) * 230;
        const curPy = 100 - y * 80;
        const isEdited = origCfg ? cfg.vals.some((v, i) => Math.abs(v - origCfg.vals[i]) > 1e-6) : false;
        html += `
          <div class="bg-slate-900/80 border ${isEdited ? 'border-amber-500/50' : 'border-slate-700'} rounded p-2">
            <div class="flex justify-between items-center mb-1 gam-card-actions">
              <span class="text-[10px] font-semibold text-slate-300 truncate pr-1">${cfg.title}</span>
              <span class="mono text-[9px] text-slate-400 bg-slate-800 px-1 py-0.5 rounded">w=${(cfg.w * 100).toFixed(0)}%</span>
              ${isEdited && isPdpProblem ? `<button class="gam-reset-btn" onclick="gamResetCurve('${p}', ${ci})" title="Reset this curve">↺</button>` : ''}
            </div>
            <svg viewBox="0 0 280 120" class="w-full h-auto" style="overflow:visible;">
              <line x1="30" y1="20" x2="270" y2="20" stroke="#334155" stroke-dasharray="2 2"/>
              <line x1="30" y1="60" x2="270" y2="60" stroke="#334155" stroke-dasharray="2 2"/>
              <line x1="30" y1="100" x2="270" y2="100" stroke="#475569" stroke-width="1.5"/>
              <text x="22" y="24" fill="#94a3b8" font-size="9" text-anchor="end">1.0</text>
              <text x="22" y="64" fill="#94a3b8" font-size="9" text-anchor="end">0.5</text>
              <text x="22" y="104" fill="#94a3b8" font-size="9" text-anchor="end">0</text>
              <path d="${pathD}" fill="none" stroke="rgb(${rgb})" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
              ${handles}
              <circle cx="${curPx}" cy="${curPy}" r="4" fill="#0f172a" stroke="rgb(${rgb})" stroke-width="2" style="pointer-events:none;"/>
              <text x="${curPx}" y="${curPy - 10}" fill="white" font-size="11" font-weight="bold" text-anchor="middle" style="pointer-events:none;">${y.toFixed(2)}</text>
            </svg>
            <div class="flex justify-between mono text-[8px] text-slate-500 mt-1 px-6">
              <span>${cfg.bps[0]}</span>
              <span class="text-blue-400 font-bold">${x.toFixed(2)}</span>
              <span>${cfg.bps[cfg.bps.length - 1]}</span>
            </div>
          </div>`;
      });
      html += '</div>';
      groupDiv.innerHTML = html;
      cont.appendChild(groupDiv);
    }
  }

  function renderCurvesL2Paged(cont) {
    const modules = modulesForGalleryPage(curvesPage);
    if (!window.gamL2Widget || !modules[window.gamL2Widget]) {
      window.gamL2Widget = Object.keys(modules)[0];
    }

    // Compose the page once so we can pull the right slot/coverage state.
    const result = window.composePage(curvesPage, window.featState);

    const wrap = document.createElement('div');
    wrap.className = 'gam-l2-shell col-span-full';
    let html = `
      <div class="gam-global-actions">
        <span>EACH WIDGET'S SCORING IS A LINEAR ADDITIVE MODEL (GAM):</span>
        <code style="color:#cbd5e1;background:#1e293b;padding:2px 6px;border-radius:3px;font-size:11px;">score = base + Σ(on_rem · remaining) + Σ(on_cov · coverage) − slot_decay · slot</code>
      </div>
      <div class="gam-l2-picker">
        ${Object.keys(modules).map(name => `
          <button class="gam-l2-pill ${name === window.gamL2Widget ? 'gam-l2-pill--on' : ''}" onclick="window.gamL2Widget='${name}';renderCurves();">${name}</button>
        `).join('')}
      </div>`;

    const name = window.gamL2Widget;
    const mod = modules[name];
    const inPage = result.page.find(e => e.name === name);
    const slot = inPage ? inPage.slot : 0;
    const score = window.scoreModule(mod, result.remaining, result.coverage, slot);

    const terms = [];
    terms.push({ label: 'base', value: mod.base, contribution: mod.base, signal: 'constant' });
    for (const p in (mod.on_rem || {})) {
      const rem = result.remaining[p] || 0;
      terms.push({ label: `on_rem · ${p}`, value: mod.on_rem[p], contribution: mod.on_rem[p] * rem, signal: `remaining ${p}=${rem.toFixed(2)}`, problem: p });
    }
    for (const p in (mod.on_cov || {})) {
      const cov = result.coverage[p] || 0;
      terms.push({ label: `on_cov · ${p}`, value: mod.on_cov[p], contribution: mod.on_cov[p] * cov, signal: `coverage ${p}=${cov.toFixed(2)}`, problem: p });
    }
    terms.push({ label: 'slot_decay', value: -(mod.slot_decay || 0), contribution: -(mod.slot_decay || 0) * slot, signal: `slot=${slot}` });

    const maxAbs = Math.max(0.01, ...terms.map(t => Math.abs(t.contribution)));

    html += `
      <div class="gam-l2-card">
        <div class="gam-l2-head">
          <div>
            <div class="gam-l2-name">${name}</div>
            <div class="gam-l2-type">${(mod.type || '').toUpperCase()} · ${inPage ? `IN ${window.PAGE_META[curvesPage].label.toUpperCase()} @ SLOT ${slot + 1}` : `NOT SELECTED FOR ${window.PAGE_META[curvesPage].label.toUpperCase()} (THIS PERSONA)`}</div>
          </div>
          <div>
            <div class="gam-l2-score">${score.toFixed(2)}</div>
            <div class="gam-l2-score__lab">SCORE @ THIS STATE</div>
          </div>
        </div>
        <div class="gam-l2-terms">
          ${terms.map(t => {
            const pct = Math.abs(t.contribution) / maxAbs * 100;
            const sign = t.contribution >= 0 ? 'pos' : 'neg';
            const color = t.contribution >= 0 ? '#34d399' : '#fb7185';
            const probAttr = t.problem ? `data-problem="${t.problem}"` : '';
            return `
              <div class="gam-l2-term">
                <div class="gam-l2-term__head">
                  <span class="gam-l2-term__lab" ${probAttr}>${t.label}</span>
                  <span class="gam-l2-term__val gam-l2-term__val--${sign}">${t.contribution >= 0 ? '+' : ''}${t.contribution.toFixed(3)}</span>
                </div>
                <div class="gam-l2-term__bar-bg">
                  <div class="gam-l2-term__bar" style="width:${pct.toFixed(0)}%;background:${color};"></div>
                </div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#64748b;margin-top:4px;letter-spacing:0.04em;">
                  weight=${t.value.toFixed(2)} · ${t.signal}
                </div>
              </div>`;
          }).join('')}
        </div>
      </div>`;
    wrap.innerHTML = html;
    cont.appendChild(wrap);
  }

  window.renderCurves = renderCurvesPaged;

  // ──────────────────────────────────────────────────────────────────────────
  // 5) Keep gallery/curves in sync with the live-page picker.
  // ──────────────────────────────────────────────────────────────────────────
  const origSetPage = window.setPage;
  window.setPage = function (id) {
    galleryPage = id;
    curvesPage = id;
    if (origSetPage) origSetPage(id);
    // If gallery / curves view is currently visible, refresh it too.
    const gv = document.getElementById('view-gallery');
    if (gv && !gv.classList.contains('hidden')) renderGalleryPaged();
    const cv = document.getElementById('view-curves');
    if (cv && !cv.classList.contains('hidden')) renderCurvesPaged();
  };

  // Default galleryPage/curvesPage to whatever the live-page picker is on.
  if (window.getCurrentPage) {
    galleryPage = window.getCurrentPage();
    curvesPage  = window.getCurrentPage();
  }

  // ──────────────────────────────────────────────────────────────────────────
  // 6) Page-aware Analytics.
  // Mirrors the orchestrator's renderAnalytics() but driven by the page
  // picker. Re-uses the existing .an-* CSS.
  // ──────────────────────────────────────────────────────────────────────────

  // Daily traffic by page-type (sessions/day, demo numbers). Larger surfaces
  // like Home/Search/PDP get more, Checkout/Post-purchase get fewer.
  const PAGE_VOLUME = {
    home:          84500,
    search:        62300,
    plp:           41200,
    pdp:           28900,
    cart:          15400,
    checkout:      11700,
    post_purchase:  9800,
  };

  // CTR baselines per widget type. Higher for interactive / shopping-led
  // surfaces; lower for informational / always-on.
  const TYPE_CTR = {
    // PDP types (mirror orchestrator's TYPE_CTR_BASELINE)
    outfit: 6.8, decision: 5.4, compare: 4.6, premium: 4.1,
    returns: 3.8, size: 3.2, price: 2.9, default: 2.3,
    // Page-specific types
    hero: 5.2, continuity: 7.4, guidance: 6.1, editorial: 5.8,
    feed: 4.4, personal: 6.0, query: 5.5, filter: 7.8, results: 4.1,
    core: 2.0, incentive: 5.7, upsell: 6.3, trust: 3.6, speed: 8.5,
    engagement: 4.8,
  };

  const TYPE_COLOR_TXT = {
    cyan: '#22d3ee', emerald: '#34d399', fuchsia: '#e879f9', rose: '#fb7185',
    amber: '#fbbf24', orange: '#fb923c', indigo: '#818cf8', slate: '#94a3b8',
    sky: '#7dd3fc', teal: '#5eead4', blue: '#93c5fd',
  };
  const TYPE_COLOR_TINT = {
    cyan: 'rgba(34,211,238,0.12)', emerald: 'rgba(52,211,153,0.12)',
    fuchsia: 'rgba(232,121,249,0.12)', rose: 'rgba(251,113,133,0.12)',
    amber: 'rgba(251,191,36,0.12)', orange: 'rgba(251,146,60,0.12)',
    indigo: 'rgba(129,140,248,0.12)', slate: 'rgba(148,163,184,0.12)',
    sky: 'rgba(125,211,252,0.12)', teal: 'rgba(94,234,212,0.12)',
    blue: 'rgba(147,197,253,0.12)',
  };

  function anHash(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) h = ((h ^ s.charCodeAt(i)) * 16777619) >>> 0;
    return h;
  }
  function anRand(seed) {
    return function () {
      seed |= 0; seed = (seed + 0x6D2B79F5) | 0;
      let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  const ANALYTICS_DAYS = 30;

  function pageComputeAnalytics(modules, version, pageId, slots) {
    const baseVolume = PAGE_VOLUME[pageId] || 12000;
    const rows = [];
    for (const name in modules) {
      const mod = modules[name];
      const addrSum = Object.values(mod.addr || {}).reduce((a, b) => a + b, 0);
      const covBoost = Object.values(mod.on_cov || {})
        .filter(v => v > 0).reduce((a, b) => a + b, 0);
      const score = mod.base + addrSum * 0.4 + covBoost * 0.25;

      const rng = anRand(anHash(name + version + pageId));
      const selectionRate = Math.max(0.04, Math.min(0.55, score * 0.4 + rng() * 0.06));
      const impressions = Math.round(selectionRate * baseVolume * ANALYTICS_DAYS);

      const ctrBase = TYPE_CTR[mod.type] || 3;
      const ctr = ctrBase + (addrSum > 0 ? Math.min(2.5, addrSum) : 0) - (rng() - 0.5) * 1.4;
      const clicks = Math.round(impressions * ctr / 100);

      const atbBase = mod.type === 'compare' || mod.type === 'decision' || mod.type === 'upsell' || mod.type === 'incentive' ? 1.2 : 0.7;
      const atbRate = atbBase + addrSum * 0.6 + (rng() - 0.4) * 0.4;
      const atbAttrib = Math.round(impressions * Math.max(0.2, atbRate) / 100);

      const resolution = Math.min(addrSum, addrSum * 0.78 + rng() * 0.06);

      const slotCount = slots || 6;
      const slotDist = [];
      let acc = 0;
      for (let i = 0; i < slotCount; i++) {
        const w = Math.max(0, 1 - i * ((mod.slot_decay || 0.04) * 1.4 + 0.04));
        slotDist.push(w);
        acc += w;
      }
      const slotPct = slotDist.map(v => v / acc);

      const drift = (anHash(name + pageId) % 100) / 50 - 1;
      const spark = [];
      for (let i = 0; i < ANALYTICS_DAYS; i++) {
        const t = i / (ANALYTICS_DAYS - 1);
        const val = 0.7 + 0.3 * Math.sin(i * 0.42 + anHash(name) * 0.01) + drift * 0.12 * t + (rng() - 0.5) * 0.08;
        spark.push(Math.max(0.1, val));
      }

      rows.push({
        name, mod,
        impressions, selectionRate, ctr, clicks,
        atbRate: Math.max(0.2, atbRate), atbAttrib,
        resolution, slotPct, spark,
      });
    }
    return rows;
  }

  let analyticsPage = 'pdp';
  let anSortKey = 'impressions';
  let anSortDir = -1;
  let anFilterType = 'all';

  function modulesForAnalyticsPage(pageId, v3) {
    if (pageId === 'pdp') return v3 ? window.modulesV3 : window.modulesV1;
    return (v3 && window.PAGE_MODULES_V3[pageId])
      ? window.PAGE_MODULES_V3[pageId]
      : window.PAGE_MODULES[pageId];
  }

  function renderAnalyticsPaged() {
    const pageId = analyticsPage;
    const meta = window.PAGE_META[pageId];
    const useV3 = !!window.useV3;
    const modules = modulesForAnalyticsPage(pageId, useV3);
    const otherModules = modulesForAnalyticsPage(pageId, !useV3);
    const rows = pageComputeAnalytics(modules, useV3 ? 'v3' : 'v1', pageId, meta.slots);
    const rowsOther = pageComputeAnalytics(otherModules, useV3 ? 'v1' : 'v3', pageId, meta.slots);
    const otherByName = Object.fromEntries(rowsOther.map(r => [r.name, r]));

    // Collect types present in this page's registry
    const typesPresent = new Set(Object.values(modules).map(m => m.type));
    const typeFilters = ['all', ...Array.from(typesPresent)];
    const typeLabels = {
      all: 'All', size: 'Size · Fit', compare: 'Comparison', outfit: 'Outfit',
      returns: 'Returns', premium: 'Premium', price: 'Price', decision: 'Decision', default: 'Defaults',
      hero: 'Hero', continuity: 'Continuity', guidance: 'Guidance', editorial: 'Editorial',
      feed: 'Feed', personal: 'Personal', query: 'Query', filter: 'Filter', results: 'Results',
      core: 'Core', incentive: 'Incentive', upsell: 'Upsell', trust: 'Trust', speed: 'Speed',
      engagement: 'Engagement',
    };
    // Reset filter if not applicable on this page
    if (anFilterType !== 'all' && !typesPresent.has(anFilterType)) anFilterType = 'all';

    // Sort & filter
    let filtered = anFilterType === 'all' ? rows : rows.filter(r => r.mod.type === anFilterType);
    filtered.sort((a, b) => (a[anSortKey] - b[anSortKey]) * anSortDir);

    // KPIs
    const totalImp = rows.reduce((s, r) => s + r.impressions, 0);
    const totalImpOther = rowsOther.reduce((s, r) => s + r.impressions, 0);
    const impDelta = ((totalImp - totalImpOther) / Math.max(1, totalImpOther) * 100);
    const avgCtr = rows.reduce((s, r) => s + r.ctr * r.impressions, 0) / Math.max(1, totalImp);
    const avgCtrOther = rowsOther.reduce((s, r) => s + r.ctr * r.impressions, 0) / Math.max(1, totalImpOther);
    const totalAtb = rows.reduce((s, r) => s + r.atbAttrib, 0);
    const totalAtbOther = rowsOther.reduce((s, r) => s + r.atbAttrib, 0);
    const atbDelta = ((totalAtb - totalAtbOther) / Math.max(1, totalAtbOther) * 100);

    // Biggest mover
    let topMover = null, topMoverPct = 0;
    rows.forEach(r => {
      const o = otherByName[r.name];
      if (!o) return;
      const d = (r.impressions - o.impressions) / Math.max(1, o.impressions) * 100;
      if (Math.abs(d) > Math.abs(topMoverPct)) { topMoverPct = d; topMover = r.name; }
    });

    const spark = (vals, color) => {
      const w = 90, h = 28, max = Math.max(...vals), min = Math.min(...vals), rng = max - min || 1;
      const pts = vals.map((v, i) => `${(i / (vals.length - 1) * w).toFixed(1)},${(h - ((v - min) / rng) * h).toFixed(1)}`).join(' ');
      return `<svg class="an-spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
        <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/>
        <circle cx="${w}" cy="${(h - ((vals[vals.length - 1] - min) / rng) * h).toFixed(1)}" r="2" fill="${color}"/>
      </svg>`;
    };

    const versionLabel = useV3 ? 'v3 evolved' : 'v1 baseline';
    const otherVersionLabel = useV3 ? 'v1 baseline' : 'v3 evolved';

    // KPI cards
    const kpis = `
      <div class="an-kpis">
        <div class="an-kpi">
          <span class="an-kpi__lab">TOTAL IMPRESSIONS · 30D</span>
          <div class="an-kpi__row">
            <span class="an-kpi__big">${(totalImp / 1000).toFixed(1)}k</span>
            <span class="an-kpi__delta ${impDelta >= 0 ? 'an-kpi__delta--up' : 'an-kpi__delta--down'}">${impDelta >= 0 ? '+' : ''}${impDelta.toFixed(1)}%</span>
          </div>
          <span class="an-kpi__sub">across <b>${Object.keys(modules).length}</b> widgets · vs ${otherVersionLabel}</span>
        </div>
        <div class="an-kpi">
          <span class="an-kpi__lab">AVERAGE CTR</span>
          <div class="an-kpi__row">
            <span class="an-kpi__big">${avgCtr.toFixed(2)}%</span>
            <span class="an-kpi__delta ${avgCtr >= avgCtrOther ? 'an-kpi__delta--up' : 'an-kpi__delta--down'}">${avgCtr >= avgCtrOther ? '+' : ''}${(avgCtr - avgCtrOther).toFixed(2)}pp</span>
          </div>
          <span class="an-kpi__sub">weighted by impressions</span>
        </div>
        <div class="an-kpi">
          <span class="an-kpi__lab">ATTRIBUTED ATB · 30D</span>
          <div class="an-kpi__row">
            <span class="an-kpi__big">${(totalAtb / 1000).toFixed(1)}k</span>
            <span class="an-kpi__delta ${atbDelta >= 0 ? 'an-kpi__delta--up' : 'an-kpi__delta--down'}">${atbDelta >= 0 ? '+' : ''}${atbDelta.toFixed(1)}%</span>
          </div>
          <span class="an-kpi__sub">last-touch attribution</span>
        </div>
        <div class="an-kpi">
          <span class="an-kpi__lab">BIGGEST MOVER ${useV3 ? '(v1 → v3)' : '(v3 → v1)'}</span>
          <div class="an-kpi__row">
            <span class="an-kpi__big" style="font-size:16px;">${topMover || '—'}</span>
            <span class="an-kpi__delta ${topMoverPct >= 0 ? 'an-kpi__delta--up' : 'an-kpi__delta--down'}">${topMoverPct >= 0 ? '+' : ''}${topMoverPct.toFixed(0)}%</span>
          </div>
          <span class="an-kpi__sub">impression share change</span>
        </div>
      </div>`;

    // Filter chips
    const filters = `
      <div class="an-filters">
        <div class="an-filter-group">
          <span class="an-filter-group__lab">TYPE</span>
          ${typeFilters.map(t => `<button class="an-chip ${anFilterType === t ? 'an-chip--on' : ''}" data-an-filter="${t}">${typeLabels[t] || t}</button>`).join('')}
        </div>
        <div class="an-filter-group" style="margin-left:auto;">
          <span class="an-filter-group__lab">VERSION</span>
          <button class="an-chip ${!useV3 ? 'an-chip--on' : ''}" data-an-version="v1">v1 baseline</button>
          <button class="an-chip ${useV3 ? 'an-chip--on' : ''}" data-an-version="v3">v3 evolved</button>
        </div>
      </div>`;

    const sortArrow = (key) => anSortKey === key ? (anSortDir < 0 ? ' ↓' : ' ↑') : '';
    const sortClass = (key) => anSortKey === key ? 'an-sort-active' : '';

    const tableRows = filtered.map((r, i) => {
      const color = TYPE_COLOR_TXT[r.mod.color] || '#94a3b8';
      const tint = TYPE_COLOR_TINT[r.mod.color] || 'rgba(148,163,184,0.12)';
      const o = otherByName[r.name];
      const delta = o ? ((r.impressions - o.impressions) / Math.max(1, o.impressions) * 100) : 0;
      const deltaCls = Math.abs(delta) < 1 ? 'an-delta--flat' : delta > 0 ? 'an-delta--up' : 'an-delta--down';
      const deltaArrow = Math.abs(delta) < 1 ? '·' : delta > 0 ? '▲' : '▼';

      const topProblems = Object.entries(r.mod.addr || {})
        .sort((a, b) => b[1] - a[1]).slice(0, 2)
        .map(([p]) => `<span class="an-problem-chip" data-problem="${p}" style="background:${tint};color:${color};">${p}</span>`)
        .join('');

      const maxSlot = Math.max(...r.slotPct);
      const slotBars = r.slotPct.map(v => `<span class="an-slots__cell" style="height:${(v / maxSlot * 26).toFixed(0)}px;background:${color};opacity:${(0.4 + v / maxSlot * 0.6).toFixed(2)};"></span>`).join('');

      const ctrBarPct = Math.min(100, r.ctr * 10);

      return `
        <tr>
          <td class="an-rank">${String(i + 1).padStart(2, '0')}</td>
          <td>
            <div class="an-name">${r.name}</div>
            <div><span class="an-type" style="background:${tint};color:${color};">${r.mod.type.toUpperCase()}</span></div>
          </td>
          <td class="an-num">
            <div class="an-num__big">${r.impressions.toLocaleString()}</div>
            <div class="an-num__sub">${(r.selectionRate * 100).toFixed(1)}% selection</div>
          </td>
          <td class="an-num">
            <div class="an-num__big">${r.ctr.toFixed(2)}%<span class="an-pct-bar"><span class="an-pct-bar__fill" style="width:${ctrBarPct.toFixed(0)}%;background:${color};"></span></span></div>
            <div class="an-num__sub">${r.clicks.toLocaleString()} clicks</div>
          </td>
          <td class="an-num">
            <div class="an-num__big">${r.atbAttrib.toLocaleString()}</div>
            <div class="an-num__sub">${r.atbRate.toFixed(2)}% rate</div>
          </td>
          <td class="an-num">
            <div class="an-num__big">${r.resolution.toFixed(2)}</div>
            <div class="an-num__sub">per impression</div>
          </td>
          <td><span class="an-delta ${deltaCls}">${deltaArrow} ${Math.abs(delta).toFixed(1)}%</span></td>
          <td><div class="an-slots">${slotBars}</div></td>
          <td>${spark(r.spark, color)}</td>
          <td><div class="an-problems">${topProblems}</div></td>
        </tr>`;
    }).join('');

    const html = `
      <div class="an-shell">
        ${pagePickerBar(pageId)}
        <header class="an-header">
          <div>
            <h1 class="an-title">Widget Analytics · ${meta.label}</h1>
            <p class="an-sub">30-day performance of all ${Object.keys(modules).length} widgets registered on the <b>${meta.label}</b> page (${meta.slots} slots, ~${(PAGE_VOLUME[pageId]||0).toLocaleString()} sessions/day). Currently <b>${versionLabel}</b>. Switch page above to inspect another surface; toggle version to compare.</p>
          </div>
        </header>

        ${kpis}
        ${filters}

        <table class="an-tbl">
          <thead>
            <tr>
              <th></th>
              <th>Widget</th>
              <th class="an-num ${sortClass('impressions')}" data-an-sort="impressions">Impressions${sortArrow('impressions')}</th>
              <th class="an-num ${sortClass('ctr')}" data-an-sort="ctr">CTR${sortArrow('ctr')}</th>
              <th class="an-num ${sortClass('atbAttrib')}" data-an-sort="atbAttrib">Attributed ATB${sortArrow('atbAttrib')}</th>
              <th class="an-num ${sortClass('resolution')}" data-an-sort="resolution">Coverage Δ${sortArrow('resolution')}</th>
              <th>vs ${otherVersionLabel}</th>
              <th>Slot Dist</th>
              <th>30-Day Trend</th>
              <th>Solves</th>
            </tr>
          </thead>
          <tbody>${tableRows}</tbody>
        </table>
      </div>`;

    const cont = document.getElementById('analytics-cont');
    cont.innerHTML = html;

    // Wire interactions
    wirePagePicker(cont, (id) => { analyticsPage = id; renderAnalyticsPaged(); });
    cont.querySelectorAll('[data-an-filter]').forEach(b => {
      b.addEventListener('click', () => { anFilterType = b.dataset.anFilter; renderAnalyticsPaged(); });
    });
    cont.querySelectorAll('[data-an-version]').forEach(b => {
      b.addEventListener('click', () => {
        window.useV3 = b.dataset.anVersion === 'v3';
        // Mirror to the orchestrator's badge if the toggleVersion mechanism is around.
        const evolveLabel = document.getElementById('evolve-label');
        const label = document.getElementById('version-label');
        const badge = document.getElementById('version-badge');
        const btn = document.getElementById('btn-evolve');
        if (label && badge && btn && evolveLabel) {
          if (window.useV3) {
            label.textContent = 'v3 evolved'; label.className = 'text-amber-300 font-bold';
            badge.className = 'px-2 py-1 rounded border border-amber-500/40 bg-amber-500/10 text-amber-400 uppercase tracking-widest';
            evolveLabel.textContent = '◂ Revert to v1';
            btn.classList.add('bg-amber-500/25','border-amber-500/70','v3-only-pulse');
            btn.classList.remove('bg-amber-500/10','border-amber-500/40');
          } else {
            label.textContent = 'v1 baseline'; label.className = 'text-slate-200 font-bold';
            badge.className = 'px-2 py-1 rounded border border-slate-700 text-slate-500 uppercase tracking-widest';
            evolveLabel.textContent = '▸ Apply v3';
            btn.classList.remove('bg-amber-500/25','border-amber-500/70','v3-only-pulse');
            btn.classList.add('bg-amber-500/10','border-amber-500/40');
          }
        }
        if (typeof window.update === 'function') window.update();
        renderAnalyticsPaged();
      });
    });
    cont.querySelectorAll('[data-an-sort]').forEach(th => {
      th.addEventListener('click', () => {
        const key = th.dataset.anSort;
        if (anSortKey === key) anSortDir = -anSortDir;
        else { anSortKey = key; anSortDir = -1; }
        renderAnalyticsPaged();
      });
    });
  }

  window.renderAnalytics = renderAnalyticsPaged;

  // Make setPage also sync analytics page.
  const _origSetPage2 = window.setPage;
  window.setPage = function (id) {
    analyticsPage = id;
    if (_origSetPage2) _origSetPage2(id);
    const av = document.getElementById('view-analytics');
    if (av && !av.classList.contains('hidden')) renderAnalyticsPaged();
  };

  // Default analyticsPage to whatever live-page picker is on.
  if (window.getCurrentPage) analyticsPage = window.getCurrentPage();

  // ──────────────────────────────────────────────────────────────────────────
  // 7) Page-aware Policy Simulator.
  // ──────────────────────────────────────────────────────────────────────────

  // Helper: state init for a given page (problems, remaining, coverage).
  function policyInitState(feat, pageId) {
    if (pageId === 'pdp') {
      const probs = window.scoreProblems(feat);
      return {
        problems: probs,
        remaining: { ...probs },
        coverage: Object.fromEntries(window.PROBLEMS.map(p => [p, 0])),
      };
    }
    // Use composePage's internal problem scoring for non-PDP pages.
    const result = window.composePage(pageId, feat);
    return {
      problems: result.problems,
      remaining: { ...result.problems },
      coverage: Object.fromEntries(Object.keys(result.problems).map(p => [p, 0])),
    };
  }

  function policyApplyAddr(mod, remaining, coverage) {
    for (const p in (mod.addr || {})) {
      if (remaining[p] == null) continue;
      remaining[p] = Math.max(0, remaining[p] - mod.addr[p]);
      coverage[p] = Math.min(1, (coverage[p] || 0) + mod.addr[p]);
    }
  }

  // The 5 baseline policies, made page-aware.
  function policyGreedy(feat, modules, slots, pageId) {
    if (pageId === 'pdp') return window.compose(feat, modules, slots);
    return window.composePage(pageId, feat);
  }
  function policyRandom(feat, modules, slots, pageId) {
    const s = policyInitState(feat, pageId);
    const names = Object.keys(modules).sort(() => Math.random() - 0.5).slice(0, slots);
    const page = names.map((name, slot) => {
      const mod = modules[name];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      policyApplyAddr(mod, s.remaining, s.coverage);
      return { slot, name, score, scores: {} };
    });
    return { page, ...s };
  }
  function policyBaseOnly(feat, modules, slots, pageId) {
    const s = policyInitState(feat, pageId);
    const names = Object.keys(modules)
      .sort((a, b) => modules[b].base - modules[a].base)
      .slice(0, slots);
    const page = names.map((name, slot) => {
      const mod = modules[name];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      policyApplyAddr(mod, s.remaining, s.coverage);
      return { slot, name, score, scores: {} };
    });
    return { page, ...s };
  }
  function policyEpsilon(feat, modules, slots, pageId, epsilon) {
    const s = policyInitState(feat, pageId);
    const page = [];
    const used = new Set();
    const keys = Object.keys(modules);
    for (let slot = 0; slot < Math.min(slots, keys.length); slot++) {
      const avail = keys.filter(n => !used.has(n));
      let pick;
      if (Math.random() < epsilon) {
        pick = avail[Math.floor(Math.random() * avail.length)];
      } else {
        let bestName = avail[0], bestScore = -Infinity;
        avail.forEach(n => {
          const sc = window.scoreModule(modules[n], s.remaining, s.coverage, slot);
          if (sc > bestScore) { bestScore = sc; bestName = n; }
        });
        pick = bestName;
      }
      const mod = modules[pick];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      page.push({ slot, name: pick, score, scores: {} });
      used.add(pick);
      policyApplyAddr(mod, s.remaining, s.coverage);
    }
    return { page, ...s };
  }
  function policyThompson(feat, modules, slots, pageId) {
    const s = policyInitState(feat, pageId);
    const page = [];
    const used = new Set();
    const keys = Object.keys(modules);
    for (let slot = 0; slot < Math.min(slots, keys.length); slot++) {
      let bestName = null, bestScore = -Infinity;
      keys.filter(n => !used.has(n)).forEach(n => {
        const mod = modules[n];
        const baseScore = window.scoreModule(mod, s.remaining, s.coverage, slot);
        const addrSum = Object.values(mod.addr || {}).reduce((a, b) => a + b, 0);
        const uncertainty = 1 / (1 + addrSum * 4);
        const noise = (Math.random() - 0.5) * uncertainty * 2.2;
        const sc = baseScore + noise;
        if (sc > bestScore) { bestScore = sc; bestName = n; }
      });
      const mod = modules[bestName];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      page.push({ slot, name: bestName, score, scores: {} });
      used.add(bestName);
      policyApplyAddr(mod, s.remaining, s.coverage);
    }
    return { page, ...s };
  }

  function policiesForPage(pageId) {
    const modulesV1 = pageId === 'pdp' ? window.modulesV1 : window.PAGE_MODULES[pageId];
    const modulesV3 = pageId === 'pdp' ? window.modulesV3 : (window.PAGE_MODULES_V3[pageId] || window.PAGE_MODULES[pageId]);
    const slots = window.PAGE_META[pageId].slots;
    return {
      v1_greedy: { id: 'v1_greedy', name: 'v1 · Greedy', short: 'v1', color: '#94a3b8',
        desc: 'Baseline greedy submodular composition on the v1 module config.',
        modules: () => modulesV1,
        select: (feat) => {
          // Force v1 composer
          const prev = window.useV3; window.useV3 = false;
          const out = policyGreedy(feat, modulesV1, slots, pageId);
          window.useV3 = prev;
          return out;
        },
      },
      v3_greedy: { id: 'v3_greedy', name: 'v3 · Evolved', short: 'v3', color: '#fbbf24',
        desc: 'Greedy on the v3 config (new on_cov synergies + base adjustments).',
        modules: () => modulesV3,
        select: (feat) => {
          const prev = window.useV3; window.useV3 = true;
          const out = policyGreedy(feat, modulesV3, slots, pageId);
          window.useV3 = prev;
          return out;
        },
      },
      random: { id: 'random', name: 'Random', short: 'rand', color: '#fb7185',
        desc: 'Shuffle the registry and take the first ' + slots + '. Lower bound — no learning.',
        modules: () => modulesV3,
        select: (feat) => policyRandom(feat, modulesV3, slots, pageId),
      },
      base_only: { id: 'base_only', name: 'Top-by-base', short: 'base', color: '#a78bfa',
        desc: 'Rank by static base score alone — ignores session signals entirely. The "popular widgets" trap.',
        modules: () => modulesV3,
        select: (feat) => policyBaseOnly(feat, modulesV3, slots, pageId),
      },
      epsilon_greedy: { id: 'epsilon_greedy', name: 'ε-greedy bandit', short: 'ε-grd', color: '#34d399',
        desc: 'Greedy with 15% per-slot random exploration. Trades short-term score for learning surface.',
        modules: () => modulesV3,
        select: (feat) => policyEpsilon(feat, modulesV3, slots, pageId, 0.15),
      },
      thompson: { id: 'thompson', name: 'Thompson sampling', short: 'thomp', color: '#60a5fa',
        desc: 'Sample widget rewards from posterior — explores well-supported widgets less, novel ones more.',
        modules: () => modulesV3,
        select: (feat) => policyThompson(feat, modulesV3, slots, pageId),
      },
    };
  }

  function policySimulate(pageId, n) {
    const policies = policiesForPage(pageId);
    const personaKeys = Object.keys(window.PERSONAS);
    const SIGNALS = window.SIGNALS;
    const meta = window.PAGE_META[pageId];

    const TYPE_CTR = {
      outfit: 6.8, decision: 5.4, compare: 4.6, premium: 4.1,
      returns: 3.8, size: 3.2, price: 2.9, default: 2.3,
      hero: 5.2, continuity: 7.4, guidance: 6.1, editorial: 5.8,
      feed: 4.4, personal: 6.0, query: 5.5, filter: 7.8, results: 4.1,
      core: 2.0, incentive: 5.7, upsell: 6.3, trust: 3.6, speed: 8.5,
      engagement: 4.8,
    };

    const out = {};
    for (const pid in policies) {
      out[pid] = {
        coverageSum: 0, residualSum: 0, problemSum: 0,
        clicksProj: 0, atbProj: 0, widgetCounts: {}, slotScoreSum: 0, trials: 0,
      };
    }

    for (let t = 0; t < n; t++) {
      const persona = personaKeys[t % personaKeys.length];
      const feat = {};
      SIGNALS.forEach(s => {
        feat[s.id] = window.PERSONAS[persona].vals[s.id] ?? s.default;
        feat[s.id] = Math.max(0, Math.min(1, feat[s.id] + (Math.random() - 0.5) * 0.05));
      });
      for (const pid in policies) {
        const result = policies[pid].select(feat);
        const modules = policies[pid].modules();
        const r = out[pid];
        const totalCov = Object.values(result.coverage).reduce((a, b) => a + b, 0);
        const totalRem = Object.values(result.remaining).reduce((a, b) => a + b, 0);
        const totalProb = Object.values(result.problems).reduce((a, b) => a + b, 0);
        r.coverageSum += totalCov;
        r.residualSum += totalRem;
        r.problemSum  += totalProb;
        let clicks = 0, atb = 0, scoreSum = 0;
        result.page.forEach(entry => {
          const mod = modules[entry.name];
          if (!mod) return;
          const ctr = TYPE_CTR[mod.type] || 3;
          clicks += ctr / 100;
          atb += ctr / 100 * 0.18;
          scoreSum += entry.score;
          r.widgetCounts[entry.name] = (r.widgetCounts[entry.name] || 0) + 1;
        });
        r.clicksProj += clicks;
        r.atbProj += atb;
        r.slotScoreSum += scoreSum;
        r.trials += 1;
      }
    }

    const final = {};
    const totalWidgets = Object.keys(policies.v3_greedy.modules()).length;
    for (const pid in out) {
      const r = out[pid];
      const trials = r.trials;
      const coverageRate = r.problemSum > 0 ? (r.coverageSum / r.problemSum) : 0;
      const widgetNames = Object.keys(r.widgetCounts);
      const totalPicks = widgetNames.reduce((a, k) => a + r.widgetCounts[k], 0);
      let entropy = 0;
      widgetNames.forEach(k => {
        const p = r.widgetCounts[k] / totalPicks;
        if (p > 0) entropy -= p * Math.log2(p);
      });
      const diversity = totalWidgets > 1 ? entropy / Math.log2(totalWidgets) : 0;
      final[pid] = {
        ...policies[pid],
        trials,
        avgCoverage: r.coverageSum / trials,
        avgResidual: r.residualSum / trials,
        coverageRate,
        avgClicks: r.clicksProj / trials,
        avgAtb: r.atbProj / trials,
        avgScore: r.slotScoreSum / trials,
        diversity,
        widgetCounts: r.widgetCounts,
        widgetVariety: widgetNames.length,
        totalWidgets,
      };
    }
    return final;
  }

  // Override the orchestrator's simulatePolicies — same signature, but
  // routes through the current policiesPage state.
  let policiesPage = 'pdp';
  if (window.getCurrentPage) policiesPage = window.getCurrentPage();
  let plLastResultsPage = null;
  let plLastResults = null;
  let plRunning = false;
  let plTrialCount = 240;

  window.simulatePolicies = function (n) {
    return policySimulate(policiesPage, n || 240);
  };

  // Override plRun so we control the cache invalidation per page.
  window.plRun = function () {
    plRunning = true;
    renderPoliciesPaged();
    setTimeout(() => {
      plLastResults = policySimulate(policiesPage, plTrialCount);
      plLastResultsPage = policiesPage;
      plRunning = false;
      renderPoliciesPaged();
    }, 30);
  };

  function renderPoliciesPaged() {
    const cont = document.getElementById('policies-cont');
    if (!cont) return;
    if (!window.POLICIES) {
      cont.innerHTML = '<div style="padding:40px;color:#fb7185;">policies.js failed to load</div>';
      return;
    }

    const meta = window.PAGE_META[policiesPage];

    // Auto-run if no results or stale (different page).
    if (!plRunning && (!plLastResults || plLastResultsPage !== policiesPage)) {
      return window.plRun();
    }

    const results = plLastResults;

    let html = '<div class="pl-shell">' + pagePickerBar(policiesPage);
    html += `
      <header class="pl-header">
        <div>
          <h1 class="pl-title">Policy Simulator · ${meta.label}</h1>
          <p class="pl-sub">Compare widget-selection strategies head-to-head on the <b>${meta.label}</b> page (${meta.slots} slots, ${Object.keys(policiesForPage(policiesPage).v3_greedy.modules()).length} widgets). Each policy sees the same trials (sampled across 8 personas with signal jitter). Best per metric is highlighted.</p>
        </div>
        <div style="display:flex;align-items:center;gap:10px;">
          <span class="pl-trials">TRIALS<input type="number" min="50" max="2000" step="50" value="${plTrialCount}" id="pl-trials-input"/></span>
          <button class="pl-run" id="pl-run-btn" ${plRunning ? 'disabled style="opacity:0.5;cursor:wait;"' : ''}>
            ${plRunning ? '<span>RUNNING…</span>' : '<span>▸ RUN SIMULATION</span>'}
          </button>
        </div>
      </header>`;

    if (!results) {
      html += '<div style="padding:60px;text-align:center;color:#64748b;font-family:monospace;">No results yet.</div></div>';
      cont.innerHTML = html;
      wirePagePicker(cont, (id) => { policiesPage = id; renderPoliciesPaged(); });
      return;
    }

    const bestOf = (key) => {
      let best = null, bestVal = -Infinity;
      for (const pid in results) {
        const v = results[pid][key];
        if (v > bestVal) { bestVal = v; best = pid; }
      }
      return best;
    };
    const bestKeys = {
      coverageRate: bestOf('coverageRate'),
      avgClicks: bestOf('avgClicks'),
      avgAtb: bestOf('avgAtb'),
      diversity: bestOf('diversity'),
    };

    html += '<div class="pl-grid">';
    Object.values(results).forEach(r => {
      const widgets = Object.entries(r.widgetCounts).sort((a, b) => b[1] - a[1]).slice(0, 4);
      html += `
        <div class="pl-card" style="--pl-color:${r.color};">
          <div class="pl-card__head">
            <span class="pl-card__name">${r.name}</span>
            <span class="pl-card__short">${r.short}</span>
          </div>
          <p class="pl-card__desc">${r.desc}</p>
          <div class="pl-card__metrics">
            <div class="pl-metric" style="${bestKeys.coverageRate === r.id ? 'box-shadow:inset 0 0 0 1px #34d399;' : ''}">
              <span class="pl-metric__lab">COVERAGE</span>
              <span class="pl-metric__val" style="color:${bestKeys.coverageRate === r.id ? '#34d399' : '#f1f5f9'};">${(r.coverageRate * 100).toFixed(1)}%</span>
              <div class="pl-bar"><div class="pl-bar__fill" style="width:${(r.coverageRate * 100).toFixed(0)}%;background:${r.color};"></div></div>
            </div>
            <div class="pl-metric" style="${bestKeys.avgClicks === r.id ? 'box-shadow:inset 0 0 0 1px #34d399;' : ''}">
              <span class="pl-metric__lab">CLICKS / SESSION</span>
              <span class="pl-metric__val" style="color:${bestKeys.avgClicks === r.id ? '#34d399' : '#f1f5f9'};">${r.avgClicks.toFixed(2)}</span>
            </div>
            <div class="pl-metric" style="${bestKeys.avgAtb === r.id ? 'box-shadow:inset 0 0 0 1px #34d399;' : ''}">
              <span class="pl-metric__lab">ATB / SESSION</span>
              <span class="pl-metric__val" style="color:${bestKeys.avgAtb === r.id ? '#34d399' : '#f1f5f9'};">${r.avgAtb.toFixed(3)}</span>
            </div>
            <div class="pl-metric" style="${bestKeys.diversity === r.id ? 'box-shadow:inset 0 0 0 1px #34d399;' : ''}">
              <span class="pl-metric__lab">DIVERSITY</span>
              <span class="pl-metric__val" style="color:${bestKeys.diversity === r.id ? '#34d399' : '#f1f5f9'};">${(r.diversity * 100).toFixed(0)}%</span>
              <div class="pl-bar"><div class="pl-bar__fill" style="width:${(r.diversity * 100).toFixed(0)}%;background:${r.color};"></div></div>
            </div>
          </div>
          <div class="pl-rankings">
            <span class="pl-rankings__lab">TOP WIDGETS · ${r.widgetVariety} UNIQUE</span>
            ${widgets.map(([name, cnt], i) => `
              <div class="pl-rank-row">
                <span class="pl-rank-row__num">${i + 1}</span>
                <span class="pl-rank-row__name">${name}</span>
                <span class="pl-rank-row__count">${cnt}</span>
              </div>`).join('')}
          </div>
        </div>`;
    });
    html += '</div>';

    html += `
      <table class="an-tbl" style="margin-top:6px;">
        <thead>
          <tr>
            <th>Policy</th>
            <th class="an-num">Trials</th>
            <th class="an-num">Avg coverage</th>
            <th class="an-num">Avg residual</th>
            <th class="an-num">Coverage rate</th>
            <th class="an-num">Avg score Σ</th>
            <th class="an-num">Clicks/sess</th>
            <th class="an-num">ATB/sess</th>
            <th class="an-num">Diversity</th>
            <th class="an-num">Widget mix</th>
          </tr>
        </thead>
        <tbody>
          ${Object.values(results)
            .sort((a, b) => b.coverageRate - a.coverageRate)
            .map((r) => `
              <tr class="${bestKeys.coverageRate === r.id ? 'pl-best' : ''}">
                <td><span style="font-family:'IBM Plex Mono',monospace;font-size:13px;font-weight:600;color:${r.color};">${r.name}</span></td>
                <td class="an-num">${r.trials}</td>
                <td class="an-num">${r.avgCoverage.toFixed(2)}</td>
                <td class="an-num">${r.avgResidual.toFixed(2)}</td>
                <td class="an-num">${(r.coverageRate * 100).toFixed(1)}%</td>
                <td class="an-num">${r.avgScore.toFixed(2)}</td>
                <td class="an-num">${r.avgClicks.toFixed(3)}</td>
                <td class="an-num">${r.avgAtb.toFixed(3)}</td>
                <td class="an-num">${(r.diversity * 100).toFixed(0)}%</td>
                <td class="an-num">${r.widgetVariety} / ${r.totalWidgets}</td>
              </tr>
            `).join('')}
        </tbody>
      </table>
    </div>`;

    cont.innerHTML = html;
    wirePagePicker(cont, (id) => { policiesPage = id; renderPoliciesPaged(); });
    // Re-wire run button + trials input (had bare-name onclick in orig)
    const btn = cont.querySelector('#pl-run-btn');
    if (btn) btn.addEventListener('click', () => window.plRun());
    const input = cont.querySelector('#pl-trials-input');
    if (input) input.addEventListener('input', () => {
      plTrialCount = Math.max(50, Math.min(2000, parseInt(input.value) || 50));
    });
  }

  window.renderPolicies = renderPoliciesPaged;

  // Chain setPage so policies also tracks active page.
  const _origSetPage3 = window.setPage;
  window.setPage = function (id) {
    policiesPage = id;
    if (_origSetPage3) _origSetPage3(id);
    const pv = document.getElementById('view-policies');
    if (pv && !pv.classList.contains('hidden')) renderPoliciesPaged();
  };

})();
