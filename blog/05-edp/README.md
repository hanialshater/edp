# Post 5 · When world knowledge replaces exploration: EDP

**Thesis.** Posts 1–4 assumed you knew nothing about the arms / edges / cities. That is rarely true in real systems. A domain expert reading a problem can often write down a *prior policy* that is already most of the way to optimal — and an LLM is a domain expert that scales. This is the conceptual move behind **Evolvable Decision Programs** (EDP): replace from-scratch exploration with an LLM-authored, human-readable policy, and let learning do the small calibrations on top.

**Interactive question.** *On the WPO problem (choose 6 of 22 widgets for a page), how good is the LLM's first guess — before any data?* The widget loads the published `paper/policy_v_017.json` and lets you drag a curve to see the page recompose live. No clicks, no learning, no warmup. Just a readable artefact a human and an LLM both author.

## Widget design

- **State:** The actual `edp/policies/edp.py` configuration (Layer 1 = 7 PWL problem shapes, Layer 2 = 22 widget GAM specs). Hardcoded as JSON inline so the widget is self-contained.
- **Display:** Three columns mirroring the orchestrator demo (`demo/edp_orchestrator.html`):
  1. *Persona controls* (sliders for size_chart, tab_switch, return_view, etc.).
  2. *Problem fingerprint* (7 bars, computed from the sliders via PWL).
  3. *Composed page* (top-6 widgets, live).
- **Edit modes:**
  1. *drag a curve* — left panel shows the PWL shape; drag a breakpoint and watch problems and composition update.
  2. *swap a widget weight* — right panel sliders for `base`, `on_rem[F32]`, etc.; watch slot order change.
  3. *load an agent edit batch* — pull `state/evolve_state/edits_round_2500.json` and watch the policy diff applied as a single PR.
- **Stats:** session reward under the current policy (computed against a Reference oracle inline); LLM authorship cost = 0 clicks; serving latency simulated as `JS evaluation time` (sub-ms).
- **Aha:** with zero data, the LLM-authored policy already places sensible widgets. Posts 1–4 needed hundreds–thousands of trials to learn this.

## Article outline

1. *The premise of Posts 1–4.* You knew nothing about the arms. That was a feature: it gave the algorithms something to do.
2. *The cost of knowing nothing.* Even smart bandit policies pay regret during warmup. On the WPO problem this regret can be substantial — the cold-start curve from the paper (§5.7, Fig. 12) shows it directly: a tuned bandit needs ~2,500 sessions to match the LLM-authored prior.
3. *Domain knowledge as a policy.* For many problems, an expert can *read* the structure and write a competent policy without ever seeing data. EDP makes that policy *executable*: a generalised additive model with named PWL shape functions, ~245 numbers, authored by an LLM offline.
4. *Why GAMs.* Three properties: (a) every parameter has a name and a domain meaning, so an LLM can author it from world knowledge; (b) it serves in microseconds; (c) edits are atomic — a one-line diff changes one curve.
5. *What this is not.* Not a learned model — there is no training run. Not a hardcoded rules engine — every "rule" is a named scalar in a typed grammar. It is the missing middle.
6. *And the open question.* If you wrote the policy with zero data, can you keep improving it as data arrives? That is Post 6.

## Status
Stub. Widget loads from the published policy JSON; reuses the live orchestrator from `demo/edp_orchestrator.html`.
