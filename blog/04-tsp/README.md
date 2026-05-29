# Post 4 · TSP when the city distances are unknown

**Thesis.** With known distances, metric TSP has a 1.5-approximation (Christofides) and is well-understood. With unknown distances revealed only along tours you traverse, you have a combinatorial bandit over tours with `n!` arms — but again the structure (per-edge distances, shared across tours) lets you escape the exponential.

**Interactive question.** *Given 8 cities placed on a map with hidden true distances, how many tours do you need to find a near-optimal one?* The widget lets you sketch tours, observe edge distances along each, and watch a combinatorial method (EXP3 over tours? CombUCB on edges + 2-opt?) converge.

## Widget design

- **State:** 8 cities placed randomly on a unit square. True pairwise distances = Euclidean + Gaussian noise with σ slider. Tour cost = sum of edges traversed; minimum tour = the optimal Hamiltonian cycle (precomputed exactly).
- **Display:** map with cities; current best estimated tour drawn in colour; shaded uncertainty around each city edge by 1/√n.
- **Modes:**
  1. *manual* — draw a tour by clicking cities in order; observe its edges.
  2. *random tours* — sample tours uniformly; report regret.
  3. *2-opt with noisy edge estimates* — maintain per-edge mean estimates; apply 2-opt swaps in expectation.
  4. *CombUCB on edges* — each edge has a mean + confidence; tour selection minimises sum of LCB along the tour (NP-hard exactly, approximate via 2-opt on LCB).
- **Stats:** tours run, cost of best estimated tour vs true optimum, edges observed, fraction of edges with confident estimate.

## Article outline

1. *Christofides recap.* 1.5-approx on metric instances.
2. *Without distances.* Each tour is an arm, but `n!` arms — full-bandit is hopeless. Per-edge feedback (semi-bandit) plus 2-opt on estimates is the right object.
3. *Two-opt as a bandit-friendly local search.* Because 2-opt edits only touch a few edges per step, the algorithm naturally focuses sampling on edges that matter.
4. *Why this is the same shape as Posts 1-3.* All four posts are "argmax over an action set, observed noisily, with progressively more structure that lets observation budget translate into better action choice."
5. *And now, the move.* In Posts 1–4 you knew nothing about the arms. What if you had a domain expert who could read the city map and *guess* good tours before sampling? That guess is what Post 5 turns into a policy.

## Status
Stub.
