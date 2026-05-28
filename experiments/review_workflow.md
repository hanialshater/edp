# Paper review & revision workflow

A repeatable loop for taking `paper/paper.md` through a venue-quality
(ICML-style) review and revising it. Each pass produced a measurable
improvement; this is the process, not a one-off.

## The loop

```
   ┌─ 1. REVIEW ─────────────────────────────────────────────┐
   │  spawn N independent reviewer agents, distinct lenses,   │
   │  the real ICML rubric. Demanding-but-fair. No coaching.  │
   └────────────────────────────┬────────────────────────────┘
                                 ▼
   ┌─ 2. META-REVIEW ────────────────────────────────────────┐
   │  cluster the weaknesses by (a) factual bug, (b) missing  │
   │  content, (c) framing/overclaim, (d) needs-new-experiment│
   │  rank by leverage × fixability. Bugs first.              │
   └────────────────────────────┬────────────────────────────┘
                                 ▼
   ┌─ 3. REVISE ─────────────────────────────────────────────┐
   │  fix bugs against the source-of-truth files; add missing │
   │  content; soften overclaims to match evidence; run any   │
   │  cheap experiment that defuses a sharp objection.        │
   └────────────────────────────┬────────────────────────────┘
                                 ▼
   ┌─ 4. VERIFY ─────────────────────────────────────────────┐
   │  python experiments/check_paper_consistency.py           │
   │  rebuild PDFs; re-read changed sections cold.            │
   └────────────────────────────┬────────────────────────────┘
                                 ▼
              repeat until reviewer scores stop moving
```

## 1. Review — reviewer lenses

Spawn three reviewers in parallel (one message, three Agent calls), each
reading `paper/paper.md` in full, each with a distinct expertise so the
weaknesses they surface do not overlap:

- **R1 — bandits / online-learning theory.** Strawman baselines? Are
  significance and mechanism claims supported? Missing baselines (neural
  bandits, IPS/DR, slate-reward estimators)? Is the metric neutral?
- **R2 — LLMs / interpretable ML / neuro-symbolic.** Novelty vs prior
  art (OPRO, FunSearch, Eureka, ADAS, EBM/GA²M, symbolic-policy RL)? Is
  related work adequate? Is the central validity threat handled? Is the
  ablation a clean isolation?
- **R3 — empirical rigor.** Are numbers internally consistent across
  abstract / tables / conclusion and against the shipped result files?
  Enough seeds for the claimed σ? Single-trial results flagged honestly?
  Cherry-picking across the two simulators?

Each returns the ICML form: Summary, Soundness/Presentation/Contribution
(1–4), Strengths, Weaknesses (cite sections), Questions, Overall (1–10),
Confidence (1–5), and "top 3 things that would raise the score."

The reviewer prompts used for the last pass are archived verbatim in
`experiments/review_prompts/` so the review is reproducible.

## 2. Meta-review — triage

Bucket every distinct weakness:

| Bucket | Action | Priority |
|---|---|---|
| (a) factual bug / inconsistency | fix against source-of-truth file; add a guardrail check | **first** — desk-reject risk |
| (b) missing content (e.g. related work) | write it; it is pure upside | high |
| (c) framing / overclaim | soften to exactly what the evidence supports | high — cheap, raises soundness |
| (d) needs a new experiment | run it if cheap & API-free; else log as the top open item | as budget allows |

Do **not** let (d) block (a)–(c). Most score movement comes from (a)–(c).

## 3. Revise — principles

- **Source of truth is the results file, not the prose.** When a table and
  a `.json`/`.npz` disagree, the file wins; recompute if the file is absent.
- **One canonical value per (method, simulator, condition).** If two
  legitimate measurements exist (e.g. N=3 subagent mean vs single canned
  trajectory), label both and cross-reference; never let them read as a
  contradiction.
- **Soften, don't delete, an interesting-but-unproven claim.** Mark it a
  conjecture, state what would prove it. (See the §5.3 UCB/TS rewrite.)
- **Every "within SE / significant" needs a test or a hedge.** A
  single-trial point cannot be "within SE" of an interval — say "indicative."

## 4. Verify

```bash
python experiments/check_paper_consistency.py     # guardrail; non-zero exit on stale numbers
python experiments/build_paper_pdf.py             # plain PDF
python experiments/build_icml_pdf.py              # ICML two-column PDF
```

`check_paper_consistency.py` cross-checks the drift table, the
decomposition table, the seed-count caption, the adversarial appendix, and
recomputes the canonical EDP-agent multi-seed number from the committed
edit trajectories. Extend it whenever a new headline number enters the
paper, so the same class of bug cannot recur.

## Standing open items (the (d) bucket, ranked)

These are the experiments reviewers most want; each is logged in §7/§8.
None has been run; the first two need no paid API.

1. **Cross-family ground-truth regeneration** — author `TRUE_PROVISIONS`
   and the editor with an open-weight non-Claude model (Llama/Qwen/Mistral).
   The single highest-leverage experiment for the circularity threat.
   (A structured-perturbation partial check is done — App C.)
2. **Per-condition exploration-parameter sweep** for every bandit, and a
   page-level / slate-reward bandit baseline (IPS/DR or slate-as-arm) that
   does not need per-arm credit.
3. **K ≥ 10 multi-seed** for the single-trial capability arms
   (§5.4d Layer-1, §5.8 Robust, §5.9 structural, §5.10 ensemble).
4. **Offline IPS/DR evaluation on a public slate-recommendation dataset**
   to ground the production claim outside the self-authored simulator.
