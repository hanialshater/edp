// =============================================================================
// PAGE WIDGETS — renderers for the non-PDP pages (home/search/plp/cart/
// checkout/post-purchase). Same visual language as widget-renderers.js
// (lp-card chrome, lp-tag badge, lp-btn classes) but new widget content.
// =============================================================================

(function () {
  const SVG = window.WidgetSVG;
  const COL = {
    cyan:     { tint: '#e8f6f9', border: '#c5e4ea', text: '#0c5a66' },
    amber:    { tint: '#fbf2dd', border: '#ead9a8', text: '#7a4e0a' },
    emerald:  { tint: '#e3f3ea', border: '#bcdfc8', text: '#0c5234' },
    fuchsia:  { tint: '#f7e7f4', border: '#e3c2dc', text: '#7a1f6a' },
    orange:   { tint: '#fbeadc', border: '#eaceab', text: '#7a3c0d' },
    rose:     { tint: '#fbe3e6', border: '#ecbfc5', text: '#7a1c2a' },
    indigo:   { tint: '#e8e9f7', border: '#c5c8e6', text: '#26307a' },
    slate:    { tint: '#f1f2f4', border: '#dcdee2', text: '#3a3f4a' },
    sky:      { tint: '#e0f2fe', border: '#b6dcf4', text: '#0c4a6e' },
    teal:     { tint: '#dff5f0', border: '#b6dfd5', text: '#0c4c46' },
    blue:     { tint: '#e0e8f7', border: '#bfcce6', text: '#1e3a8a' },
  };

  const tile = (svgKey, w = 44, h = 56, bg = '#f1efe9') => `
    <div style="width:${w}px;height:${h}px;background:${bg};border-radius:2px;display:flex;align-items:center;justify-content:center;flex:0 0 auto;">
      <div style="width:78%;height:78%;">${SVG[svgKey] ? SVG[svgKey]() : ''}</div>
    </div>`;

  const card = (color, title, badge, body, footer) => `
    <div class="lp-card" style="border-color:${COL[color]?.border || '#ececea'};">
      <div class="lp-card__head">
        <div class="lp-card__tags">
          <span class="lp-tag" style="background:${COL[color]?.tint};color:${COL[color]?.text};">${badge}</span>
        </div>
        <h3 class="lp-card__title">${title}</h3>
      </div>
      <div class="lp-card__body">${body}</div>
      ${footer ? `<div class="lp-card__footer">${footer}</div>` : ''}
    </div>`;

  // ───────────────────────────────────────────────────────────────────────────
  // HOME widgets
  // ───────────────────────────────────────────────────────────────────────────
  const HOME = {
    inspiration_hero: () => card('fuchsia', 'A new way to wear black tie',
      'INSPIRATION HERO · F12',
      `<div class="ih-grid">
         <div class="ih-feat" style="background:#1a1a1f;">
           ${SVG.mannequin()}
           <div class="ih-feat__cap">
             <div class="ih-feat__eyebrow">EDITORIAL · 4 LOOKS</div>
             <div class="ih-feat__title">The Modern Tuxedo</div>
           </div>
         </div>
         <div class="ih-side">
           ${[
             { lab: 'Velvet, Reconsidered', svg: 'tuxedo' },
             { lab: 'Black Tie, Bent',      svg: 'bow' },
             { lab: 'The After-Hours Cut',  svg: 'shoe' },
           ].map(s => `
             <div class="ih-tile">
               ${tile(s.svg, '100%', 70, '#f4f1ea')}
               <div class="ih-tile__lab">${s.lab}</div>
             </div>`).join('')}
         </div>
       </div>`,
      `<button class="lp-btn-ghost">Read the season's editorial →</button>`),

    continue_browsing: () => card('indigo', 'Pick up where you left off',
      'CONTINUE BROWSING · F35 · F51',
      `<div class="lp-row lp-row--4">
         ${[
           { svg:'tuxedo', name:'BOSS Slim-Fit Tuxedo',  meta:'Size 42 · €895',  ago:'4 min ago' },
           { svg:'tuxedo', name:'Sandro Peak-Lapel',     meta:'Size 40 · €720',  ago:'18 min ago' },
           { svg:'shoe',   name:'C&J Black Oxford',      meta:'UK 9 · €285',     ago:'1 hr ago' },
           { svg:'bow',    name:'Drake\'s Silk Bow',     meta:'€65',             ago:'Yesterday' },
         ].map(it => `
           <div class="rv-card">
             ${tile(it.svg, '100%', 100, '#e8e9f7')}
             <div class="rv-card__name">${it.name}</div>
             <div class="rv-card__row"><span>${it.meta}</span><span class="rv-card__when">${it.ago}</span></div>
           </div>`).join('')}
       </div>`),

    shopping_mission: () => card('sky', "What are you here for?",
      'GUIDANCE · F11 · F12',
      `<div class="sm-grid">
         ${[
           { lab: 'Solve a need',      sub: "I need something specific.", svg: 'shirt' },
           { lab: 'A specific event',  sub: 'Wedding, gala, work.',       svg: 'tuxedo' },
           { lab: 'Build an outfit',   sub: 'Around one anchor piece.',   svg: 'mannequin' },
           { lab: 'Just browsing',     sub: "Let's see what's new.",      svg: 'watch' },
         ].map(m => `
           <button class="sm-card">
             <div class="sm-card__art">${tile(m.svg, '100%', 80, '#e0f2fe')}</div>
             <div class="sm-card__lab">${m.lab}</div>
             <div class="sm-card__sub">${m.sub}</div>
           </button>`).join('')}
       </div>`),

    editorial_collections: () => card('fuchsia', 'Editor\'s collections',
      'EDITORIAL · F12 · F21',
      `<div class="ec-grid">
         ${[
           { n:'01', t:'The Tailoring Edit',  d:'18 pieces · €395-€2,400', bg:'#1a1a1f' },
           { n:'02', t:'Evening Wear, Refined',d:'24 pieces · €145-€895',  bg:'#2a1a1f' },
           { n:'03', t:'Italian Mills, Local Cuts',d:'12 brands · 9 mills',bg:'#1a2a2f' },
         ].map(c => `
           <div class="ec-card" style="background:${c.bg};">
             <span class="ec-card__num">${c.n}</span>
             <div class="ec-card__art">${SVG.mannequin()}</div>
             <div class="ec-card__t">${c.t}</div>
             <div class="ec-card__d">${c.d}</div>
           </div>`).join('')}
       </div>`),

    new_arrivals: () => card('amber', 'New this week',
      'NEW ARRIVALS · F21',
      `<div class="lp-row lp-row--5">
         ${[
           { svg:'tuxedo',name:'Reiss Cassini',  price:680, isNew:true },
           { svg:'tuxedo',name:'Tiger Bordeaux', price:825, isNew:true },
           { svg:'shirt', name:'Albini Marcella',price:115, isNew:true },
           { svg:'shoe',  name:'Edward Green',   price:1140,isNew:false },
           { svg:'watch', name:'NOMOS Tangente', price:1980,isNew:true },
         ].map(it => `
           <div class="si-card">
             ${tile(it.svg, '100%', 90, '#fbf2dd')}
             ${it.isNew ? '<div class="si-card__trend" style="color:#7a4e0a;">JUST IN</div>' : ''}
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),

    trending_now_home: () => card('rose', 'Trending this week',
      'TRENDING',
      `<div class="lp-row lp-row--5">
         ${[
           { svg:'tuxedo', name:'Velvet Dinner Jacket', price:695, lab:'↑ 4.2× views' },
           { svg:'mannequin',name:'Wide-Leg Tux Trouser',price:295,lab:'↑ 3.1×' },
           { svg:'shoe',   name:'Patent Loafers',       price:320, lab:'↑ 2.5×' },
           { svg:'shirt',  name:'Wing Collar Shirt',    price:110, lab:'↑ 2.1×' },
           { svg:'watch',  name:'Junghans Max Bill',    price:1190,lab:'↑ 1.9×' },
         ].map(it => `
           <div class="si-card">
             ${tile(it.svg, '100%', 90, '#fbe3e6')}
             <div class="si-card__trend">${it.lab}</div>
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),

    personal_picks_home: () => card('indigo', 'For you, Hugh',
      'PERSONAL · F35 · F51',
      `<div class="lp-row lp-row--5">
         ${[
           { svg:'shoe',     name:'Suede Derby',     price:245 },
           { svg:'watch',    name:'Dress Watch',     price:540 },
           { svg:'pocket',   name:'Silk Square',     price:55 },
           { svg:'studs',    name:'Onyx Studs',      price:110 },
           { svg:'suspenders',name:'Silk Braces',    price:95 },
         ].map(it => `
           <div class="si-card">
             ${tile(it.svg, '100%', 90, '#e8e9f7')}
             <div class="si-card__name">${it.name}</div>
             <div class="si-card__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),

    shop_the_look_home: () => card('fuchsia', 'Shop the look',
      'STYLED · F12',
      `<div class="stl-row">
         <div class="stl-hero" style="background:#1a1a1f;">
           ${SVG.mannequin()}
           <span class="stl-pin" style="left:50%;top:30%;">1</span>
           <span class="stl-pin" style="left:48%;top:46%;">2</span>
           <span class="stl-pin" style="left:48%;top:64%;">3</span>
           <span class="stl-pin" style="left:35%;top:88%;">4</span>
         </div>
         <div class="stl-items">
           ${[
             { num:1, name:'BOSS Slim Tux',   why:'The anchor — slim, low-shine',  price:895 },
             { num:2, name:'Albini Poplin',   why:'Sharp white base',              price:89 },
             { num:3, name:'Drake\'s Bow',    why:'Self-tied silk',                price:65 },
             { num:4, name:'C&J Oxford',      why:'Polished, evening-ready',       price:285 },
           ].map(it => `
             <div class="stl-row__item">
               <span class="stl-num">${it.num}</span>
               <div class="stl-meta">
                 <div class="stl-name">${it.name}</div>
                 <div class="stl-why">${it.why}</div>
               </div>
               <span class="stl-price">€${it.price}</span>
             </div>`).join('')}
         </div>
       </div>`,
      `<div class="oc-foot"><span>4 pieces · €1,334</span><button class="lp-btn-primary">Shop the look</button></div>`),

    seasonal_picks: () => card('teal', 'For the season',
      'SEASONAL',
      `<div class="lp-row lp-row--4">
         ${[
           { svg:'mannequin',name:'Wool overcoats', count:'48 items' },
           { svg:'shoe',     name:'Leather chelseas',count:'62 items' },
           { svg:'shirt',    name:'Cashmere knits', count:'94 items' },
           { svg:'belt',     name:'Lined gloves',   count:'24 items' },
         ].map(it => `
           <div class="sp-card">
             ${tile(it.svg, '100%', 100, '#dff5f0')}
             <div class="sp-card__name">${it.name}</div>
             <div class="sp-card__count">${it.count}</div>
           </div>`).join('')}
       </div>`),

    last_chance: () => card('orange', 'Last chance · final markdowns',
      'SALE · F51',
      `<div class="lp-row lp-row--5">
         ${[
           { name:'Sandro Peak',     was:720, now:540, left:3 },
           { name:'Reiss Halton',    was:540, now:380, left:7 },
           { name:'Velvet Loafer',   was:285, now:195, left:2 },
           { name:'Silk Pocket Sq.', was: 65, now: 35, left:12},
           { name:'Wool Trouser',    was:225, now:155, left:5 },
         ].map(it => `
           <div class="lc-card">
             ${tile('tuxedo','100%',80,'#fbeadc')}
             <div class="lc-row"><span class="lc-was">€${it.was}</span><span class="lc-now">€${it.now}</span></div>
             <div class="lc-name">${it.name}</div>
             <div class="lc-left">${it.left} left</div>
           </div>`).join('')}
       </div>`),
  };

  // ───────────────────────────────────────────────────────────────────────────
  // SEARCH widgets
  // ───────────────────────────────────────────────────────────────────────────
  const SEARCH = {
    query_interpretation: () => card('teal', 'We read this as: "Formal evening wear"',
      'QUERY · F13',
      `<div class="qi-row">
         <div class="qi-q">
           <div class="qi-q__lab">YOU TYPED</div>
           <div class="qi-q__val">"black tie tuxedo"</div>
         </div>
         <div class="qi-arrow">→</div>
         <div class="qi-i">
           <div class="qi-i__lab">WE\'RE FILTERING BY</div>
           <div class="qi-i__chips">
             <span class="qi-chip">Tuxedos</span>
             <span class="qi-chip">Black tie</span>
             <span class="qi-chip">Wool, satin lapel</span>
             <span class="qi-chip">€500-€2,000</span>
           </div>
         </div>
       </div>
       <p class="lp-p">Not what you meant? <b style="color:#0c4c46;cursor:pointer;border-bottom:1px dotted;">Clear and search broadly</b></p>`),

    smart_facets: () => card('orange', 'Refine — most useful for "tuxedo"',
      'SMART FACETS · F22',
      `<div class="sf-grid">
         ${[
           { lab:'Cut',         opts:[{k:'Slim',n:418,on:true},{k:'Classic',n:362},{k:'Double-Breasted',n:218},{k:'Velvet',n:124}]},
           { lab:'Lapel',       opts:[{k:'Peak',n:520,on:true},{k:'Shawl',n:312},{k:'Notch',n:182}]},
           { lab:'Fabric',      opts:[{k:'Italian wool',n:418,on:true},{k:'Wool blend',n:264},{k:'Velvet',n:124}]},
           { lab:'Price',       opts:[{k:'Under €500',n:124},{k:'€500-€1k',n:540,on:true},{k:'€1k-€2k',n:386},{k:'€2k+',n:218}]},
         ].map(g => `
           <div class="sf-group">
             <div class="sf-group__lab">${g.lab}</div>
             ${g.opts.map(o => `<span class="sf-opt ${o.on?'sf-opt--on':''}">${o.k}<span>${o.n}</span></span>`).join('')}
           </div>`).join('')}
       </div>`),

    visual_swatches: () => card('sky', 'By colour &amp; material',
      'VISUAL FILTER · F22 · F13',
      `<div class="vs-swatches">
         ${[
           { lab:'Black wool',  bg:'#15151a' },
           { lab:'Midnight',    bg:'#0e1a3a' },
           { lab:'Velvet',      bg:'#2a1a3a' },
           { lab:'Burgundy',    bg:'#3a1a25' },
           { lab:'Cream',       bg:'#e8e1d3' },
           { lab:'Forest',      bg:'#1a2f24' },
           { lab:'Charcoal',    bg:'#2a2a30' },
           { lab:'Cocoa',       bg:'#2a1f1a' },
         ].map(s => `
           <div class="vs-swatch">
             <div class="vs-swatch__sq" style="background:${s.bg};"></div>
             <div class="vs-swatch__lab">${s.lab}</div>
           </div>`).join('')}
       </div>`),

    did_you_mean: () => card('teal', 'Did you mean…',
      'DID YOU MEAN · F13',
      `<div class="dym-row">
         ${[
           { lab:'tuxedo', n:1284,on:true },
           { lab:'dinner jacket', n:486 },
           { lab:'black tie suit', n:312 },
           { lab:'velvet blazer', n:204 },
         ].map(s => `<button class="dym-pill ${s.on?'dym-pill--on':''}">${s.lab}<span>${s.n.toLocaleString()}</span></button>`).join('')}
       </div>`),

    results_grid: () => card('slate', '1,284 results · best match',
      'RESULTS',
      `<div class="lp-row lp-row--5">
         ${[
           { name:'BOSS Slim-Fit',  price:895, brand:'BOSS',          rate:4 },
           { name:'Sandro Peak',    price:720, brand:'SANDRO',        rate:2 },
           { name:'Reiss Mercer',   price:595, brand:'REISS',         rate:3 },
           { name:'Tiger Stockholm',price:825, brand:'TIGER OF SWEDEN',rate:4 },
           { name:'Sandro Bordeaux',price:645, brand:'SANDRO',        rate:5 },
         ].map(it => `
           <div class="rg-card">
             ${tile('tuxedo','100%',120,'#f1f2f4')}
             <div class="rg-brand">${it.brand}</div>
             <div class="rg-name">${it.name}</div>
             <div class="rg-foot">
               <span class="rg-price">€${it.price}</span>
               <span class="rg-rate">↓ ${it.rate}% returns</span>
             </div>
           </div>`).join('')}
       </div>`),

    fresh_picks_search: () => card('amber', 'Fresh — you haven\'t seen these',
      'FRESH PICKS · F21 · F23',
      `<div class="lp-row lp-row--4">
         ${[
           { name:'Husbands Tuxedo',     price:1480, brand:'HUSBANDS PARIS' },
           { name:'Mr P. Cream Dinner',  price:950,  brand:'MR P.' },
           { name:'Wales Bonner Tux',    price:2280, brand:'WALES BONNER' },
           { name:'Officine Generale',   price:880,  brand:'O.G.' },
         ].map(it => `
           <div class="rg-card rg-card--fresh">
             ${tile('tuxedo','100%',120,'#fbf2dd')}
             <span class="rg-fresh">NEW TO YOU</span>
             <div class="rg-brand">${it.brand}</div>
             <div class="rg-name">${it.name}</div>
             <div class="rg-foot"><span class="rg-price">€${it.price}</span></div>
           </div>`).join('')}
       </div>`),

    related_searches: () => card('rose', 'People who searched this also searched',
      'RELATED · F13 · F23',
      `<div class="rs-row">
         ${['cream tuxedo','wedding suit','dinner jacket','black tie shoes','velvet blazer','satin lapel suit'].map(s => `
           <button class="rs-pill">⌕ ${s}</button>`).join('')}
       </div>`),

    featured_brands: () => card('fuchsia', 'Brands carrying "tuxedo"',
      'FEATURED BRANDS',
      `<div class="fb-grid">
         ${['BOSS','SANDRO','REISS','TIGER OF SWEDEN','TOM FORD','HUSBANDS PARIS','MR P.','PAUL SMITH'].map(b => `
           <div class="fb-card">
             <div class="fb-card__name">${b}</div>
             <div class="fb-card__count">${(Math.random()*40+12).toFixed(0)} items</div>
           </div>`).join('')}
       </div>`),
  };

  // ───────────────────────────────────────────────────────────────────────────
  // PLP widgets
  // ───────────────────────────────────────────────────────────────────────────
  const PLP = {
    category_hero: () => card('teal', 'Tuxedos · the long-form',
      'CATEGORY HERO · F11',
      `<div class="ch-row">
         <div class="ch-art" style="background:#1a1a1f;">${SVG.mannequin()}</div>
         <div class="ch-copy">
           <p class="lp-p" style="font-size:14.5px;line-height:1.55;">A tuxedo is the most ceremonial garment a man owns, and the most fixed in tradition. Cut from worsted wool with satin or grosgrain lapels; black or midnight blue; single-button, peak or shawl. Everything else — bow tie, studs, polished oxfords — flows from that anchor.</p>
           <div class="ch-stats">
             <div><span class="ch-stats__big">142</span><span class="ch-stats__lab">ITEMS</span></div>
             <div><span class="ch-stats__big">28</span><span class="ch-stats__lab">BRANDS</span></div>
             <div><span class="ch-stats__big">€395</span><span class="ch-stats__lab">FROM</span></div>
           </div>
         </div>
       </div>`),

    facet_rail: () => card('orange', 'Filter · 142 items',
      'FACET RAIL · F22',
      `<div class="fr-row">
         ${[
           { lab:'Size', val:'42 R', on:true },
           { lab:'Cut',  val:'Slim', on:true },
           { lab:'Color',val:'Black', on:true },
           { lab:'Lapel',val:'Any', on:false },
           { lab:'Fabric',val:'Wool',on:true },
           { lab:'Brand',val:'4 selected',on:true },
           { lab:'Price',val:'€500-1k',on:true },
           { lab:'Sort', val:'Best match',on:false },
         ].map(f => `
           <button class="fr-pill ${f.on?'fr-pill--on':''}">
             <span class="fr-pill__lab">${f.lab}</span>
             <span class="fr-pill__val">${f.val}</span>
             ${f.on?'<span class="fr-pill__x">✕</span>':''}
           </button>`).join('')}
       </div>
       <div class="fr-foot">
         <span><b>56</b> items after your filters</span>
         <button class="lp-btn-ghost">Clear all</button>
       </div>`),

    size_predictor: () => card('cyan', '8 in stock in your size',
      'SIZE PREDICTOR · F22',
      `<div class="sp-row">
         <div class="sp-stat">
           <div class="sp-stat__big">8</div>
           <div class="sp-stat__lab">items in 42R<br/>across this category</div>
         </div>
         <div class="sp-list">
           ${[
             { name:'BOSS Slim',     left:4 },
             { name:'Sandro Peak',   left:2 },
             { name:'Reiss Mercer',  left:7 },
             { name:'Tiger Bordeaux',left:1 },
           ].map(it => `
             <div class="sp-list__row">
               <span class="sp-list__name">${it.name}</span>
               <span class="sp-list__bar">
                 <span class="sp-list__fill" style="width:${Math.min(100,it.left*15)}%"></span>
               </span>
               <span class="sp-list__n">${it.left}</span>
             </div>`).join('')}
         </div>
       </div>`),

    fresh_picks_plp: () => card('amber', 'New since you last looked',
      'FRESH PICKS · F21',
      `<div class="lp-row lp-row--4">
         ${[
           { name:'Husbands Bordeaux',     price:1280, days:1 },
           { name:'Sandro Black Velvet',   price:780,  days:3 },
           { name:'Tiger of Sweden Cream', price:950,  days:5 },
           { name:'BOSS Midnight Blue',    price:920,  days:7 },
         ].map(it => `
           <div class="rg-card rg-card--fresh">
             ${tile('tuxedo','100%',120,'#fbf2dd')}
             <span class="rg-fresh">${it.days}d AGO</span>
             <div class="rg-name">${it.name}</div>
             <div class="rg-foot"><span class="rg-price">€${it.price}</span></div>
           </div>`).join('')}
       </div>`),

    plp_grid: () => card('slate', '142 tuxedos · classic order',
      'PRODUCT GRID',
      `<div class="lp-row lp-row--5">
         ${[
           { name:'BOSS Slim-Fit',   price:895,  brand:'BOSS' },
           { name:'Sandro Peak',     price:720,  brand:'SANDRO' },
           { name:'Reiss Mercer',    price:595,  brand:'REISS' },
           { name:'Tiger Stockholm', price:825,  brand:'TIGER OF SWEDEN' },
           { name:'COS Velvet',      price:380,  brand:'COS' },
           { name:'Sandro Bordeaux', price:645,  brand:'SANDRO' },
           { name:'Reiss Halton',    price:540,  brand:'REISS' },
           { name:'BOSS Classic',    price:945,  brand:'BOSS' },
           { name:'Tom Ford O\'Connor',price:2480,brand:'TOM FORD' },
           { name:'Mr P. Cream Dinner',price:950,brand:'MR P.' },
         ].map(it => `
           <div class="rg-card">
             ${tile('tuxedo','100%',110,'#f1f2f4')}
             <div class="rg-brand">${it.brand}</div>
             <div class="rg-name">${it.name}</div>
             <div class="rg-foot"><span class="rg-price">€${it.price}</span></div>
           </div>`).join('')}
       </div>`),

    collection_callout: () => card('fuchsia', '"The Italian Mills" — handpicked',
      'COLLECTION · F23',
      `<div class="cc-row">
         <div class="cc-art" style="background:#2a1a1f;">
           <span class="cc-art__eyebrow">EDITORIAL</span>
           ${SVG.mannequin()}
         </div>
         <div class="cc-copy">
           <div class="cc-eyebrow">9 BRANDS · 12 ITEMS</div>
           <h4 class="cc-title">The Italian Mills</h4>
           <p class="lp-p">Tuxedos cut from Vitale Barberis, Loro Piana and Reda. All half-canvas or better.</p>
           <button class="lp-btn-ghost">View collection →</button>
         </div>
       </div>`),

    visual_browse: () => card('rose', 'Browse the gallery',
      'VISUAL BROWSE · F23',
      `<div class="vb-mosaic">
         ${[
           { bg:'#1a1a1f',svg:'mannequin', sz:'tall' },
           { bg:'#2a1a2f',svg:'tuxedo',    sz:'short' },
           { bg:'#1a2a2f',svg:'shoe',      sz:'wide'  },
           { bg:'#2a1f1a',svg:'bow',       sz:'short' },
           { bg:'#1f1f2a',svg:'mannequin', sz:'wide'  },
           { bg:'#2a1a1f',svg:'shirt',     sz:'tall'  },
         ].map(c => `
           <div class="vb-tile vb-tile--${c.sz}" style="background:${c.bg};">
             ${SVG[c.svg]()}
           </div>`).join('')}
       </div>`),

    editor_picks_plp: () => card('indigo', 'Our editor\'s 6 picks from 142',
      'EDITOR PICKS',
      `<div class="lp-row lp-row--3">
         ${[
           { name:'BOSS Slim-Fit',   price:895, why:'The safe-but-sharp pick.' },
           { name:'Husbands Bordeaux',price:1280,why:'For when black is too obvious.' },
           { name:'Mr P. Cream Dinner',price:950,why:'Summer black-tie answer.' },
         ].map((it,i) => `
           <div class="ep-pick">
             <span class="ep-pick__num">0${i+1}</span>
             ${tile('tuxedo','100%',150,'#e8e9f7')}
             <div class="ep-pick__name">${it.name}</div>
             <div class="ep-pick__why">${it.why}</div>
             <div class="ep-pick__price">€${it.price}</div>
           </div>`).join('')}
       </div>`),
  };

  // ───────────────────────────────────────────────────────────────────────────
  // CART widgets
  // ───────────────────────────────────────────────────────────────────────────
  const CART = {
    cart_summary: () => card('slate', '2 items in your bag',
      'YOUR BAG',
      `<div class="cs-list">
         ${[
           { svg:'tuxedo', brand:'BOSS', name:'Slim-Fit Black Wool Tuxedo', size:'42 R', qty:1, price:895 },
           { svg:'shirt',  brand:'ALBINI', name:'Marcella Poplin Bow Shirt', size:'M',    qty:1, price:89  },
         ].map(it => `
           <div class="cs-row">
             ${tile(it.svg,84,108,'#f1efe9')}
             <div class="cs-meta">
               <div class="cs-meta__brand">${it.brand}</div>
               <div class="cs-meta__name">${it.name}</div>
               <div class="cs-meta__attrs">Size <b>${it.size}</b> · Qty <b>${it.qty}</b></div>
               <div class="cs-meta__actions">
                 <button class="cs-act">Edit</button>
                 <button class="cs-act">Move to wishlist</button>
                 <button class="cs-act cs-act--rm">Remove</button>
               </div>
             </div>
             <div class="cs-price">€${it.price}</div>
           </div>`).join('')}
       </div>
       <div class="cs-totals">
         <div class="cs-tot__row"><span>Subtotal</span><span>€984</span></div>
         <div class="cs-tot__row"><span>Estimated shipping</span><span>€0 over €1,000</span></div>
         <div class="cs-tot__row cs-tot__row--big"><span>Total</span><span>€984</span></div>
       </div>`),

    shipping_threshold: () => card('emerald', '€16 from free shipping',
      'INCENTIVE · F45 · F51',
      `<div class="st-bar">
         <div class="st-bar__fill" style="width:98.4%;"></div>
         <span class="st-bar__cap st-bar__cap--start">€984</span>
         <span class="st-bar__cap st-bar__cap--goal">€1,000</span>
       </div>
       <p class="lp-p">Add one more item over €16 and shipping is free worldwide. Suggested: <b>Drake's Silk Bow (€65)</b>, <b>Onyx Studs (€110)</b>.</p>`),

    complete_outfit_cart: () => card('fuchsia', 'Finish the look',
      'COMPLETE THE OUTFIT · F12 · F51',
      `<div class="lp-row lp-row--5">
         ${[
           { svg:'bow',       name:'Drake\'s Bow',    price:65, why:'Match the lapel' },
           { svg:'cufflinks', name:'Onyx Cufflinks',  price:145,why:'Evening-appropriate' },
           { svg:'shoe',      name:'C&J Oxford',      price:285,why:'Polished black' },
           { svg:'pocket',    name:'White Silk Sq.',  price:55, why:'The traditional pick' },
           { svg:'belt',      name:'Patent Belt',     price:95, why:'Slim, low-shine' },
         ].map(it => `
           <div class="cou-card">
             ${tile(it.svg,'100%',80,'#f7e7f4')}
             <div class="cou-name">${it.name}</div>
             <div class="cou-why">${it.why}</div>
             <div class="cou-foot"><span>€${it.price}</span><button class="cou-add">＋</button></div>
           </div>`).join('')}
       </div>`),

    return_assurance_cart: () => card('rose', '30-day, free, no questions — same on this bag',
      'RETURN ASSURANCE · F46',
      `<div class="erp-row">
         <div class="erp-stat"><div class="erp-stat__big">30</div><div class="erp-stat__lab">DAYS</div></div>
         <div class="erp-stat"><div class="erp-stat__big">€0</div><div class="erp-stat__lab">LABEL</div></div>
         <div class="erp-stat"><div class="erp-stat__big">3d</div><div class="erp-stat__lab">REFUND</div></div>
       </div>
       <p class="lp-p">Try it on at home. Don't love it? Pre-paid label is in your account. 8,000+ drop-off points across Europe.</p>`),

    decision_help_cart: () => card('indigo', 'Still thinking? Here\'s what helps',
      'DECISION HELP · F51',
      `<div class="dh-grid">
         ${[
           { t:"Sleep on it",         d:"Save your bag — we'll hold your size for 3 days.", cta:"Save bag" },
           { t:"See it on you",       d:"Try the AR fitting room from your phone.",       cta:"Open AR" },
           { t:"Ask your tailor",     d:"Free 10-min video call with a London fitter.",   cta:"Book"     },
         ].map(it => `
           <div class="dh-card">
             <div class="dh-card__t">${it.t}</div>
             <div class="dh-card__d">${it.d}</div>
             <button class="dh-card__cta">${it.cta} →</button>
           </div>`).join('')}
       </div>`),

    price_freeze: () => card('orange', 'Freeze this price for 7 days',
      'PRICE FREEZE · F53 · F51',
      `<div class="pf-row">
         <div class="pf-icon">❄</div>
         <div class="pf-copy">
           <div class="pf-title">€984 today.</div>
           <div class="pf-sub">If the price drops, we honor today's. If it rises, you still pay €984 within 7 days.</div>
         </div>
         <button class="lp-btn-primary pf-btn">Freeze price</button>
       </div>`),

    gift_options: () => card('amber', 'Sending this as a gift?',
      'GIFT OPTIONS',
      `<div class="go-row">
         <label class="go-toggle">
           <input type="checkbox" /> <span>Add gift wrap (€8)</span>
         </label>
         <label class="go-toggle">
           <input type="checkbox" /> <span>Hide prices on packing slip</span>
         </label>
         <label class="go-toggle">
           <input type="checkbox" checked /> <span>Add a hand-written note</span>
         </label>
       </div>`),

    saved_for_later: () => card('indigo', 'You saved 3 items for later',
      'SAVED · F51 · F53',
      `<div class="lp-row lp-row--3">
         ${[
           { svg:'tuxedo', name:'Sandro Peak-Lapel',   price:720, days:4 },
           { svg:'shoe',   name:'Edward Green Oxford', price:1140,days:11},
           { svg:'watch',  name:'NOMOS Tangente',      price:1980,days:18},
         ].map(it => `
           <div class="rv-card">
             ${tile(it.svg,'100%',100,'#e8e9f7')}
             <div class="rv-card__name">${it.name}</div>
             <div class="rv-card__row"><span>€${it.price}</span><span class="rv-card__when">${it.days}d saved</span></div>
           </div>`).join('')}
       </div>`),
  };

  // ───────────────────────────────────────────────────────────────────────────
  // CHECKOUT widgets
  // ───────────────────────────────────────────────────────────────────────────
  const CHECKOUT = {
    order_summary: () => card('slate', 'Order summary',
      'CHECKOUT · YOUR ORDER',
      `<div class="os-list">
         ${[
           { brand:'BOSS', name:'Slim-Fit Tuxedo · 42R', qty:1, price:895 },
           { brand:'ALBINI',name:'Marcella Bow Shirt · M', qty:1, price:89 },
         ].map(it => `
           <div class="os-row">
             ${tile('tuxedo',60,72,'#f1f2f4')}
             <div class="os-meta">
               <div class="os-meta__brand">${it.brand}</div>
               <div class="os-meta__name">${it.name}</div>
             </div>
             <div class="os-price">€${it.price}</div>
           </div>`).join('')}
       </div>
       <div class="os-totals">
         <div><span>Subtotal</span><span>€984</span></div>
         <div><span>Shipping</span><span>FREE</span></div>
         <div><span>VAT (incl.)</span><span>€164</span></div>
         <div class="os-totals__big"><span>Total</span><span>€984</span></div>
       </div>`),

    express_payment: () => card('emerald', 'Skip the form',
      'EXPRESS · F52',
      `<div class="ex-row">
         <button class="ex-btn ex-btn--apple">  Pay</button>
         <button class="ex-btn ex-btn--gpay">G Pay</button>
         <button class="ex-btn ex-btn--paypal">PayPal</button>
         <button class="ex-btn ex-btn--klarna">Klarna</button>
       </div>
       <div class="ex-or">or fill in the form below</div>`),

    trust_signals: () => card('emerald', 'You\'re in safe hands',
      'TRUST · F52',
      `<div class="ts-grid">
         ${[
           { ico:'◑', t:'PCI-DSS Level 1', d:'Same standard as your bank.' },
           { ico:'⚿', t:'Encrypted', d:'TLS 1.3 end-to-end.' },
           { ico:'✓', t:'9.4 Trustpilot', d:'42,108 reviews.' },
           { ico:'$', t:'Buyer protection', d:'Item not as described? Full refund.' },
         ].map(s => `
           <div class="ts-card">
             <div class="ts-card__ico">${s.ico}</div>
             <div class="ts-card__t">${s.t}</div>
             <div class="ts-card__d">${s.d}</div>
           </div>`).join('')}
       </div>`),

    shipping_options: () => card('slate', 'Shipping',
      'SHIPPING',
      `<div class="sh-list">
         ${[
           { lab:'Standard · DHL',     eta:'Thu, May 23',  price:'FREE', on:true  },
           { lab:'Next Day · DHL',     eta:'Wed, May 22',  price:'€12',  on:false },
           { lab:'Saturday delivery',  eta:'Sat, May 25',  price:'€18',  on:false },
           { lab:'Pickup point',       eta:'Wed, May 22',  price:'FREE', on:false },
         ].map(s => `
           <label class="sh-row ${s.on?'sh-row--on':''}">
             <input type="radio" name="ship" ${s.on?'checked':''} />
             <div class="sh-row__main">
               <div class="sh-row__lab">${s.lab}</div>
               <div class="sh-row__eta">${s.eta}</div>
             </div>
             <div class="sh-row__price">${s.price}</div>
           </label>`).join('')}
       </div>`),

    return_micro: () => card('rose', '30-day returns, on us',
      'RETURNS · F46',
      `<div class="rm-row">
         <div class="rm-ico">↩</div>
         <div class="rm-copy">
           <div class="rm-t">Free returns within 30 days · Refund in 3 days</div>
           <div class="rm-d">Pre-paid label, 8,000+ drop-off points. We email you the label automatically.</div>
         </div>
       </div>`),

    price_lock_assurance: () => card('orange', 'Price-lock guarantee',
      'PRICE LOCK · F53',
      `<div class="pla-row">
         <div class="pla-icon">€</div>
         <div class="pla-copy">
           <div class="pla-t">If the price drops in 14 days, we refund the difference.</div>
           <div class="pla-d">Automatic. No claim form. We email you a credit note.</div>
         </div>
       </div>`),
  };

  // ───────────────────────────────────────────────────────────────────────────
  // POST-PURCHASE widgets
  // ───────────────────────────────────────────────────────────────────────────
  const POST = {
    order_status: () => card('slate', 'Your tuxedo, in motion',
      'ORDER #94821',
      `<div class="osh-timeline">
         ${[
           { lab:'Order placed',  date:'Mon · 14:22',  on:'done' },
           { lab:'Picked',        date:'Tue · 09:08',  on:'done' },
           { lab:'Shipped',       date:'Tue · 18:40',  on:'now'  },
           { lab:'Out for delivery', date:'Thu · est', on:'next' },
           { lab:'Delivered',     date:'Thu · est',    on:'next' },
         ].map((s,i,arr) => `
           <div class="osh-step osh-step--${s.on}">
             <span class="osh-dot"></span>
             <div class="osh-lab">${s.lab}</div>
             <div class="osh-date">${s.date}</div>
             ${i<arr.length-1?'<span class="osh-line"></span>':''}
           </div>`).join('')}
       </div>
       <p class="lp-p">DHL tracking <b>JD0123456789DE</b> · arriving Thursday, May 23.</p>`),

    care_guide: () => card('teal', 'How to keep this tuxedo for 10 years',
      'CARE GUIDE · F62',
      `<div class="cg-grid">
         ${[
           { ico:'❄', t:'After wearing',     d:'Hang on a wide wooden hanger overnight.' },
           { ico:'⌖', t:'Brush, don\'t wash',d:'Soft horsehair brush. Steam, never iron.' },
           { ico:'⌬', t:'Dry clean rarely',  d:'Twice a year is plenty. Specialist only.' },
           { ico:'☐', t:'Storage',           d:'Garment bag, cedar block, not in plastic.' },
         ].map(s => `
           <div class="cg-card">
             <div class="cg-card__ico">${s.ico}</div>
             <div class="cg-card__t">${s.t}</div>
             <div class="cg-card__d">${s.d}</div>
           </div>`).join('')}
       </div>`,
      `<button class="lp-btn-ghost">Download the BOSS care PDF →</button>`),

    style_companion: () => card('fuchsia', 'Now build the rest',
      'STYLE COMPANION · F61 · F12',
      `<div class="sc-row">
         <div class="sc-anchor" style="background:#1a1a1f;">${SVG.mannequin()}<span class="sc-anchor__lab">YOUR TUX</span></div>
         <div class="sc-items">
           ${[
             { name:'Albini Marcella Shirt', why:'The traditional dress-shirt partner.', price:115 },
             { name:'Drake\'s Self-Tie Bow',why:'Adjustable silk, evening-grade.', price:65 },
             { name:'C&J Black Oxford',     why:'Polished, not patent.', price:285 },
             { name:'Onyx Shirt Studs',     why:'Replace the buttons. Old-school.', price:110 },
           ].map((it,i) => `
             <div class="sc-item">
               <span class="sc-item__num">0${i+1}</span>
               <div class="sc-item__meta">
                 <div class="sc-item__name">${it.name}</div>
                 <div class="sc-item__why">${it.why}</div>
               </div>
               <div class="sc-item__price">€${it.price}</div>
               <button class="sc-item__add">＋</button>
             </div>`).join('')}
         </div>
       </div>`),

    repeat_in_color: () => card('indigo', 'Get it again, in another colour',
      'REPEAT · F64',
      `<div class="lp-row lp-row--4">
         ${[
           { lab:'Midnight Blue', bg:'#0e1a3a', delta:'+€0',  prim:true },
           { lab:'Cream',         bg:'#e8e1d3', delta:'+€55' },
           { lab:'Burgundy',      bg:'#3a1a25', delta:'+€80' },
           { lab:'Forest',        bg:'#1a2f24', delta:'+€80' },
         ].map(c => `
           <div class="rc-card">
             <div class="rc-sw" style="background:${c.bg};"></div>
             <div class="rc-name">${c.lab}</div>
             <div class="rc-delta ${c.prim?'rc-delta--prim':''}">${c.delta}</div>
             <button class="lp-btn-ghost rc-btn">Reorder</button>
           </div>`).join('')}
       </div>`),

    wardrobe_check: () => card('rose', 'A check-in — does this still feel like you?',
      'WARDROBE CHECK · F63',
      `<div class="wc-grid">
         ${[
           { lab:'Yes, it nails it.',     col:'#0c5234' },
           { lab:'OK but not "wow".',     col:'#7a4e0a' },
           { lab:'Not quite. Returning.', col:'#7a1c2a' },
         ].map(o => `
           <button class="wc-btn" style="border-color:${o.col};color:${o.col};">${o.lab}</button>`).join('')}
       </div>
       <p class="lp-p">Your honest read teaches our stylists what to push next. 91% of customers answer; we never spam this.</p>`),

    review_prompt: () => card('amber', 'How was the fit? 60 seconds, real impact',
      'REVIEW PROMPT',
      `<div class="rp-row">
         <div class="rp-stars">★★★★★</div>
         <div class="rp-prompts">
           ${['Fit was…','Fabric was…','Tailoring was…','Worth €895?'].map(p => `
             <button class="rp-pill">${p}</button>`).join('')}
         </div>
         <button class="lp-btn-primary">Write review · 60s</button>
       </div>`),

    referral_thanks: () => card('emerald', 'Bring a friend, get €50 each',
      'REFERRAL',
      `<div class="rt-row">
         <div class="rt-code">
           <div class="rt-code__lab">YOUR CODE</div>
           <div class="rt-code__val">HUGH50</div>
         </div>
         <p class="lp-p" style="flex:1;">Share with one friend. When they spend over €200, you both get €50 in store credit. No cap — refer the whole wedding party.</p>
         <button class="lp-btn-ghost">Copy link</button>
       </div>`),

    coordinate_recent: () => card('fuchsia', 'Coordinate with your recent buys',
      'COORDINATE · F61 · F64',
      `<div class="lp-row lp-row--4">
         ${[
           { svg:'shoe',  name:'Velvet Loafer',     price:285, w:'For the same tux' },
           { svg:'shirt', name:'Pleated Dress Shirt',price:135,w:'A more formal alt' },
           { svg:'bow',   name:'Midnight Bow Tie',  price:75, w:'Match midnight blue' },
           { svg:'belt',  name:'Patent Dress Belt', price:95, w:'Slim, low-shine' },
         ].map(it => `
           <div class="cou-card">
             ${tile(it.svg,'100%',80,'#f7e7f4')}
             <div class="cou-name">${it.name}</div>
             <div class="cou-why">${it.w}</div>
             <div class="cou-foot"><span>€${it.price}</span><button class="cou-add">＋</button></div>
           </div>`).join('')}
       </div>`),
  };

  // ── Public registry by page id ────────────────────────────────────────────
  window.PageWidgets = {
    home: HOME,
    search: SEARCH,
    plp: PLP,
    cart: CART,
    checkout: CHECKOUT,
    post_purchase: POST,
  };
})();
