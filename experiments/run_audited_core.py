"""Focused audited experiment for the lean paper revision.

This script removes three confounds from the historical headline table:
1. evaluation is on held-out environment streams rather than the editor's seed-42 stream;
2. Bayesian-EDP is split into no-editor and observable-editor variants;
3. the former `GreedyLinTS` label is replaced by an explicit random-coefficient
   EDP-SGD ablation. No Thompson sampling is claimed.

Run from the repository root:

    python experiments/run_audited_core.py --out results/audited_core.json
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import numpy as np

from edp.agents import BayesianEDPAgent, BanditAgent, EDPAgent, run_episode
from edp.env import PageCompositionEnv
from edp.policies.bandit import BanditPolicy
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.policies.edp import EDPPolicy, make_modules


TEST_SEEDS = (101, 202, 303)
OBSERVABLE_DIRS = (
    Path("state/observable_llm_rep1"),
    Path("state/observable_llm_rep2"),
    Path("state/observable_llm_rep3"),
)


def schedule(directory: Path) -> dict[int, str]:
    return {
        step: str(directory / f"edits_round_{step}.json")
        for step in (2500, 5000, 7500)
        if (directory / f"edits_round_{step}.json").exists()
    }


def random_coeff_modules(seed: int, sigma: float = 0.05) -> dict:
    """Keep the EDP feature/address structure but remove its authored coefficients."""
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


def run_method(name: str, env_seed: int, replicate: int, n: int) -> float:
    feedback_seed = env_seed * 1009 + replicate * 17 + 7
    env = PageCompositionEnv(
        n=n,
        seed=env_seed,
        source="llm",
        delay=500,
        noise_sigma=0.20,
        feedback_seed=feedback_seed,
    )

    if name == "static_llm_prior":
        agent = EDPAgent(EDPPolicy())
    elif name == "edp_sgd_llm_init_no_editor":
        policy = BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3)
        agent = BayesianEDPAgent(policy, schedule={})
    elif name == "edp_sgd_random_coeff_no_editor":
        modules = random_coeff_modules(seed=feedback_seed)
        policy = BayesianEDPPolicy(
            modules=modules,
            prior_modules=modules,
            lr=5e-4,
            lam=2.0,
            prior_sigma=0.3,
        )
        agent = BayesianEDPAgent(policy, schedule={})
    elif name == "observable_editor":
        agent = EDPAgent(EDPPolicy(), schedule=schedule(OBSERVABLE_DIRS[replicate]))
    elif name == "observable_editor_sgd":
        policy = BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3)
        agent = BayesianEDPAgent(policy, schedule=schedule(OBSERVABLE_DIRS[replicate]))
    elif name == "lints_warm_tuned_sensitivity":
        policy = BanditPolicy(ctx_dim=7, alpha=0.05, seed=feedback_seed)
        agent = BanditAgent(policy, context="warm")
    elif name == "lints_warm_default":
        policy = BanditPolicy(ctx_dim=7, alpha=0.30, seed=feedback_seed)
        agent = BanditAgent(policy, context="warm")
    else:
        raise ValueError(name)

    return float(run_episode(env, agent)["regret_pct"])


def summarize(values: list[float]) -> dict:
    array = np.asarray(values, dtype=float)
    return {
        "mean_pct": float(array.mean()),
        "sem_pct": float(array.std(ddof=1) / np.sqrt(len(array))) if len(array) > 1 else 0.0,
        "all_pct": [float(value) for value in array],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10_000)
    parser.add_argument("--out", default="results/audited_core.json")
    args = parser.parse_args()

    methods = (
        "static_llm_prior",
        "edp_sgd_llm_init_no_editor",
        "edp_sgd_random_coeff_no_editor",
        "observable_editor",
        "observable_editor_sgd",
        "lints_warm_tuned_sensitivity",
        "lints_warm_default",
    )
    output = {
        "protocol": {
            "source": "llm",
            "n": args.n,
            "train_stream_for_editor_edits": 42,
            "held_out_test_streams": list(TEST_SEEDS),
            "delay": 500,
            "noise_sigma": 0.20,
            "note": "One independent observable edit trajectory is paired with each held-out stream.",
        },
        "methods": {},
    }

    for name in methods:
        values = []
        for replicate, env_seed in enumerate(TEST_SEEDS):
            value = run_method(name, env_seed, replicate, args.n)
            values.append(value)
            print(f"{name:38s} seed={env_seed}: {value:6.2f}%", flush=True)
        output["methods"][name] = summarize(values)
        cell = output["methods"][name]
        print(
            f"{name:38s} mean={cell['mean_pct']:.2f} +/- {cell['sem_pct']:.2f}%",
            flush=True,
        )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2), flush=True)


if __name__ == "__main__":
    main()
