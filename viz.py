"""
Paper-quality figures for the bandit-vs-EDP comparison.

Loads multi-seed bandit data + 3-rep EDP-agent/OPRO trajectories and produces
conference-paper-quality plots with error bands and consistent styling.

Five core figures (production-conditions story):
  fig1_cumregret.png       — main figure: cum regret over 10k sessions, all
                              methods, with shaded standard-error bands
  fig2_stressor.png        — section 5.2: bandit regret per reward condition
  fig3_power_sweep.png     — section 5.3: cum regret at milestone N with bands
  fig4_persona_heatmap.png — section 5.4: per-persona regret % by method
  fig5_opro_ablation.png   — section 5.5: agent vs OPRO with bands

Drops the earlier weak figures (fig6 per-batch bars and fig7 widget heatmap).
"""
from __future__ import annotations
import glob
import json
import os
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from sim import make_session_stream, ORACLE_REWARDS, TRUE_NEEDS

FIG_DIR = 'figures'
os.makedirs(FIG_DIR, exist_ok=True)

# Conference-paper-quality matplotlib defaults
plt.rcParams.update({
    'figure.dpi': 130,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.08,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10.5,
    'axes.titlesize': 11.5,
    'axes.labelsize': 10.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.labelpad': 4,
    'xtick.labelsize': 9.5,
    'ytick.labelsize': 9.5,
    'legend.fontsize': 9.5,
    'legend.frameon': False,
    'legend.borderpad': 0.3,
    'axes.grid': True,
    'grid.alpha': 0.22,
    'grid.linestyle': '-',
    'grid.linewidth': 0.5,
    'lines.linewidth': 1.8,
})

# Consistent palette — colorblind-friendly, also legible in greyscale
# (EDP family: blues/teals; bandit family: red/brown; static/OPRO: grey/orange)
COLORS = {
    'edp_agent':    '#1b5e8c',   # deep blue
    'edp_canned':   '#2e8b57',   # sea green
    'edp_opro':     '#e08214',   # orange
    'edp_static':   '#5a5a5a',   # grey
    'bandit_warm':  '#c0392b',   # red
    'bandit_cold':  '#7d3c98',   # purple (less common, distinguishable)
}
LINESTYLE = {
    'edp_agent':   '-',
    'edp_canned':  '--',
    'edp_opro':    '-',
    'edp_static':  ':',
    'bandit_warm': '-',
    'bandit_cold': '--',
}
LABELS = {
    'edp_agent':   'EDP-agent  (report-based, ours)',
    'edp_canned':  'EDP-canned  (offline-curated edits)',
    'edp_opro':    'EDP-OPRO  (ablation: no diagnostic)',
    'edp_static':  'EDP-static  (no online update)',
    'bandit_warm': 'LinTS-warm  (production stack)',
    'bandit_cold': 'LinTS-cold  (production stack)',
}


# ---------- Data loaders ----------
def load_bandits_multiseed(path='results_multiseed.npz'):
    """Returns dict with oracle, edp_static, edp_canned, bandit_warm (R,N), bandit_cold (R,N)."""
    d = np.load(path)
    return {k: d[k] for k in d.files}


def load_agent_reps(prefix: str, n: int) -> np.ndarray:
    """
    Stack reward trajectories from all replicate directories matching
    `{prefix}_rep*/state.json`. Returns (n_reps, n) array.
    """
    dirs = sorted(glob.glob(f'{prefix}_rep*'))
    out = []
    for d in dirs:
        path = os.path.join(d, 'state.json')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            s = json.load(f)
        arr = np.array(s['rewards'])
        if len(arr) >= n:
            out.append(arr[:n])
    if not out:
        return np.zeros((0, n))
    return np.stack(out)


def cum_regret(r, o):
    return np.cumsum(o - r)


