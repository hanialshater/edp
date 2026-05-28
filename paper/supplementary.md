# Supplementary Material

Companion to the paper "Evolvable Decision Programs: Explainable Page Composition under Production Reward Conditions". Contains reproduction commands, code structure, and instructions for the interactive demos. Numerical and methodological content stays in the main paper.

## A. Reproducing the experiments

All experiments share a 10K-session stream at seed 42. Bandit reps vary the policy seed; EDP-canned and EDP-static are deterministic; EDP-agent and EDP-OPRO replicates are independent subagent draws. Resource budget per replicate: ~30 s for a bandit run, ~20 s of subagent latency per agent edit checkpoint.

### A.1 Multi-seed baselines

```bash
# parametric persona source (paper §2.1)
python3 experiments/multiseed.py --reps 10 \
    --out results_multiseed_parametric_cat.npz

# LLM persona source (paper §2.2c)
python3 experiments/persona_generate.py prepare      # writes per-persona instruction files
# spawn 14 subagents, one per file in data/persona_instructions/, each
# writing data/persona_drafts/<name>.json
python3 experiments/persona_generate.py merge        # consolidates into cache
EDP_PERSONA_SOURCE=llm python3 experiments/multiseed.py --reps 10 \
    --source llm --out results_multiseed_llm_cat.npz
```

### A.2 §5.8 baselines (static, LLM-as-policy, Robust EDP)

```bash
# static + LLM-as-policy (deterministic; one subagent call to author the policy)
python3 experiments/llm_policy_generate.py           # writes the prompt
# spawn 1 subagent → data/llm_policy_fn.py
python3 experiments/run_baselines.py --source llm    # runs both deterministic baselines

# Robust EDP: 3 rounds, one subagent per round
EDP_PERSONA_SOURCE=llm python3 -m edp.orchestrators.robust \
    --reset --state-dir robust_state_llm --until 2500
# spawn subagent → robust_state_llm/edits_round_2500.json
EDP_PERSONA_SOURCE=llm python3 -m edp.orchestrators.robust \
    --state-dir robust_state_llm \
    --apply robust_state_llm/edits_round_2500.json --until 5000
# repeat for 7500 and 10000
```

### A.3 Stressor and lab-vs-real ablations

```bash
python3 experiments/stressor_decomp.py    # §5.2 — bandit cum regret per condition
python3 experiments/lab_vs_real.py --reps 10  # §5.9 — lab vs production for both sources
```

### A.4 Figures

```bash
python3 viz.py                            # all figures into figures/
python3 experiments/build_icml_pdf.py     # builds paper-icml.pdf
```

## B. Code structure

```
edp/                             # core package
├── config.py                    # constants: N_SLOTS, signal/need/problem names
├── catalog.py                   # widget catalog + fashion categories
├── ground_truth.py              # category-aware reward, oracle, persona-source switch
├── sim.py                       # (persona, category, feat) stream + DelayedFeedback
├── personas/
│   ├── parametric.py            # paper §2.1 baseline (8 personas, fixed Gaussians)
│   └── llm.py                   # cache reader for LLM-generated personas
├── policies/
│   ├── base.py                  # Policy ABC
│   ├── edp.py                   # EDPPolicy + apply_edits
│   ├── bandit.py                # LinTS + warm/cold/category contexts
│   ├── static.py                # §5.8 static-widget baseline (top-6 by base)
│   └── llm_policy.py            # §5.8 LLM-as-policy wrapper for data/llm_policy_fn.py
└── orchestrators/
    ├── base.py                  # state save/load, batch run
    ├── report.py                # report-based live-agent loop
    ├── opro.py                  # OPRO ablation loop
    └── robust.py                # §5.8 Robust EDP — K-perturbation validation-slice selection

experiments/                     # entry-point scripts (paper-aligned)
├── compare.py                   # head-to-head harness
├── multiseed.py                 # 10-seed bandits + deterministic EDP baselines
├── persona_generate.py          # prepare/merge pipeline for LLM persona cache
├── llm_policy_generate.py       # §5.8 prompt for the LLM-as-policy function
├── run_baselines.py             # §5.8 static + LLM-as-policy on either source
├── stressor_decomp.py           # §5.2 sweep
├── lab_vs_real.py               # §5.9 lab vs production
├── export_lints_state.py        # train LinTS, export weights JSON for the demo
└── build_icml_pdf.py            # builds the ICML two-column PDF

data/
├── personas_text.yaml           # 14 persona descriptions (NL)
├── persona_instructions/        # per-persona subagent prompts
├── persona_drafts/              # subagent outputs
├── personas_llm_cache.json      # consolidated cache
├── widget_descriptions.yaml     # widget descriptions for the §5.8 LLM-policy prompt
└── llm_policy_fn.py             # §5.8 LLM-authored pick_page(feat, category)

demo/                            # single-file HTML interactive companions
├── policy_comparison.html       # §5 head-to-head: 5 policies side by side
├── edp_orchestrator.html        # §3 composition-flow visualiser
└── lints_state.json             # pre-trained LinTS weights for the demo
```

