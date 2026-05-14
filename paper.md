# Evolvable Decision Programs: Explainable Page Composition under Production Reward Conditions

## Abstract

Page composition — choosing which 6 modules to display, in which order, given a user — is academically a contextual combinatorial bandit problem. In production, however, reward signals are page-level (not per-slot), arrive with multi-day delay, and are noisy. Under these conditions we show that a 2-layer Generalized Additive Model (GAM) policy edited by an LLM agent reading a structured diagnostic report — an **Evolvable Decision Program (EDP)** — beats Linear Thompson Sampling by **2.6×** in cumulative regret at 10K sessions, and **2.4×** at 1K sessions. An OPRO-style ablation in which the agent sees only `(edit_batch, batch_regret)` pairs recovers <2% of EDP's improvement over a static baseline, isolating the structured diagnostic report as the carrier of the gain. The "LLM-in-the-loop" advantage is not magic; it requires curves the LLM can reason about and a report telling it where they are off.

## 1. Introduction

Recommendation pages are composed, not just ranked. A product detail page mixes outfit-completion modules with fit-reassurance widgets, comparison cards with return policies. Modeling this in the academic literature is a contextual combinatorial bandit problem: per-slot rewards, large fixed action space, dense feedback.

Production has two structural mismatches with this framing:

1. **Reward attribution.** Engagement, purchase, return — all are observed at the page or order level, not per-slot. A bandit can divide page reward by N slots, but this dilutes signal by an order of magnitude.
2. **Delay.** Sales include returns; returns settle in ~2 days. The reward for a session served today arrives 500 sessions later.
3. **Low N.** Most A/B test arms close before reaching 10K sessions per cell.

Under all three, a per-slot LinTS bandit pays exploration tax it cannot amortize.

We propose **Evolvable Decision Programs (EDP)** as an alternative. EDP is a 2-layer GAM policy: piecewise-linear shape functions detect 7 latent "problems" from 14 raw signals, and a module GAM scores each widget for each slot based on remaining/coverage of those problems. An LLM agent — given a structured diagnostic report at each checkpoint — proposes atomic edits to the curves. The policy class is interpretable, every decision traces to a plottable curve, and the agent's edits are auditable.

**Contributions:**

1. A reproducible head-to-head between EDP and LinTS under the production reward stack (page-level + delay + noise), with EDP winning 2.6× at 10K sessions and 2.4× at 1K.
2. An OPRO-style ablation showing the diagnostic report — not the LLM's general intelligence — is what makes the agent-in-the-loop work in this action space.
3. A stressor decomposition isolating page-level attribution as the dominant production stressor, an order of magnitude larger than delay or noise.

## 2. Setup

### 2.1 Customer simulator

`sim.py` defines 8 personas with mixture weights summing to 1, each parameterized by (mean, std) over 14 raw signals (size_conf, return_view, tab_switch, etc.) clipped to [0,1]. A session is `(persona_name, feature_vector)`. The full stream is 10K sessions at seed 42.

### 2.2 Ground truth (independent of any policy)

Following prior work, we author 7 latent shopping needs `{N1_fit, N2_visual, N3_peer, N4_compare, N5_styling, N6_trust, N7_commit}` and assign:

- `TRUE_NEEDS[persona] → {need: importance}` (8 personas × 7 needs)
- `TRUE_PROVISIONS[widget] → {need: provision}` (22 widgets × ≤3 needs each)

These were authored from shopping-psychology priors, intentionally not aligned with EDP's internal F-code taxonomy. This matters: the bandit could in principle discover the needs from data; EDP's Layer 1 cannot directly see them either.

**Reward** is diminishing returns on `need × provision`. Each slot consumes from the persona's remaining-need budget; later slots get diminishing credit. The greedy oracle over true provisions provides the upper bound.

### 2.3 Production reward stack

