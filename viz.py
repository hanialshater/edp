"""
Figures for the paper.

Produces (saved as PNGs in figures/):
  - fig1_cumregret.png       — cum regret over time, all 6 methods
  - fig2_stressor.png        — bandit cum regret per stressor condition
  - fig3_power_sweep.png     — cum regret at milestone N
  - fig4_persona_heatmap.png — per-persona regret % by method
  - fig5_opro_ablation.png   — report-agent vs OPRO trajectory
  - fig6_evolution.png       — per-round batch regret + edit counts
  - fig7_widget_activation.png — widget activation heatmap across rounds

All figures are loaded from saved data files; no simulation reruns needed.
"""
from __future__ import annotations
import json
import os
import re
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sim import make_session_stream, ORACLE_REWARDS, TRUE_NEEDS, WIDGETS

FIG_DIR = 'figures'
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({
    'figure.dpi': 110,
    'savefig.dpi': 150,
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

METHOD_STYLE = {
    'edp_evolved_agent':   dict(color='#1f77b4', linestyle='-',  linewidth=2.0, label='EDP-agent (live, report-based)'),
    'edp_evolved_canned':  dict(color='#2ca02c', linestyle='--', linewidth=1.5, label='EDP-canned'),
    'edp_evolved_opro':    dict(color='#ff7f0e', linestyle='-',  linewidth=1.7, label='EDP-OPRO (ablation)'),
    'edp_static':          dict(color='#7f7f7f', linestyle=':',  linewidth=1.5, label='EDP-static'),
    'bandit_warm':         dict(color='#d62728', linestyle='-',  linewidth=2.0, label='LinTS-warm (production)'),
    'bandit_cold':         dict(color='#8c564b', linestyle='--', linewidth=1.5, label='LinTS-cold'),
}


def load_all():
    """Returns (oracle, methods_dict) keyed by method name -> per-session reward."""
    npz = np.load('results_prod_stack.npz', allow_pickle=True)
    oracle = npz['oracle']
    methods = {
        'edp_static':         npz['edp_static'],
        'edp_evolved_canned': npz['edp_evolved'],
        'bandit_warm':        npz['bandit_warm'],
        'bandit_cold':        npz['bandit_cold'],
    }
    with open('evolve_state/state.json') as f:
        methods['edp_evolved_agent'] = np.array(json.load(f)['rewards'])
    with open('opro_state/state.json') as f:
        methods['edp_evolved_opro'] = np.array(json.load(f)['rewards'])
    return oracle, methods


def cum_regret(r, o):
    return np.cumsum(o - r)


# ---------- Fig 1: cumulative regret over time ----------
def fig_cumregret():
    oracle, methods = load_all()
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    order = ['bandit_cold', 'bandit_warm', 'edp_static', 'edp_evolved_opro',
             'edp_evolved_canned', 'edp_evolved_agent']
    for m in order:
        ax.plot(np.arange(1, len(oracle) + 1), cum_regret(methods[m], oracle),
                **METHOD_STYLE[m])
    # Vertical lines at agent checkpoints
    for chk in (2500, 5000, 7500):
        ax.axvline(chk, color='gray', alpha=0.3, linestyle=':', linewidth=0.8)
    ax.set_xlabel('Session #')
    ax.set_ylabel('Cumulative regret (vs oracle)')
    ax.set_title('Cumulative regret over 10K sessions  (page-level reward, delay=500, σ=0.2)')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(alpha=0.25)
    ax.set_xlim(0, len(oracle))
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig1_cumregret.png')
    plt.close(fig)
    print('  fig1_cumregret.png')


# ---------- Fig 2: stressor decomposition ----------
def fig_stressor():
    if not os.path.exists('stressor_results.json'):
        print('  fig2_stressor.png  SKIP (run stressor_decomp.py first)')
        return
    with open('stressor_results.json') as f:
        S = json.load(f)
    labels = list(S.keys())
    crs = [S[l]['cum_regret_10k'] for l in labels]
    short = [
        l.replace(' (delay=0, sigma=0)', '').replace(' (per-slot, ', ' (')
         .replace(' (sigma=0)', '').replace('sigma=', 'σ=')
        for l in labels
    ]
    fig, ax = plt.subplots(figsize=(9.0, 4.5))
    # Color: red gradient with intensity ~ regret
    norm_crs = (np.array(crs) - min(crs)) / (max(crs) - min(crs) + 1e-9)
    colors = plt.cm.Reds(0.35 + 0.55 * norm_crs)
    bars = ax.barh(range(len(short)), crs, color=colors, edgecolor='white')
    for i, (b, cr) in enumerate(zip(bars, crs)):
        ax.text(cr + 25, i, f'{cr:.0f}', va='center', fontsize=9)
    ax.set_yticks(range(len(short)))
    ax.set_yticklabels(short, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('Cumulative regret @ 10K sessions')
    ax.set_title('Stressor decomposition — LinTS-warm under each reward condition')
    ax.grid(axis='x', alpha=0.25)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig2_stressor.png')
    plt.close(fig)
    print('  fig2_stressor.png')


# ---------- Fig 3: low-N statistical power ----------
def fig_power_sweep():
    oracle, methods = load_all()
    milestones = [500, 1000, 2500, 5000, 7500, 10000]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    order = ['edp_evolved_agent', 'edp_evolved_canned', 'edp_evolved_opro',
             'edp_static', 'bandit_warm', 'bandit_cold']
    width = 0.13
    x = np.arange(len(milestones))
    for i, m in enumerate(order):
        crs = [cum_regret(methods[m], oracle)[ms - 1] for ms in milestones]
        offset = (i - len(order) / 2 + 0.5) * width
        ax.bar(x + offset, crs, width, color=METHOD_STYLE[m]['color'],
               label=METHOD_STYLE[m]['label'])
    ax.set_xticks(x)
    ax.set_xticklabels([f'{m}' for m in milestones])
    ax.set_xlabel('Session count')
    ax.set_ylabel('Cumulative regret')
    ax.set_title('Cumulative regret at each statistical-power milestone')
    ax.legend(loc='upper left', fontsize=8.5, ncol=2)
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig3_power_sweep.png')
    plt.close(fig)
    print('  fig3_power_sweep.png')


# ---------- Fig 4: per-persona regret heatmap ----------
def fig_persona_heatmap():
    oracle, methods = load_all()
    stream = make_session_stream(len(oracle), seed=42)
    personas = sorted(TRUE_NEEDS.keys(), key=lambda p: -ORACLE_REWARDS[p])
    order = ['bandit_cold', 'bandit_warm', 'edp_static', 'edp_evolved_opro',
             'edp_evolved_canned', 'edp_evolved_agent']

    matrix = np.zeros((len(personas), len(order)))
    persona_arr = np.array([p for p, _ in stream])
    for j, m in enumerate(order):
        r = methods[m]
        for i, persona in enumerate(personas):
            mask = (persona_arr == persona)
            if not mask.any():
                continue
            regret_pct = (oracle[mask] - r[mask]).mean() / oracle[mask].mean() * 100
            matrix[i, j] = regret_pct

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', vmin=0,
                    vmax=max(20, matrix.max()))
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([METHOD_STYLE[m]['label'] for m in order],
                        rotation=20, ha='right', fontsize=9)
    ax.set_yticks(range(len(personas)))
    ax.set_yticklabels(personas, fontsize=9)
    for i in range(len(personas)):
        for j in range(len(order)):
            color = 'white' if matrix[i, j] > 12 else 'black'
            ax.text(j, i, f'{matrix[i, j]:.1f}', ha='center', va='center',
                    fontsize=8.5, color=color)
    ax.set_title('Per-persona regret (% of oracle reward) by method')
    cbar = fig.colorbar(im, ax=ax, fraction=0.04)
    cbar.set_label('% regret')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig4_persona_heatmap.png')
    plt.close(fig)
    print('  fig4_persona_heatmap.png')


# ---------- Fig 5: OPRO ablation focus ----------
def fig_opro_ablation():
    oracle, methods = load_all()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for m in ['edp_evolved_agent', 'edp_evolved_opro', 'edp_static']:
        ax.plot(np.arange(1, len(oracle) + 1),
                cum_regret(methods[m], oracle),
                **METHOD_STYLE[m])
    for chk in (2500, 5000, 7500):
        ax.axvline(chk, color='gray', alpha=0.4, linestyle=':')
        ax.text(chk, ax.get_ylim()[1] * 0.05 if False else 30,
                f'round at {chk}', rotation=90, fontsize=8,
                color='gray', va='bottom')
    ax.set_xlabel('Session #')
    ax.set_ylabel('Cumulative regret')
    ax.set_title('OPRO ablation: agent with diagnostic report vs (edits, score) history only')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig5_opro_ablation.png')
    plt.close(fig)
    print('  fig5_opro_ablation.png')


# ---------- Fig 6: evolution trajectory (batch regret per round) ----------
def fig_evolution():
    with open('evolve_state/state.json') as f:
        a = json.load(f)
    with open('opro_state/state.json') as f:
        b = json.load(f)

    checkpoints = [0, 2500, 5000, 7500, 10000]
    def batches(state):
        rs = state['rewards']
        os_ = state['oracle']
        out = []
        for i in range(len(checkpoints) - 1):
            lo, hi = checkpoints[i], checkpoints[i + 1]
            if hi > len(rs):
                break
            br = sum(os_[lo:hi]) - sum(rs[lo:hi])
            out.append(br)
        return out

    a_batches = batches(a)
    b_batches = batches(b)
    rounds = ['R0\n(baseline)', 'R1', 'R2', 'R3']
    x = np.arange(len(rounds))
    width = 0.35

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.bar(x - width / 2, a_batches, width, color=METHOD_STYLE['edp_evolved_agent']['color'],
            label='Report-based agent', edgecolor='white')
    ax.bar(x + width / 2, b_batches, width, color=METHOD_STYLE['edp_evolved_opro']['color'],
            label='OPRO ablation', edgecolor='white')
    for i, (av, bv) in enumerate(zip(a_batches, b_batches)):
        ax.text(i - width / 2, av + 5, f'{av:.0f}', ha='center', fontsize=9)
        ax.text(i + width / 2, bv + 5, f'{bv:.0f}', ha='center', fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(rounds)
    ax.set_ylabel('Batch regret (2500-session window)')
    ax.set_title('Per-batch regret across evolution rounds')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.25)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig6_evolution.png')
    plt.close(fig)
    print('  fig6_evolution.png')


# ---------- Fig 7: widget activation across rounds (report-agent only) ----------
def parse_widget_act_from_report(path: str) -> dict[str, float]:
    """Extract widget activation % from a report markdown file."""
    out = {w: 0.0 for w in WIDGETS}
    with open(path) as f:
        lines = f.readlines()
    in_widget_section = False
    for line in lines:
        if 'Widget activation rate' in line:
            in_widget_section = True
            continue
        if in_widget_section:
            # Either a widget data line or the next section header
            if line.strip().startswith('##') or line.strip().startswith('-'):
                break
            m = re.match(r'\s+(\S+)\s+([0-9.]+)\s+', line)
            if m:
                w, pct = m.group(1), float(m.group(2))
                if w in out:
                    out[w] = pct
    return out


def fig_widget_activation():
    rounds = [2500, 5000, 7500, 10000]
    data = []
    for ms in rounds:
        path = f'evolve_state/report_at_{ms}.md'
        if not os.path.exists(path):
            return
        data.append(parse_widget_act_from_report(path))
    # Sort widgets by activation at round 0 (descending)
    order = sorted(WIDGETS, key=lambda w: -data[0].get(w, 0.0))
    matrix = np.zeros((len(order), len(rounds)))
    for j, d in enumerate(data):
        for i, w in enumerate(order):
            matrix[i, j] = d.get(w, 0.0)

    fig, ax = plt.subplots(figsize=(7.5, 9.0))
    im = ax.imshow(matrix, aspect='auto', cmap='Blues', vmin=0, vmax=20)
    ax.set_xticks(range(len(rounds)))
    ax.set_xticklabels([f'After R{j}\n(@{rounds[j]})' for j in range(len(rounds))],
                        fontsize=9)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=8.5)
    for i in range(len(order)):
        for j in range(len(rounds)):
            v = matrix[i, j]
            color = 'white' if v > 12 else 'black'
            ax.text(j, i, f'{v:.1f}' if v > 0.05 else '·',
                    ha='center', va='center', fontsize=8, color=color)
    ax.set_title('Widget activation (% of all slots) across report-agent rounds')
    cbar = fig.colorbar(im, ax=ax, fraction=0.04)
    cbar.set_label('activation %')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig7_widget_activation.png')
    plt.close(fig)
    print('  fig7_widget_activation.png')


def main():
    print(f'Generating figures into {FIG_DIR}/')
    fig_cumregret()
    fig_stressor()
    fig_power_sweep()
    fig_persona_heatmap()
    fig_opro_ablation()
    fig_evolution()
    fig_widget_activation()
    print('done.')


if __name__ == '__main__':
    main()
