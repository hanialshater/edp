// Shared product data + SVG illustrations for thematic recommendations widgets.
// SVGs are stylized "photograph-ish" renderings of fashion items on a light bg,
// designed to read as product imagery in a clean modern retail layout.

// ─── SVG ILLUSTRATIONS ─────────────────────────────────────────────────────

const Tuxedo = ({ scale = 1 }) => (
  <svg viewBox="0 0 200 280" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    {/* shadow */}
    <ellipse cx="100" cy="270" rx="55" ry="4" fill="#000" opacity="0.08" />
    {/* trousers */}
    <path d="M 70 165 L 65 268 L 92 268 L 100 175 L 108 268 L 135 268 L 130 165 Z" fill="#15151a" />
    {/* jacket back */}
    <path d="M 55 80 Q 55 70 75 65 L 125 65 Q 145 70 145 80 L 148 170 L 130 175 L 100 165 L 70 175 L 52 170 Z" fill="#1a1a1f" />
    {/* lapels */}
    <path d="M 75 65 L 95 75 L 90 150 L 100 165 L 100 90 Z" fill="#0c0c10" />
    <path d="M 125 65 L 105 75 L 110 150 L 100 165 L 100 90 Z" fill="#0c0c10" />
    {/* shirt */}
    <path d="M 92 70 L 108 70 L 108 165 L 100 170 L 92 165 Z" fill="#fafaf7" />
    {/* bow tie */}
    <path d="M 88 80 L 100 86 L 100 92 L 88 98 Z M 112 80 L 100 86 L 100 92 L 112 98 Z" fill="#0a0a0d" />
    <rect x="98" y="84" width="4" height="10" fill="#0a0a0d" />
    {/* buttons */}
    <circle cx="100" cy="120" r="1.2" fill="#0a0a0d" />
    <circle cx="100" cy="135" r="1.2" fill="#0a0a0d" />
    <circle cx="100" cy="150" r="1.2" fill="#0a0a0d" />
    {/* collar */}
    <path d="M 88 70 L 100 76 L 112 70 L 108 80 L 100 84 L 92 80 Z" fill="#0c0c10" />
  </svg>
);

const BowTie = () => (
  <svg viewBox="0 0 200 200" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="155" rx="50" ry="3" fill="#000" opacity="0.08" />
    <path d="M 30 75 Q 35 70 45 72 L 90 95 L 90 115 L 45 138 Q 35 140 30 135 Z" fill="#1a1a1f" />
    <path d="M 170 75 Q 165 70 155 72 L 110 95 L 110 115 L 155 138 Q 165 140 170 135 Z" fill="#1a1a1f" />
    <rect x="88" y="92" width="24" height="26" rx="2" fill="#0a0a0d" />
    {/* texture */}
    <g opacity="0.15" fill="#fff">
      <circle cx="55" cy="90" r="0.8" /><circle cx="65" cy="95" r="0.8" /><circle cx="75" cy="100" r="0.8" />
      <circle cx="55" cy="115" r="0.8" /><circle cx="65" cy="120" r="0.8" /><circle cx="75" cy="115" r="0.8" />
      <circle cx="135" cy="100" r="0.8" /><circle cx="145" cy="95" r="0.8" />
      <circle cx="135" cy="120" r="0.8" /><circle cx="145" cy="115" r="0.8" />
    </g>
  </svg>
);

