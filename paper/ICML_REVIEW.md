# ICML-style review: WPO-Gym / Evolvable Decision Programs

**Recommendation on the audited draft:** Reject (major scientific revision required)  
**Score:** 3/10  
**Confidence:** 5/5

This review evaluates the claims against the checked-in implementation and result provenance, not only the prose.

## Summary

The submission proposes WPO-Gym, a synthetic environment for selecting page modules under delayed, noisy, page-level feedback, and Evolvable Decision Programs (EDPs), a compact GAM policy that can be authored and edited by an LLM offline. The core product intuition is strong: an interpretable, version-controlled policy that can be edited by humans and agents, then served without an LLM, is an interesting systems and ML direction. The repository is unusually transparent and contains many ablations, committed trajectories, and diagnostic artifacts.

However, the central empirical comparison is not valid as currently framed. The report-based EDP editor is given simulator-private variables—including exact persona labels, oracle-derived regret, the simulator's persona need vectors, category multipliers, and widget provision vectors—while the bandit baselines receive only delayed noisy page reward. In addition, the reward is permutation-invariant, so the environment evaluates six-widget **set selection**, not ordered page composition. Several baselines are described as combinatorial/slate methods although their implementation simply assigns the same `page_reward / 6` target to every selected widget. The former "oracle" was greedy rather than exact. Together, these issues invalidate the headline interpretation even though the engineering artifact remains promising.

## Strengths

1. **Compelling representation idea.** A small named GAM that is editable by both humans and LLMs, auditable through additive decompositions, and served as ordinary code is genuinely interesting.
2. **Strong artifact orientation.** The repository includes policies, edit histories, simulator sources, result files, and multiple ablations rather than presenting an opaque one-off demonstration.
3. **Useful negative result.** The draft eventually concedes that a tuned feature-matched LinTS can match the best GAM at 10K sessions. This is scientifically healthier than preserving a simple "LLM beats bandits" story.
4. **Good deployment questions.** Delay, page-level feedback, cold start, auditability, and serving dependencies are relevant production constraints often absent from academic recommendation benchmarks.
5. **Readable exposition and visual diagnostics.** The policy traces and edit diffs make the proposed representation concrete.

## Major concerns

### 1. The EDP-agent comparison leaks the simulator ground truth

Severity: **fatal to the main empirical claim**.

The paper says EDP receives the same delayed/noisy/page-level signal and uses it through a diagnostic report. The implementation does something else:

- `edp/orchestrators/base.py` evaluates the policy with immediate noise-free `true_page_reward`, computes `oracle_reward`, and stores the latent persona and oracle regret for every session.
- `edp/orchestrators/report.py` aggregates per-persona and per-(persona, category) oracle regret.
- The prompt contains `TRUE_NEEDS`, the category multipliers, and `TRUE_PROVISIONS`—the exact objects defining the simulator reward.
- The bandit baselines do not receive these variables.

This is not merely a richer explanation of the same feedback. It is privileged access to the reward model. The current `EDP-agent` result should be treated as a **simulator-informed upper-bound editor**, not as a production-feedback learner. The OPRO ablation mostly compares privileged structured ground truth against a scalar score-only channel; it does not isolate "structured diagnostics" in the production-observable sense.

**Required fix:** remove this row from the main fair leaderboard, relabel the committed trajectories as privileged diagnostics, build an editor that only consumes observable context and matured noisy page reward, rerun it, and report both variants separately.

### 2. The benchmark does not evaluate ordering

Severity: **fatal to the current WPO/ordered-slate framing**.

For each need dimension, the reward is

`needs[d] * min(needs[d], sum_w provision[w,d])`.

The sequential implementation with a remaining budget is algebraically identical and therefore invariant to permutation. Reversing a page produces exactly the same reward. The valid action space is consequently

`C(22, 6) = 74,613`

six-widget sets, not

`P(22, 6) = 53,721,360`

ordered pages. Slot order affects the EDP scoring process, but the environment never rewards a better order. Calling the benchmark whole-page **ordering** or an ordered-slate benchmark overstates what is tested.

**Required fix:** either (a) reframe the paper consistently as contextual module-set selection, or (b) introduce and validate an order-aware reward with position exposure, attention decay, adjacency/synergy, or user interaction dynamics, then rerun all methods. This audit chooses the honest near-term option (a).

### 3. The former oracle was a greedy approximation

Severity: **major correctness issue, small numerical effect on the current catalog**.

The old implementation greedily chose the widget with the largest immediate marginal reward and called the result an oracle. Greedy is a standard approximation for monotone submodular maximization, not an exact oracle. It happened to be exact on all 48 parametric persona-category cells, but it is suboptimal on several LLM-persona cells. The largest audited gap is the `paralyzed_wishlister × shoes` cell: approximately 2.17% below the exact set optimum.

Because only 74,613 sets exist, there is no reason to approximate. The audit branch replaces the greedy reference with exact enumeration and adds regression tests.

**Required fix:** rerun all tables and figures against the exact oracle. Do not silently reuse old percentages.

### 4. The "combinatorial" baselines are weaker than their labels imply

Severity: **major baseline-validity issue**.

`SlateLinTSPolicy` and `CombLinUCB` select top-K widgets from independent per-widget models and then update each selected model with the same `page_reward / 6`. This is a uniform-credit heuristic. It is not a general full-bandit combinatorial linear method and does not perform joint slate credit inference.