def cum_regret_band(reps: np.ndarray, oracle: np.ndarray):
    """
    Given reps of shape (R, N), returns (mean_cumregret_per_session,
                                          stderr_cumregret_per_session).
    """
    cr_per_rep = np.cumsum(oracle[None, :] - reps, axis=1)  # (R, N)
    mean = cr_per_rep.mean(axis=0)
    sem = cr_per_rep.std(axis=0, ddof=1) / np.sqrt(cr_per_rep.shape[0]) if cr_per_rep.shape[0] > 1 else np.zeros_like(mean)
    return mean, sem


def plot_method(ax, x, mean, sem, key, **kwargs):
    ax.plot(x, mean, color=COLORS[key], linestyle=LINESTYLE[key],
            label=LABELS[key], **kwargs)
    if sem is not None and np.any(sem > 0):
        ax.fill_between(x, mean - sem, mean + sem,
                         color=COLORS[key], alpha=0.18, linewidth=0)


# ============================================================================
# Fig 1: cumulative regret over time, all methods, with error bands
# ============================================================================
def fig_cumregret():
    bd = load_bandits_multiseed()
    oracle = bd['oracle']
    n = len(oracle)
    x = np.arange(1, n + 1)

    agent = load_agent_reps('evolve_state', n)
    opro = load_agent_reps('opro_state', n)

    fig, ax = plt.subplots(figsize=(8.5, 5.0))

    # Bandits with bands (10 seeds)
    m, s = cum_regret_band(bd['bandit_cold'], oracle)
    plot_method(ax, x, m, s, 'bandit_cold')
    m, s = cum_regret_band(bd['bandit_warm'], oracle)
    plot_method(ax, x, m, s, 'bandit_warm')

    # Static / canned: deterministic, one trace
    plot_method(ax, x, cum_regret(bd['edp_static'], oracle), None, 'edp_static')
    plot_method(ax, x, cum_regret(bd['edp_canned'], oracle), None, 'edp_canned')

    # OPRO with bands (3 reps)
    if opro.shape[0] > 0:
        m, s = cum_regret_band(opro, oracle)
        plot_method(ax, x, m, s, 'edp_opro')

    # EDP-agent with bands (3 reps) -- LAST so it sits on top
    if agent.shape[0] > 0:
        m, s = cum_regret_band(agent, oracle)
        plot_method(ax, x, m, s, 'edp_agent', linewidth=2.4)

    # Checkpoint markers for the EDP agents
    for chk in (2500, 5000, 7500):
        ax.axvline(chk, color='black', alpha=0.12, linestyle='-', linewidth=0.5)

    ax.set_xlabel('Session #')
    ax.set_ylabel('Cumulative regret  (vs oracle)')
    ax.set_title('Cumulative regret over 10K sessions  ·  page-level reward, '
                 'delay=500, σ=0.2  ·  bands = ±1 SE')
    ax.legend(loc='upper left', ncol=1)
    ax.set_xlim(0, n)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig1_cumregret.png')
    plt.close(fig)
    print('  fig1_cumregret.png')


# ============================================================================
# Fig 2: stressor decomposition (single-axis ablation on LinTS-warm)
# ============================================================================
def fig_stressor():
    if not os.path.exists('stressor_results.json'):
        print('  fig2 SKIP (no stressor_results.json)')
        return
    with open('stressor_results.json') as f:
        S = json.load(f)
    # Reorder for narrative: clean, single-axis effects, then combined
    order_keys = [
        'clean (per-slot, delay=0, sigma=0)',
        '+noise sigma=0.2 (per-slot, delay=0)',
        '+delay=500 (per-slot, sigma=0)',
        '+delay=1000 (per-slot, sigma=0)',
        '+page-attribution (delay=0, sigma=0)',
        '+page +delay=500 (sigma=0)',
        '+page +noise=0.2 (delay=0)',
        'full prod stack (page +delay=500 +noise=0.2)',
    ]
    crs = [S[k]['cum_regret_10k'] for k in order_keys]
    display = [
        'clean baseline',
        '+noise σ=0.2',
        '+delay=500',
        '+delay=1000',
        '+page-attribution',
        '+page +delay=500',
        '+page +noise=0.2',
        'full prod stack',
    ]
    # Color: blue for benign stressors, red for page-attr stressors
    is_page = ['page' in k for k in order_keys]
    colors = ['#5a5a5a' if i == 0 else ('#c0392b' if p else '#7fb3d5')
              for i, p in enumerate(is_page)]

    fig, ax = plt.subplots(figsize=(8.5, 4.0))
    y = np.arange(len(crs))
    bars = ax.barh(y, crs, color=colors, edgecolor='white', linewidth=0.8)
    for i, (b, cr) in enumerate(zip(bars, crs)):
        ax.text(cr + 30, i, f'{cr:.0f}', va='center', fontsize=9.5)
    ax.set_yticks(y)
    ax.set_yticklabels(display)
    ax.invert_yaxis()
    ax.set_xlabel('Cumulative regret @ 10K sessions  (LinTS-warm)')
    ax.set_title('Stressor decomposition — page-level attribution is the dominant axis')
    # Custom legend
    from matplotlib.patches import Patch
    handles = [
        Patch(facecolor='#5a5a5a', label='clean (baseline)'),
        Patch(facecolor='#7fb3d5', label='delay / noise only'),
        Patch(facecolor='#c0392b', label='page-level attribution'),
    ]
    ax.legend(handles=handles, loc='lower right')
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig2_stressor.png')
    plt.close(fig)
    print('  fig2_stressor.png')