const OxfordShoe = () => (
  <svg viewBox="0 0 240 160" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="120" cy="135" rx="95" ry="5" fill="#000" opacity="0.12" />
    {/* sole */}
    <path d="M 30 120 Q 25 130 35 132 L 210 132 Q 225 130 215 118 Z" fill="#0a0a0d" />
    {/* shoe body */}
    <path d="M 35 118 Q 30 90 50 78 Q 90 60 140 65 Q 200 72 215 100 Q 218 115 210 122 L 40 122 Q 32 122 35 118 Z" fill="#1a1a1f" />
    {/* shine highlight */}
    <path d="M 50 85 Q 90 72 150 75 Q 195 80 205 95" stroke="#3a3a45" strokeWidth="2" fill="none" opacity="0.7" />
    <path d="M 60 92 Q 100 82 160 85" stroke="#55555f" strokeWidth="1" fill="none" opacity="0.5" />
    {/* laces area */}
    <path d="M 95 95 L 95 118 L 140 118 L 145 95 Z" fill="#0a0a0d" />
    <line x1="100" y1="100" x2="140" y2="100" stroke="#fafaf7" strokeWidth="0.8" opacity="0.6" />
    <line x1="100" y1="106" x2="140" y2="106" stroke="#fafaf7" strokeWidth="0.8" opacity="0.6" />
    <line x1="100" y1="112" x2="140" y2="112" stroke="#fafaf7" strokeWidth="0.8" opacity="0.6" />
  </svg>
);

const Shirt = () => (
  <svg viewBox="0 0 200 260" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="250" rx="60" ry="4" fill="#000" opacity="0.08" />
    {/* sleeves */}
    <path d="M 50 60 L 30 90 L 35 200 L 65 195 L 70 75 Z" fill="#fafaf7" stroke="#e8e8e3" strokeWidth="0.5" />
    <path d="M 150 60 L 170 90 L 165 200 L 135 195 L 130 75 Z" fill="#fafaf7" stroke="#e8e8e3" strokeWidth="0.5" />
    {/* body */}
    <path d="M 65 55 Q 65 50 75 50 L 125 50 Q 135 50 135 55 L 138 240 L 62 240 Z" fill="#ffffff" stroke="#e8e8e3" strokeWidth="0.5" />
    {/* collar */}
    <path d="M 75 50 L 95 40 L 100 55 L 105 40 L 125 50 L 122 65 L 100 58 L 78 65 Z" fill="#ffffff" stroke="#d8d8d3" strokeWidth="0.6" />
    {/* placket */}
    <line x1="100" y1="58" x2="100" y2="240" stroke="#e8e8e3" strokeWidth="0.8" />
    {/* buttons */}
    {[80, 110, 140, 170, 200, 225].map(y => (
      <circle key={y} cx="100" cy={y} r="1.2" fill="#d0d0c8" />
    ))}
    {/* shadow fold */}
    <path d="M 65 55 L 70 60 L 72 235 L 62 240 Z" fill="#000" opacity="0.04" />
  </svg>
);

const Cufflinks = () => (
  <svg viewBox="0 0 200 200" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="160" rx="60" ry="4" fill="#000" opacity="0.08" />
    {/* left cufflink */}
    <g>
      <circle cx="65" cy="95" r="22" fill="#1a1a1f" />
      <circle cx="65" cy="95" r="22" fill="url(#gemL)" />
      <circle cx="65" cy="95" r="18" fill="#0a0a0d" />
      <circle cx="60" cy="90" r="4" fill="#3a3a3f" opacity="0.6" />
      <rect x="62" y="115" width="6" height="20" fill="#2a2a2f" />
      <ellipse cx="65" cy="138" rx="10" ry="3" fill="#1a1a1f" />
    </g>
    {/* right cufflink */}
    <g>
      <circle cx="135" cy="105" r="22" fill="#1a1a1f" />
      <circle cx="135" cy="105" r="18" fill="#0a0a0d" />
      <circle cx="130" cy="100" r="4" fill="#3a3a3f" opacity="0.6" />
      <rect x="132" y="125" width="6" height="20" fill="#2a2a2f" />
      <ellipse cx="135" cy="148" rx="10" ry="3" fill="#1a1a1f" />
    </g>
    <defs>
      <radialGradient id="gemL"><stop offset="0%" stopColor="#4a4a55" /><stop offset="100%" stopColor="#0a0a0d" /></radialGradient>
    </defs>
  </svg>
);

