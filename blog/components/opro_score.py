#!/usr/bin/env python3
"""Black-box scorer for the OPRO post's three objectives.

Mirrors the score() functions in blog/05-opro/index.html exactly. Used to test
"can an LLM explore?" with subagents: a subagent proposes candidates and calls
this CLI to score them, seeing ONLY the scalar (lower is better) — never this
source. That is the OPRO loop with the LLM as the optimizer.

Usage:
    python3 opro_score.py <task> '<json-candidate>'
    task ∈ {regression, tsp, lp}
Prints one float (lower = better). Invalid candidates score a large penalty.

Known optima (for grading a run):
    regression : 0.0    at {"a": 2,   "b": -1.5}
    tsp        : 2.3257 at {"route": [0,1,2,3,4]}
    lp         : -5.8   at {"x": 1.8, "y": 0.2}   (rides the binding-constraint corner)

Recorded agent run (3 general-purpose subagents, blind to this file):
    regression -> 0.0189 in 34 calls (near-perfect descent)
    tsp        -> 2.3257 in 13 calls (exact global optimum)
    lp         -> -5.60  in 27 calls (stuck one corner short of -5.80)
The LP near-miss is the point: score-only feedback has no gradient, so the agent
exploited a locally-good corner and could not see the better binding corner --
the OPRO fragility the post describes, and what structured context (EDP) fixes.
"""
import sys, json, math

TSP_PTS = [[.12, .22], [.72, .16], [.86, .68], [.36, .82], [.18, .58]]

def score_regression(c):
    a = float(c.get("a", 0)); b = float(c.get("b", 0))
    return (a - 2) ** 2 + (b + 1.5) ** 2 + 0.08 * abs(a + b - 0.5)

def score_tsp(c):
    r = c.get("route", [])
    try:
        r = [int(x) for x in r]
    except (TypeError, ValueError):
        return 99.0
    if len(set(r)) != 5 or any(x < 0 or x > 4 for x in r):
        return 99.0
    s = 0.0
    for i in range(5):
        a = TSP_PTS[r[i]]; b = TSP_PTS[r[(i + 1) % 5]]
        s += math.hypot(a[0] - b[0], a[1] - b[1])
    return s

def score_lp(c):
    x = float(c.get("x", 0)); y = float(c.get("y", 0))
    penalty = 20 * max(0, x + y - 2) + 20 * max(0, .5 - x) + 20 * max(0, .2 - y)
    return -(3 * x + 2 * y) + penalty

SCORERS = {"regression": score_regression, "tsp": score_tsp, "lp": score_lp}

def main():
    if len(sys.argv) < 3:
        print("usage: opro_score.py <regression|tsp|lp> '<json>'", file=sys.stderr)
        sys.exit(2)
    task = sys.argv[1]
    if task not in SCORERS:
        print(f"unknown task {task!r}", file=sys.stderr); sys.exit(2)
    try:
        cand = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"50.0  # invalid JSON: {e}")  # malformed proposal -> bad score
        return
    print(f"{SCORERS[task](cand):.5f}")

if __name__ == "__main__":
    main()
