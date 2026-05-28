"""
Final head-to-head: load all method trajectories on the same 10k-session
stream and report cumulative regret at milestone sessions.

Methods:
  - oracle              (per-session upper bound from sim.oracle_reward)
  - edp_static          (no evolution, from results_prod_stack.npz)
  - edp_evolved_canned  (canned edits at 2500/5000/7500, from results_prod_stack.npz)
  - bandit_warm         (LinTS warm context under production stack, from results_prod_stack.npz)
  - bandit_cold         (LinTS cold context under production stack, from results_prod_stack.npz)
  - edp_evolved_agent   (live report-based subagent edits, from evolve_state/state.json)
  - edp_evolved_opro    (OPRO-style live subagent edits, from opro_state/state.json)
"""
from __future__ import annotations
import json
import numpy as np

from sim import make_session_stream, oracle_reward


def load_npz_results(path='../results/results_prod_stack.npz'):
    data = np.load(path, allow_pickle=True)
    return {k: data[k] for k in data.files if k != 'stream_personas'}


def load_orchestrator_rewards(state_json: str) -> np.ndarray:
    with open(state_json) as f:
        s = json.load(f)
    return np.array(s['rewards']), np.array(s['oracle'])


def cum_regret(reward: np.ndarray, oracle: np.ndarray) -> np.ndarray:
    return np.cumsum(oracle - reward)


def main():
    # All methods use the same session stream (seed=42, n=10000).
    n = 10000
    stream = make_session_stream(n, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])

    npz = load_npz_results('../results/results_prod_stack.npz')
    r_report, o_report = load_orchestrator_rewards('../state/evolve_state/state.json')
    r_opro, o_opro = load_orchestrator_rewards('../state/opro_state/state.json')

    # Sanity: all oracles should agree
    assert np.allclose(oracle, o_report), 'report-agent oracle stream differs!'
    assert np.allclose(oracle, o_opro), 'OPRO oracle stream differs!'
    assert np.allclose(oracle, npz['oracle']), 'bandit oracle stream differs!'

    methods = {
        'edp_static':          npz['edp_static'],
        'edp_evolved_canned':  npz['edp_evolved'],
        'edp_evolved_agent':   r_report,
        'edp_evolved_opro':    r_opro,
        'bandit_warm':         npz['bandit_warm'],
        'bandit_cold':         npz['bandit_cold'],
    }

    print('=' * 96)
    print(f'{"FINAL COMPARISON":^96s}')
    print('=' * 96)
    print(f'10k sessions, page-level attribution, delay=500, sigma=0.2 (bandits only)')
    print()

    # Milestone cum-regret table
    milestones = [100, 500, 1000, 2500, 5000, 7500, 10000]
    headers = list(methods.keys())
    print(f'CUM REGRET (lower = better)')
    print(f'  {"session":>8s} ' + ' '.join(f'{h:>20s}' for h in headers))
    for m in milestones:
        row = [f'{cum_regret(methods[h], oracle)[m - 1]:20.1f}' for h in headers]
        print(f'  {m:>8d} ' + ' '.join(row))

    # Final summary
    print()
    print(f'FINAL @ 10k SESSIONS (cum regret, % of oracle reward kept)')
    total_oracle = oracle.sum()
    for h, r in methods.items():
        cr = (oracle - r).sum()
        pct_kept = r.sum() / total_oracle * 100
        print(f'  {h:25s}  cum_regret={cr:8.1f}   reward_kept={pct_kept:5.1f}%')

    # Ratios
    print()
    print(f'EDP-evolved-agent advantage over each baseline @ 10k')
    base_cr = (oracle - methods['edp_evolved_agent']).sum()
    for h, r in methods.items():
        if h == 'edp_evolved_agent':
            continue
        other_cr = (oracle - r).sum()
        ratio = other_cr / base_cr if base_cr > 0 else float('inf')
        print(f'  vs {h:25s}  ratio = {ratio:.2f}x  ({other_cr - base_cr:+.1f} regret)')

    # OPRO ablation: same agent architecture but no diagnostic report
    print()
    print(f'OPRO ABLATION: removing the diagnostic report')
    cr_agent = (oracle - methods['edp_evolved_agent']).sum()
    cr_opro = (oracle - methods['edp_evolved_opro']).sum()
    cr_static = (oracle - methods['edp_static']).sum()
    diff = cr_opro - cr_agent
    print(f'  report-based agent: {cr_agent:.1f} regret')
    print(f'  OPRO (score-only):  {cr_opro:.1f} regret  ({diff:+.1f} vs report-based)')
    print(f'  EDP-static:         {cr_static:.1f} regret')
    print(f'  -> Removing the diagnostic report loses '
          f'{(cr_opro - cr_agent) / (cr_static - cr_agent) * 100:.0f}% '
          f'of the agent\'s improvement over static.')

    # Save sampled curves
    pts = np.linspace(50, n, 50, dtype=int)
    arrays = {h: cum_regret(r, oracle) for h, r in methods.items()}
    out = {h: [round(float(arrays[h][m - 1]), 1) for m in pts] for h in headers}
    with open('curves_50pt.json', 'w') as f:
        json.dump({'milestones': [int(m) for m in pts], 'curves': out}, f, indent=2)
    print(f'\n50-point chart-ready curves -> curves_50pt.json')


if __name__ == '__main__':
    main()
