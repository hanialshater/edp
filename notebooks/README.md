# Example notebooks

Worked examples for the `edp` package, built around the Gym-like
environment/agent API (`edp/env.py`, `edp/agents.py`).

| Notebook | Shows |
|---|---|
| `01_quickstart.ipynb` | The `PageCompositionEnv` + `run_episode` API. Runs EDP-static, LinTS-warm, and Bayesian-EDP through the same environment and plots cumulative regret. |
| `02_explainability.ipynb` | The open-box decision trace behind Figure 9: one session traced from 14 raw signals → 7 problem scores → an additive slot-1 score decomposition. |
| `03_custom_policy.ipynb` | Writing your own agent. A deterministic baseline and a small online learner, each conforming to the `act` / `learn` / `maybe_checkpoint` protocol. |

The notebooks are checked in without pre-executed outputs. Every code
cell has been verified to run; regenerate the notebooks with
`python experiments/build_notebooks.py`.

Run them from this directory (they add the repo root to `sys.path`):

```bash
cd notebooks
jupyter lab        # or: jupyter notebook
```