const PocketSquare = () => (
  <svg viewBox="0 0 200 180" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="155" rx="60" ry="4" fill="#000" opacity="0.08" />
    {/* folded square */}
    <path d="M 50 80 L 100 50 L 150 80 L 150 145 L 50 145 Z" fill="#ffffff" stroke="#e0e0d8" strokeWidth="0.6" />
    {/* fold lines */}
    <path d="M 50 80 L 100 110 L 150 80" stroke="#e8e8e3" strokeWidth="0.8" fill="none" />
    <path d="M 75 65 L 100 80 L 125 65" stroke="#e8e8e3" strokeWidth="0.6" fill="none" opacity="0.6" />
    <path d="M 100 50 L 100 145" stroke="#e8e8e3" strokeWidth="0.4" opacity="0.5" />
    {/* shadow */}
    <path d="M 50 80 L 100 110 L 100 145 L 50 145 Z" fill="#000" opacity="0.025" />
  </svg>
);

const Watch = () => (
  <svg viewBox="0 0 200 220" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="200" rx="40" ry="3" fill="#000" opacity="0.08" />
    {/* strap top */}
    <path d="M 80 30 L 120 30 L 122 80 L 78 80 Z" fill="#1a1a1f" />
    {/* strap bottom */}
    <path d="M 78 140 L 122 140 L 120 190 L 80 190 Z" fill="#1a1a1f" />
    {/* watch case */}
    <circle cx="100" cy="110" r="42" fill="#2a2a35" />
    <circle cx="100" cy="110" r="40" fill="#1a1a20" />
    <circle cx="100" cy="110" r="36" fill="#0c0c10" />
    {/* face */}
    <circle cx="100" cy="110" r="32" fill="#0a0a0d" />
    {/* indices */}
    {[0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330].map(deg => {
      const r = deg * Math.PI / 180;
      const x1 = 100 + Math.sin(r) * 27;
      const y1 = 110 - Math.cos(r) * 27;
      const x2 = 100 + Math.sin(r) * 30;
      const y2 = 110 - Math.cos(r) * 30;
      return <line key={deg} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#d0d0c8" strokeWidth="1" />;
    })}
    {/* hands */}
    <line x1="100" y1="110" x2="100" y2="90" stroke="#fafaf7" strokeWidth="1.8" strokeLinecap="round" />
    <line x1="100" y1="110" x2="115" y2="115" stroke="#fafaf7" strokeWidth="1.2" strokeLinecap="round" />
    <circle cx="100" cy="110" r="1.5" fill="#c9764a" />
    {/* crown */}
    <rect x="142" y="105" width="6" height="10" fill="#2a2a35" />
  </svg>
);

const Cummerbund = () => (
  <svg viewBox="0 0 240 140" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="120" cy="120" rx="95" ry="4" fill="#000" opacity="0.08" />
    <path d="M 30 50 Q 25 45 35 42 L 205 42 Q 215 45 210 50 L 215 95 Q 215 105 200 108 L 40 108 Q 25 105 25 95 Z" fill="#1a1a1f" />
    {/* pleats */}
    {[50, 65, 80, 95, 110, 125, 140, 155, 170, 185].map(x => (
      <line key={x} x1={x} y1="50" x2={x} y2="100" stroke="#0a0a0d" strokeWidth="2" opacity="0.5" />
    ))}
    {/* top highlight */}
    <path d="M 30 50 L 210 50" stroke="#3a3a45" strokeWidth="1" opacity="0.5" />
  </svg>
);

const Studs = () => (
  <svg viewBox="0 0 200 200" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="170" rx="60" ry="4" fill="#000" opacity="0.08" />
    {/* row of studs */}
    {[0, 1, 2, 3].map(i => (
      <g key={i} transform={`translate(${40 + i * 38}, ${85 + (i % 2) * 8})`}>
        <circle cx="0" cy="0" r="12" fill="#1a1a1f" />
        <circle cx="0" cy="0" r="9" fill="url(#studG)" />
        <circle cx="-2" cy="-2" r="3" fill="#5a5a65" opacity="0.6" />
      </g>
    ))}
    <defs>
      <radialGradient id="studG"><stop offset="0%" stopColor="#3a3a45" /><stop offset="100%" stopColor="#0a0a0d" /></radialGradient>
    </defs>
  </svg>
);

