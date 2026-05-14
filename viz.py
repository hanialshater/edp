"""
Paper-quality figures for the bandit-vs-EDP comparison.

Now handles two persona sources: parametric and LLM-generated.
"""
from __future__ import annotations
import glob
import json
import os
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from edp import make_session_stream, oracle_reward, TRUE_NEEDS

FIG_DIR = 'figures'
os.makedirs(FIG_DIR, exist_ok=True)

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
    'axes.grid': True,
    'grid.alpha': 0.22,
    'grid.linewidth': 0.5,
    'lines.linewidth': 1.8,
})

COLORS = {
    'edp_agent':    '#1b5e8c',
    'edp_canned':   '#2e8b57',
    'edp_opro':     '#e08214',
    'edp_static':   '#5a5a5a',
    'bandit_warm':  '#c0392b',
    'bandit_cold':  '#7d3c98',
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
    'edp_agent':   'EDP-agent',
    'edp_canned':  'EDP-canned',
    'edp_opro':    'EDP-OPRO (ablation)',
    'edp_static':  'EDP-static',
    'bandit_warm': 'LinTS-warm',
    'bandit_cold': 'LinTS-cold',
}


def cum_regret(r, o):
    return np.cumsum(o - r)


def load_multiseed(path):
    d = np.load(path)
    return {k: d[k] for k in d.files}


def load_orch_rewards(state_path: str, n: int) -> np.ndarray:
    if not os.path.exists(state_path):
        return np.zeros((0, n))
    with open(state_path) as f:
        s = json.load(f)
    arr = np.array(s['rewards'])
    if len(arr) < n:
        return np.zeros((0, n))
    return arr[:n][None, :]


def plot_method(ax, x, mean, sem, key, **kwargs):
    ax.plot(x, mean, color=COLORS[key], linestyle=LINESTYLE[key],
            label=LABELS[key], **kwargs)
    if sem is not None and np.any(sem > 0):
        ax.fill_between(x, mean - sem, mean + sem,
                         color=COLORS[key], alpha=0.18, linewidth=0)


def band(reps, oracle):
    cr = np.cumsum(oracle[None, :] - reps, axis=1)
    return cr.mean(axis=0), (cr.std(axis=0, ddof=1) / np.sqrt(cr.shape[0])
                              if cr.shape[0] > 1 else np.zeros(cr.shape[1]))


