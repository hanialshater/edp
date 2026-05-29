# Blog series workflow

A side project of the WPO-Gym / EDP research (`paper/paper.md`). Six
interactive blog posts on **how to solve classical problems when the
parameters are unknown** — the unifying lens behind multi-armed bandits,
combinatorial bandits, and the paper's own claim that domain knowledge
plus structured editing (EDP) shortcuts the exploration.

## The arc

Each post takes a textbook problem with a *known* solution and asks: what
do you do when the inputs are unknown? Complexity grows along two axes —
the problem's combinatorial size, and what you bring beyond click data.

| # | Post | Classical problem | When parameters unknown | Interactive widget |
|---|---|---|---|---|
| 1 | **Select max** | max(x₁..xₖ) — one comparison | Multi-armed bandit | K-armed slot machines; switch between ε-greedy / UCB / Thompson and watch regret accumulate |
| 2 | **Sort** | sort(x₁..xₙ) — n log n comparisons | Noisy / dueling bandits | Drag-to-sort with hidden values, noisy-comparison oracle, mergesort vs Borda |
| 3 | **Shortest path** | Dijkstra on known graph | Online shortest path (combinatorial bandit) | Grid graph with hidden edge weights, walk the path, watch a UCB-on-edges policy converge |
| 4 | **TSP** | Christofides 1.5× on metric TSP | Combinatorial bandit over tours | Click cities, pick tours, see regret; compare random / 2-opt / EXP3 over tours |
| 5 | **EDP** | "I know the domain" — a GAM with named curves authored by an LLM | The win is that you don't need to learn from scratch | The orchestrator demo: drag a curve, watch a page recompose; no clicks needed |
| 6 | **EDP that adapts and explores** | Coefficient updates + structural edits at checkpoints | The paper's bet: cold-start *and* keep improving | Mini WPO-Gym: race tuned bandit vs Bayesian-EDP from session 0 |

The series ends pointing at the paper — Posts 1–4 are the textbook
backdrop, Post 5 is the conceptual move EDP makes, Post 6 is the
research bet (the cold-start curve from §5.7 made playable in-browser).

## Format

- **Single-file HTML per post.** `blog/0X-name/index.html` contains the
  article *and* the interactive widget; no build step, no npm, opens in
  any browser, viewable on GitHub Pages.
- **Vanilla JS + Canvas.** No frameworks. Each widget is ~300–500 lines.
  Shared styling in `blog/shared/style.css`.
- **Dark theme to match `demo/edp_orchestrator.html`.**
- **One widget, played in the body.** Not a separate page. The reader
  reads → plays → reads.
- **No external assets.** Everything inline so a clone of the repo
  works offline.

## Per-post procedure

1. **Outline.** Title + 3-sentence thesis + the *interactive question* the
   widget will let the reader answer. Commit `README.md` first.
2. **Article draft.** ≤ 1,200 words. Three sections:
   - The classical problem (what we know how to do)
   - The unknown-parameter twist
   - What the widget below lets you discover
3. **Widget build.** Single HTML, vanilla JS, Canvas. State machine
   tight; reset always works. The widget must answer the post's
   interactive question — not be a generic playground.
4. **Self-review checklist** (`blog/REVIEW.md` template — see below):
   - [ ] Reader can answer the interactive question in < 60 seconds.
   - [ ] Widget loads with zero clicks needed; one button onboards.
   - [ ] Reset button always returns to a clean state.
   - [ ] Mobile-readable (article wraps; widget at least functional).
   - [ ] No external network calls.
   - [ ] Links forward to next post, backward to prev, and to the paper
     where relevant.
5. **Publish.** Add to `blog/README.md` index.

## Relationship to the research project

The series is a side project, not a popularization with looser standards.
Three rules:
- Posts 5 and 6 cite `paper/paper.md` and link to specific sections.
- Any number from the paper that appears in a post is sourced from the
  same `results/*.json` and checked by `experiments/check_paper_consistency.py`
  if it's load-bearing.
- The cold-start curve in Post 6 is the same data as Fig. 12 in the
  paper (`results/coldstart.json`); the widget renders it live, the
  paper renders it static. They cannot disagree.

## Status

| # | Post | State |
|---|---|---|
| 1 | Select max (multi-armed bandit) | **complete** (article + playable widget) |
| 2 | Sort with unknown values | stub: outline + widget design |
| 3 | Shortest path with unknown weights | stub: outline + widget design |
| 4 | TSP with unknown distances | stub: outline + widget design |
| 5 | EDP — when world knowledge replaces exploration | stub: outline + widget design |
| 6 | EDP that adapts and explores (the paper) | stub: outline + widget design |

Build the rest by following the procedure above, one post at a time.