The paper may compare against these implementations, but it must name them accurately—for example, **Pooled LinTS + uniform credit** and **Pooled LinUCB + uniform credit**—and may not conclude that combinatorial bandits as a class fail. Stronger full-bandit or slate-reward baselines are needed, such as a page-level linear model over summed/set features, neural contextual bandit, policy-gradient/slate RL baseline, or a combinatorial method designed for aggregate feedback.

### 5. Hyperparameter selection uses the evaluation conditions

Severity: **major empirical-method issue**.

The best alpha is selected per simulator/condition and reported on that same condition. This is test-set tuning. It is useful as a sensitivity analysis, but the tuned value cannot be interpreted as an unbiased leaderboard entry.

**Required fix:** define train/validation/test simulator seeds (and preferably simulator variants), tune alpha only on validation, lock it, then report test performance. Report the complete sweep in the appendix.

### 6. Shared LLM authorship creates circular simulator alignment

Severity: **major external-validity concern**.

LLMs author the persona descriptions/exemplars, latent needs, widget provisions, initial EDP parameters, and later edits. Different labels do not ensure independence: the same semantic shopping priors can align all components. Strong EDP cold-start performance may therefore measure agreement between LLM-authored artifacts rather than transferable decision quality.

**Required fix:** add at least one independently specified reward source. Strong options are: human-expert needs/provisions blinded to the policy, a behavioral model fitted to real logged interactions, multiple model families for simulator generation versus policy authoring, or an adversarially generated reward family held out from all policy construction.

### 7. Uncertainty estimates are too narrow

Severity: **major empirical-rigor concern**.

Most bandit estimates vary only the learner seed while holding one session stream fixed. EDP-agent uses three LLM trajectories. This measures algorithmic randomness on one synthetic world, not benchmark uncertainty. Some claims are based on single trials, and multiple analyses appear to have been added after inspecting outcomes.

**Required fix:** vary session streams, feedback noise seeds, simulator parameter draws, persona exemplars, and LLM editor runs. Use at least 10 independent environment seeds for numeric methods and enough editor repetitions to estimate variance credibly. Predeclare the primary metric and comparisons.

### 8. The simulator is controllable, not calibrated

Severity: **positioning concern**.

No evidence ties the synthetic reward scale, delay, noise, persona mixture, or provision map to production data. Calling it "calibrated" is unsupported. The environment is a transparent synthetic sandbox, which can still be valuable, but claims about production realism must be scoped accordingly.

### 9. Submission-format and reproducibility issues

Severity: **desk-reject risk**.

ICML 2026 requires the official style and an eight-page main paper, with appendices and references outside that limit. The checked-in `paper-icml.tex` explicitly says it uses an "ICML-spirit" imitation rather than the official style. It therefore is not a submission artifact. The manuscript is also far too broad for an eight-page main paper unless aggressively narrowed.

Use the official style files, make the main scientific claim fit in eight pages, move secondary demonstrations to the appendix, and provide one command that rebuilds every table, figure, and PDF from a clean checkout.

## Minor concerns

- "Microsecond-servable" is misleading when the reported measurement is approximately 1 ms; use "millisecond-scale" and report hardware, repetitions, median, and tail latency.
- The environment previously returned the latent persona in `StepResult.info` despite saying it was withheld. The audit branch removes it.
- The paper alternates between benchmark, method, systems primitive, and Software 3.0 manifesto. The contribution is stronger when narrowed.
- The category-sensitive reward is not matched by category context in the default bandit setup, while the privileged editor sees per-category oracle regret. This further weakens fairness.
- The claim that logged evaluation "cannot" study the problem is too absolute. Logged evaluation is difficult because of support and propensity issues, but restrictions or structured policies can make counterfactual evaluation possible.
- The policy's apparent order-specific parameters (`slot_decay`) are not identifiable from an order-invariant reward without additional assumptions.

## Questions for the authors

1. What information would a real deployment possess at an edit checkpoint? In particular, where would persona labels, need vectors, widget provisions, and per-persona oracle regret come from?
2. Is the intended contribution a set-selection benchmark or an ordered-page benchmark? If ordering is essential, what user model makes position causally affect reward?
3. Why were full-bandit page-level models omitted when aggregate page reward is the defining setting?
4. How independent are the LLM calls that authored the simulator, the prior, and the edits? Were prompts/models held out across roles?
5. What real-world measurement supports `delay=500`, `sigma=0.2`, the mixture weights, and the provision map?
6. Can the main result survive a held-out simulator family and a validation/test hyperparameter protocol?

## Minimum revision that could become reviewable

A focused resubmission could be strong if it does the following:

1. Rename the task to **contextual module-set selection under delayed aggregate feedback** unless an order-aware reward is added.
2. Use the exact finite-set oracle and regenerate every result.
3. Split the editor into:
   - **observable editor:** matured noisy page reward + observable contexts only;
   - **privileged editor:** simulator internals, clearly labeled as an upper bound.
4. Replace baseline labels with accurate names and add at least one true page-level/full-bandit learner.
5. Tune on validation seeds and evaluate once on held-out seeds/simulator variants.
6. Add an independently authored or data-fitted reward family.
7. Narrow the main paper to one claim: whether an interpretable GAM prior/update class improves cold-start under aggregate delayed feedback while remaining auditable.
8. Use the official ICML style and eight-page main-paper limit.

## Overall assessment

The representation and engineering direction are promising, and the repository is much more transparent than most early research artifacts. But the current paper's strongest result is driven by privileged simulator information, the benchmark does not test the ordered action it claims to test, and the baseline labels overstate comparator strength. These are not cosmetic issues; they change the scientific question. I would reject the current submission but encourage a substantially narrower, leakage-free resubmission.