# ============================================================================
# fig1: cumulative regret over time (both persona sources side by side)
# ============================================================================
def fig1_cumregret_both(parametric_path='results_multiseed_parametric_cat.npz',
                        llm_path='results_multiseed_llm_cat.npz'):
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0), sharey=False)
    for ax, (path, title) in zip(axes, [(parametric_path, 'Parametric personas (8) + categories'),
                                          (llm_path, 'LLM-generated personas (14) + categories')]):
        if not os.path.exists(path):
            ax.text(0.5, 0.5, f'(missing: {path})', transform=ax.transAxes,
                    ha='center', va='center', fontsize=10, color='gray')
            ax.set_title(title)
            continue
        bd = load_multiseed(path)
        oracle = bd['oracle']
        n = len(oracle)
        x = np.arange(1, n + 1)
        m, s = band(bd['bandit_cold'], oracle)
        plot_method(ax, x, m, s, 'bandit_cold')
        m, s = band(bd['bandit_warm'], oracle)
        plot_method(ax, x, m, s, 'bandit_warm')
        plot_method(ax, x, cum_regret(bd['edp_static'], oracle), None, 'edp_static')
        plot_method(ax, x, cum_regret(bd['edp_canned'], oracle), None, 'edp_canned')
        # EDP-agent — pick the appropriate state dir
        if 'llm' in path.lower() or 'llm' in title.lower():
            agent_dir = 'evolve_state_llm'
        else:
            agent_dir = 'evolve_state'
        agent_reps = load_orch_rewards(f'{agent_dir}/state.json', n)
        if agent_reps.shape[0] > 0:
            m, s = band(agent_reps, oracle)
            plot_method(ax, x, m, s, 'edp_agent', linewidth=2.4)
        for chk in (2500, 5000, 7500):
            ax.axvline(chk, color='black', alpha=0.12, linewidth=0.5)
        ax.set_xlabel('Session #')
        ax.set_xlim(0, n)
        ax.set_ylim(bottom=0)
        ax.set_title(title)
    axes[0].set_ylabel('Cumulative regret  (vs oracle)')
    axes[0].legend(loc='upper left', fontsize=9)
    fig.suptitle('Cumulative regret on production stack  ·  '
                  'page-level reward, delay=500, σ=0.2  ·  bands = ±1 SE',
                  fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig1_cumregret.png')
    plt.close(fig)
    print('  fig1_cumregret.png')


# ============================================================================
# fig2: stressor (unchanged, from prior stressor_results.json)
# ============================================================================
def fig2_stressor():
    path = 'stressor_results.json'
    if not os.path.exists(path):
        return
    with open(path) as f:
        S = json.load(f)
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
    display = ['clean baseline', '+noise σ=0.2', '+delay=500', '+delay=1000',
               '+page-attribution', '+page +delay=500', '+page +noise=0.2',
               'full prod stack']
    is_page = ['page' in k for k in order_keys]
    colors = ['#5a5a5a' if i == 0 else ('#c0392b' if p else '#7fb3d5')
              for i, p in enumerate(is_page)]
    fig, ax = plt.subplots(figsize=(8.5, 4.0))
    y = np.arange(len(crs))
    ax.barh(y, crs, color=colors, edgecolor='white', linewidth=0.8)
    for i, cr in enumerate(crs):
        ax.text(cr + 30, i, f'{cr:.0f}', va='center', fontsize=9.5)
    ax.set_yticks(y)
    ax.set_yticklabels(display)
    ax.invert_yaxis()
    ax.set_xlabel('Cumulative regret @ 10K sessions  (LinTS-warm)')
    ax.set_title('Stressor decomposition — page-level attribution is the dominant axis')
    handles = [
        Patch(facecolor='#5a5a5a', label='clean baseline'),
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
# fig3: % regret kept by each method, both sources side by side
# ============================================================================
def fig3_relative_regret(parametric_path='results_multiseed_parametric_cat.npz',
                          llm_path='results_multiseed_llm_cat.npz'):
    def cr10k_pct(path, agent_dir):
        if not os.path.exists(path):
            return None
        bd = load_multiseed(path)
        oracle = bd['oracle']
        total_oracle = float(oracle.sum())
        out = {}
        for k in ['edp_static', 'edp_canned']:
            out[k] = (float((oracle - bd[k]).sum()) / total_oracle * 100, 0.0)
        for k in ['bandit_warm', 'bandit_cold']:
            cr = (oracle[None, :] - bd[k]).sum(axis=1) / total_oracle * 100
            out[k] = (float(cr.mean()),
                      float(cr.std(ddof=1) / np.sqrt(len(cr))))
        agent = load_orch_rewards(f'{agent_dir}/state.json', len(oracle))
        if agent.shape[0] > 0:
            cr = (oracle[None, :] - agent).sum(axis=1) / total_oracle * 100
            out['edp_agent'] = (float(cr.mean()),
                                 float(cr.std(ddof=1) / np.sqrt(len(cr))) if len(cr) > 1 else 0.0)
        return out

    p = cr10k_pct(parametric_path, 'evolve_state')
    l = cr10k_pct(llm_path, 'evolve_state_llm')

    methods = ['edp_agent', 'edp_canned', 'edp_static', 'bandit_warm', 'bandit_cold']
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    x = np.arange(len(methods))
    width = 0.38
    for i, (label, source) in enumerate([('Parametric (8 personas)', p),
                                          ('LLM (14 personas)', l)]):
        if source is None:
            continue
        means = [source.get(m, (np.nan, 0.0))[0] for m in methods]
        sems = [source.get(m, (np.nan, 0.0))[1] for m in methods]
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, means, width,
                       color=['#aab8d0', '#d7a576'][i],
                       label=label, edgecolor='white',
                       yerr=sems, capsize=3, error_kw={'linewidth': 0.7})
        for b, mv in zip(bars, means):
            if not np.isnan(mv):
                ax.text(b.get_x() + b.get_width() / 2, mv + 0.3, f'{mv:.1f}%',
                        ha='center', fontsize=8.5)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[m] for m in methods], rotation=15, ha='right')
    ax.set_ylabel('% of oracle reward lost (cumulative regret / total oracle)')
    ax.set_title('Method robustness across simulator setups  ·  '
                  '10K sessions, prod stack  ·  error = ±1 SE')
    ax.legend(loc='upper left')
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig3_robustness.png')
    plt.close(fig)
    print('  fig3_robustness.png')


