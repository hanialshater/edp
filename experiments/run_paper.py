"""Reproduce the lean paper's primary held-out experiment.

The observable editor trajectories and LinTS exploration value are selected on
stream 42. Evaluation uses held-out streams 101, 202, and 303.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from statistics import mean, stdev

import numpy as np

from edp.agents import BayesianEDPAgent, BanditAgent, EDPAgent, run_episode
from edp.env import PageCompositionEnv
from edp.policies.bandit import BanditPolicy
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.edp import EDPPolicy, make_modules

TEST_SEEDS = (101, 202, 303)
EDITOR_DIRS = (
    Path("artifacts/observable_editor/llm_rep1"),
    Path("artifacts/observable_editor/llm_rep2"),
    Path("artifacts/observable_editor/llm_rep3"),
)
MILESTONES = (500, 1000, 2500, 5000, 7500, 10000)


def edit_schedule(directory: Path) -> dict[int, str]:
    schedule = {
        step: str(directory / f"edits_{step}.json")
        for step in (2500, 5000, 7500)
    }
    missing = [path for path in schedule.values() if not Path(path).exists()]
    if missing:
        raise FileNotFoundError(f"missing editor artifacts: {missing}")
    return schedule


def random_coeff_modules(seed: int, sigma: float = 0.05) -> dict:
    """Remove authored coefficients while retaining EDP structure and addresses."""
    rng = np.random.default_rng(seed)
    modules = copy.deepcopy(make_modules())
    for module in modules.values():
        module["base"] = float(rng.normal(0.0, sigma))
        module["slot_decay"] = 0.0
        module["on_rem"] = {
            key: float(rng.normal(0.0, sigma)) for key in module.get("on_rem", {})
        }
        module["on_cov"] = {
            key: float(rng.normal(0.0, sigma)) for key in module.get("on_cov", {})
        }
    return modules


def build_agent(name: str, replicate: int, seed: int):
    if name == "static_llm_prior":
        return EDPAgent(EDPPolicy())
    if name == "edp_sgd_llm_init_no_editor":
        return BayesianEDPAgent(
            BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3), schedule={}
        )
    if name == "edp_sgd_random_coeff_no_editor":
        modules = random_coeff_modules(seed)
        return BayesianEDPAgent(
            BayesianEDPPolicy(
                modules=modules,
                prior_modules=modules,
                lr=5e-4,
                lam=2.0,
                prior_sigma=0.3,
            ),
            schedule={},
        )
    if name == "observable_editor":
        return EDPAgent(EDPPolicy(), schedule=edit_schedule(EDITOR_DIRS[replicate]))
    if name == "observable_editor_sgd":
        return BayesianEDPAgent(
            BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3),
            schedule=edit_schedule(EDITOR_DIRS[replicate]),
        )
    if name == "lints_warm_validation_selected":
        return BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.05, seed=seed), context="warm")
    if name == "lints_warm_default":
        return BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.30, seed=seed), context="warm")
    raise ValueError(name)


def run_cell(name: str, env_seed: int, replicate: int, n: int):
    policy_seed = env_seed * 1009 + replicate * 17 + 7
    env = PageCompositionEnv(
        n=n,
        seed=env_seed,
        source="llm",
        delay=500,
        noise_sigma=0.20,
        feedback_seed=policy_seed,
    )
    result = run_episode(env, build_agent(name, replicate, policy_seed))
    return float(result["regret_pct"]), env


def summarize(values: list[float]) -> dict:
    array = np.asarray(values, dtype=float)
    return {
        "mean_pct": float(array.mean()),
        "sem_pct": float(array.std(ddof=1) / np.sqrt(len(array))) if len(array) > 1 else 0.0,
        "all_pct": [float(value) for value in array],
    }


def paired_improvement(methods: dict, baseline: str, improved: str) -> dict:
    values = [
        a - b
        for a, b in zip(methods[baseline]["all_pct"], methods[improved]["all_pct"])
    ]
    return {
        "mean_pp": float(mean(values)),
        "sem_pp": float(stdev(values) / len(values) ** 0.5) if len(values) > 1 else 0.0,
        "all_pp": values,
    }


def milestone_curve(agent_name: str, n: int) -> list[float]:
    curves = []
    reps = range(3) if agent_name.startswith("lints") else range(1)
    for rep in reps:
        _, env = run_cell(agent_name, 42, rep, n)
        curve = []
        for milestone in MILESTONES:
            oracle = float(env.oracles[:milestone].sum())
            reward = float(env.rewards[:milestone].sum())
            curve.append(100.0 * (oracle - reward) / oracle)
        curves.append(curve)
    return np.asarray(curves).mean(axis=0).tolist()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--out", default="artifacts/paper_results.json")
    args = parser.parse_args()

    names = (
        "static_llm_prior",
        "edp_sgd_llm_init_no_editor",
        "edp_sgd_random_coeff_no_editor",
        "observable_editor",
        "observable_editor_sgd",
        "lints_warm_validation_selected",
        "lints_warm_default",
    )
    methods = {}
    for name in names:
        values = []
        for replicate, env_seed in enumerate(TEST_SEEDS):
            value, _ = run_cell(name, env_seed, replicate, args.n)
            values.append(value)
            print(f"{name:38s} stream={env_seed}: {value:6.2f}%", flush=True)
        methods[name] = summarize(values)

    output = {
        "version": 1,
        "protocol": {
            "source": "llm",
            "n": args.n,
            "train_stream_for_editor_and_alpha_selection": 42,
            "held_out_test_streams": list(TEST_SEEDS),
            "delay": 500,
            "noise_sigma": 0.20,
            "metric": "percentage loss against exact latent-persona clairvoyant oracle",
            "editor_pairing": "one independent observable trajectory per held-out stream",
        },
        "held_out_primary": methods,
        "paired_improvements": {
            "observable_editor_plus_sgd_vs_static": paired_improvement(
                methods, "static_llm_prior", "observable_editor_sgd"
            ),
            "observable_editor_plus_sgd_vs_no_editor_sgd": paired_improvement(
                methods, "edp_sgd_llm_init_no_editor", "observable_editor_sgd"
            ),
            "observable_editor_plus_sgd_vs_observable_editor": paired_improvement(
                methods, "observable_editor", "observable_editor_sgd"
            ),
            "llm_init_sgd_vs_random_coeff_sgd": paired_improvement(
                methods, "edp_sgd_random_coeff_no_editor", "edp_sgd_llm_init_no_editor"
            ),
        },
        "cold_start_stream42": {
            "sessions": list(MILESTONES),
            "static_llm_prior": milestone_curve("static_llm_prior", args.n),
            "lints_warm_alpha_005": milestone_curve(
                "lints_warm_validation_selected", args.n
            ),
        },
        "limitations": [
            "Three held-out streams are preliminary.",
            "The exact oracle observes latent persona and is a clairvoyant upper bound.",
            "The random-coefficient ablation retains the authored feature taxonomy and module address structure.",
            "A genuine full-bandit page-level comparator is not yet included.",
        ],
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2), flush=True)


if __name__ == "__main__":
    main()
