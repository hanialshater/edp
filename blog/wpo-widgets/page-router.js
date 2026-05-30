// =============================================================================
// PAGE ROUTING — patches the live-page view to switch among 7 page types.
//
// Strategy:
//   • Read existing renderLivePage / buildPageHtml / autoScalePhones / setViewport
//     from window (declared in the orchestrator HTML as global function decls).
//   • Replace renderLivePage with a version that dispatches by current pageId,
//     building chrome via PageShells[id](ctx) and slots via the right module
//     registry + the right renderer pool.
//   • Build the page-type sub-tab bar.
//
// Persona / signal state is OWNED by the orchestrator and shared — switching
// pages does not reset signals, so the same shopper "walks" across pages.
// =============================================================================

(function () {
  const PAGES = window.PAGES;
  const PAGE_META = window.PAGE_META;

  // ── state ────────────────────────────────────────────────────────────────
  let pageId = 'pdp';
  window.getCurrentPage = () => pageId;

  // ── build the sub-tab bar (page picker) ──────────────────────────────────
  function buildPageBar() {
    const bar = document.getElementById('page-typebar');
    if (!bar) return;
    const items = PAGES.map(id => {
      const m = PAGE_META[id];
      const on = id === pageId;
      return `
        <button class="lp-pagebar__btn ${on ? 'lp-pagebar__btn--on' : ''}" data-page="${id}">
          ${m.label}
          <span class="lp-pagebar__btn__slug">${m.slug}</span>
        </button>`;
    }).join('');
    bar.innerHTML = `<span class="lp-pagebar__lab">PAGE TYPE</span>${items}`;
    bar.querySelectorAll('[data-page]').forEach(btn => {
      btn.addEventListener('click', () => setPage(btn.dataset.page));
    });
  }

  function setPage(id) {
    if (!PAGE_META[id]) return;
    pageId = id;
    buildPageBar();
    window.renderLivePage();
  }
  window.setPage = setPage;

  // ── pick the active persona label from the orchestrator buttons ──────────
  function activePersonaLabel() {
    let label = null;
    document.querySelectorAll('#presets button').forEach(b => {
      if (b.classList.contains('ring-1')) label = b.textContent.trim();
    });
    return label;
  }

  // ── build a page (chrome + slots) for a given pageId / compose-result ────
  function buildPage(id, result, ctx) {
    const meta = PAGE_META[id];
    const shell = window.PageShells[id];

    // For PDP, prefer the original chrome (pdpShell) — produces same look as
    // the v1 buildPageHtml. Other pages use their own shells.
    const shellHtml = shell({
      meta,
      problems: result.problems,
      useV3: window.useV3,
      persona: ctx.persona,
      slotCount: meta.slots,
    });

    // Build slot HTML.
    const modules = result.modules;
    const renderers = (id === 'pdp')
      ? window.WidgetRenderers
      : (window.PageWidgets[id] || {});

    const slotsHtml = result.page.map((entry, i) => {
      const mod = modules[entry.name];
      const renderer = renderers[entry.name];
      let widgetHtml = renderer
        ? renderer({ entry, mod, slotIdx: i, problems: result.problems, coverage: result.coverage })
        : `<div class="lp-card"><div class="lp-card__head"><h3 class="lp-card__title">${entry.name}</h3></div><p class="lp-p" style="color:#9a9a9a;font-style:italic;">(no renderer for ${id}.${entry.name})</p></div>`;
      widgetHtml = window.pCodes ? window.pCodes(widgetHtml) : widgetHtml;
      const accentMap = {
        cyan: '#7eb5bf', amber: '#d4a851', emerald: '#5fa080',
        fuchsia: '#c068ad', orange: '#d9824a', rose: '#d96678',
        indigo: '#7e87c4', slate: '#9aa0ad', sky: '#7cb1d4',
        teal: '#5fa090', blue: '#7e87c4',
      };
      const accent = accentMap[mod.color] || '#9aa0ad';
      return `
        <div class="lp-slot" style="animation-delay:${i * 50}ms">
          <span class="lp-slot__chip">SLOT ${i + 1} · <b>Σ ${entry.score.toFixed(2)}</b></span>
          ${widgetHtml.replace('<div class="lp-card"', `<div class="lp-card" style="border-left-color:${accent};animation-delay:${i * 50}ms"`)}
        </div>`;
    }).join('');

    return shellHtml.replace('{{SLOTS}}', `<div class="lp-slots">${slotsHtml}</div>`);
  }

  // ── replace renderLivePage with page-aware version ───────────────────────
  const _origAutoScale = window.autoScalePhones;

  window.renderLivePage = function (precomputed) {
    const cont = document.getElementById('page-cont');
    if (!cont) return;

    // Compose for current page. precomputed only applies to PDP; ignore for others
    // so cross-page calls still work.
    const persona = activePersonaLabel();

    if (window.viewportMode === 'desktop') {
      const result = window.composePage(pageId, window.featState || {});
      cont.className = '';
      cont.innerHTML = `<div class="lp-shell">${buildPage(pageId, result, { persona })}</div>`;
      return;
    }

    if (window.viewportMode === 'mobile') {
      const result = window.composePage(pageId, window.featState || {});
      cont.className = '';
      cont.innerHTML = `
        <div class="lp-mobile-stage">
          <div class="lp-phone-col">
            <div class="lp-phone-cap">${PAGE_META[pageId].label} · ${window.useV3 ? 'v3' : 'v1'}</div>
            <div class="lp-phone">
              <div class="lp-phone__notch"><span class="lp-phone__status">9:41</span><span class="lp-phone__status">●●● ⚡ 100%</span></div>
              <div class="lp-shell">${buildPage(pageId, result, { persona })}</div>
            </div>
          </div>
        </div>`;
      requestAnimationFrame(_origAutoScale);
      return;
    }

    // compare: v1 vs v3 — only PDP has v3 edits; for other pages render same
    // composition twice with labels (so the side-by-side comparison still
    // tells a coherent story).
    if (window.viewportMode === 'compare') {
      // Force v1/v3 by toggling window.useV3 around compose; safer: directly call
      // composePage twice with explicit useV3 override.
      const prev = window.useV3;
      window.useV3 = false;
      const resV1 = window.composePage(pageId, window.featState || {});
      window.useV3 = true;
      const resV3 = window.composePage(pageId, window.featState || {});
      window.useV3 = prev;

      cont.className = '';
      cont.innerHTML = `
        <div class="lp-mobile-stage lp-mobile-stage--multi">
          <div class="lp-phone-col">
            <div class="lp-phone-cap">${PAGE_META[pageId].label} · v1</div>
            <div class="lp-phone">
              <div class="lp-phone__notch"><span class="lp-phone__status">9:41</span><span class="lp-phone__status">●●● ⚡ 100%</span></div>
              <div class="lp-shell">${(() => { window.useV3 = false; const h = buildPage(pageId, resV1, { persona }); window.useV3 = prev; return h; })()}</div>
            </div>
          </div>
          <div class="lp-phone-col">
            <div class="lp-phone-cap">${PAGE_META[pageId].label} · v3</div>
            <div class="lp-phone">
              <div class="lp-phone__notch"><span class="lp-phone__status">9:41</span><span class="lp-phone__status">●●● ⚡ 100%</span></div>
              <div class="lp-shell">${(() => { window.useV3 = true; const h = buildPage(pageId, resV3, { persona }); window.useV3 = prev; return h; })()}</div>
            </div>
          </div>
        </div>`;
      requestAnimationFrame(_origAutoScale);
    }
  };

  // ── extend PROBLEM_DESC with new journey codes so hover tooltips work
  //    on every page (the orchestrator HTML only defines F32–F51 by default)
  // ────────────────────────────────────────────────────────────────────────
  const EXTRA_DESCS = {
    F11: { name: 'Category Overwhelm',     summary: '12,000 items in one category and no obvious entry point. Common on first visits and broad searches.',                  signals: 'new customer · long scroll without filter · short session' },
    F12: { name: 'Inspiration Gap',        summary: "Browsing without a target. Doesn't know what's in style this season.",                                                  signals: 'editorial visits · style stretch · seasonal search' },
    F13: { name: 'Need Translation',       summary: 'Natural-language query that does not map cleanly to a category.',                                                       signals: 'broad search · zero-result queries · category bouncing' },
    F21: { name: 'Option Set Stagnation',  summary: 'Repeat visits showing the exact same items. Boredom from the algorithm.',                                               signals: 'multi-session same-item exposure · low CTR on repeat impressions' },
    F22: { name: 'Filter Friction',        summary: 'Heavy filter use, refining and resetting — they cannot get to the right results.',                                      signals: 'filter toggles · filter resets · empty result counts' },
    F23: { name: 'Discovery Boredom',      summary: '"Nothing surprises me." Low scroll velocity, short dwell, early exit.',                                                 signals: 'low scroll velocity · short dwell · early exit' },
    F31: { name: 'Detail Anxiety',         summary: 'Needs to see the item from every angle before they trust it.',                                                          signals: 'image zoom · gallery cycles · video play' },
    F35: { name: 'PDP Stagnation',         summary: 'Returning to the same PDP and seeing the same modules.',                                                                signals: 'repeat PDP visit · same module exposure' },
    F52: { name: 'Checkout Doubt',         summary: '"Wait, is this site legit? Is my card safe?" Common on first-time mobile checkouts.',                                   signals: 'guest checkout · trust badge dwell · abandon at payment' },
    F53: { name: 'Price Anchoring Block',  summary: '"I saw this for less last week. I will wait for a sale."',                                                              signals: 'price history view · long wishlist tenure · sale-page visits' },
    F61: { name: 'Styling Orphan',         summary: 'Bought a bold piece and now does not know what to wear with it.',                                                       signals: 'low repeat-wear · post-purchase email open' },
    F62: { name: 'Care Knowledge Gap',     summary: '"How do I wash this without ruining it?"',                                                                              signals: 'care-instructions search · review mentions of damage' },
    F63: { name: 'Wardrobe Drift',         summary: '"My style has changed. Why are you still showing me the old me?"',                                                      signals: 'category mix shift · returned items pattern · new search vocab' },
    F64: { name: 'Repeat Trigger',         summary: '"I love it — want another in a different colour."',                                                                     signals: 'past-purchase reorder · color variant views · brand loyalty' },
  };
  if (typeof PROBLEM_DESC !== 'undefined') {
    for (const k in EXTRA_DESCS) {
      if (!PROBLEM_DESC[k]) PROBLEM_DESC[k] = EXTRA_DESCS[k];
    }
  }

  // ── init on DOM ready ────────────────────────────────────────────────────
  function init() {
    buildPageBar();
    // Force a re-render if the live-page view is already visible.
    const view = document.getElementById('view-page');
    if (view && !view.classList.contains('hidden')) window.renderLivePage();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
