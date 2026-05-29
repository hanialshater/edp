// Shared helpers for the "Solving with unknown parameters" blog series.
// Inlined into each post's <script> so files are self-contained.
//
// Provides: rng, gauss, beta, clamp, COLORS, Chart, mod (modular helpers).
// Vanilla JS, no deps, ~180 lines.

const COLORS = {
  blue:    '#4c8df6',
  green:   '#5fd2a3',
  orange:  '#f0a058',
  purple:  '#c879f0',
  red:     '#e16c6c',
  pink:    '#ff7eb6',
  dim:     '#5b6378',
  faint:   '#3a4358',
  fg:      '#e6edf3',
  bg:      '#0e1626',
  cycle: ['#4c8df6','#5fd2a3','#f0a058','#c879f0','#e16c6c'],
};

// Deterministic seeded RNG (mulberry32). Returns a function: rng() -> [0,1).
function rng(seed) {
  let s = seed | 0 || 1;
  return function() {
    s = (s + 0x6D2B79F5) | 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Standard normal via Box-Muller. Pass any 0-arg uniform RNG.
function gauss(rand) {
  let u = rand() || 1e-12, v = rand();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

// Cheap beta(a,b) sampler: gamma ratio approximation, fine for TS demo scale.
function beta(a, b, rand) {
  const x = Math.pow(rand(), 1 / Math.max(a, 0.01));
  const y = Math.pow(rand(), 1 / Math.max(b, 0.01));
  return x / (x + y);
}

function clamp(x, lo, hi) { return Math.max(lo, Math.min(hi, x)); }

function argmax(arr) {
  let i = 0;
  for (let j = 1; j < arr.length; j++) if (arr[j] > arr[i]) i = j;
  return i;
}

// ---------------------------------------------------------------
// Minimal canvas chart: multiple named lines, autoscaled, high-DPI.
//
// const c = new Chart(canvasEl, {xlabel:'pulls', ylabel:'regret'});
// c.line('UCB', COLORS.blue);
// c.push('UCB', x, y);    // x is independent var, y is dependent
// c.render();             // call when data changes
// c.reset();              // clear all lines
//
class Chart {
  constructor(canvas, opts) {
    this.canvas = canvas;
    this.opts = Object.assign({
      xlabel: '', ylabel: '', padding: {l: 44, r: 12, t: 16, b: 28},
      grid: 4, yMin: null, yMax: null, xMin: 0, xMax: null,
    }, opts || {});
    this.series = {};   // name -> {color, points: [[x,y],...]}
  }
  line(name, color) {
    this.series[name] = { color: color || COLORS.cycle[Object.keys(this.series).length % 5], points: [] };
    return this;
  }
  push(name, x, y) {
    if (!this.series[name]) this.line(name);
    this.series[name].points.push([x, y]);
  }
  reset() {
    for (const k in this.series) this.series[k].points = [];
  }
  remove(name) {
    delete this.series[name];
  }
  _bounds() {
    let xMin = this.opts.xMin, xMax = this.opts.xMax;
    let yMin = this.opts.yMin, yMax = this.opts.yMax;
    let any = false;
    for (const k in this.series) {
      const pts = this.series[k].points;
      if (!pts.length) continue;
      any = true;
      for (const [x, y] of pts) {
        if (xMax === null || x > xMax) xMax = x;
        if (yMax === null || y > yMax) yMax = y;
        if (yMin === null || y < yMin) yMin = y;
      }
    }
    if (!any) return null;
    if (xMax === null) xMax = 1;
    if (yMax === null) yMax = 1;
    if (yMin === null) yMin = 0;
    if (yMax - yMin < 1e-6) yMax = yMin + 1;
    return { xMin, xMax, yMin, yMax };
  }
  render() {
    const c = this.canvas;
    const dpr = window.devicePixelRatio || 1;
    const W = c.clientWidth, H = c.clientHeight || c.height;
    c.width = W * dpr; c.height = H * dpr;
    const ctx = c.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const p = this.opts.padding;
    const pw = W - p.l - p.r, ph = H - p.t - p.b;
    // grid
    ctx.strokeStyle = 'rgba(255,255,255,0.05)';
    ctx.lineWidth = 1;
    ctx.font = '11px ui-monospace, Menlo, monospace';
    ctx.fillStyle = COLORS.dim;
    for (let i = 0; i <= this.opts.grid; i++) {
      const y = p.t + (i / this.opts.grid) * ph;
      ctx.beginPath(); ctx.moveTo(p.l, y); ctx.lineTo(p.l + pw, y); ctx.stroke();
    }
    const b = this._bounds();
    if (!b) {
      ctx.fillText('— waiting for data —', p.l + 12, p.t + ph / 2);
      if (this.opts.xlabel) ctx.fillText(this.opts.xlabel, W - 60, H - 6);
      if (this.opts.ylabel) ctx.fillText(this.opts.ylabel, 4, p.t + 8);
      return;
    }
    const xToPx = x => p.l + ((x - b.xMin) / (b.xMax - b.xMin || 1)) * pw;
    const yToPx = y => p.t + (1 - (y - b.yMin) / (b.yMax - b.yMin || 1)) * ph;
    // axis labels
    ctx.fillText(b.yMax.toFixed(b.yMax > 10 ? 0 : 2), 4, p.t + 4);
    ctx.fillText(b.yMin.toFixed(b.yMin > 10 ? 0 : 2), 4, p.t + ph + 4);
    ctx.fillText(this.opts.xlabel ? `${this.opts.xlabel}: ${b.xMax|0}` : `${b.xMax|0}`, W - 100, H - 4);
    if (this.opts.ylabel) { ctx.save(); ctx.fillText(this.opts.ylabel, 4, p.t + 16); ctx.restore(); }
    // lines
    for (const name in this.series) {
      const s = this.series[name];
      if (s.points.length < 2) continue;
      ctx.strokeStyle = s.color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i < s.points.length; i++) {
        const [x, y] = s.points[i];
        const px = xToPx(x), py = yToPx(y);
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
      }
      ctx.stroke();
    }
    // legend (top right)
    let lx = W - p.r - 10, ly = p.t + 8;
    ctx.textAlign = 'right';
    for (const name in this.series) {
      ctx.fillStyle = this.series[name].color;
      ctx.fillText(name, lx, ly);
      ly += 14;
    }
    ctx.textAlign = 'left';
  }
}
