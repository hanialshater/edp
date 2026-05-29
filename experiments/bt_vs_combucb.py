"""Bradley-Terry active sorting vs Combinatorial-UCB bandit on top-k.

Two policies on the SAME synthetic top-k slate problem (N items, pick K),
to show the generality thread of the blog series: both are a bandit shell
wrapped around a base solver, but they consume different feedback.

  Policy A - Bradley-Terry active sorting.
    Feedback: one noisy pairwise comparison per round (a duel).
    Solver:   fit latent item utilities by online BT-logistic SGD; sort.
    Philosophy: preference estimation -> ranking inference.

  Policy B - Combinatorial-UCB bandit.
    Feedback: noisy reward for each of the K selected items (semi-bandit).
    Solver:   UCB score per item; pick top-K.
    Philosophy: online slate decision-making.

This is deliberately NOT a fair head-to-head: Comb-UCB sees K reward
samples per round, BT sees one comparison bit. The point is not "who wins"
but that the same top-k goal admits two feedback regimes, and the
combinatorial-bandit shell is the general one (BT is the special case
whose base solver happens to be a preference model). The blog widget and
the surrounding text both state this caveat explicitly.

Headless; writes results/bt_vs_combucb.json. No plotting, no pandas.
    python experiments/bt_vs_combucb.py
"""
from __future__ import annotations
import json
import os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_SEED = 42
N_ITEMS = 30
K = 5
T = 1000
N_RUNS = 40
BT_LR0 = 0.25
CB_NOISE_STD = 0.5
CB_ALPHA = 1.5


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def top_k_accuracy(selected, optimal_set):
    return len(set(selected) & optimal_set) / len(optimal_set)


def run_one(seed):
    rng = np.random.default_rng(seed)
    true_theta = rng.normal(0, 1, size=N_ITEMS)
    true_order = np.argsort(-true_theta)
    optimal_items = true_order[:K]
    optimal_set = set(optimal_items.tolist())
    optimal_value = float(true_theta[optimal_items].sum())

    # ---- Policy A: Bradley-Terry active sorting ----
    bt_theta = np.zeros(N_ITEMS)
    bt_counts = np.zeros(N_ITEMS)

    def bt_prob(i, j, theta):
        return sigmoid(theta[i] - theta[j])

    def sample_duel(i, j):
        return (i, j) if rng.random() < bt_prob(i, j, true_theta) else (j, i)

    def choose_uncertain_pair():
        order = np.argsort(-bt_theta)
        boundary = list(order[max(0, K - 3): min(N_ITEMS, K + 4)])
        best_pair, best_score = None, -np.inf
        for a in boundary:
            for b in boundary:
                if a >= b:
                    continue
                gap = abs(bt_theta[a] - bt_theta[b])
                unc = 1 / np.sqrt(1 + bt_counts[a]) + 1 / np.sqrt(1 + bt_counts[b])
                score = unc - gap
                if score > best_score:
                    best_score, best_pair = score, (a, b)
        return best_pair

    bt_regret, bt_acc = [], []
    for t in range(1, T + 1):
        i, j = choose_uncertain_pair()
        w, l = sample_duel(i, j)
        lr = BT_LR0 / np.sqrt(1 + t / 100)
        p = bt_prob(w, l, bt_theta)
        g = 1 - p
        bt_theta[w] += lr * g
        bt_theta[l] -= lr * g
        bt_theta -= bt_theta.mean()
        bt_counts[i] += 1
        bt_counts[j] += 1
        sel = np.argsort(-bt_theta)[:K]
        bt_regret.append(optimal_value - float(true_theta[sel].sum()))
        bt_acc.append(top_k_accuracy(sel.tolist(), optimal_set))

    # ---- Policy B: Combinatorial-UCB bandit ----
    cb_mean = np.zeros(N_ITEMS)
    cb_counts = np.zeros(N_ITEMS)
    cb_regret, cb_acc = [], []
    for t in range(1, T + 1):
        ucb = cb_mean + CB_ALPHA * np.sqrt(np.log(t + 1) / (1 + cb_counts))
        sel = np.argsort(-ucb)[:K]
        rewards = true_theta[sel] + rng.normal(0, CB_NOISE_STD, size=K)
        for item, r in zip(sel, rewards):
            cb_counts[item] += 1
            cb_mean[item] += (r - cb_mean[item]) / cb_counts[item]
        cb_regret.append(optimal_value - float(true_theta[sel].sum()))
        cb_acc.append(top_k_accuracy(sel.tolist(), optimal_set))

    return (np.array(bt_regret), np.array(bt_acc),
            np.array(cb_regret), np.array(cb_acc))


