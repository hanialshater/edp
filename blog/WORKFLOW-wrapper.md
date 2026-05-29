# Workflow addendum — the "combinatorial bandit as a wrapper" thread

Adds the unifying idea the series was missing: a combinatorial bandit is
not a new algorithm, it is a **reduction** — an optimism (or posterior)
wrapper around a *classical solver you already have*.

```
comb_bandit(solver, problem, T):
    est = per-parameter mean + count          # one scalar per edge / pair / arm
    for t in 1..T:
        optimistic = est.mean − bonus(est.count, t)   # UCB-style optimism
        action     = solver(problem, optimistic)      # <-- classical algo, UNCHANGED
        observed   = problem.play(action)             # semi-bandit: per-component feedback
        est.update(observed)                          # only the touched parameters
```

Swap `solver` and you get a different combinatorial bandit for free:
- `solver = argmax`           → multi-armed bandit (Post 1)
- `solver = rank-aggregate`   → sort under a **Bradley-Terry** oracle (Post 2)
- `solver = Dijkstra`         → online shortest path (Post 3)
- `solver = Prim`             → online minimum spanning tree (new)
- `solver = 2-opt`            → online TSP (Post 4)
- `solver = greedy submodular`→ **GreedyLinTS / the EDP architecture** (the paper, §5.4c)

EDP is the same shape with the optimism term replaced by an LLM-authored
prior: `action = solver(problem, prior + small SGD correction)`.

## Two deliverables

1. **Post 2 → Bradley-Terry, made explicit.** The noisy comparison
   oracle `P(i≻j) = σ(s_i − s_j)` *is* the Bradley-Terry model. Add a
   panel that fits BT latent skills from the win matrix (a few Newton /
   MM steps) and shows the estimates converging to the true skills. The
   point: the comb bandit chooses *which pairs to compare* (experimental
   design) and a BT fit + sort sits on top.

2. **New Interlude post (`blog/4b-pattern/`).** One widget, one fixed
   wrapper, a dropdown of base solvers on a shared hidden-weight graph
   (argmax / Dijkstra / Prim-MST / 2-opt). The reader changes one
   function and watches the identical learning machinery drive a
   different classical algorithm. Closes with the line to the paper:
   GreedyLinTS is this wrapper around the greedy page composer; EDP swaps
   optimism for an LLM prior.

## Numbering

Insert as an interlude between Post 4 and Post 5 (`blog/4b-pattern/`),
leaving the 1–6 folders and links intact. Index lists it as
"Interlude · after Post 4".

## Verify
- Both files smoke-test under Node (parse + IIFE run).
- BT fit recovers true skill order (Kendall τ → 1) on a clean run.
- Interlude: each solver's regret curve flattens; switching solver
  re-inits cleanly.
