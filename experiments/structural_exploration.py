"""
Structural exploration test: at session 5000 a new widget is added to the
catalog. Existing methods cannot use it (Static, LinTS instances trained
without it, EDP-static/canned with no edits referencing it). The
report-based agent can include it in its next edit batch.

The new widget is `virtual_try_on` with provisions {N1_fit:0.65, N2_visual:0.45}
— a strong fit-and-visual contributor, useful for size_anxious_new,
returner_anxious, post_return_returner, and shoes / outerwear categories.

Workflow:
  1. Build a stream that uses the EXTENDED catalog throughout (so the
     oracle includes the new widget at all sessions). This gives us the
     correct upper bound at every t.
  2. Run policies on that stream. Methods that don't reference the new
     widget never select it; their reward stays the same as if the widget
     didn't exist.
  3. After session 5000, give the report-based agent a checkpoint with the
     new widget visible in the report. The agent's edit batch can include
     `virtual_try_on.base / on_rem / on_cov` paths.
  4. Resume to session 10000. Compare cum regret.

Persona source: LLM (paper §2.2c).
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import shutil
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NEW_WIDGET = 'virtual_try_on'
NEW_PROVISIONS = {'N1_fit': 0.65, 'N2_visual': 0.45, 'N6_trust': 0.20}
ADD_AT = 5000


def patch_catalog():
    """Monkey-patch the catalog to include the new widget. Idempotent."""
    from edp import catalog as cat
    if NEW_WIDGET in cat.TRUE_PROVISIONS:
        return
    cat.TRUE_PROVISIONS[NEW_WIDGET] = NEW_PROVISIONS
    cat.WIDGETS.append(NEW_WIDGET)
    cat.WIDGET_IDX[NEW_WIDGET] = len(cat.WIDGETS) - 1
    cat.N_WIDGETS = len(cat.WIDGETS)
    # bust the ground_truth oracle cache
    from edp import ground_truth as gt
    gt._ORACLE_CACHE = None
    gt._EFFECTIVE_CACHE = None
    gt._TRUE_NEEDS_CACHE = None
    # bump the static EDP modules to *include* the new widget with a
    # default-tier base so it's a candidate. The agent's edit batch will
    # tune these.
    return


def add_module_default(modules):
    """Add the new widget to an EDPPolicy modules dict if missing."""
    if NEW_WIDGET in modules:
        return
    # Map provisions onto the closest F-codes for EDP's internal view.
    # virtual_try_on serves F32 (size anxiety) primarily, with F46 / F33
    # secondary. addr drives consumption; choose modest values.
    modules[NEW_WIDGET] = dict(
        addr={'F32': 0.45, 'F46': 0.20, 'F33': 0.15},
        base=0.05,
        on_rem={'F32': 1.6, 'F46': 0.5, 'F33': 0.4},
        on_cov={'F32': -0.6},
        slot_decay=0.06,
        type='premium-fit',
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=str, default='results_structural_exploration.json')
    args = ap.parse_args()

    patch_catalog()
    from edp.ground_truth import set_source
    set_source('llm')
    from edp import (make_session_stream, oracle_reward, true_page_reward,
                     EDPPolicy, BanditPolicy, DelayedFeedback)
    from edp.policies.bandit import context_warm
    from edp.policies.edp import (make_modules, make_problem_shapes,
                                   load_edits_json, apply_edits)

    stream = make_session_stream(10_000, seed=42)
    oracle = np.array([oracle_reward(p, c) for p, c, _ in stream])

    shapes = make_problem_shapes()

    # Method 1: EDP-static  (modules don't include the new widget at all)
    print('Running EDP-static (without virtual_try_on)...')
    pol = EDPPolicy()
    r_static = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        r_static[i] = true_page_reward(p, c, pol.select_page(f))

    # Method 2: EDP-canned  (canned edits, doesn't reference new widget)
    print('Running EDP-canned...')
    pol = EDPPolicy()
    sched = [
        (2500, load_edits_json('edits/round1.json')[0]),
        (5000, load_edits_json('edits/round2.json')[0]),
        (7500, load_edits_json('edits/round3.json')[0]),
    ]
    sched_idx = 0
    r_canned = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        while sched_idx < len(sched) and i == sched[sched_idx][0]:
            pol.apply_edit_batch(sched[sched_idx][1])
            sched_idx += 1
        r_canned[i] = true_page_reward(p, c, pol.select_page(f))

    # Method 3: EDP-agent  (existing live-agent edits at 2500/5000/7500;
    # doesn't know about the new widget either)
    print('Running EDP-agent (LLM-source live-agent edits)...')
    pol = EDPPolicy()
    sched = [
        (2500, load_edits_json('evolve_state_llm/edits_round_2500.json')[0]),
        (5000, load_edits_json('evolve_state_llm/edits_round_5000.json')[0]),
        (7500, load_edits_json('evolve_state_llm/edits_round_7500.json')[0]),
    ]
    sched_idx = 0
    r_agent = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        while sched_idx < len(sched) and i == sched[sched_idx][0]:
            pol.apply_edit_batch(sched[sched_idx][1])
            sched_idx += 1
        r_agent[i] = true_page_reward(p, c, pol.select_page(f))

    # Method 4: EDP-agent + structural-exploration round at session 5000
    # The agent at session 5000 is shown the new widget in its modules
    # config (added with default values) and is asked to propose edits.
    # We need to:
    #   - run sessions 0->2500 with EDP-static
    #   - apply round1 edits, run 2500->5000
    #   - ADD virtual_try_on to modules with default values, dump report,
    #     spawn subagent (already done), apply that round, run 5000->7500
    #   - spawn another subagent for 7500->10000
    #
    # For this script, we just leave the path here but rely on the agent's
    # per-checkpoint edit JSONs in struct_state_llm/. The script runs the
    # already-cached agent edits.
    struct_dir = 'struct_state_llm'
    if all(os.path.exists(f'{struct_dir}/edits_round_{x}.json')
           for x in (2500, 5000, 7500)):
        print(f'Running EDP-agent + structural exploration (cached from {struct_dir}/)...')
        pol = EDPPolicy()
        sched_idx = 0
        sched = [
            (2500, load_edits_json(f'{struct_dir}/edits_round_2500.json')[0]),
            (5000, load_edits_json(f'{struct_dir}/edits_round_5000.json')[0]),
            (7500, load_edits_json(f'{struct_dir}/edits_round_7500.json')[0]),
        ]
        r_struct = np.zeros(len(stream))
        for i, (p, c, f) in enumerate(stream):
            if i == ADD_AT:
                add_module_default(pol.modules)
            while sched_idx < len(sched) and i == sched[sched_idx][0]:
                pol.apply_edit_batch(sched[sched_idx][1])
                sched_idx += 1
            r_struct[i] = true_page_reward(p, c, pol.select_page(f))
    else:
        print(f'No struct_state_llm/ edits found; skipping the +structural-exploration arm')
        r_struct = None

    # Method 5: LinTS-warm — bandit was trained with original 22-arm
    # space; since the new widget's index doesn't exist in its arms, we
    # can't easily extend it without retraining. We simply note this:
    # the bandit IS the per-slot LinTS from the multiseed runs; its
    # post-drift behaviour just doesn't see the new widget.
    print('Running LinTS-warm (1 seed for indicative number)...')
    from edp.catalog import N_WIDGETS, WIDGETS
    # NOTE: BanditPolicy was instantiated AFTER patch_catalog so it sees
    # the extended catalog. But the new arm has no posterior data yet, so
    # in practice it gets picked rarely (high uncertainty under TS).
    pol = BanditPolicy(ctx_dim=7, alpha=0.3, seed=7)
    fb = DelayedFeedback(delay=500, noise_sigma=0.2, seed=701)
    r_warm = np.zeros(len(stream))
    for i, (p, c, f) in enumerate(stream):
        for r_obs, payload in fb.drain_ready(i):
            pol.record_feedback(payload, r_obs)
        x = context_warm(f, shapes, c, with_category=False)
        page, payload = pol.select_page_with_payload(x)
        r = true_page_reward(p, c, page)
        r_warm[i] = r
        fb.submit(i, r, payload)
    for r_obs, payload in fb.drain_all():
        pol.record_feedback(payload, r_obs)

    pre = slice(0, ADD_AT)
    post = slice(ADD_AT, None)

    def pct(r, sl):
        return float((oracle[sl] - r[sl]).sum() / oracle[sl].sum() * 100)

    rows = [
        ('EDP-static',         r_static),
        ('EDP-canned',         r_canned),
        ('EDP-agent',          r_agent),
        ('LinTS-warm',         r_warm),
    ]
    if r_struct is not None:
        rows.append(('EDP-agent + struct-explore', r_struct))

    summary = {}
    print('\n' + '=' * 92)
    print('STRUCTURAL EXPLORATION  ·  virtual_try_on added at session 5000  ·  LLM personas')
    print('=' * 92)
    print(f'  {"method":32s} {"pre-add":>10s}  {"post-add":>10s}  {"full":>10s}')
    for name, r in rows:
        a, b, c = pct(r, pre), pct(r, post), pct(r, slice(None))
        summary[name] = {'pre_pct': a, 'post_pct': b, 'full_pct': c}
        print(f'  {name:32s} {a:9.2f}%  {b:9.2f}%  {c:9.2f}%')

    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f'\nsaved -> {args.out}')


if __name__ == '__main__':
    main()
