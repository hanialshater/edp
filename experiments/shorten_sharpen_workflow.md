# Workflow: shorten + sharpen pass

A focused revision pass with three goals, run as one loop. Companion to
`review_workflow.md` (which is the review→revise→verify loop); this file
records the specific pass triggered by "shorten the paper, improve EDP,
bandits are good but LLM edits are unique."

## Goals

1. **Shorten.** The paper grew to 948 lines / ~18.5K words; §5 Results is
   403 lines with 11 subsections, and reviewers flagged that the same
   caveats (single-trial, circularity, simulator-dependence) recur across
   many sections. Target: consolidate, do not delete evidence.
2. **Sharpen EDP's unique axis.** After the α-sweep showed a tuned bandit
   ties EDP on regret, the distinctive contribution is no longer a regret
   margin. It is that the policy is **LLM-authored and LLM-editable as a
   readable artifact** — the one axis no bandit has. Make that the thesis.
3. **Credit bandits honestly.** Bandits are strong: tuned, feature-matched,
   they tie the GAM on the primary simulator. State this plainly and stop
   competing on regret; compete on the LLM-edit/closure axis.

## Procedure

### Step 1 — consolidate caveats (shortening)
- Single repeated caveats (single-trial → "K≥5 open", circularity →
  "cross-family open", simulator-dependence) get **one** canonical
  statement in §7 and are referenced, not re-argued, elsewhere.
- Merge the single-trial capability subsections (§5.8 Robust-EDP, §5.9
  drift/structural, §5.10 ensemble) into one "Capability demonstrations
  (single-trial)" subsection. Keep every number; drop the repeated
  hedging prose.
- Trim §2: the Gym-API prose and the ground-truth detail overlap; keep one
  statement of each.

### Step 2 — sharpen the LLM-edit thesis
- Abstract + §1 + §6.0 lead with: bandits tie on regret; the unique,
  defensible axis is LLM authorship + scalar-edit closure of a readable
  policy. Everything else (cold-start, audit, funnel) follows from it.
- §6.0's four properties keep their honest scope tags, but the framing
  sentence names LLM-edit closure as the *root* property, the others as
  consequences.

### Step 3 — credit bandits
- Replace any residual "bandits collapse / wrong abstraction" language with
  "bandits are strong under tuning; the gap is regime + features, and the
  GAM class's edge is the LLM-edit axis, not regret."

### Step 4 — verify
- `python experiments/check_paper_consistency.py` (must stay green — no
  number may change in this pass; it is editorial).
- Rebuild PDFs; confirm page count dropped.
- Re-read abstract + §6.0 cold: does the unique axis read as the thesis?

## Invariant
This pass changes **prose, structure, and emphasis only**. No results
number changes. The consistency checker passing before and after is the
proof that shortening did not corrupt a figure.
