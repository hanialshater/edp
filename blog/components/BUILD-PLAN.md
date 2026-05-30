# Dynamic build plan — CombUCB post rebuild

Live tracker for the component-first rebuild of posts 2/3/4. Updated every
build round. Workflow rules live in `README.md`; this file is the *state*.

Legend: ☐ todo · ◐ building · ☑ done & smoke-passing · ✦ in post

## Post 2 · Sort = sports skill estimation

The visceral version of "sort under a noisy oracle": footballers with hidden
skill, 1v1 matches as noisy comparisons, a league table as the live estimate.

- ☑ `sort/pitch-match.html` — animated 1v1 pitch + Bradley-Terry leaderboard,
  pairing-policy knob, reveal-truth, τ sparkline. *(flagship hero+widget)*
- ◐ `sort/pairing-race.html` — race random / round-robin / ladder / active on
  the SAME league to τ=1 on one chart. The "where do you spend matches" aha.
- ☐ `sort/bt-vs-combucb.html` — keep the existing replayed BT-vs-CombUCB panel
  (top-k recovery) — port it into the components harness for consistency.

## Decisions (locked)

- **Map source:** berlin52 coords power BOTH post 3 and post 4 (real Berlin
  locations, offline). Post 3 = k-NN street graph on the points; post 4 = tour.
- **Compose mode:** approved components REPLACE the abstract widgets; keep the
  article prose + the BT-vs-CombUCB replay panel.

## Post 3 · Shortest path = berlin52 street graph

- ☑ `path/berlin-path.html` — k-NN (k=5) graph on berlin52 points, hidden
  per-edge travel times (Euclidean × congestion + magnitude-scaled noise);
  CombUCB-on-edges (Dijkstra on magnitude-scaled LCB) vs route-as-an-arm (UCB1
  over 8 enumerated routes). CombUCB gap 7%→0.4% by round 150 (→0.2% @300),
  cum-regret flattens; arm stalls ~4.5% with linear regret. Smoke: green.

## Post 4 · TSP = berlin52

- ☑ `tsp/berlin52.json` — real TSPLIB coords (52 pts), optimal = 7542.
- ☑ `tsp/berlin52.html` — cities on the Berlin layout (y-flipped); explore/
  exploit split: explore traverses an LCB tour, exploit recommends 2-opt on
  means (bounded 10 passes, NN restarts). Race random / 2-opt-on-estimate /
  CombUCB. CombUCB +1–3% over optimal (7542) by ~300 rounds across seeds;
  baselines stall (+34%, +233%). Smoke: green.

## Shared

- ☑ `shared/lib.js` — rng, gauss, Bradley-Terry MM, kendallTau, ranksFromScores.
- ☐ extend with: Dijkstra, 2-opt, UCB/LCB edge-estimator helpers.

## Open questions (need a call before some builds)

1. **Map source for post 3.** Real OSM extract embedded offline (heavier,
   truly "real"), or a hand-built recognizable schematic (lighter, still a
   street graph)? Default if no answer: a compact hand-built grid-of-streets
   with named roads, fully offline.
2. **Compose vs keep workshop.** Do these replace the current post 2/3/4
   widgets outright, or sit alongside as upgraded heroes? Default: replace the
   abstract widgets, keep the article prose + the BT-vs-CombUCB replay panel.

## Verify

`node components/test.mjs` after every component. Each must: run headless
without throwing, expose `window.__component.mount`, and (where it has a model)
satisfy a recovery invariant.
