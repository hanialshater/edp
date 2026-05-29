# Blog series workflow v2 — visuals + storytelling standard

Supersedes `WORKFLOW.md` for the upgraded visual and narrative standard.
Every post now ships with the higher bar described here.

## What "much better" means concretely

### Visuals
- **Hero element.** Every post opens with a live, animated visual *before*
  the first paragraph. The reader sees motion within 2 seconds of loading.
  Sets the vibe; teases the question.
- **Race-style charts.** Where multiple policies are compared, render their
  curves on a *single* canvas, racing side by side in real time. Showing
  one policy at a time, then another, is not the standard — comparison is
  the point.
- **Per-element visualization.** Don't just show aggregate stats. Show
  the per-arm pull counts, the per-edge confidence, the per-city distance
  estimate — concretely, with bars or stacks or rings, so the reader can
  see *where* the algorithm is spending its budget.
- **Reveal mechanics.** Hidden truth, reveal-on-demand. Posts about
  unknown parameters should make the reader *feel* not knowing.
- **Scene breaks.** Articles have visible structural rhythm: hero,
  acts (1–3 short sections), big interactive, secondary playground,
  outro. Visual dividers (`<hr class="scene">`) separate acts.

### Storytelling
- **Concrete scenario opener.** Don't open with the abstract problem.
  Open with a small story: "You're running 5 ad creatives. You have
  10,000 impressions. Which one do you push?"
- **Questions as headers.** "What if you could read the numbers?" /
  "What if you couldn't?" / "How long until you know?". Headers should
  be the things the reader is wondering.
- **The aha is the widget, not the prose.** The article sets up the
  question; the widget delivers the answer; the closing paragraph names
  it briefly. Don't pre-spoil what the reader is about to discover by
  playing.
- **Forward arrow.** Every post ends with a single sharp question that
  motivates the next. "Bandits beat a random pull. But what if the arms
  aren't independent — like the edges of a path?" → Post 3.
- **No padding.** ≤ 1,000 words of prose per post. The widget is the
  load-bearing part; the prose is scaffolding around it.

## File pattern

Each post is **one self-contained HTML file** at `blog/0X-name/index.html`:

```
<head>
  inline <style>      (~150 lines, post-specific overrides on shared base)
</head>
<body>
  series-nav (top)
  hero (animated, ~80 lines)
  article act 1 — concrete scenario
  scene break
  article act 2 — the unknown-parameter twist
  scene break
  interactive widget — the core experience
  article act 3 — what you just saw, briefly
  secondary playground (optional, if the widget has a "manual mode")
  outro + forward arrow
  series-nav (bottom)
  inline <script>     (~400-600 lines of vanilla JS, no deps)
</body>
```

Inlined CSS so the file works from raw URLs and htmlpreview. No external
fonts, no external libraries, no build step.

## Shared JS helpers (inlined per file)

Each post inlines this small lib at the top of its `<script>`:

- `rng(seed)` — deterministic RNG factory.
- `gauss(rng)` — standard normal sampler.
- `beta(a, b, rng)` — beta sampler for Thompson sampling.
- `clamp(x, lo, hi)`.
- `Chart(canvas)` — minimal canvas chart class: `chart.line(name, color)`,
  `chart.push(name, x, y)`, `chart.render()`. Handles axes, gridlines,
  high-DPI scaling.
- `colors` — shared palette object.

About 150 lines. Each post inlines it; minor redundancy is the price of
portability.

## Per-post procedure

1. **Concrete scenario** in 1 sentence. Write it first; it constrains
   every visual choice.
2. **The widget's central question** in 1 sentence. The reader should
   be able to *answer* it by playing for < 60 seconds.
3. **Hero animation.** Build it before the article. If it isn't
   compelling, the rest doesn't matter.
4. **Core widget.** Builds on hero but adds interactivity. State machine
   tight; reset always works; mobile-friendly.
5. **Article** in 3 acts, ≤ 1,000 words.
6. **Self-review checklist** (`REVIEW.md`):
   - [ ] Hero animates within 2 seconds of load.
   - [ ] Reader can answer the widget's question in < 60 seconds.
   - [ ] Reset works at any time, deterministically.
   - [ ] Multi-policy comparison is on a single chart, not sequential.
   - [ ] Reads on a phone (manual test: open via htmlpreview on phone).
   - [ ] No external network calls; no relative-path assets.
   - [ ] Closing arrow points forward (or, for Post 6, back to the paper).

## Status

| # | Post | State |
|---|---|---|
| 1 | Picking the max (bandit) | upgraded v2: hero + race + playground |
| 2 | Sort with unknown values | v1 complete: noisy-compare widget |
| 3 | Shortest path with unknown weights | v1 complete: grid + per-edge UCB |
| 4 | TSP with unknown distances | v1 complete: city map + 2-opt race |
| 5 | EDP — world knowledge as policy | v1 complete: persona → page widget |
| 6 | EDP that adapts and explores | v1 complete: in-browser cold-start race |
