# Archived ICML reviewer prompts

The three reviewer-agent prompts used in the review pass that drove the
revision documented in `../review_workflow.md`. Each was given to an
independent subagent that read `paper/paper.md` in full and returned the
ICML review form. They are archived verbatim so the review is reproducible
and so the next pass can diff its prompts against these.

Spawn all three in parallel (one message, three Agent tool calls). Keep the
lenses disjoint; the value is in non-overlapping weaknesses.
