# Post 2 · Sorting numbers you cannot read

**Thesis.** Sorting is `O(n log n)` comparisons when the comparison oracle is exact. When the oracle is noisy (you only get the *probability* that x > y), the algorithm changes: you are in the **dueling bandit** / **noisy comparison sort** regime. Repeated comparisons let you build confidence intervals on each pair; the trick is which pairs to query, and how often.

**Interactive question.** *How many noisy comparisons do you need to sort 8 unknown numbers correctly?* The widget will let you query pairs by clicking; show the running posterior order; let you pick between mergesort-with-repeats and Copeland/Borda aggregation. Reveal the truth at the end.

## Widget design

Single HTML, vanilla JS, matching `01-bandit/`.

- **State:** 8 hidden true values drawn from Uniform(0,1). Noisy comparison oracle: P(x ≻ y) = sigmoid(τ · (xᵢ − xⱼ)) with a noise temperature τ slider (default τ = 4).
- **Display:** 8 cards in a row, each showing its current rank-estimate (1–8) and a confidence band based on wins/total per opponent.
- **Modes:**
  1. *manual* — click two cards to compare them, see the noisy answer.
  2. *uniform Borda* — round-robin every pair the same number of times, rank by win-count.
  3. *adaptive (active)* — at each step query the pair whose order is most uncertain (largest overlap of confidence bands).
- **Stats:** total comparisons used, current Kendall τ between estimated and true order, count of pairs whose order is currently "confident" (CI separation > δ).
- **Aha:** the adaptive policy reaches τ = 1.0 in ~3–4× fewer comparisons than uniform Borda. Mergesort with each comparison repeated until confident is in between.

## Article outline (≤ 1,200 words)

1. *Classical sort.* Merge / quick / heap — fully solved with an exact oracle.
2. *The twist.* What if the oracle is a wine-tasting panel: each comparison is noisy, but multiple comparisons average out? Now the algorithm spends a *budget* of comparisons across pairs.
3. *Three policies.* Uniform Borda (cheap, wasteful), adaptive sampling (where mergesort goes wrong when its noisy split is incorrect — and how to fix with repeats), Copeland aggregation.
4. *Connection to bandits.* Each pair (i, j) is a Bernoulli arm with success P(i ≻ j); you are running ⌈n/2⌉² parallel bandits, asking "which arm has the highest success prob" at the *pair* level.
5. *Why the active policy wins.* The information you need is concentrated at boundary pairs (adjacent in true order); uniform Borda spends equally on every pair, most of which are easy. Adaptive policies route budget to the boundary.
6. *Looking ahead.* Sorting is choose-the-max repeated. The next post is choose-the-max with structure: a graph, where each edge is an arm.

## Status
Stub. Build by following the procedure in `../WORKFLOW.md`.
