# Component workshop — build small, iterate, then compose

The CombUCB posts (sort / shortest-path / TSP) are being rebuilt around
concrete, pedagogical demos instead of abstract cards and dots:

- **02-sort** → *sports skill estimation*: animated 1v1 matches on a pitch,
  live counters, a leaderboard, Bradley-Terry skill bars converging to the
  true ranking. "Which pairs do you make play, and how often, to learn the
  table fastest?"
- **03-shortest-path** → *a real street map* with hidden travel times; walk
  a route, observe per-edge times, watch CombUCB-on-edges converge.
- **04-tsp** → *berlin52* (TSPLIB) drawn on a map; sketch tours, observe
  per-edge distances, watch 2-opt-on-LCB converge against the known optimum.

These widgets are big and need a lot of back-and-forth, so we build each
**visual component in isolation** first, get it right, then inline it into
the post. This folder is the workshop.

## Layout

```
components/
  README.md            ← this file (the workflow)
  index.html           ← gallery: open any component standalone
  test.mjs             ← dependency-free Node smoke test (DOM/canvas stub)
  shared/lib.js        ← canonical helpers (rng, gauss, BT fit, Chart, COLORS)
  sort/                ← components for post 2
  path/                ← components for post 3
  tsp/                 ← components for post 4
```

## The component contract

Each component is **one self-contained `.html` file** that works when opened
directly *and* exposes a reusable mount function so it can be embedded into a
post without edits.

```html
<script>
  // 1. PURE LOGIC first (no DOM): models, simulators, estimators.
  //    Copy-pasteable into the post; importable by test.mjs.
  // 2. function mountX(root, opts) { ... builds DOM inside `root` ... }
  // 3. expose it:
  window.__component = { name: 'sort/pitch-match', mount: mountX };
  // 4. auto-mount when opened standalone:
  if (document.getElementById('stage')) mountX(document.getElementById('stage'), {});
</script>
```

Rules that make components portable:
- **No external assets / network.** Inline everything (SVG, data, fonts off).
- **Dark theme** matching the blog (`--bg:#0b1220`, accent `#4c8df6`, …).
- **`mount(root, opts)` owns its DOM** — it creates every element it needs
  inside `root`, never assumes global IDs. This is what lets two components
  coexist on one page when composed.
- **Deterministic.** Seeded RNG; `opts.seed` reproduces a run.
- **Pure logic separated from rendering**, so `test.mjs` can exercise the
  model headlessly and so the math is trivially auditable.

## Per-component loop (the back-and-forth)

1. **Spec** in 2-3 lines at the top of the file: what it shows, what the
   reader should *feel*, the one knob that matters.
2. **Build** the standalone `.html`. Pure logic, then mount.
3. **Smoke test:** `node components/test.mjs` — runs every component's script
   against a DOM/canvas stub and asserts no throw + required model invariants
   (e.g. BT fit recovers the true order on a clean run).
4. **Preview & iterate** with the reviewer (open the file, or screenshot).
   Most rounds happen here: pacing, colours, copy, animation feel.
5. **Compose:** once approved, inline the component into the post's
   `index.html` (the mount call + its logic), then run the post through the
   `WORKFLOW-v2.md` self-review checklist.

## Status

| Component | Post | File | State |
|---|---|---|---|
| Pitch 1v1 match + leaderboard | 02-sort | `sort/pitch-match.html` | building |
| Pairing-policy race | 02-sort | `sort/pairing-race.html` | planned |
| Street-map shortest path | 03-shortest-path | `path/city-map.html` | planned |
| berlin52 tour explorer | 04-tsp | `tsp/berlin52.html` | planned |