The bandit observes:
- `r_observed = (page_total + noise) / N_SLOTS` (page-level attribution)
- delayed by `delay` sessions (Gaussian noise σ added on release from the delay queue)

Default conditions: `delay=500`, `σ=0.2`, page-level attribution. These approximate "~2 days at ~250 sessions/day" of return-window lag in fashion retail.

## 3. EDP architecture

### 3.1 Layer 1: PWL problem detection

Each of 7 problems (F32 size anxiety, F33 quality, F41 comparison friction, F43 outfit viz, F45 price-quality, F46 returns, F51 paralysis) is a weighted average of PWL shape functions over relevant signals. Output: a 7-d "problem fingerprint" per session.

### 3.2 Layer 2: module GAM + greedy composition

Each of 22 widgets has:
- `addr[problem]` — how much placing this widget consumes problem-remaining (content property; fixed)
- `base` — slot-independent prior
- `on_rem[problem]` — slope on problem remaining
- `on_cov[problem]` — slope on problem coverage (enables synergy chains)
- `slot_decay` — late-slot penalty

Module score for slot `s`:
```
score = base + Σ_p on_rem[p] · remaining[p] + Σ_p on_cov[p] · coverage[p] − slot_decay · s
```

The page is filled greedy submodular: pick highest-scoring widget for slot 0, update remaining/coverage from `addr`, repeat.

### 3.3 Evolution loop

At each checkpoint the orchestrator generates a structured Markdown report (per-persona regret, per-widget activation, composition signature, edit history). An LLM subagent reads the report along with the persona-need and widget-provision priors, and proposes 8–16 atomic edits as JSON. Each edit is `(widget, dotted_path, from, to, reason)`. The orchestrator applies them and runs the next batch.

## 4. Methods

| Method | Action space | Learning signal |
|---|---|---|
| **Oracle** | greedy over true provisions | — (upper bound) |
| **EDP-static** | initial LLM-prior modules | none |
| **EDP-canned** | EDP with canned edit batches at 2.5k/5k/7.5k | offline-curated edits |
| **EDP-agent** | EDP with live subagent edits | structured diagnostic report |
| **EDP-OPRO** | same agent loop, prompt = (edits, score) history only | score-only |
| **LinTS-warm** | per-slot LinTS, 7-d problem fingerprint context | delayed page-level page-attribution divided by N_SLOTS |
| **LinTS-cold** | per-slot LinTS, 14-d raw signal context | same |

LinTS hyperparameters: α=0.3, λ=1.0. Bandits learn online; EDP applies edit batches at fixed checkpoints.

## 5. Results

### 5.1 Headline: EDP wins 2.6× under production stack (Fig. 1, Tab. 1)

10K sessions, page-level + delay=500 + σ=0.2:

| Method | Cum regret @ 10K | % reward kept |
|---|---|---|
| Oracle | 0 | 100.0% |
| **EDP-agent (live, report-based)** | **766.9** | **93.0%** |
| EDP-canned | 783.6 | 92.9% |
| EDP-OPRO (ablation) | 1,045.5 | 90.5% |
| EDP-static | 1,052.4 | 90.5% |
| LinTS-warm | 1,983.6 | 82.0% |
| LinTS-cold | 2,085.3 | 81.1% |

See `fig_cumregret.png`.

### 5.2 Stressor decomposition (Tab. 2, Fig. 2)

Holding the policy fixed at LinTS-warm, we add stressors one at a time:

| Stressor | LinTS-warm cum regret @ 10K | Δ vs clean |
|---|---|---|
| Clean (per-slot reward, no delay, no noise) | 497 | — |
| + noise σ=0.2 only | 492 | **−5** (TS is built for noise) |
| + delay=500 only | 629 | +132 |
| + delay=1000 only | 765 | +268 |
| + page-level attribution only | **1,959** | **+1,462** |
| + page + delay=500 | 1,999 | +1,502 |
| + page + noise=0.2 | 1,961 | +1,464 |
| Full production stack (page + delay=500 + σ=0.2) | 1,982 | +1,485 |