# ============================================================================
# Fig 3: statistical-power sweep — cum regret at milestone N with bands
# ============================================================================
def fig_power_sweep():
    bd = load_bandits_multiseed()
    oracle = bd['oracle']
    n = len(oracle)
    agent = load_agent_reps('evolve_state', n)
    opro = load_agent_reps('opro_state', n)

    milestones = [500, 1000, 2500, 5000, 7500, 10000]

    def cr_at(r1d, m):
        return float(cum_regret(r1d, oracle)[m - 1])

    def cr_at_band(reps, m):
        if reps.shape[0] == 0:
            return float('nan'), 0.0
        vals = np.array([cr_at(reps[i], m) for i in range(reps.shape[0])])
        return float(vals.mean()), float(vals.std(ddof=1) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0

    methods_order = ['edp_agent', 'edp_canned', 'edp_opro', 'edp_static',
                      'bandit_warm', 'bandit_cold']

    data = {k: ([], []) for k in methods_order}  # method -> (means, sems)
    for m in milestones:
        data['edp_static'][0].append(cr_at(bd['edp_static'], m))
        data['edp_static'][1].append(0.0)
        data['edp_canned'][0].append(cr_at(bd['edp_canned'], m))
        data['edp_canned'][1].append(0.0)
        for key, reps in [('bandit_warm', bd['bandit_warm']),
                           ('bandit_cold', bd['bandit_cold'])]:
            mu, se = cr_at_band(reps, m)
            data[key][0].append(mu)
            data[key][1].append(se)
        mu, se = cr_at_band(agent, m)
        data['edp_agent'][0].append(mu)
        data['edp_agent'][1].append(se)
        mu, se = cr_at_band(opro, m)
        data['edp_opro'][0].append(mu)
        data['edp_opro'][1].append(se)

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    x = np.arange(len(milestones))
    width = 0.13
    for i, k in enumerate(methods_order):
        means, sems = data[k]
        offset = (i - len(methods_order) / 2 + 0.5) * width
        bars = ax.bar(x + offset, means, width, color=COLORS[k],
                       yerr=sems, capsize=2.5, error_kw={'linewidth': 0.7},
                       edgecolor='white', linewidth=0.5, label=LABELS[k])

    ax.set_xticks(x)
    ax.set_xticklabels([f'{m:,}' for m in milestones])
    ax.set_xlabel('Sessions observed')
    ax.set_ylabel('Cumulative regret')
    ax.set_title('Statistical-power sweep — cum regret at each milestone N')
    ax.legend(loc='upper left', ncol=2)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig3_power_sweep.png')
    plt.close(fig)
    print('  fig3_power_sweep.png')


# ============================================================================
# Fig 4: per-persona regret heatmap
# ============================================================================
def fig_persona_heatmap():
    bd = load_bandits_multiseed()
    oracle = bd['oracle']
    n = len(oracle)
    stream = make_session_stream(n, seed=42)
    persona_arr = np.array([p for p, _ in stream])

    # Methods to display (deterministic or mean-of-reps)
    agent = load_agent_reps('evolve_state', n)
    opro = load_agent_reps('opro_state', n)

    def mean_reps(reps):
        return reps.mean(axis=0) if reps.shape[0] else np.zeros(n)

    methods = {
        'bandit_cold':  bd['bandit_cold'].mean(axis=0),
        'bandit_warm':  bd['bandit_warm'].mean(axis=0),
        'edp_static':   bd['edp_static'],
        'edp_opro':     mean_reps(opro),
        'edp_canned':   bd['edp_canned'],
        'edp_agent':    mean_reps(agent),
    }
    order = ['bandit_cold', 'bandit_warm', 'edp_static', 'edp_opro',
             'edp_canned', 'edp_agent']

    # Order personas by oracle reward magnitude (largest -> smallest)
    personas = sorted(TRUE_NEEDS.keys(), key=lambda p: -ORACLE_REWARDS[p])
    matrix = np.zeros((len(personas), len(order)))
    for j, m in enumerate(order):
        r = methods[m]
        for i, persona in enumerate(personas):
            mask = (persona_arr == persona)
            if not mask.any():
                continue
            matrix[i, j] = (oracle[mask] - r[mask]).mean() / oracle[mask].mean() * 100

    fig, ax = plt.subplots(figsize=(9.0, 4.6))
    vmax = max(20.0, np.percentile(matrix, 99))
    im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', vmin=0, vmax=vmax)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([LABELS[k].split('  ')[0] for k in order],
                        rotation=18, ha='right')
    ax.set_yticks(range(len(personas)))
    ax.set_yticklabels(personas)
    for i in range(len(personas)):
        for j in range(len(order)):
            v = matrix[i, j]
            color = 'white' if v > vmax * 0.55 else 'black'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                    fontsize=9, color=color)
    ax.set_title('Per-persona regret  (% of oracle reward)  ·  averaged across reps')
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label('% regret')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig4_persona_heatmap.png')
    plt.close(fig)
    print('  fig4_persona_heatmap.png')


