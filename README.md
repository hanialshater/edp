# Bandit vs EDP for whole-page composition

Clean reimplementation of an EDP-vs-LinTS bandit head-to-head under realistic
production conditions:
- **Page-level reward** (the bandit can only credit a slot via `page_total / N_SLOTS`)
- **Delayed observation** (~500 sessions ≈ 2 days at 250 sessions/day, for returns to settle)
- **Gaussian noise** σ=0.2 on observed page reward

Two EDP "learning" loops are included:
1. **Report-based agent** — each checkpoint, a Claude subagent reads a structured diagnostic report (per-persona regret, per-widget activation, composition signatures) and proposes atomic config edits.
2. **OPRO-style ablation** — same checkpoint cadence, same action space, but the subagent receives ONLY the history of `(edit_batch, batch_regret)` pairs. No diagnostics.

## Headline result (10k sessions, page-level, delay=500, σ=0.2)

| Method | Cum regret @ 10k | Reward kept | vs Oracle |
|---|---|---|---|
| Oracle (upper bound) | 0 | 100.0% | 1.00× |
| **EDP-evolved (live report-based agent)** | **766.9** | **93.0%** | best |
| EDP-evolved (canned edits) | 783.6 | 92.9% | +2.2% regret |
| EDP-static (no evolution) | 1,052.4 | 90.5% | +37% regret |
| **EDP-evolved (OPRO-style live agent)** | **1,045.5** | **90.5%** | +36% regret |
| Bandit-warm (LinTS, 7-d context) | 1,983.6 | 82.0% | +159% regret |
| Bandit-cold (LinTS, 14-d context) | 2,085.3 | 81.1% | +172% regret |

The report-based agent beats bandit-warm by **2.59×**.

## OPRO ablation

The cleanest finding in the table: **removing the diagnostic report loses 98% of the agent's improvement over static EDP**.

- Report-based agent: 766.9 cum regret
- OPRO (score-only):  1,045.5 cum regret (+278.6)
- EDP-static:          1,052.4 cum regret (the baseline OPRO recovers to)

OPRO sees `(edit_batch, batch_regret)` pairs and tries to pattern-match a better config. In this action space (22 widgets × many fields, sparse alignment with personas), score-only signal is too weak; the second round even regressed. The structured report (per-persona regret + widget activation + composition signature) is what lets the agent reason about WHICH curve to nudge.

This makes the "GAMs as Software 3.0 primitive" claim concrete: the value isn't just "an LLM in the loop", it's "an LLM reading structured diagnostics over interpretable curves".

## Files

| File | Role |
|---|---|
| `sim.py` | Personas, ground-truth needs/provisions, `DelayedFeedback` queue, oracle. |
| `policy_edp.py` | EDP policy: PWL Layer-1 shapes → 7-d problem fingerprint → module GAM → greedy submodular composition. `apply_edits()`. |
| `policy_bandit.py` | Per-slot LinTS with page-uniqueness mask and warm/cold contexts. |
| `compare.py` | Head-to-head harness for static + canned + bandits on a shared stream. |
| `orchestrator.py` | Report-based live-agent loop. Persists `evolve_state/`. |
| `orchestrator_opro.py` | OPRO-style ablation. Persists `opro_state/`. |
| `final_compare.py` | Loads every method's reward trajectory and prints the final table. |
| `test_basic.py` | Basic correctness tests. |
| `edits/round{1,2,3}.json` | Canned LLM-proposed edits (from prior work, for the "canned" arm). |
| `evolve_state/` | Persisted state for the report-based live run. |
| `opro_state/` | Persisted state for the OPRO ablation. |

## How to run

### Static + canned + bandits (no LLM needed)
```bash
python3 compare.py                           # default: 10k, delay=500, sigma=0.2
python3 compare.py --n 2000 --delay 200      # smaller scan
python3 compare.py --methods bandit_warm     # subset
```

### Report-based live-agent EDP evolution

Each command runs the next 2,500 sessions; between commands you spawn a
Claude subagent and point it at the generated prompt.

```bash
python3 orchestrator.py --reset --until 2500
# -> evolve_state/AGENT_PROMPT_at_2500.md  (subagent reads this)
# -> subagent writes evolve_state/edits_round_2500.json
python3 orchestrator.py --apply evolve_state/edits_round_2500.json --until 5000
# ...repeat for 7500, 10000
```

The subagent's job is captured in `AGENT_PROMPT_TEMPLATE` inside `orchestrator.py`.
It is given the diagnostic report plus the LLM-authored persona need vectors and
widget provision vectors as priors, then asked for 8–16 atomic edits.

### OPRO-style ablation

Same shape, but `orchestrator_opro.py` writes a prompt that contains ONLY the
history of `(edits, batch_regret)` pairs — no diagnostics, no priors.

```bash
python3 orchestrator_opro.py --reset --until 2500
python3 orchestrator_opro.py --apply opro_state/edits_round_2500.json --until 5000
python3 orchestrator_opro.py --apply opro_state/edits_round_5000.json --until 7500
python3 orchestrator_opro.py --apply opro_state/edits_round_7500.json --until 10000
```

### Final comparison

Loads everything and prints the unified table:
```bash
python3 final_compare.py
```

## Trajectory of the report-based agent

| Batch | Sessions | Edits | Cum regret | Note |
|---|---|---|---|---|
| 0 | 0 → 2500 | 0 | 281.2 | baseline EDP-static config |
| 1 | 2500 → 5000 | 16 | 451.2 | revived returns + size + material widgets |
| 2 | 5000 → 7500 | 16 | 548.0 | revived style/visual widgets; dialed back returns over-firing |
| 3 | 7500 → 10000 | 12 | 766.9 | stabilization: pulled back over-promoted defaults |

## Trajectory of the OPRO-style agent

| Batch | Sessions | Cum regret | Note |
|---|---|---|---|
| 0 | 0 → 2500 | 281.2 | baseline |
| 1 | 2500 → 5000 | 387.4 | blind exploration: modest base lifts on diverse widgets |
| 2 | 5000 → 7500 | 737.6 | exploit attempt scaled magnitudes up — regressed badly |
| 3 | 7500 → 10000 | 1,045.5 | retreat — close to static |

## Open extensions

- Drift / distribution shift mid-run
- Structural exploration (LLM agent proposes a new widget)
- Layer-1 PWL evolution (currently only Layer-2 module config evolves)
- Neural bandit baseline (NeuralUCB / MLP+TS)
- Replace LLM-authored ground truth with a logged-data eval
