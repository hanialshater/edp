# WPO-Gym / Evolvable Decision Programs

Research prototype for **contextual page-module selection under delayed,
noisy, aggregate feedback**, plus an interpretable GAM policy that can be
written and edited offline by humans or LLM agents.

> **Scientific status:** the checked-in paper predates the independent audit in
> [`paper/ICML_REVIEW.md`](paper/ICML_REVIEW.md) and is **not ready for ICML
> submission**. Historical result files remain useful for provenance, but their
> headline interpretation is superseded until the experiments are rerun under
> the corrected protocol below.

## What the environment currently tests

A policy observes behavioral/product features and a fashion category, then
selects six distinct widgets from a registry of 22. The production-style
feedback stack provides:

- one page-level reward;
- a configurable delay (default 500 sessions);
- Gaussian observation noise (default sigma 0.20).

The current reward is weighted capped coverage over latent needs. It is
**permutation-invariant**: the selected widget set matters, but widget order does
not. The finite action space is therefore `C(22, 6) = 74,613` sets. Position-
sensitive ordering is future work and must not be inferred from current results.

## Audit corrections in this branch

1. **Exact oracle.** `edp/ground_truth.py` now enumerates all 74,613 valid sets.
   The former greedy reference was suboptimal in several LLM-persona/category
   cells.
2. **Strict action contract.** Unknown widgets, duplicate widgets, and pages
   larger than six are rejected.
3. **No latent persona in the public API.** `StepResult.info` exposes category
   only.
4. **Honest baseline names.** The historical "Slate-LinTS" and "CombLinUCB"
   implementations are documented as pooled per-widget learners with uniform
   `page_reward / 6` credit. They are not claimed to represent the full class of
   aggregate-feedback combinatorial bandits.
5. **Leakage-free editor path.** `edp/orchestrators/observable.py` generates an
   edit report using only observable context and matured noisy page reward. It
   excludes personas, true needs, widget provisions, oracle reward, and regret.
6. **Scientific-contract tests.** `tests/test_scientific_contracts.py` locks the
   exact oracle, order invariance, page validity, and persona-hiding behavior.

## Important provenance distinction

The committed historical report-based EDP trajectories were generated with a
**privileged simulator report**. The editor saw exact persona labels,
per-persona oracle regret, persona need vectors, category multipliers, and
widget provision vectors. Those trajectories are valuable as a
simulator-informed upper bound and as an interpretability demonstration, but
are not a fair production-feedback comparison against bandits.

New main-table editor results must be generated with
`ObservableReportOrchestrator`. Privileged trajectories should be reported in a
separate upper-bound table.

## Repository map

| Path | Purpose |
|---|---|
| `edp/env.py` | Shared delayed-feedback environment |
| `edp/ground_truth.py` | Reward and exact finite-set oracle |
| `edp/policies/edp.py` | Named PWL/GAM policy and greedy composer |
| `edp/policies/bayesian_edp.py` | Online page-reward SGD with an EDP prior |
| `edp/policies/bandit.py` | Per-position LinTS with uniform page credit |
| `edp/policies/slate.py` | Pooled LinTS + uniform page credit |
| `edp/policies/comblinucb.py` | Pooled LinUCB + uniform page credit |
| `edp/orchestrators/observable.py` | Leakage-free LLM edit reports |
| `edp/orchestrators/report.py` | Historical privileged-report reproduction |
| `experiments/` | Leaderboards, sweeps, robustness runs |
| `results/` | Committed historical outputs; rerun after audit changes |
| `paper/ICML_REVIEW.md` | Independent scientific audit and revision gate |

## Quick checks

```bash
python tests/test_scientific_contracts.py
python experiments/run_leaderboard.py --n 10000 --seeds 10 \
  --out results/leaderboard_exact_oracle.json
```

The second command updates numeric-policy results to the exact oracle. It does
**not** regenerate a leakage-free LLM-editor trajectory.

## Generate a leakage-free editor trajectory

Run from the repository root. Select the persona source through the same
configuration used by the other experiments.

```bash
python -m edp.orchestrators.observable \
  --state-dir state/observable_editor_llm --reset --until 2500

# Have the editing agent follow the generated PROMPT_at_2500.md and write the
# requested edits JSON, then continue:
python -m edp.orchestrators.observable \
  --state-dir state/observable_editor_llm \
  --apply state/observable_editor_llm/edits_round_2500.json \
  --until 5000
```

Repeat for 7,500 and 10,000 sessions. The prompt contains no simulator-private
variables.

## Required experiment protocol before resubmission

- Regenerate every table and figure with the exact oracle.
- Put the observable editor in the main leaderboard and the privileged editor
  in an explicitly labeled upper-bound analysis.
- Add a genuine page-level/full-bandit baseline rather than relying only on
  uniform per-widget credit.
- Tune hyperparameters on validation seeds and report once on held-out test
  seeds/simulator variants.
- Vary environment streams, feedback noise, persona exemplars, and editor runs;
  do not estimate uncertainty from learner seeds on one fixed stream alone.
- Add an independently authored or data-fitted reward family to break the
  shared-LLM simulator/prior alignment.
- Use the official ICML style and an eight-page main paper.

## Scope of the EDP idea

The durable research hypothesis is narrower than the old headline: a compact,
named GAM may provide a useful **cold-start prior and editable deployment
artifact** under aggregate delayed feedback while remaining inspectable and
servable without an online LLM. The corrected experiments should test that
hypothesis directly, without relying on privileged simulator knowledge.