# ============================================================================
# Fig 5: OPRO ablation — focused 3-method comparison with bands
# ============================================================================
def fig_opro_ablation():
    bd = load_bandits_multiseed()
    oracle = bd['oracle']
    n = len(oracle)
    x = np.arange(1, n + 1)

    agent = load_agent_reps('evolve_state', n)
    opro = load_agent_reps('opro_state', n)

    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    plot_method(ax, x, cum_regret(bd['edp_static'], oracle), None, 'edp_static')
    if opro.shape[0] > 0:
        m, s = cum_regret_band(opro, oracle)
        plot_method(ax, x, m, s, 'edp_opro')
    if agent.shape[0] > 0:
        m, s = cum_regret_band(agent, oracle)
        plot_method(ax, x, m, s, 'edp_agent', linewidth=2.4)

    for chk in (2500, 5000, 7500):
        ax.axvline(chk, color='black', alpha=0.18, linestyle='-', linewidth=0.6)
        ax.text(chk, 50, f'edit round  →', rotation=90, va='bottom',
                fontsize=8, color='gray', alpha=0.7)

    ax.set_xlabel('Session #')
    ax.set_ylabel('Cumulative regret')
    ax.set_title('OPRO ablation  ·  same agent, action space, model — '
                 'only the prompt content differs  ·  bands = ±1 SE')
    ax.legend(loc='upper left')
    ax.set_xlim(0, n)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig5_opro_ablation.png')
    plt.close(fig)
    print('  fig5_opro_ablation.png')


def main():
    print(f'Generating figures into {FIG_DIR}/  (paper-quality, multi-seed)')
    fig_cumregret()
    fig_stressor()
    fig_power_sweep()
    fig_persona_heatmap()
    fig_opro_ablation()
    print('done.')


if __name__ == '__main__':
    main()
