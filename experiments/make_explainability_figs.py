"""Concrete explainability figures for the paper.

Generates four PNGs that exercise the "you can read the policy" claim:

  fig9_pwl_shapes.png        — Layer-1 PWL curves grid (one panel per problem)
  fig10_decision_trace.png   — one full session: signals -> problems -> slot-1 score
                               decomposition for the top-3 candidate widgets
  fig11_agent_edit_diff.png  — before/after parameter values for the round-2500
                               agent edit batch, with the agent's own reasons
                               printed alongside (proves the audit trail is real)
  fig12_bayesian_drift.png   — Bayesian-EDP `base` parameters at session 0 (LLM
                               prior) vs session 10K (after delayed-reward SGD),
                               showing how online learning pulls the readable
                               representation off the prior

Outputs land in figures/. No external services; uses cached evolve_state JSONs
and re-runs Bayesian-EDP for ~30s on the parametric simulator.
"""
from __future__ import annotations
import os
import sys
import json
import copy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edp.policies.edp import (
    make_problem_shapes, make_modules, score_problems, score_module,
    apply_edits, load_edits_json,
)
from edp.policies.bayesian_edp import BayesianEDPPolicy
from edp.config import PROBLEMS, N_SLOTS
from edp.sim import make_session_stream, DelayedFeedback
from edp.ground_truth import set_source, true_page_reward


PROBLEM_LABEL = {
    'F32': 'F3.2 size anxiety',
    'F33': 'F3.3 quality deficit',
    'F41': 'F4.1 comparison',
    'F43': 'F4.3 outfit visualization',
    'F45': 'F4.5 price-quality',
    'F46': 'F4.6 return hesitation',
    'F51': 'F5.1 decision paralysis',
}


def fig9_pwl_shapes(out='figures/fig9_pwl_shapes.png'):
    """Grid of Layer-1 PWL curves, one panel per problem."""
    shapes = make_problem_shapes()
    fig, axes = plt.subplots(2, 4, figsize=(13, 6))
    axes = axes.flatten()
    xs = np.linspace(0, 1, 200)
    cmap = plt.get_cmap('tab10')
    for ax, prob in zip(axes, PROBLEMS):
        sigs = shapes[prob]
        for i, (sig_name, cfg) in enumerate(sigs.items()):
            ys = np.interp(xs, cfg['bps'], cfg['vals'])
            ax.plot(xs, ys, lw=2, color=cmap(i), label=f"{sig_name} (w={cfg['weight']:.2f})")
            ax.scatter(cfg['bps'], cfg['vals'], s=24, color=cmap(i), zorder=3,
                       edgecolors='white', linewidth=0.8)
        ax.set_title(PROBLEM_LABEL[prob], fontsize=10)
        ax.set_xlabel('signal value')
        ax.set_ylabel('shape output')
        ax.set_xlim(0, 1)
        ax.set_ylim(-0.02, 1.02)
        ax.grid(alpha=0.3)
        ax.legend(fontsize=7, loc='lower right', framealpha=0.9)
    axes[-1].axis('off')
    fig.suptitle('Layer-1: PWL shape functions (signal → problem score)\n'
                 'Markers = LLM-authored breakpoints; lines = the GAM at serving time',
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches='tight')
    plt.close(fig)
    print(f'  -> {out}')


