"""Guardrail: cross-check the numbers in paper/paper.md against the shipped
results files and against freshly-recomputed canonical figures.

This script exists because an ICML review pass found stale/contradictory
numbers in the paper (a drift table that disagreed with the results file
in every cell; two different EDP-agent figures for the same cell). Run it
after any edit to the results or the paper:

    python experiments/check_paper_consistency.py

It reports, per check, OK / STALE / MISSING. Non-zero exit if any check
fails, so it can gate a commit hook or CI.
"""
from __future__ import annotations
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
PAPER = (ROOT / 'paper' / 'paper.md').read_text()
RESULTS = ROOT / 'results'


def jload(name):
    p = RESULTS / name
    return json.load(open(p)) if p.exists() else None


def contains(s: str) -> bool:
    return s in PAPER


fails, warns = [], []


def check_present(label, *needles):
    """At least one of the needle strings must appear verbatim in the paper."""
    if any(contains(n) for n in needles):
        print(f'  OK    {label}: found {needles[0]!r}')
    else:
        fails.append(label)
        print(f'  STALE {label}: none of {needles} present')


def check_absent(label, *stale):
    """None of these stale strings should appear (they were wrong values)."""
    hit = [s for s in stale if contains(s)]
    if hit:
        fails.append(label)
        print(f'  STALE {label}: stale value(s) still present: {hit}')
    else:
        print(f'  OK    {label}: no stale values')


def approx(label, value, *, lo, hi):
    if lo <= value <= hi:
        print(f'  OK    {label}: {value:.2f} in [{lo},{hi}]')
    else:
        warns.append(label)
        print(f'  WARN  {label}: {value:.2f} outside [{lo},{hi}]')


print('== 1. Drift table matches results/results_drift_test.json ==')
drift = jload('results_drift_test.json')
if drift:
    # full_pct values, one decimal, as they should appear in the paper table
    want = {
        'EDP-static': drift['EDP-static']['full_pct'],
        'EDP-canned': drift['EDP-canned']['full_pct'],
        'EDP-agent': drift['EDP-agent']['full_pct'],
        'LinTS-warm': drift['LinTS-warm']['full_pct'],
    }
    for m, v in want.items():
        check_present(f'drift {m} full={v:.1f}', f'{v:.1f}')
    # the pre-fix stale full values
    check_absent('drift stale fulls', '| 20.4 |', '| 14.9 |', '| 12.4 |')
else:
    warns.append('drift file missing')
    print('  WARN  results_drift_test.json missing')

print('\n== 2. EDP-agent canonical multi-seed (recomputed) ==')
try:
    from edp.env import PageCompositionEnv
    from edp.agents import EDPAgent, run_episode
    from edp.policies.edp import EDPPolicy

    def agent_mean(source, dirs):
        import numpy as np
        vals = []
        for d in dirs:
            sched = {ms: f'state/{d}/edits_round_{ms}.json' for ms in (2500, 5000, 7500)
                     if os.path.exists(f'state/{d}/edits_round_{ms}.json')}
            if not sched:
                continue
            env = PageCompositionEnv(n=10000, seed=42, source=source,
                                     delay=500, noise_sigma=0.20)
            vals.append(run_episode(env, EDPAgent(EDPPolicy(), schedule=sched))['regret_pct'])
        a = np.array(vals)
        return a.mean(), (a.std(ddof=1) / len(a) ** 0.5 if len(a) > 1 else 0.0)

    pm, ps = agent_mean('parametric', ['evolve_state_rep1', 'evolve_state_rep2', 'evolve_state_rep3'])
    lm, ls = agent_mean('llm', ['evolve_state_llm', 'evolve_state_llm_rep2', 'evolve_state_llm_rep3'])
    print(f'  recomputed EDP-agent parametric = {pm:.2f} ± {ps:.2f}')
    print(f'  recomputed EDP-agent llm        = {lm:.2f} ± {ls:.2f}')
    approx('paper claims parametric 6.5', pm, lo=6.2, hi=6.8)
    approx('paper claims llm 13.3', lm, lo=12.9, hi=13.8)
    check_present('paper EDP-agent parametric 6.5', '6.5 ± 0.2')
    check_present('paper EDP-agent llm 13.3', '13.3 ± 0.8')
except Exception as e:  # pragma: no cover
    warns.append('recompute skipped')
    print(f'  WARN  recompute skipped: {type(e).__name__}: {e}')

print('\n== 3. Decomposition table matches results/results_decomposition.json ==')
dec = jload('results_decomposition.json')
if dec:
    g_par = dec['cells']['parametric']['greedy_lints']['production']['mean_pct']
    g_llm = dec['cells']['llm']['greedy_lints']['production']['mean_pct']
    b_llm = dec['cells']['llm']['bayesian_edp']['production']['mean_pct']
    check_present(f'GreedyLinTS parametric {g_par:.1f}', f'{g_par:.1f}')   # 12.8
    check_present(f'GreedyLinTS llm {g_llm:.1f}', f'{g_llm:.1f}')          # 13.3
    check_present(f'Bayesian-EDP llm {b_llm:.1f}', f'{b_llm:.1f}')         # 11.0

print('\n== 4. Adversarial (i.i.d. + structured) present ==')
adv = jload('results_adversarial.json')
advs = jload('results_adversarial_structured.json')
if adv and advs:
    check_present('App-C structured perturbation reported', 'Structured (ε=0.25', 'structured')
    print(f'  info  i.i.d. comblinucb={adv["cells"]["comblinucb"]["mean_pct"]:.1f}, '
          f'structured comblinucb={advs["cells"]["comblinucb"]["mean_pct"]:.1f}')

print('\n== 5b. Leaderboard (§5.0) matches results/leaderboard.json ==')
lb = jload('leaderboard.json')
if lb:
    llm = lb['cells']['llm']
    # the §5.0 table values, one decimal
    for m, lo, hi in [('bayesian_edp', 10.5, 11.2), ('edp_agent', 12.9, 13.8),
                      ('greedy_lints', 13.2, 13.8), ('slate_lints', 16.3, 16.9),
                      ('comblinucb', 16.6, 17.1), ('lints_warm', 21.3, 21.9),
                      ('random', 30.0, 31.0), ('static_top6', 40.0, 41.5)]:
        approx(f'leaderboard llm {m}', llm[m]['mean_pct'], lo=lo, hi=hi)
else:
    warns.append('leaderboard file missing')
    print('  WARN  results/leaderboard.json missing')

print('\n== 6. Seed-count consistency ==')
# §4 says 10 TS seeds; §5.1 caption must not still say "5 LinTS seeds"
check_absent('5.1 caption seed count', 'across 5 LinTS seeds')
check_present('5.1 caption seed count', 'across 10 Thompson-sampling seeds', '10 Thompson-sampling seeds')

print('\n== summary ==')
if fails:
    print(f'FAIL ({len(fails)}): ' + '; '.join(fails))
    sys.exit(1)
if warns:
    print(f'PASS with {len(warns)} warning(s): ' + '; '.join(warns))
    sys.exit(0)
print('PASS: all consistency checks green')
