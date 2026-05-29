# Post 6 · EDP that adapts and explores: can a written policy keep improving?

**Thesis.** Post 5 wrote the policy from world knowledge. Post 6 asks the harder question: can the same policy keep improving as data arrives — closing the gap to the learning bandits of Posts 1–4, without losing the readable representation? This is the research bet behind the paper (`paper/paper.md`, WPO-Gym): yes, by treating LLM-authored edits as Gaussian priors and running regularised SGD on the same parameters between checkpoints (Bayesian-EDP, §5.4b). The widget makes the cold-start curve from §5.7 / Fig. 12 *playable*: race a tuned bandit against Bayesian-EDP from session 0 and watch the gap close (or not).

**Interactive question.** *Starting from session 0, at what horizon does a tuned per-slot bandit catch up to a Bayesian-EDP — and is there any horizon where it leads?* The widget runs both policies in-browser against a small in-browser WPO simulator (a 3-persona × 3-category cut of the real one) and animates the cumulative regret curves side by side.

## Widget design

- **State:** A miniature WPO simulator written in JS (3 personas, 3 categories, 8 widgets, 4 slots — a 1/3 scale of the paper's setup that runs fast in-browser). Hidden ground-truth provisions match the paper's structure but compressed.
- **Display:** Two columns:
  1. *EDP-static* (LLM prior loaded, no learning) — flat regret curve.
  2. *Bayesian-EDP* (LLM prior + SGD between mock checkpoints) — falling curve.
  3. *LinTS-warm tuned* (α = 0.05, the bandit that ties at 10K in the paper) — slowly falling curve.
- **Controls:** play/pause; speed (1×, 10×, 100×); reset; "load the real paper trajectory" button that overlays the actual `results/coldstart.json` curve so the reader sees the in-browser sim matches the paper.
- **Stats:** sessions elapsed (counter), regret-% over first N for each policy (live), gap between Bayesian-EDP and tuned bandit (positive = bandit ahead).
- **Aha:** the bandit's curve crosses Bayesian-EDP somewhere around session 5–10K *and* drifts above again — the paper's "matches or beats at every horizon" claim made visible at session scale.

## Article outline

1. *Recap.* Posts 1–4: learn from clicks, pay warmup regret. Post 5: write the policy, skip the warmup, no learning.
2. *Why "no learning" is not enough.* The world drifts (the paper's §5.9). The prior was a guess and won't be perfect.
3. *Bayesian-EDP: prior + SGD.* The LLM authors the policy *and* sets the prior of an SGD process on the same parameters. λ controls how much you trust the prior vs the data. As λ → ∞ you recover EDP-static (no learning); as λ → 0 you recover a per-slot bandit on the EDP architecture (the paper calls this GreedyLinTS).
4. *What the cold-start curve shows.* §5.7 / Fig. 12: Bayesian-EDP matches or beats even the tuned bandit at every horizon, dominates below 5K. The widget below makes that claim a play-along.
5. *Where this lands.* The series started with "you know nothing about the arms" (Post 1) and ended with "you know quite a lot and you keep learning the rest" (this post). The qualitative shift is from *learning policies* to *editing them*. The paper argues that for whole-page composition, the editable-policy axis is the unique one — bandits cover the regret axis well enough, and EDP's claim to belong in the conversation rests on what its closure properties enable for deployment.
6. *Read the paper.* `paper/paper.md`.

## Status
Stub. The mini-simulator is the biggest unbuilt piece; it should reproduce the published cold-start curve within a few percentage points to be credible.
