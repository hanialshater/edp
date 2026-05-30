// =============================================================================
// PAGE SHELLS — chrome (nav, hero, two-column layouts) for each page type.
//
// Each shell function returns the HTML that WRAPS the orchestrator slots.
// Slots are injected at the {{SLOTS}} placeholder by the live-page renderer.
// =============================================================================

(function () {

  // ── Shared chrome: top nav and footer rule ────────────────────────────────
  const navBar = (active) => {
    const items = [
      { id: 'home',          label: 'BOSS' /*brand*/, brand: true },
      { id: 'plp',           label: 'Men' },
      { id: 'plp',           label: 'Women' },
      { id: 'plp',           label: 'Tailoring' },
      { id: 'plp',           label: 'Shoes' },
      { id: 'plp',           label: 'Accessories' },
      { id: 'editorial',     label: 'Stories' },
      { id: 'sale',          label: 'Sale', alert: true },
    ];
    return `
      <nav class="lp-nav">
        <div class="lp-nav__brand">BOSS</div>
        <ul class="lp-nav__items">
          ${items.slice(1).map(it => `
            <li class="lp-nav__item ${it.alert ? 'lp-nav__item--alert' : ''}">${it.label}</li>
          `).join('')}
        </ul>
        <div class="lp-nav__icons">
          <button class="lp-nav__icon" title="Search">⌕</button>
          <button class="lp-nav__icon" title="Account">◑</button>
          <button class="lp-nav__icon" title="Wishlist">♡</button>
          <button class="lp-nav__icon lp-nav__icon--bag" title="Bag">⌂ <span>2</span></button>
        </div>
      </nav>`;
  };

  // ── Composition banner (kept on every page — shows the orchestrator state)─
  function compBanner(meta, problemScores, useV3, activePersona, slotCount) {
    const top = Object.entries(problemScores)
      .sort((a, b) => b[1] - a[1]).slice(0, 3)
      .map(([id, val]) => `<span data-problem="${id}">${id}</span> <b>${val.toFixed(2)}</b>`)
      .join(' · ');
    return `
      <div class="lp-comp">
        <span class="lp-comp__pill lp-comp__pill--page">PAGE: <b>${meta.label.toUpperCase()}</b></span>
        <span class="lp-comp__pill">PERSONA: <b>${activePersona || 'custom'}</b></span>
        <span class="lp-comp__pill">VERSION: <b>${useV3 ? 'v3 evolved' : 'v1 baseline'}</b></span>
        <span class="lp-comp__pill">TOP: ${top || '—'}</span>
        <span class="lp-comp__rule"></span>
        <span class="lp-comp__pill">${slotCount} SLOTS</span>
      </div>`;
  }

  // ──────────────────────────── HOME shell ──────────────────────────────────
  function homeShell(ctx) {
    return `
      ${navBar('home')}
      <section class="lp-home-hero">
        <div class="lp-home-hero__eyebrow">A/W · TAILORING SEASON</div>
        <h1 class="lp-home-hero__title">The Tuxedo,<br/>Reconsidered.</h1>
        <p class="lp-home-hero__sub">Three cuts. One occasion. Built in Italy from Vitale Barberis wool.</p>
        <div class="lp-home-hero__ctas">
          <button class="lp-btn-primary">Shop tailoring</button>
          <button class="lp-btn-ghost">Read the story</button>
        </div>
        <div class="lp-home-hero__art">
          ${window.WidgetSVG.mannequin()}
        </div>
      </section>
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ──────────────────────────── SEARCH shell ────────────────────────────────
  function searchShell(ctx) {
    return `
      ${navBar('search')}
      <section class="lp-search-bar">
        <div class="lp-search-bar__field">
          <span class="lp-search-bar__icon">⌕</span>
          <span class="lp-search-bar__query">black tie tuxedo</span>
          <button class="lp-search-bar__clear">✕</button>
        </div>
        <div class="lp-search-bar__meta">
          <span><b>1,284</b> results</span>
          <span class="lp-search-bar__sep">·</span>
          <span>Sort: <b>Best match</b></span>
        </div>
      </section>
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ──────────────────────────── PLP shell ───────────────────────────────────
  function plpShell(ctx) {
    return `
      ${navBar('plp')}
      <div class="lp-crumbs">
        Home <span>›</span> Men <span>›</span> Suits &amp; Tailoring <span>›</span> <b>Tuxedos</b>
      </div>
      <section class="lp-plp-hero">
        <div class="lp-plp-hero__copy">
          <div class="lp-plp-hero__eyebrow">CATEGORY · 142 ITEMS</div>
          <h1 class="lp-plp-hero__title">Tuxedos</h1>
          <p class="lp-plp-hero__sub">Slim, classic and double-breasted cuts. Half-canvas to full-canvas construction.</p>
        </div>
        <div class="lp-plp-hero__chips">
          <span class="lp-plp-hero__chip lp-plp-hero__chip--on">All</span>
          <span class="lp-plp-hero__chip">Slim</span>
          <span class="lp-plp-hero__chip">Classic</span>
          <span class="lp-plp-hero__chip">Double-Breasted</span>
          <span class="lp-plp-hero__chip">Velvet</span>
        </div>
      </section>
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ──────────────────────────── PDP shell ───────────────────────────────────
  // For PDP we keep the existing hero unchanged so this version is a
  // drop-in replacement for buildPageHtml().
  function pdpShell(ctx) {
    const P = window.WidgetProduct;
    const hero = `
      <div class="lp-hero">
        <div>
          <div class="lp-hero__crumbs">Men / Suits &amp; Tuxedos / <b>${P.brand}</b></div>
          <div class="lp-hero__img">${window.WidgetSVG.tuxedo()}</div>
        </div>
        <div>
          <div class="lp-hero__crumbs" style="visibility:hidden">.</div>
          <div class="lp-hero__brand">${P.brand}</div>
          <h1 class="lp-hero__name">${P.name}</h1>
          <div class="lp-hero__rating">
            <span>★★★★☆</span><span>${P.rating} / 5 · ${P.reviews} reviews</span>
            <span style="margin-left:auto;color:#0c5a66;font-weight:600;">↓ ${P.returnRate}% returns</span>
          </div>
          <div class="lp-hero__price">€${P.price}</div>
          <div class="lp-hero__sizes">
            ${P.sizes.map(s => `<button class="lp-hero__size ${s === P.selectedSize ? 'lp-hero__size--on' : ''}">${s}</button>`).join('')}
          </div>
          <div class="lp-hero__cta">
            <button>Add to bag</button>
            <button>♡</button>
          </div>
        </div>
      </div>`;
    return `
      ${navBar('pdp')}
      ${hero}
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ──────────────────────────── CART shell ──────────────────────────────────
  // Cart needs a two-column feel but we keep slots full-width below for
  // consistency with how the orchestrator visualizes composition.
  function cartShell(ctx) {
    return `
      ${navBar('cart')}
      <section class="lp-cart-head">
        <h1 class="lp-cart-head__title">Your bag</h1>
        <div class="lp-cart-head__meta">
          <span><b>2</b> items</span><span class="lp-cart-head__dot">·</span>
          <span>Subtotal <b>€984</b></span><span class="lp-cart-head__dot">·</span>
          <span class="lp-cart-head__ship">€55 to free shipping</span>
        </div>
        <button class="lp-btn-primary lp-cart-head__cta">Continue to checkout →</button>
      </section>
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ──────────────────────────── CHECKOUT shell ──────────────────────────────
  function checkoutShell(ctx) {
    return `
      ${navBar('checkout')}
      <section class="lp-checkout-head">
        <div class="lp-checkout-head__brand">BOSS</div>
        <ol class="lp-checkout-steps">
          <li class="lp-checkout-step lp-checkout-step--done"><span>1</span> Bag</li>
          <li class="lp-checkout-step lp-checkout-step--on"><span>2</span> Shipping &amp; pay</li>
          <li class="lp-checkout-step"><span>3</span> Confirm</li>
        </ol>
        <div class="lp-checkout-head__total">€984 <span>total</span></div>
      </section>
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ──────────────────────────── POST-PURCHASE shell ─────────────────────────
  function postPurchaseShell(ctx) {
    return `
      ${navBar('post_purchase')}
      <section class="lp-pp-hero">
        <div class="lp-pp-hero__check">✓</div>
        <div class="lp-pp-hero__copy">
          <div class="lp-pp-hero__eyebrow">ORDER #94821 · CONFIRMED</div>
          <h1 class="lp-pp-hero__title">Thank you, your tuxedo is on its way.</h1>
          <p class="lp-pp-hero__sub">Arriving Thursday, May 23 · 12 Park Lane, London · DHL tracking in your email.</p>
        </div>
        <button class="lp-btn-ghost lp-pp-hero__track">Track order →</button>
      </section>
      ${compBanner(ctx.meta, ctx.problems, ctx.useV3, ctx.persona, ctx.slotCount)}
      {{SLOTS}}
    `;
  }

  // ── Public API ────────────────────────────────────────────────────────────
  window.PageShells = {
    home: homeShell,
    search: searchShell,
    plp: plpShell,
    pdp: pdpShell,
    cart: cartShell,
    checkout: checkoutShell,
    post_purchase: postPurchaseShell,
  };
})();