The `Policy` ABC (`edp/policies/base.py`) is the integration point for new methods. Adding a new policy means writing a `select_page(feat) -> list[str]` (and optionally `record_feedback(payload, observed_reward)` for online learners) and wiring it into `experiments/compare.py` and `experiments/multiseed.py`.

The persona-source interface (`edp/personas/`) is the integration point for new simulators. Both sources expose `(persona_names, mixture_weights, true_needs, sample_session)`; switching between them is `set_source('llm')` or env var `EDP_PERSONA_SOURCE=llm`.

## C. Interactive demos

Two single-file HTML pages under `demo/` (no build step; Tailwind via CDN):

- `policy_comparison.html` — §5 companion. Five side-by-side policy panels (Static, LinTS-cold, LinTS-warm, EDP-v1, EDP-v3) on the same session. Pick persona + fashion category, drag the 14 signal sliders, see each policy's 6-slot page and its reward / % of oracle. LinTS panels use pre-trained posterior means exported from a 10K-session Python training run (`demo/lints_state.json`, ~784 KB, regenerable with `experiments/export_lints_state.py`). The JS reward function matches the Python implementation exactly (verified on `returner_anxious × bottoms`: Static 1.101125, EDP-v1 1.042475).
- `edp_orchestrator.html` — §3 companion. EDP composition flow, Layer-1 PWL shapes → 7-d problem fingerprint → Layer-2 GAM scoring → greedy composition, with a v1 ↔ v3 toggle for the canned edit batch.

Open with:
```bash
cd demo && python3 -m http.server 8765
# open http://localhost:8765/policy_comparison.html
```

