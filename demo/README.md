# EDP interactive demo

`edp_orchestrator.html` — single-file interactive visualization of the EDP
pipeline (Layer-1 PWL problem shapes → 7-d problem fingerprint → Layer-2 GAM
module scoring → greedy submodular composition). Matches the canonical
`edp_sim.py` reference implementation.

## Use

Open directly in a browser:

```bash
xdg-open demo/edp_orchestrator.html       # Linux
open demo/edp_orchestrator.html            # macOS
start demo/edp_orchestrator.html           # Windows
```

No server, no build step — Tailwind via CDN, plain HTML + JS.

## What you can do

- Pick a persona archetype from the dropdown to load its signal profile
- Drag the 14 raw signal sliders to construct a custom session
- Watch the 7-d problem fingerprint update in real time as Layer-1 PWL
  shapes evaluate
- Step through the 6-slot greedy composition, with `remaining` / `coverage`
  state updating per slot
- Toggle the v1 ↔ v3 module config to see the effect of LLM-agent edits
- Switch to the GAM-curves tab to inspect each Layer-1 shape function

Useful for figures, screenshots, and intuition-building before reading the
paper's Section 3.