const Belt = () => (
  <svg viewBox="0 0 240 140" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="120" cy="115" rx="95" ry="3" fill="#000" opacity="0.08" />
    {/* strap */}
    <rect x="30" y="55" width="180" height="20" fill="#1a1a1f" />
    <rect x="30" y="55" width="180" height="3" fill="#3a3a45" opacity="0.4" />
    {/* buckle */}
    <rect x="135" y="48" width="30" height="34" rx="2" fill="#c9c2b3" stroke="#a09682" strokeWidth="0.8" />
    <rect x="140" y="53" width="20" height="24" rx="1" fill="#1a1a1f" />
    <line x1="150" y1="48" x2="150" y2="82" stroke="#a09682" strokeWidth="1.5" />
    {/* tip */}
    <path d="M 30 55 L 22 60 L 22 70 L 30 75 Z" fill="#0a0a0d" />
    {/* holes */}
    {[185, 195, 205].map(x => (
      <circle key={x} cx={x} cy="65" r="1.5" fill="#0a0a0d" />
    ))}
  </svg>
);

const Cologne = () => (
  <svg viewBox="0 0 160 240" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="80" cy="225" rx="45" ry="4" fill="#000" opacity="0.08" />
    {/* bottle */}
    <path d="M 45 90 L 45 215 Q 45 220 50 220 L 110 220 Q 115 220 115 215 L 115 90 Z" fill="url(#bottleG)" stroke="#2a2a35" strokeWidth="0.8" />
    {/* neck */}
    <rect x="65" y="60" width="30" height="32" fill="#1a1a1f" />
    {/* cap */}
    <rect x="60" y="30" width="40" height="35" rx="2" fill="#0a0a0d" />
    <rect x="60" y="30" width="40" height="6" rx="2" fill="#2a2a35" />
    {/* label */}
    <rect x="55" y="140" width="50" height="50" fill="#fafaf7" />
    <line x1="65" y1="155" x2="95" y2="155" stroke="#1a1a1f" strokeWidth="1" />
    <line x1="65" y1="165" x2="90" y2="165" stroke="#1a1a1f" strokeWidth="0.5" />
    <line x1="65" y1="175" x2="92" y2="175" stroke="#1a1a1f" strokeWidth="0.5" />
    <defs>
      <linearGradient id="bottleG" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stopColor="#1a1a25" />
        <stop offset="50%" stopColor="#3a3a48" />
        <stop offset="100%" stopColor="#1a1a25" />
      </linearGradient>
    </defs>
  </svg>
);

const Suspenders = () => (
  <svg viewBox="0 0 200 240" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="100" cy="225" rx="60" ry="4" fill="#000" opacity="0.08" />
    {/* straps Y-shape */}
    <path d="M 55 30 L 60 130 L 95 160 L 95 210 L 105 210 L 105 160 L 140 130 L 145 30" stroke="#1a1a1f" strokeWidth="14" fill="none" strokeLinecap="round" />
    {/* clips */}
    <rect x="48" y="20" width="14" height="18" rx="2" fill="#c9c2b3" />
    <rect x="138" y="20" width="14" height="18" rx="2" fill="#c9c2b3" />
    <rect x="90" y="200" width="20" height="22" rx="2" fill="#c9c2b3" />
    {/* center adjuster */}
    <rect x="95" y="155" width="10" height="14" fill="#c9c2b3" />
  </svg>
);