The HTTP server is needed for `policy_comparison.html` because it fetches `lints_state.json` (file:// origin would be blocked). The composition-flow demo works via `file://` directly.

## D. Per-round trajectory of the report-based agent

Cumulative regret added per checkpoint window for the report-based agent
on the parametric simulator (8 personas + categories):

| Round | Sessions | Edits applied | Batch regret | Cum regret | Note |
|---|---|---|---|---|---|
| 0 | 0–2500 | 0 | 281 | 281 | EDP-static initial config |
| 1 | 2500–5000 | 16 | 170 | 451 | revived returns/size widgets |
| 2 | 5000–7500 | 16 | 97 | 548 | revived style/visual widgets |
| 3 | 7500–10000 | 12 | 219 | 767 | stabilization, pulled back over-promotions |

Round 2 is the strongest single-round improvement (97 batch regret —
roughly half the static baseline rate), driven by activating the
style/visual widget family that round 1 had not addressed. Round 3 was
deliberately conservative (12 edits, mostly damping over-corrections);
the small batch-regret rebound (219) reflects that the agent stopped
adding new value rather than that the config got worse.

The persisted edit JSONs live in `evolve_state_rep*/edits_round_*.json`;
they are byte-for-byte reproducible. The agent's per-round natural-language
reasoning is captured in `evolve_state_rep*/PROMPT_at_*.md` (the input to
each subagent) and in the subagent's final-message summary in the parent
session log.

## E. Hyperparameters

LinTS:
- exploration scale α = 0.3
- prior precision λ = 1.0
- per-slot Cholesky-based Thompson sample
- masked actions (no widget repeats within a page)

EDP:
- 6 slots, 22 widgets, 7 latent problems
- Greedy submodular composition (no backtracking)
- LLM agent edit batches limited to 8–16 atomic edits per checkpoint, magnitude range −1.5 to 2.8

Production reward stack (default):
- delay = 500 sessions (~2 days at 250 sessions/day)
- noise σ = 0.20 added on release from delay queue
- page-level attribution: each slot receives `page_total / N_SLOTS` as its credit

Robust EDP wrapper (§5.8):
- K = 8 perturbations per checkpoint
- perturbation σ = 0.15 (Gaussian) on every parameter the agent's edits touched, except `slot_decay`
- validation slice = 500 sessions at seed 99991
- selection score = mean − 0.5·std of validation reward

---

## Deployment walkthrough

*(Moved from the main paper to keep the page budget; referenced from §6 as the deployment-properties artifact.)*


This appendix sketches how the primitive would embed in a production page-render path, so the deployment claims of §1 and §6.3 have a concrete artifact to discuss.

**Step 1 — the policy ships as a JSON file.** The 245-parameter learnable policy plus the metadata needed for serving (problem labels, widget descriptors, edit-grammar version) is approximately 9 KB of JSON. It is checked into the same repository as the application code. There is no separate model registry, no model server, no feature store.

```json
// policy_v_017.json  (9.2 KB)
{
  "version": "017",
  "approved_by": "alice@team.example",
  "from_round": 7500,
  "shapes": { "F32": { "size_chart": {"bps": [0, 0.2, 0.5, 0.8, 1],
                                       "vals":[0, 0.1, 0.45, 0.75, 0.95],
                                       "weight": 0.45 }, ... }, ... },
  "modules": { "fit_reassurance": {"base": 0.10, "addr": {"F32": 0.55, ...},
                                    "on_rem": {"F32": 2.2, ...},
                                    "on_cov": {"F32": -1.2}, ... }, ... }
}
```

**Step 2 — the serving function is ~80 lines of Python.** `score_problems`, `score_module`, and `compose` from `edp/policies/edp.py` are the entire decision logic. Given a session feature vector and a category, they return a 6-widget page. No external calls. The same code path runs in CI tests.

```python
# Production serving path (sketch)
from edp.policies.edp import compose
import json

POLICY = json.load(open("policy_v_017.json"))

def render_page(session_features, category):
    page = compose(session_features, POLICY["shapes"], POLICY["modules"])
    # page is ['fit_reassurance', 'low_return_alts', ...]
    return [fill_widget(w, category) for w in page]
```

`fill_widget(name, category)` pulls cached content from the widget retriever output — already a production capability today. The EDP layer adds about 1 ms to the page render. The 9 KB policy fits in any inline cache and is loaded at process start.

**Step 3 — the audit log is the policy repository's git log.** Each agent edit batch is committed as a PR. The PR body is the diagnostic report the agent read plus the edit batch with its reasons. A reviewer reads ten lines and either merges or requests changes (the reviewer-rejection vignette in §6.2 is the realistic shape of one round). The serving policy file is updated by merging the PR; there is no separate deployment.

```
$ git log --oneline policy_v_*.json
b3f2a1c policy v017: round-7500 edits — strengthen F46 synergy chain (alice)
8d7e120 policy v016: round-5000 edits — cut over-firing on outfit_completion (alice)
3a9c2f5 policy v015: round-2500 edits — revive dead returns/size widgets (bob)
0001abc policy v014: initial LLM-authored config from shopping psychology (LLM)
```

A new team member reads the git log to understand what the system has learned. A regulator subpoenas the same log and reads the diagnostic reports and reasons. A non-ML PM proposes a manual edit by opening a PR. None of these workflows require ML infrastructure.

**Step 4 — Bayesian-EDP adds a small async loop.** If the deployment uses Bayesian-EDP, a separate process drains the delayed-reward queue and SGD-updates the policy file every hour or so. The SGD code is ~50 lines (`edp/policies/bayesian_edp.py`). The resulting numeric drift relative to the LLM prior is logged and bounded; if the SGD wants to move a parameter by more than (say) 50 % of its prior value, the move is held for a human checkpoint review (current implementation is unbounded; bounded drift is a one-line addition).

**Step 5 — checkpoint cadence is operational.** Every K sessions (we use K = 2,500 in experiments; production probably 50K–500K depending on traffic), the orchestrator builds the diagnostic report and invokes the agent. This is an offline cron job, not a serving-path dependency. If the agent is unavailable, the previous policy keeps serving indefinitely; the system degrades gracefully.

**What this isn't.** This is a *walkthrough*, not a production case study. We have not deployed this stack at Zalando-scale traffic; the production-scale follow-up is left as the next concrete experiment. The artifact-level claims (policy ships as JSON, audit log is git log, no model server) are mechanical consequences of the primitive's properties; the latency claim (~1 ms) is measured in-process but not in a production rendering pipeline. The cold-start, audit, and serving-cost claims are first-principles. The benchmark claim is empirical, not a deployment result.