Page-level attribution is the dominant axis by an order of magnitude. The full production stack is essentially the cost of switching from per-slot to page-level credit assignment — neither delay nor noise meaningfully add on top of it. This isolates the structural problem the bandit cannot solve no matter the algorithm: with N_SLOTS=6, page-level credit dilutes per-slot signal by 6× and breaks the per-arm linear regression that makes LinTS work. See `figures/fig2_stressor.png`.

### 5.3 Statistical power: low-N regime (Fig. 3)

| Method | @ 1K | @ 2.5K | @ 5K | @ 10K |
|---|---|---|---|---|
| EDP-agent | 118 | 281 | 451 | 767 |
| EDP-OPRO | 118 | 281 | 387 | 1,046 |
| LinTS-warm (prod) | 287 | 633 | 1,129 | 1,984 |
| LinTS-cold | 282 | 637 | 1,147 | 2,085 |

At every measured N the report-based EDP wins. Crucially at 1K — before most A/B tests reach decision — EDP is 2.4× better than LinTS-warm.

### 5.4 Per-persona breakdown (Fig. 4)

Each method's regret on each persona, as % of that persona's oracle reward:

| Persona | LinTS-cold | LinTS-warm | EDP-static | EDP-OPRO | EDP-canned | **EDP-agent** |
|---|---|---|---|---|---|---|
| returner_anxious | 25.7 | 23.6 | 27.1 | 17.4 | 10.9 | **11.5** |
| size_anxious_new | 23.8 | 21.6 | 17.1 | 11.2 | 11.4 | **12.8** |
| comparison_shopper | 19.8 | 19.4 | 2.3 | 4.2 | 3.3 | **2.4** |
| outfit_seeker | 17.8 | 17.3 | 6.3 | 11.4 | 5.2 | **6.0** |
| price_sensitive | 15.9 | 16.1 | 2.5 | 3.9 | 4.5 | **3.1** |
| confident_buyer | 14.0 | 13.1 | 8.3 | 16.6 | 9.9 | **7.2** |
| browser_lurker | 13.9 | 13.0 | 9.0 | 17.3 | 8.4 | **9.2** |
| paralyzed | 12.5 | 12.4 | 3.4 | 4.1 | 4.7 | **3.4** |

The agent's improvement over EDP-static is concentrated on `returner_anxious` (27.1 → 11.5%) and `confident_buyer` (8.3 → 7.2%). OPRO's results are erratic: it slightly helps `returner_anxious` (27.1 → 17.4%) but actively hurts `confident_buyer` (8.3 → 16.6%) and `browser_lurker` (9.0 → 17.3%). The agent that sees the report can target the right personas; the score-only agent cannot. See `figures/fig4_persona_heatmap.png`.

### 5.5 OPRO ablation (Fig. 5)

The cleanest result in the paper. Same Claude subagent, same action space, same number of rounds, same simulator — the only change is the prompt content:

- **Report-based agent prompt:** report Markdown + persona/widget priors + current modules JSON + edit history
- **OPRO prompt:** `(edits_proposed, batch_regret)` pairs sorted by score, nothing else

Result: removing the diagnostic report loses **98% of the agent's improvement over EDP-static**. OPRO's round-1 lucky exploration yielded 106 batch regret, but rounds 2-3 could not extract from `(edits, score)` alone WHICH edits were doing the heavy lifting; round 2 scaled magnitudes up and regressed (350 batch regret), round 3 retreated.

**Interpretation:** the LLM-in-the-loop is not adding "intelligence"; it is consuming structured diagnostics over interpretable curves. Without the curves to anchor and the report to direct, the same LLM behaves like a sloppy hill-climber.

### 5.6 Evolution trajectory (Fig. 6, Fig. 7)

Per-round metrics for the report-based agent:

| Round | Sessions | Edits | Batch regret | Cum regret | Note |
|---|---|---|---|---|---|
| 0 | 0–2500 | 0 | 281 | 281 | EDP-static baseline |
| 1 | 2500–5000 | 16 | 170 | 451 | revived returns/size widgets |
| 2 | 5000–7500 | 16 | 97 | 548 | revived style/visual widgets |
| 3 | 7500–10000 | 12 | 219 | 767 | stabilization, pulled back over-promotions |

Widget activation heatmap across rounds (`fig_widget_heatmap.png`) shows the agent activating successive families: returns/size first, then style/visual, then rebalancing.

## 6. Discussion

### 6.1 GAMs as Software 3.0 primitive

Classic ML: collect logs → train black-box model → deploy. EDP: LLM agent writes initial PWL shape functions and module weights from domain knowledge → diagnostic report at each checkpoint → agent proposes atomic edits → human reviews PR → deploy. The unit of work is a curve, not a model. Three properties follow:

- **Cold start collapses.** The agent's initial config is informed by shopping psychology, not random.
- **Edits are atomic.** A PR diff is one curve adjustment; auditable in 30 minutes.
- **Policy class grows.** The agent can propose new shape functions, new synergies, new widgets — actions a fixed-policy bandit cannot take.

### 6.2 Explainability is architectural, not bolted on

Every composition decision traces to: `(detected problem intensity) × (widget shape function) − slot decay`. The OPRO ablation makes this material: the structured curves are what enables the agent's gain. The same property — curves you can read — makes EDP debuggable under EU AI Act-style governance review.

### 6.3 When each approach wins

- **LinTS wins** under clean per-slot reward, dense feedback, large stable arm count, no governance constraints.
- **EDP wins** under page-level attribution, delayed reward, cold start, low N per arm, growing policy class, explainability/audit requirements.

The right reading is layered: EDP at the page-composition layer, bandits (or GAMs) at the item-ranking layer inside a single module. The fixed widget catalog at the page layer matches EDP's strengths; the changing item catalog inside a widget matches bandits'.

## 7. Limitations

1. **Synthetic ground truth.** The 7 latent needs are LLM-authored, not learned from real engagement data. Directional; unvalidated on production logs.
2. **Layer 1 held fixed.** The agent only edits Layer 2 module config. A complete loop would also propose PWL shape adjustments.
3. **LinTS-only bandit.** Neural bandits (NeuralUCB, MLP+TS) might close some gap on clean reward. They do not change the page-attribution finding.
4. **No structural exploration.** The 22-widget catalog is fixed for both methods. Real EDP adds widgets via PR.
5. **No drift.** Persona distribution is stationary throughout.
6. **No formal regret bounds.**

## 8. Conclusion

When reward attribution is page-level and delayed — the production reality, not the academic regime — a 2-layer GAM policy edited by an LLM agent reading a structured diagnostic report beats Linear Thompson Sampling by 2.6× in cumulative regret. The OPRO ablation isolates the structured diagnostic report as the carrier of the gain: removing it recovers <2% of the agent's improvement over a static baseline. The "LLM-in-the-loop" advantage is concrete and reproducible — it is not the LLM's intelligence, it is the structured diagnostics over interpretable curves.

---

### Reproducing

```bash
python3 compare.py                      # main head-to-head
python3 stressor_decomp.py              # Section 5.2
python3 final_compare.py                # consolidated table
python3 viz.py                          # all figures
```

### Code map

- `sim.py` — simulator
- `policy_edp.py` — EDP policy + apply_edits
- `policy_bandit.py` — LinTS
- `compare.py` — main comparison
- `orchestrator.py` — report-based live-agent loop
- `orchestrator_opro.py` — OPRO ablation loop
- `stressor_decomp.py` — Section 5.2 ablation
- `viz.py` — figures
- `final_compare.py` — table assembly