const Mannequin = () => (
  <svg viewBox="0 0 260 400" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">
    <ellipse cx="130" cy="392" rx="70" ry="4" fill="#000" opacity="0.1" />
    {/* head */}
    <ellipse cx="130" cy="50" rx="22" ry="26" fill="#d8c4ad" />
    {/* hair */}
    <path d="M 110 36 Q 130 22 152 36 Q 152 28 145 25 Q 130 18 115 25 Q 108 30 110 36" fill="#2a221a" />
    {/* neck */}
    <rect x="120" y="72" width="20" height="14" fill="#c9b59b" />
    {/* shirt collar */}
    <path d="M 105 86 L 130 92 L 155 86 L 158 100 L 130 96 L 102 100 Z" fill="#fafaf7" />
    {/* jacket */}
    <path d="M 75 95 Q 75 88 95 85 L 165 85 Q 185 88 185 95 L 195 240 L 165 250 L 130 235 L 95 250 L 65 240 Z" fill="#1a1a1f" />
    {/* lapels */}
    <path d="M 95 85 L 122 100 L 118 215 L 130 230 L 130 110 Z" fill="#0a0a0d" />
    <path d="M 165 85 L 138 100 L 142 215 L 130 230 L 130 110 Z" fill="#0a0a0d" />
    {/* shirt visible */}
    <path d="M 122 95 L 138 95 L 138 230 L 130 235 L 122 230 Z" fill="#fafaf7" />
    {/* bow tie */}
    <path d="M 116 102 L 130 110 L 130 118 L 116 124 Z M 144 102 L 130 110 L 130 118 L 144 124 Z" fill="#0a0a0d" />
    <rect x="127" y="106" width="6" height="14" fill="#0a0a0d" />
    {/* trousers */}
    <path d="M 95 245 L 88 388 L 122 388 L 130 255 L 138 388 L 172 388 L 165 245 Z" fill="#15151a" />
    {/* arms */}
    <path d="M 75 100 L 60 220 L 80 225 L 92 110 Z" fill="#1a1a1f" />
    <path d="M 185 100 L 200 220 L 180 225 L 168 110 Z" fill="#1a1a1f" />
    {/* hands */}
    <circle cx="70" cy="228" r="8" fill="#c9b59b" />
    <circle cx="190" cy="228" r="8" fill="#c9b59b" />
    {/* shoes */}
    <ellipse cx="100" cy="390" rx="18" ry="5" fill="#0a0a0d" />
    <ellipse cx="160" cy="390" rx="18" ry="5" fill="#0a0a0d" />
  </svg>
);

// Generic photo-style frame wrapping an SVG illustration on a soft gray bg.
const Photo = ({ children, bg = '#f4f4f1', ratio = '4/5', radius = 4 }) => (
  <div style={{
    position: 'relative', width: '100%', aspectRatio: ratio, background: bg,
    borderRadius: radius, overflow: 'hidden', display: 'flex', alignItems: 'center', justifyContent: 'center',
  }}>
    <div style={{ width: '78%', height: '78%' }}>{children}</div>
  </div>
);

// ─── PRODUCT CATALOG ───────────────────────────────────────────────────────

