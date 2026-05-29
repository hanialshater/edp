# Post 3 · Shortest path when the edge weights are hidden

**Thesis.** Dijkstra is a five-line algorithm when you know the edge weights. If you can only sample weights by traversing edges, you have an **online shortest-path problem** — a structured combinatorial bandit. The action is a *path*, the reward is path-additive, but feedback is per-edge. The trick is that the per-edge structure lets you reuse information across paths in a way per-arm bandits cannot.

**Interactive question.** *On a 4×4 grid graph with hidden edge weights, can you reach the bottom-right corner with low total weight before you've seen every edge?* The widget will let you click a path, observe its edge weights, watch a UCB-on-edges policy converge to the optimal path, and compare against a "treat each path as an arm" baseline.

## Widget design

- **State:** 4×4 grid graph, edge weights drawn from Uniform(0.1, 1.0). Source = top-left, sink = bottom-right.
- **Display:** the grid, edge thickness = your current uncertainty (1/√n), edge colour = mean estimate. The optimal path is a hidden "ground truth" overlay revealed on demand.
- **Modes:**
  1. *manual* — click cells to build a path; on "go", traverse it and reveal edge weights along the path (one noisy sample each).
  2. *full-bandit* — each path is one arm. After T trials, regret is large because the action space (number of paths) is exponential in the grid size and never deduplicates per-edge knowledge.
  3. *combinatorial UCB (CombLinUCB-style)* — each edge has a mean + confidence; pick the path minimising the LCB sum. Converges in O(|E| · log T) regret.
- **Stats:** trials so far, edges sampled, current best path, regret vs the (hidden) optimal path.
- **Aha:** combinatorial UCB needs ~|E| trials to converge; full-bandit needs ~|paths|.

## Article outline

1. *Dijkstra with known weights.* The algorithm.
2. *Online setting.* You traverse a path, observe weights along it. This is the *semi-bandit* observation model; full-bandit would only show you the total.
3. *Why per-edge bandits beat per-path bandits.* The combinatorial action space is exponential, but knowledge is per-edge and is *shared* across paths that include the same edge. CombLinUCB exploits this.
4. *The credit-assignment foreshadow.* Semi-bandit (per-edge) feedback is much easier than bandit (only total) feedback — and this is the same axis that defeats per-slot LinTS in the WPO paper (§5.2): page-level attribution is the bandit case, per-slot attribution is the semi-bandit case. The harder credit problem is harder for the *same* structural reason.
5. *Onward.* TSP, where the action space and the structure both intensify.

## Status
Stub.