# ============================================================================
# fig4: per-persona regret heatmap (LLM personas + categories)
# ============================================================================
def fig4_persona_heatmap_llm(path='results_multiseed_llm_cat.npz'):
    if not os.path.exists(path):
        return
    bd = load_multiseed(path)
    oracle = bd['oracle']
    n = len(oracle)
    # Need persona stream — regenerate it with the llm source
    from edp.ground_truth import set_source
    set_source('llm')
    stream = make_session_stream(n, seed=42)
    persona_arr = np.array([p for p, _, _ in stream])

    agent = load_orch_rewards('evolve_state_llm/state.json', n)

    def mean_method(arr):
        return arr.mean(axis=0) if arr.ndim == 2 and arr.shape[0] else arr

    methods = {
        'bandit_cold':  mean_method(bd['bandit_cold']),
        'bandit_warm':  mean_method(bd['bandit_warm']),
        'edp_static':   bd['edp_static'],
        'edp_canned':   bd['edp_canned'],
        'edp_agent':    mean_method(agent) if agent.shape[0] else None,
    }
    order = [m for m in ['bandit_cold', 'bandit_warm', 'edp_static',
                          'edp_canned', 'edp_agent'] if methods[m] is not None]

    personas = list(TRUE_NEEDS.keys())
    matrix = np.zeros((len(personas), len(order)))
    for j, m in enumerate(order):
        r = methods[m]
        for i, persona in enumerate(personas):
            mask = (persona_arr == persona)
            if not mask.any():
                continue
            matrix[i, j] = (oracle[mask] - r[mask]).mean() / max(oracle[mask].mean(), 1e-9) * 100

    fig, ax = plt.subplots(figsize=(9.5, 6.5))
    vmax = max(20.0, np.percentile(matrix, 98))
    im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', vmin=0, vmax=vmax)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([LABELS[m] for m in order], rotation=18, ha='right')
    ax.set_yticks(range(len(personas)))
    ax.set_yticklabels([p.replace('_', ' ') for p in personas])
    for i in range(len(personas)):
        for j in range(len(order)):
            v = matrix[i, j]
            color = 'white' if v > vmax * 0.55 else 'black'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                    fontsize=8.5, color=color)
    ax.set_title('Per-persona regret  (% of that persona\'s oracle reward)  ·  LLM personas')
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02)
    cbar.set_label('% regret')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig4_persona_heatmap_llm.png')
    plt.close(fig)
    print('  fig4_persona_heatmap_llm.png')


# ============================================================================
# fig5: per-category regret heatmap (LLM personas + 6 categories)
# ============================================================================
def fig5_category_heatmap(path='results_multiseed_llm_cat.npz'):
    if not os.path.exists(path):
        return
    bd = load_multiseed(path)
    oracle = bd['oracle']
    n = len(oracle)
    from edp.ground_truth import set_source
    from edp.catalog import CATEGORIES
    set_source('llm')
    stream = make_session_stream(n, seed=42)
    cat_arr = np.array([c for _, c, _ in stream])

    agent = load_orch_rewards('evolve_state_llm/state.json', n)

    def mean_method(arr):
        return arr.mean(axis=0) if arr.ndim == 2 and arr.shape[0] else arr

    methods = {
        'bandit_cold':  mean_method(bd['bandit_cold']),
        'bandit_warm':  mean_method(bd['bandit_warm']),
        'edp_static':   bd['edp_static'],
        'edp_canned':   bd['edp_canned'],
        'edp_agent':    mean_method(agent) if agent.shape[0] else None,
    }
    order = [m for m in ['bandit_cold', 'bandit_warm', 'edp_static',
                          'edp_canned', 'edp_agent'] if methods[m] is not None]

    matrix = np.zeros((len(CATEGORIES), len(order)))
    for j, m in enumerate(order):
        r = methods[m]
        for i, c in enumerate(CATEGORIES):
            mask = (cat_arr == c)
            if not mask.any():
                continue
            matrix[i, j] = (oracle[mask] - r[mask]).mean() / max(oracle[mask].mean(), 1e-9) * 100

    fig, ax = plt.subplots(figsize=(8.0, 3.5))
    vmax = max(20.0, np.percentile(matrix, 98))
    im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd', vmin=0, vmax=vmax)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels([LABELS[m] for m in order], rotation=18, ha='right')
    ax.set_yticks(range(len(CATEGORIES)))
    ax.set_yticklabels(CATEGORIES)
    for i in range(len(CATEGORIES)):
        for j in range(len(order)):
            v = matrix[i, j]
            color = 'white' if v > vmax * 0.55 else 'black'
            ax.text(j, i, f'{v:.1f}', ha='center', va='center',
                    fontsize=8.5, color=color)
    ax.set_title('Per-category regret  (% of category\'s oracle reward)  ·  LLM personas')
    cbar = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
    cbar.set_label('% regret')
    fig.tight_layout()
    fig.savefig(f'{FIG_DIR}/fig5_category_heatmap.png')
    plt.close(fig)
    print('  fig5_category_heatmap.png')


def main():
    print(f'Generating figures into {FIG_DIR}/')
    fig1_cumregret_both()
    fig2_stressor()
    fig3_relative_regret()
    fig4_persona_heatmap_llm()
    fig5_category_heatmap()
    print('done.')


if __name__ == '__main__':
    main()
