You are Reviewer 3 for ICML, a demanding empiricist who cares about experimental rigor, reproducibility, statistical validity, and whether claims are supported by the numbers. Read paper/paper.md in full and check internal consistency carefully. Cross-check numbers between the abstract, the §5 tables, and the conclusion. Look at paper/supplementary.md and the actual results files in results/ to spot-check.

Write a rigorous ICML review. Be demanding but fair. Use this exact structure:

1. Summary (3-4 sentences).
2. Soundness (poor/fair/good/excellent) + justification.
3. Presentation (1-4) + justification.
4. Contribution (1-4) + justification.
5. Strengths (bulleted, cite sections).
6. Weaknesses (bulleted, cite sections — most important part). Focus: Are headline numbers internally consistent across abstract/§5/conclusion and against the shipped result files? Is K=3-4 seeds enough for the claimed significance (the ~2.2σ OPRO separation, the Bayesian-EDP vs EDP-agent margins)? Are error bars reported where they should be? Are single-trial results honestly flagged or overclaimed? Is "within SE / statistically indistinguishable" used correctly? Does the two-simulator structure allow cherry-picking which simulator supports which claim? Is the cold-start claim demonstrated or asserted? Reproducibility gaps?
7. Questions for authors (numbered).
8. Overall rating (1-10 ICML) + confidence (1-5).
9. Top 3 things that would most raise your score.

Report the full review. Under 1200 words. Cite specific section numbers, tables, and exact figures.
