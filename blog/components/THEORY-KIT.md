# Theory kit — match the bandit post's math/theory layer

Posts 2/3/4 should gain the same theory affordances `01-bandit/index.html` has:
formatted equation lines (`.latex-line`), intuition notes (`.math-intuition`),
and a tabbed algorithm explainer (`.algo-box` + `.algo-tab`/`.algo-panel`), plus
optional side-by-side `.algo-grid`/`.algo-card`. Keep everything offline/inline.

## 1. CSS to ensure present in each post `<head>` (add any that are missing)

```css
.latex-line{font-family:var(--mono);font-size:13px;line-height:1.55;color:var(--fg);background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:6px;padding:8px 10px;margin:8px 0;overflow-x:auto}
.latex-line .label{color:var(--dim);margin-right:8px}
.latex-line .eq{font-size:14px;color:#fff}
.latex-line sup,.latex-line sub{line-height:0}
.math-intuition{color:var(--dim);font-size:13.5px;margin-top:8px}
.algo-box{background:var(--code);border:1px solid var(--border);border-left:3px solid var(--accent);border-radius:8px;padding:15px;margin:18px 0;font-size:14px}
.algo-box .title{font-family:var(--mono);font-size:11px;color:var(--accent);text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px}
.algo-tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px}
.algo-tab{font-family:var(--mono);font-size:12px;padding:6px 10px;background:var(--card2);color:var(--fg);border:1px solid var(--border);border-radius:6px;cursor:pointer}
.algo-tab.on{background:var(--accent2);border-color:var(--accent);color:var(--accent)}
.algo-panel{display:none;background:rgba(255,255,255,0.035);border:1px solid var(--border);border-radius:8px;padding:13px}
.algo-panel.on{display:block}
.algo-panel h4{margin:0 0 8px;font-size:15px;color:#fff}
.algo-panel p{margin:8px 0;color:var(--dim);line-height:1.48}
.algo-panel ul{margin:8px 0 0 18px;padding:0;color:var(--dim)}
.algo-panel li{margin:4px 0}
.algo-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.algo-card{background:rgba(255,255,255,0.035);border:1px solid var(--border);border-radius:8px;padding:12px}
.algo-card h4{margin:0 0 6px;font-size:14px;color:#fff}
.algo-card p{margin:7px 0;color:var(--dim);line-height:1.45}
.algo-card .formula{font-family:var(--mono);font-size:12px;color:var(--fg);background:rgba(255,255,255,0.04);border-radius:5px;padding:6px;margin:8px 0}
```
(`button{...}` base style already exists; `.algo-tab` above is self-sufficient.)

## 2. Tab-switch JS (add ONE copy inside the post's existing <script>, top level)

```js
document.querySelectorAll('.algo-tab').forEach(btn=>{
  btn.onclick=()=>{
    const key=btn.dataset.tab;
    const box=btn.closest('.algo-box');
    box.querySelectorAll('.algo-tab').forEach(b=>b.classList.toggle('on',b===btn));
    box.querySelectorAll('.algo-panel').forEach(p=>p.classList.toggle('on',p.dataset.panel===key));
  };
});
```
Note: scope to `btn.closest('.algo-box')` so multiple algo-boxes on one page work.

## 3. Equation-line markup pattern (use real HTML sub/sup, NOT MathJax)

```html
<div class="latex-line"><span class="label">Label:</span><span class="eq">P(i ≻ j) = σ(β(s<sub>i</sub> − s<sub>j</sub>))</span></div>
<p class="math-intuition"><strong>Intuition:</strong> one-sentence plain-language meaning.</p>
```

## 4. Per-post theory content to ADD (keep existing widgets/prose intact)

