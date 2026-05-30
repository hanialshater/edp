// Widget renderers for the EDP Orchestrator demo.
// Each function returns a vanilla HTML string for one of the 22 widgets in the
// registry. They share a consistent retail/PDP look (Inter Tight, off-white
// surfaces, charcoal text, coral accent) so the live page reads as a real
// product page even when the orchestrator's slot picks change.
//
// The renderers consume a small `ctx` object: { problems, coverage, slotIdx }.
// Everything else (product, copy) is fixed fixtures so the demo stays focused
// on widget selection, not data.

(function () {
  // ─── PRODUCT FIXTURE ─────────────────────────────────────────────────────
  const PRODUCT = {
    brand: 'BOSS',
    name: 'Slim-Fit Black Wool Tuxedo',
    price: 895,
    sizes: ['38', '40', '42', '44', '46', '48'],
    selectedSize: '42',
    rating: 4.7,
    reviews: 284,
    returnRate: 4,
    category: 'Suits & Tuxedos',
  };

  // ─── SVG ATOMS ───────────────────────────────────────────────────────────
  // Tiny garment glyphs that look like real product photography on a tinted bg.
  const SVG = {
    tuxedo: () => `<svg viewBox="0 0 200 280" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M70 165 L65 268 L92 268 L100 175 L108 268 L135 268 L130 165Z" fill="#15151a"/>
      <path d="M55 80 Q55 70 75 65 L125 65 Q145 70 145 80 L148 170 L130 175 L100 165 L70 175 L52 170Z" fill="#1a1a1f"/>
      <path d="M75 65 L95 75 L90 150 L100 165 L100 90Z" fill="#0c0c10"/>
      <path d="M125 65 L105 75 L110 150 L100 165 L100 90Z" fill="#0c0c10"/>
      <path d="M92 70 L108 70 L108 165 L100 170 L92 165Z" fill="#fafaf7"/>
      <path d="M88 80 L100 86 L100 92 L88 98Z M112 80 L100 86 L100 92 L112 98Z" fill="#0a0a0d"/>
      <rect x="98" y="84" width="4" height="10" fill="#0a0a0d"/>
    </svg>`,
    bow: () => `<svg viewBox="0 0 200 130" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M30 50 Q35 45 45 47 L90 70 L90 90 L45 113 Q35 115 30 110Z" fill="#1a1a1f"/>
      <path d="M170 50 Q165 45 155 47 L110 70 L110 90 L155 113 Q165 115 170 110Z" fill="#1a1a1f"/>
      <rect x="88" y="67" width="24" height="26" rx="2" fill="#0a0a0d"/>
    </svg>`,
    shoe: () => `<svg viewBox="0 0 240 160" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M30 120 Q25 130 35 132 L210 132 Q225 130 215 118Z" fill="#0a0a0d"/>
      <path d="M35 118 Q30 90 50 78 Q90 60 140 65 Q200 72 215 100 Q218 115 210 122 L40 122 Q32 122 35 118Z" fill="#1a1a1f"/>
      <path d="M50 85 Q90 72 150 75 Q195 80 205 95" stroke="#3a3a45" stroke-width="2" fill="none" opacity=".7"/>
      <path d="M95 95 L95 118 L140 118 L145 95Z" fill="#0a0a0d"/>
    </svg>`,
    shirt: () => `<svg viewBox="0 0 200 260" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M50 60 L30 90 L35 200 L65 195 L70 75Z" fill="#fafaf7" stroke="#e0e0d8" stroke-width=".6"/>
      <path d="M150 60 L170 90 L165 200 L135 195 L130 75Z" fill="#fafaf7" stroke="#e0e0d8" stroke-width=".6"/>
      <path d="M65 55 Q65 50 75 50 L125 50 Q135 50 135 55 L138 240 L62 240Z" fill="#fff" stroke="#e0e0d8" stroke-width=".6"/>
      <path d="M75 50 L95 40 L100 55 L105 40 L125 50 L122 65 L100 58 L78 65Z" fill="#fff" stroke="#d0d0c8" stroke-width=".6"/>
      <line x1="100" y1="58" x2="100" y2="240" stroke="#e0e0d8" stroke-width=".8"/>
    </svg>`,
    cufflinks: () => `<svg viewBox="0 0 200 200" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <circle cx="65" cy="95" r="22" fill="#1a1a1f"/><circle cx="65" cy="95" r="17" fill="#0a0a0d"/>
      <circle cx="60" cy="90" r="4" fill="#3a3a3f" opacity=".6"/>
      <circle cx="135" cy="105" r="22" fill="#1a1a1f"/><circle cx="135" cy="105" r="17" fill="#0a0a0d"/>
      <circle cx="130" cy="100" r="4" fill="#3a3a3f" opacity=".6"/>
    </svg>`,
    cummerbund: () => `<svg viewBox="0 0 240 140" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M30 50 Q25 45 35 42 L205 42 Q215 45 210 50 L215 95 Q215 105 200 108 L40 108 Q25 105 25 95Z" fill="#1a1a1f"/>
      <g stroke="#0a0a0d" stroke-width="2" opacity=".5">
        <line x1="50" y1="50" x2="50" y2="100"/><line x1="80" y1="50" x2="80" y2="100"/>
        <line x1="110" y1="50" x2="110" y2="100"/><line x1="140" y1="50" x2="140" y2="100"/>
        <line x1="170" y1="50" x2="170" y2="100"/>
      </g>
    </svg>`,
    watch: () => `<svg viewBox="0 0 200 220" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M80 30 L120 30 L122 80 L78 80Z" fill="#1a1a1f"/>
      <path d="M78 140 L122 140 L120 190 L80 190Z" fill="#1a1a1f"/>
      <circle cx="100" cy="110" r="42" fill="#2a2a35"/><circle cx="100" cy="110" r="36" fill="#0c0c10"/>
      <circle cx="100" cy="110" r="32" fill="#0a0a0d"/>
      <line x1="100" y1="110" x2="100" y2="90" stroke="#fafaf7" stroke-width="1.8"/>
      <line x1="100" y1="110" x2="115" y2="115" stroke="#fafaf7" stroke-width="1.2"/>
      <circle cx="100" cy="110" r="1.5" fill="#c9764a"/>
    </svg>`,
    pocket: () => `<svg viewBox="0 0 200 180" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M50 80 L100 50 L150 80 L150 145 L50 145Z" fill="#fff" stroke="#d0d0c8" stroke-width=".6"/>
      <path d="M50 80 L100 110 L150 80" stroke="#e0e0d8" stroke-width=".8" fill="none"/>
      <path d="M50 80 L100 110 L100 145 L50 145Z" fill="#000" opacity=".03"/>
    </svg>`,
    studs: () => `<svg viewBox="0 0 200 200" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <circle cx="50" cy="85" r="10" fill="#0a0a0d"/><circle cx="50" cy="85" r="6" fill="#3a3a3f"/>
      <circle cx="90" cy="95" r="10" fill="#0a0a0d"/><circle cx="90" cy="95" r="6" fill="#3a3a3f"/>
      <circle cx="130" cy="85" r="10" fill="#0a0a0d"/><circle cx="130" cy="85" r="6" fill="#3a3a3f"/>
      <circle cx="170" cy="95" r="10" fill="#0a0a0d"/><circle cx="170" cy="95" r="6" fill="#3a3a3f"/>
    </svg>`,
    suspenders: () => `<svg viewBox="0 0 200 240" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <path d="M55 30 L60 130 L95 160 L95 210 L105 210 L105 160 L140 130 L145 30" stroke="#1a1a1f" stroke-width="14" fill="none" stroke-linecap="round"/>
      <rect x="48" y="20" width="14" height="18" rx="2" fill="#c9c2b3"/>
      <rect x="138" y="20" width="14" height="18" rx="2" fill="#c9c2b3"/>
    </svg>`,
    belt: () => `<svg viewBox="0 0 240 140" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <rect x="30" y="55" width="180" height="20" fill="#1a1a1f"/>
      <rect x="135" y="48" width="30" height="34" rx="2" fill="#c9c2b3"/>
      <rect x="140" y="53" width="20" height="24" rx="1" fill="#1a1a1f"/>
    </svg>`,
    mannequin: () => `<svg viewBox="0 0 260 400" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <ellipse cx="130" cy="50" rx="22" ry="26" fill="#d8c4ad"/>
      <path d="M110 36 Q130 22 152 36 Q152 28 145 25 Q130 18 115 25 Q108 30 110 36" fill="#2a221a"/>
      <rect x="120" y="72" width="20" height="14" fill="#c9b59b"/>
      <path d="M105 86 L130 92 L155 86 L158 100 L130 96 L102 100Z" fill="#fafaf7"/>
      <path d="M75 95 Q75 88 95 85 L165 85 Q185 88 185 95 L195 240 L165 250 L130 235 L95 250 L65 240Z" fill="#1a1a1f"/>
      <path d="M95 85 L122 100 L118 215 L130 230 L130 110Z" fill="#0a0a0d"/>
      <path d="M165 85 L138 100 L142 215 L130 230 L130 110Z" fill="#0a0a0d"/>
      <path d="M122 95 L138 95 L138 230 L130 235 L122 230Z" fill="#fafaf7"/>
      <path d="M116 102 L130 110 L130 118 L116 124Z M144 102 L130 110 L130 118 L144 124Z" fill="#0a0a0d"/>
      <rect x="127" y="106" width="6" height="14" fill="#0a0a0d"/>
      <path d="M95 245 L88 388 L122 388 L130 255 L138 388 L172 388 L165 245Z" fill="#15151a"/>
      <path d="M75 100 L60 220 L80 225 L92 110Z" fill="#1a1a1f"/>
      <path d="M185 100 L200 220 L180 225 L168 110Z" fill="#1a1a1f"/>
      <ellipse cx="100" cy="390" rx="18" ry="5" fill="#0a0a0d"/>
      <ellipse cx="160" cy="390" rx="18" ry="5" fill="#0a0a0d"/>
    </svg>`,
    fabric: () => `<svg viewBox="0 0 200 200" preserveAspectRatio="xMidYMid meet" width="100%" height="100%">
      <rect x="20" y="20" width="160" height="160" rx="4" fill="#1a1a1f"/>
      <g stroke="#2a2a35" stroke-width="1">
        <line x1="20" y1="40" x2="180" y2="40"/><line x1="20" y1="60" x2="180" y2="60"/>
        <line x1="20" y1="80" x2="180" y2="80"/><line x1="20" y1="100" x2="180" y2="100"/>
        <line x1="20" y1="120" x2="180" y2="120"/><line x1="20" y1="140" x2="180" y2="140"/>
        <line x1="20" y1="160" x2="180" y2="160"/>
        <line x1="40" y1="20" x2="40" y2="180"/><line x1="60" y1="20" x2="60" y2="180"/>
        <line x1="80" y1="20" x2="80" y2="180"/><line x1="100" y1="20" x2="100" y2="180"/>
        <line x1="120" y1="20" x2="120" y2="180"/><line x1="140" y1="20" x2="140" y2="180"/>
        <line x1="160" y1="20" x2="160" y2="180"/>
      </g>
    </svg>`,
  };

  // tile: a tinted product cell with a tiny image
  const tile = (svgKey, w = 44, h = 56, bg = '#f1efe9') => `
    <div style="width:${w}px;height:${h}px;background:${bg};border-radius:2px;display:flex;align-items:center;justify-content:center;flex:0 0 auto;">
      <div style="width:78%;height:78%;">${SVG[svgKey] ? SVG[svgKey]() : ''}</div>
    </div>`;

  // ─── COMMON CARD CHROME ──────────────────────────────────────────────────
  const widgetChrome = (color, title, badge, body, footer) => `
    <div class="lp-card" style="border-color:${COL[color]?.border || '#ececea'};">
      <div class="lp-card__head">
        <div class="lp-card__tags">
          <span class="lp-tag" style="background:${COL[color]?.tint || '#fafaf7'};color:${COL[color]?.text || '#55555f'};">${badge}</span>
        </div>
        <h3 class="lp-card__title">${title}</h3>
      </div>
      <div class="lp-card__body">${body}</div>
      ${footer ? `<div class="lp-card__footer">${footer}</div>` : ''}
    </div>`;

  // Accent palette mapped from Tailwind colors used in the orchestrator so the
  // live page echoes the dark-side problem hues, but in muted light tints.
  const COL = {
    cyan:     { tint: '#e8f6f9', border: '#c5e4ea', text: '#0c5a66' },
    amber:    { tint: '#fbf2dd', border: '#ead9a8', text: '#7a4e0a' },
    emerald:  { tint: '#e3f3ea', border: '#bcdfc8', text: '#0c5234' },
    fuchsia:  { tint: '#f7e7f4', border: '#e3c2dc', text: '#7a1f6a' },
    orange:   { tint: '#fbeadc', border: '#eaceab', text: '#7a3c0d' },
    rose:     { tint: '#fbe3e6', border: '#ecbfc5', text: '#7a1c2a' },
    indigo:   { tint: '#e8e9f7', border: '#c5c8e6', text: '#26307a' },
    slate:    { tint: '#f1f2f4', border: '#dcdee2', text: '#3a3f4a' },
  };

  // ─── 22 RENDERERS ────────────────────────────────────────────────────────

  const R = {

    // ─── SIZE · FIT (cyan) ───────────────────────────────────────────────
    fit_reassurance: () => widgetChrome('cyan', 'Confident in your size',
      'FIT REASSURANCE · F32',
      `<div class="fit-row">
         <div class="fit-stat">
           <div class="fit-stat__num">87%</div>
           <div class="fit-stat__lab">kept their<br/>regular size</div>
         </div>
         <div class="fit-bar">
           <div class="fit-bar__seg" style="flex:1.0;background:#0c5a66;" title="True to size">
             <span class="fit-bar__pct">87% TRUE TO SIZE</span>
           </div>
           <div class="fit-bar__seg" style="flex:.10;background:#7eb5bf;" title="Runs large"></div>
           <div class="fit-bar__seg" style="flex:.03;background:#cfe6ec;" title="Runs small"></div>
         </div>
       </div>
       <p class="lp-p">Based on 284 reviews from owners who tried this tuxedo on. Slim cut, true shoulders.</p>`),

    size_guide: () => widgetChrome('cyan', 'Your size, in measurements',
      'SIZE GUIDE · F32',
      `<div class="sz-tbl">
         <div class="sz-row sz-row--head">
           <span>SIZE</span><span>CHEST</span><span>WAIST</span><span>SLEEVE</span>
         </div>
         ${['38 · 31in waist', '40 · 33in waist', '42 · 35in waist', '44 · 37in waist'].map((row, i) => {
           const sz = row.split(' · ')[0];
           const active = sz === '42';
           return `<div class="sz-row ${active ? 'sz-row--active' : ''}">
             <span>${sz}${active ? ' · YOURS' : ''}</span>
             <span>${36 + i*2}in</span><span>${31 + i*2}in</span><span>${33 + Math.floor(i*0.5)}in</span>
           </div>`;
         }).join('')}
       </div>
       <button class="lp-btn-ghost">Find your size →</button>`),

    low_return_alts: () => widgetChrome('cyan', 'Lowest return rate in this category',
      'LOW-RETURN ALTERNATIVES · F32 · F46',
      `<div class="lp-row">
         ${[
           { tile: 'tuxedo', name: 'Sandro Peak-Lapel', rate: '2%', price: 720 },
           { tile: 'tuxedo', name: 'Reiss Mercer Tux', rate: '3%', price: 595 },
           { tile: 'tuxedo', name: 'Tiger of Sweden', rate: '4%', price: 825 },
         ].map(it => `
           <div class="alt-card">
             ${tile(it.tile, '100%', 110, '#f1efe9')}
             <div class="alt-card__meta">
               <div class="alt-card__rate">↓ ${it.rate} return</div>
               <div class="alt-card__name">${it.name}</div>
               <div class="alt-card__price">€${it.price}</div>
             </div>
           </div>`).join('')}
       </div>`),

    // ─── COMPARISON (emerald) ────────────────────────────────────────────
    comparison_card: () => widgetChrome('emerald', 'Compare what you\'ve been viewing',
      'SIDE-BY-SIDE · F41',
      `<div class="cmp-tbl">
         <div class="cmp-row cmp-row--head">
           <span></span>
           <span><b>BOSS Tuxedo</b><br/><span class="cmp-pill cmp-pill--this">VIEWING</span></span>
           <span><b>Sandro Peak-Lapel</b></span>
           <span><b>Reiss Mercer</b></span>
         </div>
         <div class="cmp-row"><span>Price</span><span><b>€895</b></span><span>€720</span><span>€595</span></div>
         <div class="cmp-row"><span>Fabric</span><span><b>100% wool</b></span><span>70% wool</span><span>poly blend</span></div>
         <div class="cmp-row"><span>Return rate</span><span><b>4%</b></span><span>2%</span><span>6%</span></div>
         <div class="cmp-row"><span>Made in</span><span><b>Italy</b></span><span>Portugal</span><span>Turkey</span></div>
       </div>`),

    customers_chose: () => widgetChrome('emerald', '92% chose this over the alternative',
      'CUSTOMERS CHOSE · F41 · F51',
      `<div class="vs-row">
         <div class="vs-card vs-card--this">
           ${tile('tuxedo', 70, 90)}
           <div>
             <div class="vs-card__name">BOSS Slim-Fit</div>
             <div class="vs-card__price">€895</div>
             <div class="vs-card__pct">CHOSEN BY <b>92%</b></div>
           </div>
         </div>
         <span class="vs-mid">vs</span>
         <div class="vs-card">
           ${tile('tuxedo', 70, 90, '#ececea')}
           <div>
             <div class="vs-card__name">Tiger of Sweden</div>
             <div class="vs-card__price">€825</div>
             <div class="vs-card__pct">8%</div>
           </div>
         </div>
       </div>
       <p class="lp-p">When customers compared similar items, the BOSS won on fit (89%) and fabric (94%).</p>`),

    value_breakdown: () => widgetChrome('emerald', 'Why this costs €895',
      'VALUE BREAKDOWN · F45 · F33',
      `<div class="vb-stack">
         <div class="vb-row"><span class="vb-row__bar" style="width:48%;background:#0c5234;"></span><span class="vb-row__lab">Italian wool fabric</span><span class="vb-row__amt">€430</span></div>
         <div class="vb-row"><span class="vb-row__bar" style="width:22%;background:#0c5234;"></span><span class="vb-row__lab">Handfinished tailoring</span><span class="vb-row__amt">€195</span></div>
         <div class="vb-row"><span class="vb-row__bar" style="width:18%;background:#3e8060;"></span><span class="vb-row__lab">Half-canvas construction</span><span class="vb-row__amt">€160</span></div>
         <div class="vb-row"><span class="vb-row__bar" style="width:12%;background:#7cb59c;"></span><span class="vb-row__lab">Brand · packaging</span><span class="vb-row__amt">€110</span></div>
       </div>
       <div class="vb-foot">Cost-per-wear at 30 events: <b>€29.83</b></div>`),

    // ─── OUTFIT (fuchsia) ────────────────────────────────────────────────
    outfit_completion: () => widgetChrome('fuchsia', 'Complete the look',
      'OUTFIT COMPLETION · F43',
      `<div class="oc-lay">
         <div class="oc-item" style="left:8%;top:6%;width:34%;height:58%;transform:rotate(-4deg);">${tile('shirt','100%','100%','#f4f4f1')}</div>
         <div class="oc-item" style="left:54%;top:8%;width:30%;height:22%;transform:rotate(7deg);">${tile('bow','100%','100%','#f1efe9')}</div>
         <div class="oc-item" style="left:48%;top:36%;width:44%;height:18%;transform:rotate(-3deg);">${tile('cummerbund','100%','100%','#f0eee8')}</div>
         <div class="oc-item" style="left:62%;top:58%;width:24%;height:22%;transform:rotate(5deg);">${tile('cufflinks','100%','100%','#f3f1eb')}</div>
         <div class="oc-item" style="left:10%;top:68%;width:46%;height:28%;transform:rotate(-2deg);">${tile('shoe','100%','100%','#efede7')}</div>
       </div>
       <div class="oc-list">
         ${[
           { num: 1, name: 'Albini Poplin Shirt', price: 89 },
           { num: 2, name: 'Drake\'s Silk Bow', price: 65 },
           { num: 3, name: 'Eton Cummerbund', price: 95 },
           { num: 4, name: 'Onyx Cufflinks', price: 145 },
           { num: 5, name: 'Crockett & Jones Oxford', price: 285 },
         ].map(it => `
           <div class="oc-row">
             <span class="oc-num">${it.num}</span>
             <span class="oc-name">${it.name}</span>
             <span class="oc-price">€${it.price}</span>
           </div>`).join('')}
       </div>`,
      `<div class="oc-foot">
         <span>5 pieces · €679</span>
         <button class="lp-btn-primary">Add full look to bag</button>
       </div>`),

    style_bridge: () => widgetChrome('fuchsia', 'One tuxedo, three ways',
      'STYLE BRIDGE · F43',
      `<div class="sb-tabs">
         <button class="sb-tab sb-tab--on">Black-Tie</button>
         <button class="sb-tab">Cocktail</button>
         <button class="sb-tab">Wedding Guest</button>
       </div>
       <div class="sb-row">
         <div class="sb-hero">${tile('mannequin', '100%', '100%', '#f1efe9')}</div>
         <div class="sb-items">
           ${[
             { svg: 'shirt', name: 'Crisp poplin shirt', why: 'Sharp base under the suit', price: 89 },
             { svg: 'bow', name: 'Silk self-tie bow', why: 'Classic black-tie protocol', price: 65 },
             { svg: 'shoe', name: 'Polished oxfords', why: 'Mirrors the suit\'s shine', price: 285 },
             { svg: 'cufflinks', name: 'Onyx cufflinks', why: 'Subtle, evening-appropriate', price: 145 },
           ].map((it, i) => `
             <div class="sb-item">
               <span class="sb-item__num">0${i+1}</span>
               ${tile(it.svg, 48, 48, '#fafaf7')}
               <div class="sb-item__meta">
                 <div class="sb-item__name">${it.name}</div>
                 <div class="sb-item__why">${it.why}</div>
               </div>
               <span class="sb-item__price">€${it.price}</span>
             </div>`).join('')}
         </div>
       </div>`),

    occasion_lookbook: () => widgetChrome('fuchsia', 'Where you\'ll wear it',
      'OCCASION LOOKBOOK · F43',
      `<div class="ob-grid">
         ${[
           { lab: 'Black-Tie Gala', n: '01', mood: '#1a1a1f' },
           { lab: 'Wedding Reception', n: '02', mood: '#3a2a2a' },
           { lab: 'Awards Dinner', n: '03', mood: '#1a2a3a' },
           { lab: 'New Year\'s Eve', n: '04', mood: '#2a1a3a' },
         ].map(o => `
           <div class="ob-card" style="background:${o.mood};">
             <span class="ob-card__num">${o.n}</span>
             <div class="ob-card__man">${SVG.mannequin()}</div>
             <div class="ob-card__lab">${o.lab}</div>
           </div>`).join('')}
       </div>`),

    // ─── RETURNS (rose) ──────────────────────────────────────────────────
    return_explainer: () => widgetChrome('rose', 'How returns work',
      'RETURN EXPLAINER · F46',
      `<div class="re-steps">
         ${[
           { n: '1', t: 'Try on at home', d: 'You\'ve got 30 days to decide.' },
           { n: '2', t: 'Print the label', d: 'Pre-paid label in your account.' },
           { n: '3', t: 'Drop it anywhere', d: '8,000+ partner pickup points.' },
           { n: '4', t: 'Money back in 3 days', d: 'Refunded to original payment.' },
         ].map((s, i) => `
           <div class="re-step">
             <div class="re-step__num">${s.n}</div>
             <div>
               <div class="re-step__t">${s.t}</div>
               <div class="re-step__d">${s.d}</div>
             </div>
             ${i < 3 ? '<div class="re-step__line"></div>' : ''}
           </div>`).join('')}
       </div>`),

    easy_returns_promise: () => widgetChrome('rose', '30 days, free, no questions',
      'EASY RETURNS · F46',
      `<div class="erp-row">
         <div class="erp-stat"><div class="erp-stat__big">30</div><div class="erp-stat__lab">DAYS</div></div>
         <div class="erp-stat"><div class="erp-stat__big">€0</div><div class="erp-stat__lab">FREE LABEL</div></div>
         <div class="erp-stat"><div class="erp-stat__big">3d</div><div class="erp-stat__lab">REFUND</div></div>
       </div>
       <p class="lp-p">No reason needed. Original tags only. Same card refund.</p>`),

    // ─── PREMIUM (amber) ─────────────────────────────────────────────────
    brand_story: () => widgetChrome('amber', 'From BOSS · Metzingen, since 1924',
      'BRAND STORY · F33',
      `<div class="bs-row">
         <div class="bs-img">${tile('mannequin', '100%', 140, '#fbf2dd')}</div>
         <div class="bs-body">
           <p class="lp-p">A century of tailoring out of southern Germany. This tuxedo is cut on the Mercer pattern — slim through the waist, soft at the shoulder, finished by hand at the buttonholes.</p>
           <div class="bs-marks">
             <div class="bs-mark"><span class="bs-mark__year">1924</span><span class="bs-mark__lab">FOUNDED</span></div>
             <div class="bs-mark"><span class="bs-mark__year">102</span><span class="bs-mark__lab">YEARS</span></div>
             <div class="bs-mark"><span class="bs-mark__year">DE</span><span class="bs-mark__lab">CUT</span></div>
           </div>
         </div>
       </div>`),

    material_deep_dive: () => widgetChrome('amber', '100% Vitale Barberis wool · S110',
      'MATERIAL DEEP DIVE · F33',
      `<div class="md-row">
         <div class="md-fabric">${SVG.fabric()}</div>
         <div class="md-meta">
           <div class="md-prop"><span class="md-prop__lab">Yarn</span><span class="md-prop__val">S110, 18.2 micron</span></div>
           <div class="md-prop"><span class="md-prop__lab">Weight</span><span class="md-prop__val">280 g/m²</span></div>
           <div class="md-prop"><span class="md-prop__lab">Mill</span><span class="md-prop__val">Vitale Barberis, IT</span></div>
           <div class="md-prop"><span class="md-prop__lab">Lining</span><span class="md-prop__val">Bemberg cupro</span></div>
           <div class="md-prop"><span class="md-prop__lab">Canvas</span><span class="md-prop__val">Half · horsehair</span></div>
         </div>
       </div>`),

    // ─── PRICE (orange) ──────────────────────────────────────────────────
    price_history: () => widgetChrome('orange', 'Lowest price in 90 days',
      'PRICE HISTORY · F45',
      `<div class="ph-chart">
         <svg viewBox="0 0 320 100" preserveAspectRatio="none" style="width:100%;height:80px;">
           <defs><linearGradient id="phg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7a3c0d" stop-opacity=".25"/><stop offset="100%" stop-color="#7a3c0d" stop-opacity="0"/></linearGradient></defs>
           <path d="M0 30 L40 28 L70 35 L110 28 L150 22 L190 24 L230 60 L270 65 L300 72 L320 70 L320 100 L0 100 Z" fill="url(#phg)"/>
           <path d="M0 30 L40 28 L70 35 L110 28 L150 22 L190 24 L230 60 L270 65 L300 72 L320 70" fill="none" stroke="#7a3c0d" stroke-width="2"/>
           <circle cx="270" cy="65" r="4" fill="#7a3c0d"/>
           <text x="270" y="56" fill="#7a3c0d" font-size="10" font-weight="700" text-anchor="middle">€895 now</text>
         </svg>
         <div class="ph-axis"><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span><span>Nov</span><span>Dec</span><span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span></div>
       </div>
       <div class="ph-stats">
         <div><span class="ph-stat__lab">90-DAY LOW</span><span class="ph-stat__val">€895</span></div>
         <div><span class="ph-stat__lab">AVG</span><span class="ph-stat__val">€1,020</span></div>
         <div><span class="ph-stat__lab">HIGH</span><span class="ph-stat__val">€1,120</span></div>
       </div>`),

    price_drop_notify: () => widgetChrome('orange', 'Tell me if it drops',
      'PRICE DROP · F51 · F45',
      `<div class="pd-row">
         <div class="pd-target">
           <span class="pd-target__lab">Notify me when below</span>
           <div class="pd-target__pill">€<span class="pd-target__amt">795</span><span class="pd-target__edit">edit</span></div>
         </div>
         <button class="lp-btn-primary">Watch this price</button>
       </div>
       <p class="lp-p">2,431 shoppers tracking. Average drop within 60 days: 11%.</p>`),

    // ─── DECISION (indigo) ───────────────────────────────────────────────
    recently_viewed: () => widgetChrome('indigo', 'Pick up where you left off',
      'RECENTLY VIEWED · F51',
      `<div class="lp-row">
         ${[
           { svg: 'tuxedo', name: 'Sandro Tuxedo', price: 720, when: '8 min ago' },
           { svg: 'tuxedo', name: 'Reiss Mercer', price: 595, when: '12 min ago' },
           { svg: 'tuxedo', name: 'Tiger Tux', price: 825, when: 'Yesterday' },
           { svg: 'shoe',   name: 'C&J Oxford',  price: 285, when: 'Yesterday' },
         ].map(it => `
           <div class="rv-card">
             ${tile(it.svg, '100%', 90, '#e8e9f7')}
             <div class="rv-card__name">${it.name}</div>
             <div class="rv-card__row"><span>€${it.price}</span><span class="rv-card__when">${it.when}</span></div>
           </div>`).join('')}
       </div>`),

    wishlist_save: () => widgetChrome('indigo', 'Not sure yet? Save it',
      'WISHLIST · F51',
      `<div class="ws-row">
         <div class="ws-heart">
           <svg width="32" height="32" viewBox="0 0 24 24" fill="#26307a" stroke="#26307a" stroke-width="1.5">
             <path d="M12 21s-7-4.5-9.5-9C0.8 8.7 2.5 5 6 5c2 0 3.5 1.2 4.5 2.6C11.5 6.2 13 5 15 5c3.5 0 5.2 3.7 3.5 7-2.5 4.5-9.5 9-9.5 9z"/>
           </svg>
         </div>
         <div class="ws-body">
           <div class="ws-title">Sleep on it — we'll remember the size.</div>
           <div class="ws-sub">Items in your wishlist average 4 days to purchase. 71% come back.</div>
         </div>
         <button class="lp-btn-ghost">Save to wishlist</button>
       </div>`),

    expert_pick: () => widgetChrome('indigo', 'Editor\'s pick',
      'EXPERT PICK · F51 · F33',
      `<div class="ep-row">
         <div class="ep-portrait">
           <div class="ep-portrait__inner">RC</div>
         </div>
         <div class="ep-body">
           <div class="ep-quote">"This is the tuxedo I send guys to when they need one suit that does black-tie, weddings, and corporate galas. The fit is forgiving without being baggy."</div>
           <div class="ep-author">Rohan C. · Menswear editor, 12 yrs at Mr Porter</div>
         </div>
       </div>`),

    // ─── DEFAULTS (slate) ────────────────────────────────────────────────
    similar_items: () => widgetChrome('slate', 'Similar tuxedos',
      'SIMILAR ITEMS',
      `<div class="lp-row lp-row--6">
         ${[
           { name: 'Reiss Mercer',   price: 595 },
           { name: 'Sandro Peak',    price: 720 },
           { name: 'Tiger Stockholm',price: 825 },
           { name: 'Sandro Bordeaux',price: 645 },
           { name: 'Reiss Halton',   price: 540 },
           { name: 'COS Velvet',     price: 380 },
         ].map(it => `
           <div class="si-card">
             ${tile('tuxedo', '100%', 100, '#f1f2f4')}
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),

    also_bought: () => widgetChrome('slate', 'Customers also bought',
      'ALSO BOUGHT',
      `<div class="lp-row lp-row--5">
         ${[
           { svg: 'shirt',     name: 'Albini Poplin Shirt', price: 89 },
           { svg: 'bow',       name: 'Drake\'s Silk Bow',   price: 65 },
           { svg: 'shoe',      name: 'C&J Oxford',          price: 285 },
           { svg: 'cufflinks', name: 'Onyx Cufflinks',      price: 145 },
           { svg: 'belt',      name: 'Anderson\'s Belt',    price: 75 },
         ].map(it => `
           <div class="si-card">
             ${tile(it.svg, '100%', 90, '#f1f2f4')}
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),

    trending_now: () => widgetChrome('slate', 'Trending in formalwear',
      'TRENDING NOW',
      `<div class="lp-row lp-row--5">
         ${[
           { svg: 'tuxedo', name: 'Velvet Dinner Jacket', price: 695, lab: '↑ 4.2x views' },
           { svg: 'tuxedo', name: 'Cream Tuxedo',          price: 950, lab: '↑ 2.8x' },
           { svg: 'shoe',   name: 'Patent Loafers',         price: 320, lab: '↑ 2.5x' },
           { svg: 'shirt',  name: 'Wing Collar Shirt',      price: 110, lab: '↑ 2.1x' },
           { svg: 'watch',  name: 'Junghans Max Bill',      price: 1190,lab: '↑ 1.9x' },
         ].map(it => `
           <div class="si-card">
             ${tile(it.svg, '100%', 90, '#f1f2f4')}
             <div class="si-card__trend">${it.lab}</div>
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),

    personal_recs: () => widgetChrome('slate', 'For you',
      'PERSONAL RECS',
      `<div class="lp-row lp-row--5">
         ${[
           { svg: 'shoe',      name: 'Suede Derby',        price: 245 },
           { svg: 'watch',     name: 'Vintage Dress Watch',price: 540 },
           { svg: 'pocket',    name: 'White Silk Square',  price: 55 },
           { svg: 'studs',     name: 'Onyx Shirt Studs',   price: 110 },
           { svg: 'suspenders',name: 'Silk Braces',        price: 95 },
         ].map(it => `
           <div class="si-card">
             ${tile(it.svg, '100%', 90, '#f1f2f4')}
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),
  };

  // ─── PUBLIC API ──────────────────────────────────────────────────────────
  window.WidgetRenderers = R;
  window.WidgetProduct = PRODUCT;
  window.WidgetSVG = SVG;
})();