def main():
    btR, btA, cbR, cbA = [], [], [], []
    for r in range(N_RUNS):
        a, b, c, d = run_one(BASE_SEED + r)
        btR.append(a); btA.append(b); cbR.append(c); cbA.append(d)
    btR = np.vstack(btR); btA = np.vstack(btA)
    cbR = np.vstack(cbR); cbA = np.vstack(cbA)

    milestones = [10, 25, 50, 100, 200, 500, 1000]
    out = {
        "config": {"n_items": N_ITEMS, "k": K, "T": T, "n_runs": N_RUNS,
                   "bt_lr0": BT_LR0, "cb_noise_std": CB_NOISE_STD,
                   "cb_alpha": CB_ALPHA, "seed": BASE_SEED},
        "milestones": milestones,
        "bt": {"acc": [float(btA[:, m - 1].mean()) for m in milestones],
               "regret": [float(btR[:, m - 1].mean()) for m in milestones],
               "final_acc_mean": float(btA[:, -1].mean()),
               "final_acc_std": float(btA[:, -1].std()),
               "cum_regret_mean": float(btR.sum(axis=1).mean())},
        "cb": {"acc": [float(cbA[:, m - 1].mean()) for m in milestones],
               "regret": [float(cbR[:, m - 1].mean()) for m in milestones],
               "final_acc_mean": float(cbA[:, -1].mean()),
               "final_acc_std": float(cbA[:, -1].std()),
               "cum_regret_mean": float(cbR.sum(axis=1).mean())},
    }
    # downsampled mean curves for the blog; force-include the final round
    # so the last plotted point equals the converged value (not a mid-run
    # exploration dip at round 991).
    idxs = list(range(0, T, 10))
    if idxs[-1] != T - 1:
        idxs.append(T - 1)
    out["curve_x"] = [i + 1 for i in idxs]
    out["bt_acc_curve"] = [float(btA[:, t].mean()) for t in idxs]
    out["cb_acc_curve"] = [float(cbA[:, t].mean()) for t in idxs]
    out["bt_regret_curve"] = [float(btR[:, t].mean()) for t in idxs]
    out["cb_regret_curve"] = [float(cbR[:, t].mean()) for t in idxs]
    path = os.path.join(ROOT, "results", "bt_vs_combucb.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"saved -> {path}")
    print(f"\n{'milestone':>9} {'BT acc':>8} {'CB acc':>8} {'BT reg':>8} {'CB reg':>8}")
    for i, m in enumerate(milestones):
        print(f"{m:>9} {out['bt']['acc'][i]:>8.2f} {out['cb']['acc'][i]:>8.2f} "
              f"{out['bt']['regret'][i]:>8.2f} {out['cb']['regret'][i]:>8.2f}")
    print(f"\nfinal top-k acc: BT {out['bt']['final_acc_mean']:.3f}+/-{out['bt']['final_acc_std']:.3f}  "
          f"CB {out['cb']['final_acc_mean']:.3f}+/-{out['cb']['final_acc_std']:.3f}")
    print(f"cumulative regret: BT {out['bt']['cum_regret_mean']:.1f}  CB {out['cb']['cum_regret_mean']:.1f}")


if __name__ == "__main__":
    main()
