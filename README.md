# Evolvable Decision Programs

A lean research release for contextual **module-set selection** under delayed, noisy, page-level feedback.

The repository contains one focused experiment, one result manifest, the exact simulator/oracle, three observable editor trajectories, contract tests, and the current working paper/PDF. Historical blogs, demos, privileged editor state, duplicated result files, and checkpoint prompt dumps have been removed from this research branch.

## Current result

On three held-out LLM-persona streams, with observable editor trajectories and bandit exploration selected on stream 42:

| Method | Loss vs exact clairvoyant oracle |
|---|---:|
| Observable editor + regularized SGD | **10.35 ± 0.46%** |
| LinTS warm, validation-selected α=0.05 | 10.61 ± 0.52% |
| Observable editor only | 15.02 ± 0.80% |
| EDP-SGD, LLM initialization, no editor | 16.15 ± 0.05% |
| Static LLM prior | 20.00 ± 0.01% |
| LinTS warm, default α=0.30 | 21.76 ± 0.09% |
| EDP-SGD, random coefficients | 28.51 ± 2.33% |

The result supports complementary observable editing and continuous calibration. It does **not** establish superiority over aggregate-feedback learners as a class; a genuine full-bandit page-level comparator remains missing.

## Repository map

```text
edp/                         simulator, exact oracle, policies, observable editor
experiments/run_paper.py     single primary held-out experiment
artifacts/paper_results.json canonical numbers used by the paper
artifacts/observable_editor/ retained edit batches from three independent runs
paper/paper.tex              canonical paper source
paper/paper.pdf              generated working paper
paper/figures/               generated figures used by the paper
scripts/make_figures.py      regenerate figures from the result manifest
scripts/build_paper.sh       regenerate the PDF
tests/                       scientific and artifact contracts
```

## Run

```bash
python -m pip install -e .
python experiments/run_paper.py --out artifacts/paper_results_rerun.json
python scripts/make_figures.py
bash scripts/build_paper.sh
```

Run the checks:

```bash
python tests/test_scientific_contracts.py
python tests/test_paper_artifacts.py
```

## Scientific scope

- The reward is order-invariant. The benchmark evaluates six-module **sets**, not page ordering.
- The oracle enumerates all `C(22, 6) = 74,613` valid sets.
- The metric is loss against a latent-persona clairvoyant oracle, not conventional observable-context regret.
- Observable editors see delayed noisy page reward, selected sets, categories, and feature cohorts only.
- The random-coefficient ablation retains the authored EDP feature taxonomy and module-address structure.
- The simulator is transparent and controllable, not calibrated to production behavior.

The paper discusses the remaining validity threats and the next experiment required for a stronger claim.