### 02-sort — Bradley-Terry + ranking + at-scale
- Upgrade the existing "Math object" mathbox to `.latex-line` rows:
  - Latent skills: `s_i ∈ ℝ`; true order = sort by s_i (desc).
  - Match (BT/logistic): `P(i ≻ j) = σ(β (s_i − s_j))`.
  - MM update used by the widget: `p_i ← (W_i) / Σ_{j≠i} n_ij /(p_i+p_j)`, `s_i=ln p_i` (note +0.5 smoothing).
  - Metric: Kendall `τ = (concordant − discordant) / C(n,2)`.
  - Comparison-sort budget: classical exact-oracle sort = `Θ(n log n)`; noisy oracle needs `Θ(log(1/δ)/Δ²)` repeats per close pair (gap Δ).
- New `.algo-box` "How the scheduler picks the next match" with tabs:
  round-robin, ladder (adjacent), active (boundary), and Elo-at-scale.
  - Elo (≈ online BT): `E_i = σ((R_i−R_j)/s_elo)`, `R_i ← R_i + K(1{i wins} − E_i)`,
    `s_elo = 400/ln 10`. One sentence on why Elo ≈ streaming Bradley-Terry.
  - Active/boundary: sample matches where `|s_i − s_j|` is small and counts low —
    the information is at the order boundary; explain top-k recall@K at scale
    (`recall@K = |est_topK ∩ true_topK| / K`) and the 50M all-pairs vs adaptive point.

### 03-shortest-path — semi-bandit + CombUCB + Dijkstra
- Keep Act-1 `.algo-box` (Dijkstra). Add a math object mathbox with `.latex-line`:
  - Edge means: `w_e` unknown; path cost `c(P) = Σ_{e∈P} w_e`.
  - Semi-bandit feedback: play path P, observe `{w_e + noise : e∈P}` (per-edge),
    vs bandit feedback: observe only `c(P)` (per-route).
  - Per-edge estimate + count: `ŵ_e = mean of samples`, `n_e`.
  - LCB optimism (the widget): `LCB_e = ŵ_e − β·σ·ŵ_e·sqrt(2 ln t /(n_e+1))`; choose
    `argmin_P Σ_{e∈P} LCB_e` via Dijkstra on LCBs.
  - Regret: `Σ_t (c(P_t) − c(P*))`.
- New `.algo-box` "Two ways to credit a path" with tabs:
  - CombUCB-on-edges (semi-bandit): Dijkstra on LCB; regret `Õ(|E|√T)` — linear in
    edges, knowledge shared across routes.
  - Route-as-an-arm (full bandit): UCB1 over enumerated routes; regret scales with
    the NUMBER of routes (exponential), no per-edge sharing.
  - Why semi-bandit wins: per-edge credit assignment; tie to the WPO paper's §5.2
    page-level-vs-per-slot attribution (the same axis).

### 04-tsp — combinatorial bandit over tours + 2-opt
- Keep Act-1 (Christofides/2-opt). Add a math object mathbox with `.latex-line`:
  - Distances `d_ij` unknown; tour cost `c(T) = Σ_{(i,j)∈T} d_ij`; `n!/(2n)` tours.
  - Semi-bandit: drive tour, observe each leg `d_ij + noise`; per-edge `d̂_ij, n_ij`.
  - LCB: `LCB_ij = d̂_ij − β·D̄·sqrt(ln t/(n_ij+1))`, `D̄` = global mean leg.
  - Solver: 2-opt local search on the LCB (or mean) matrix; cost vs optimum 7542.
  - The escape: `C(n,2)=1326` edge parameters, not `~10^65` tours.
- New `.algo-box` "Three tour strategies" with tabs:
  random tours; 2-opt on mean estimates (no exploration → biased by unseen edges =
  global mean); CombUCB = 2-opt on LCB (optimism explores short under-sampled edges).
  Each: one formula line + good/bad bullet.
- Optionally a short `.algo-grid` contrasting known-distance solvers
  (exact DP `O(2^n n²)`, Christofides `1.5×`, 2-opt local optimum).

## 5. Validate
For each edited post:
`node blog/components/test-post.mjs <post>/index.html` → 3/3 (offline, runs, nav).
Confirm the algo-tabs actually toggle (open the file; click tabs) and that all
equations render with plain HTML sub/sup (no external math lib).