def fig10_decision_trace(out='figures/fig10_decision_trace.png'):
    """Single session decision trace: 14 signals -> 7 problems -> slot-1 score
    decomposition for the top-3 widgets."""
    set_source('parametric')
    stream = make_session_stream(50, seed=42)
    # pick a size-anxious session for visual punch
    persona, category, feat = next(s for s in stream if s[0] == 'size_anxious_new')

    shapes = make_problem_shapes()
    modules = make_modules()
    problems = score_problems(feat, shapes)

    remaining = dict(problems)
    coverage = {p: 0.0 for p in PROBLEMS}
    slot = 0
    scored = []
    for name, mod in modules.items():
        s_base = mod['base']
        s_rem = sum(w * remaining.get(p, 0.0) for p, w in mod.get('on_rem', {}).items())
        s_cov = sum(w * coverage.get(p, 0.0) for p, w in mod.get('on_cov', {}).items())
        s_decay = -mod['slot_decay'] * slot
        scored.append((name, s_base, s_rem, s_cov, s_decay, s_base + s_rem + s_cov + s_decay))
    scored.sort(key=lambda r: -r[-1])
    top = scored[:5]

    fig = plt.figure(figsize=(13, 8.5))
    gs = GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 1.6],
                  hspace=0.55, wspace=0.25)

    # row 0: raw signals
    ax0 = fig.add_subplot(gs[0, :])
    sig_names = ['size_conf', 'price_sens', 'return_hist', 'style_stretch', 'new',
                 'mobile', 'size_chart', 'tab_switch', 'zoom', 'price_dwell',
                 'cart_osc', 'wishlist', 'return_view', 'revisit']
    sig_vals = [feat.get(s, 0.0) for s in sig_names]
    ax0.bar(sig_names, sig_vals, color='#4C72B0')
    ax0.set_ylim(0, 1.05)
    ax0.set_ylabel('signal value')
    ax0.set_title(f'Step 1: 14 raw behavioural signals  '
                  f'(persona={persona}, category={category})',
                  fontsize=11)
    ax0.tick_params(axis='x', rotation=45, labelsize=8)
    ax0.grid(axis='y', alpha=0.3)

    # row 1: problem scores
    ax1 = fig.add_subplot(gs[1, :])
    prob_names = PROBLEMS
    prob_vals = [problems[p] for p in prob_names]
    prob_labels = [PROBLEM_LABEL[p] for p in prob_names]
    colors = ['#C44E52' if p == 'F32' else '#4C72B0' for p in prob_names]
    ax1.bar(prob_labels, prob_vals, color=colors)
    ax1.set_ylim(0, 1.05)
    ax1.set_ylabel('problem score')
    ax1.set_title('Step 2: 7 latent problem scores (Layer-1 PWL output)',
                  fontsize=11)
    ax1.tick_params(axis='x', rotation=20, labelsize=8)
    ax1.grid(axis='y', alpha=0.3)
    ax1.axhline(0.5, color='grey', ls='--', lw=0.8, alpha=0.5)

    # row 2: top-5 widget score decomposition for slot 1
    ax2 = fig.add_subplot(gs[2, :])
    names = [r[0] for r in top]
    bases = np.array([r[1] for r in top])
    rems = np.array([r[2] for r in top])
    covs = np.array([r[3] for r in top])
    decays = np.array([r[4] for r in top])
    totals = np.array([r[5] for r in top])
    width = 0.7
    x = np.arange(len(names))
    ax2.bar(x, bases, width, label='base', color='#7F7F7F')
    ax2.bar(x, rems, width, bottom=bases, label='on_remaining (problem still needs filling)',
            color='#C44E52')
    bot = bases + rems
    ax2.bar(x, covs, width, bottom=bot, label='on_coverage (synergy / anti-synergy)',
            color='#55A868')
    bot += covs
    ax2.bar(x, decays, width, bottom=bot, label='slot_decay', color='#937860')
    ax2.scatter(x, totals, marker='D', s=70, color='black', zorder=5,
                label='total score', edgecolors='white', linewidth=1)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=15, fontsize=9)
    ax2.set_ylabel('score contribution')
    ax2.set_title(f'Step 3: slot-1 score decomposition for top-5 candidate widgets  '
                  f'(winner = {top[0][0]})',
                  fontsize=11)
    ax2.axhline(0, color='black', lw=0.5)
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend(loc='upper right', fontsize=8, framealpha=0.95)

    fig.suptitle('Open-box decision trace: every page choice factors into readable curves',
                 fontsize=12, y=0.995)
    fig.savefig(out, dpi=140, bbox_inches='tight')
    plt.close(fig)
    print(f'  -> {out}')


