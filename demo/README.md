# EDP interactive demos

Two single-file HTML pages, no build step. Both use Tailwind via CDN.

## `policy_comparison.html` — side-by-side head-to-head (paper §5 companion)

The main paper demo. Pick a persona and a fashion category, drag the signal
sliders, and see what each of 5 policies puts on the page at that session.
Reward per page is computed under the persona-and-category effective need
vector; the panel with the highest reward gets a green border.

The 5 policies (left → right, by paper performance ranking):

| Policy | Action |
|---|---|
| `Static widgets` | top-6 widgets by initial `base` weight — same page every time |
| `LinTS-cold` | per-slot LinTS with 14-d raw-signal context, pre-trained on 10K |
| `LinTS-warm` | per-slot LinTS with 7-d problem-fingerprint context, pre-trained on 10K |
| `EDP-static (v1)` | 2-layer GAM with the LLM-prior modules |
| `EDP-evolved (v3)` | same GAM, after a canned 12-edit batch (paper Round 1-3 distilled) |

LinTS weights are pre-trained in Python on the production reward stack
(page-level + delay=500 + σ=0.2) and exported to `lints_state.json`
(~784 KB). The demo loads it via `fetch` on page load — so **open the file
from a small HTTP server**, not via `file://`, or the fetch will be blocked.
The simplest:

```bash
cd demo
python3 -m http.server 8765
# then open http://localhost:8765/policy_comparison.html
```

Numerical sanity-check: the JS `pageReward` and `oracleReward` match the
Python reference implementations exactly on `returner_anxious` × `bottoms`
with both the EDP-v1 and the static-widget pages.

To regenerate the LinTS weights:

```bash
python3 experiments/export_lints_state.py
```

## `edp_orchestrator.html` — EDP composition flow (paper §3 companion)

Interactive visualisation of the EDP pipeline (Layer-1 PWL problem shapes
→ 7-d problem fingerprint → Layer-2 GAM module scoring → greedy submodular
composition). Matches the original `edp_sim.py` reference implementation.

Open directly in a browser — no server needed.

What you can do:

- Pick a persona from the dropdown to load its mean signal profile
- Drag the 14 raw signal sliders to construct a custom session
- Watch the 7-d problem fingerprint update in real time as Layer-1 PWL
  shapes evaluate
- Step through the 6-slot greedy composition with `remaining` / `coverage`
  state updating per slot
- Toggle the v1 ↔ v3 module config to see the canned-edit trajectory
- Switch to the GAM-curves tab to inspect each Layer-1 shape function

## What's NOT in the demos

For scope reasons, the demos do not include:

- The live report-based agent loop (would need a backend Anthropic call)
- The OPRO ablation (same reason)
- The Robust EDP wrapper (needs many sessions to manifest; would slow the UI)
- The LLM-as-policy baseline (its `pick_page` is a Python function;
  port to JS is straightforward and on the to-do list)
- The 14 LLM-generated personas (descriptions are in
  `data/personas_text.yaml` and the cache is `data/personas_llm_cache.json`)

The Python codebase (`edp/`, `experiments/`) is the source of truth for
those; the demos are intuition-builders for figures and live walkthroughs.