const PRODUCTS = {
  shirt: { id: 'shirt', category: 'SHIRT', brand: 'Albini Milano', name: 'Crisp Poplin Shirt', price: 89, why: 'A sharp white base complements the suit\'s stark black.', img: Shirt, bg: '#f4f4f1' },
  bow: { id: 'bow', category: 'ACCESSORY', brand: 'Drake\'s', name: 'Silk Self-Tie Bow', price: 65, why: 'Classic texture against the plain black tuxedo.', img: BowTie, bg: '#f1efe9' },
  shoes: { id: 'shoes', category: 'SHOES', brand: 'Crockett & Jones', name: 'Polished Oxford Shoes', price: 285, why: 'Mirrors the suit\'s formal shine and sleek silhouette.', img: OxfordShoe, bg: '#efede7' },
  cummerbund: { id: 'cummerbund', category: 'ACCESSORY', brand: 'Eton', name: 'Satin Cummerbund Set', price: 95, why: 'Completes the traditional tuxedo line for cohesion.', img: Cummerbund, bg: '#f0eee8' },
  cufflinks: { id: 'cufflinks', category: 'JEWELLERY', brand: 'Lanvin', name: 'Minimalist Onyx Cufflinks', price: 145, why: 'Subtle accents that nod to the suit\'s elegance.', img: Cufflinks, bg: '#f3f1eb' },
  pocket: { id: 'pocket', category: 'ACCESSORY', brand: 'Tom Ford', name: 'White Silk Pocket Square', price: 55, why: 'A bright counterpoint that lifts the lapel.', img: PocketSquare, bg: '#f4f4f1' },
  watch: { id: 'watch', category: 'WATCH', brand: 'Junghans', name: 'Max Bill Automatic', price: 1190, why: 'Pared-back face suits formalwear without competing.', img: Watch, bg: '#efede6' },
  studs: { id: 'studs', category: 'JEWELLERY', brand: 'Lanvin', name: 'Onyx Shirt Studs (4-pack)', price: 110, why: 'Replace plain buttons for proper black-tie protocol.', img: Studs, bg: '#f3f1eb' },
  belt: { id: 'belt', category: 'ACCESSORY', brand: 'Anderson\'s', name: 'Satin Formal Belt', price: 75, why: 'Slim profile that disappears under the jacket line.', img: Belt, bg: '#f0eee8' },
  cologne: { id: 'cologne', category: 'FRAGRANCE', brand: 'Byredo', name: 'Bal d\'Afrique 50ml', price: 195, why: 'A warm vetiver finish for the evening.', img: Cologne, bg: '#eeece5' },
  suspenders: { id: 'suspenders', category: 'ACCESSORY', brand: 'Albert Thurston', name: 'Black Silk Braces', price: 95, why: 'Keeps the trouser line clean — no belt required.', img: Suspenders, bg: '#f1efe9' },
};

// Theme presets — each is a curated set of 5 product ids.
const THEMES = {
  blackTie: {
    id: 'blackTie',
    eyebrow: 'MODERN FORMAL ELEGANCE',
    title: 'Complete Your Black-Tie Look',
    subtitle: 'Elevate your slim-fit black tuxedo with these essential finishing touches.',
    items: ['shirt', 'bow', 'shoes', 'cummerbund', 'cufflinks'],
  },
  cocktail: {
    id: 'cocktail',
    eyebrow: 'AFTER-DARK · COCKTAIL',
    title: 'Style It for Cocktail Hour',
    subtitle: 'Dial it down — keep the tuxedo, lose the formality.',
    items: ['shirt', 'pocket', 'shoes', 'watch', 'cologne'],
  },
  wedding: {
    id: 'wedding',
    eyebrow: 'WEDDING GUEST',
    title: 'Dress for the Reception',
    subtitle: 'Refined, considered, and warm — the right notes for a black-tie wedding.',
    items: ['shirt', 'bow', 'shoes', 'pocket', 'cufflinks'],
  },
  modern: {
    id: 'modern',
    eyebrow: 'MODERN MINIMAL',
    title: 'A Pared-Back Take',
    subtitle: 'Strip back the traditional cues — let the cut do the talking.',
    items: ['shirt', 'shoes', 'watch', 'belt', 'cologne'],
  },
  traditional: {
    id: 'traditional',
    eyebrow: 'CLASSIC BLACK-TIE',
    title: 'The Traditional Tuxedo',
    subtitle: 'Every protocol observed — no shortcuts, no compromises.',
    items: ['shirt', 'bow', 'shoes', 'studs', 'suspenders'],
  },
};

const ANCHOR = {
  category: 'TUXEDO',
  brand: 'BOSS',
  name: 'Slim-Fit Black Wool Tuxedo',
  price: 895,
  size: '42',
  img: Tuxedo,
  bg: '#f1efe9',
};

Object.assign(window, {
  Tuxedo, BowTie, OxfordShoe, Shirt, Cufflinks, PocketSquare, Watch, Cummerbund, Studs, Belt, Cologne, Suspenders, Mannequin,
  Photo, PRODUCTS, THEMES, ANCHOR,
});