def fig11_agent_edit_diff(out='figures/fig11_agent_edit_diff.png'):
    """Bar chart of agent's round-2500 edits with reasons printed alongside."""
    edits, note = load_edits_json('state/evolve_state/edits_round_2500.json')
    # take the first 10 scalar edits with both `from` and `to`
    rows = [e for e in edits if 'from' in e and 'to' in e][:10]

    fig, ax = plt.subplots(figsize=(13, max(5, 0.55 * len(rows) + 2)))
    y = np.arange(len(rows))
    froms = np.array([e['from'] for e in rows])
    tos = np.array([e['to'] for e in rows])
    labels = [f"{e['widget']}.{e['path']}" for e in rows]

    h = 0.38
    ax.barh(y - h / 2, froms, height=h, color='#7F7F7F', label='before (LLM prior)')
    ax.barh(y + h / 2, tos, height=h, color='#C44E52', label='after (agent edit)')
    for i, e in enumerate(rows):
        reason = e.get('reason', '')
        if len(reason) > 95:
            reason = reason[:92] + '…'
        ax.text(max(froms[i], tos[i]) + 0.05, i, reason,
                fontsize=7.5, va='center', color='#333')
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel('parameter value')
    ax.set_xlim(0, max(tos.max(), froms.max()) + 2.0)
    ax.grid(axis='x', alpha=0.3)
    ax.legend(loc='lower right', fontsize=9)
    ax.set_title('Agent edit batch at session 2500 — every change carries an LLM-authored '
                 'reason that survives in the audit log',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches='tight')
    plt.close(fig)
    print(f'  -> {out}')
    print(f'    (note: {note[:120]}…)')


def fig12_bayesian_drift(out='figures/fig12_bayesian_drift.png'):
    """Run Bayesian-EDP for 10K sessions, snapshot widget `base` parameters
    before and after, plot the drift away from the LLM prior."""
    set_source('parametric')
    stream = make_session_stream(10_000, seed=42)

    pol = BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3)
    prior_bases = {w: m['base'] for w, m in pol.modules.items()}

    sched = {2500, 5000, 7500}
    sched_files = {
        2500: 'state/evolve_state/edits_round_2500.json',
        5000: 'state/evolve_state/edits_round_5000.json',
        7500: 'state/evolve_state/edits_round_7500.json',
    }

    fb = DelayedFeedback(delay=500, noise_sigma=0.20, seed=42)
    for i, (p, c, f) in enumerate(stream):
        if i in sched and os.path.exists(sched_files[i]):
            edits, _ = load_edits_json(sched_files[i])
            new_modules = apply_edits(pol.modules, [
                (e['widget'], e['path'], e.get('from', 0.0),
                 e['to'], e.get('reason', ''))
                for e in edits
            ])
            pol.reset_prior(new_modules)
        for r_obs, payload in fb.drain_ready(i):
            pol.update_from_delayed(payload, r_obs)
        page, payload = pol.select_page_with_payload(f)
        r = true_page_reward(p, c, page)
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.update_from_delayed(payload, r_obs)

    post_bases = {w: m['base'] for w, m in pol.modules.items()}

    widgets = sorted(prior_bases, key=lambda w: prior_bases[w])
    x = np.arange(len(widgets))
    pri = np.array([prior_bases[w] for w in widgets])
    pos = np.array([post_bases[w] for w in widgets])

    fig, ax = plt.subplots(figsize=(13, 5))
    width = 0.4
    ax.bar(x - width / 2, pri, width, color='#7F7F7F', label='LLM prior (session 0)')
    ax.bar(x + width / 2, pos, width, color='#4C72B0', label='Bayesian-EDP posterior (session 10K)')
    for i, w in enumerate(widgets):
        d = pos[i] - pri[i]
        if abs(d) > 0.05:
            ax.text(i, max(pri[i], pos[i]) + 0.02, f'{d:+.2f}',
                    ha='center', fontsize=7,
                    color=('#2E7D32' if d > 0 else '#B71C1C'))
    ax.set_xticks(x)
    ax.set_xticklabels(widgets, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel("widget `base` parameter")
    ax.grid(axis='y', alpha=0.3)
    ax.legend(loc='upper left', fontsize=9)
    ax.set_title('Bayesian-EDP: prior (LLM-authored) → posterior (after 10K sessions of '
                 'delayed-reward SGD)\nEvery change is a readable scalar — no opaque weights',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig(out, dpi=140, bbox_inches='tight')
    plt.close(fig)
    print(f'  -> {out}')


def main():
    os.makedirs('figures', exist_ok=True)
    print('Generating explainability figures...')
    fig9_pwl_shapes()
    fig10_decision_trace()
    fig11_agent_edit_diff()
    fig12_bayesian_drift()
    print('done.')


if __name__ == '__main__':
    main()
