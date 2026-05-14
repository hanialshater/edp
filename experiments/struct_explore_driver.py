"""
Driver for the structural-exploration test.

Subcommands:
  init       — fresh struct_state_llm/, run 0->5000 using existing
               evolve_state_llm round-1 edits, then add `virtual_try_on`
               to the modules and write a new report-at-5000 + prompt.
  apply      — apply edits at given session, run to next checkpoint, write
               next report + prompt.

Usage:
  python3 experiments/struct_explore_driver.py init
  # spawn subagent → struct_state_llm/edits_round_5000.json
  python3 experiments/struct_explore_driver.py apply --apply struct_state_llm/edits_round_5000.json --until 7500
  # spawn subagent → struct_state_llm/edits_round_7500.json
  python3 experiments/struct_explore_driver.py apply --apply struct_state_llm/edits_round_7500.json --until 10000
"""
from __future__ import annotations
import argparse
import json
import os
import shutil
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NEW_WIDGET = 'virtual_try_on'
NEW_PROVISIONS = {'N1_fit': 0.65, 'N2_visual': 0.45, 'N6_trust': 0.20}
ADD_AT = 5000
STATE_DIR = 'struct_state_llm'


def patch_catalog():
    from edp import catalog as cat
    if NEW_WIDGET in cat.TRUE_PROVISIONS:
        return
    cat.TRUE_PROVISIONS[NEW_WIDGET] = NEW_PROVISIONS
    cat.WIDGETS.append(NEW_WIDGET)
    cat.WIDGET_IDX[NEW_WIDGET] = len(cat.WIDGETS) - 1
    cat.N_WIDGETS = len(cat.WIDGETS)
    from edp import ground_truth as gt
    gt._ORACLE_CACHE = None
    gt._EFFECTIVE_CACHE = None
    gt._TRUE_NEEDS_CACHE = None


def new_module_defaults():
    return dict(
        addr={'F32': 0.45, 'F46': 0.20, 'F33': 0.15},
        base=0.05,
        on_rem={'F32': 1.6, 'F46': 0.5, 'F33': 0.4},
        on_cov={'F32': -0.6},
        slot_decay=0.06,
        type='premium-fit',
    )


def cmd_init():
    """
    Initialise struct_state_llm/ by running 0->5000 fresh:
      - 0->2500 with EDP-static
      - apply evolve_state_llm round-1 edits, run 2500->5000
      - ADD virtual_try_on to modules + catalog
      - generate a report at 5000 that references the new widget
    """
    from edp.ground_truth import set_source
    set_source('llm')
    os.makedirs(STATE_DIR, exist_ok=True)
    state_path = os.path.join(STATE_DIR, 'state.json')
    if os.path.exists(state_path):
        os.remove(state_path)

    from edp.orchestrators.report import ReportOrchestrator
    orch = ReportOrchestrator(STATE_DIR)
    # Phase 1: 0 -> 2500
    state = orch.load_state()
    state = orch.run_batch(state, 2500)
    orch.save_state(state)
    print(f'[init] phase 1: 0 -> 2500 done')

    # Phase 2: apply existing round-1 edits, run 2500 -> 5000
    state = orch.apply_edits_from_file(state, 'evolve_state_llm/edits_round_2500.json')
    state = orch.run_batch(state, 5000)
    orch.save_state(state)
    print(f'[init] phase 2: 2500 -> 5000 done (with round-1 edits)')

    # Phase 3: STRUCTURAL CHANGE — add virtual_try_on
    patch_catalog()
    if NEW_WIDGET not in state['modules']:
        state['modules'][NEW_WIDGET] = new_module_defaults()
    orch.save_state(state)
    print(f'[init] phase 3: added {NEW_WIDGET} to modules + catalog')

    # Generate report at 5000 with the new widget in modules
    notice = (
        f'# STRUCTURAL CHANGE — `{NEW_WIDGET}` added to the catalog at '
        f'session {ADD_AT}\n\n'
        f'A new widget has been added to the catalog with provisions '
        f'{NEW_PROVISIONS}. The widget appears in the modules JSON below '
        f'with default values; it will show 0% activation in this batch '
        f'because no edits have targeted it yet. Please consider whether '
        f'this widget should fire for any (persona, category) cells '
        f'(its provisions strongly favour personas with high N1_fit / '
        f'N2_visual / N6_trust needs, e.g. size_anxious_new, '
        f'returner_anxious, post_return_returner, hesitant_first_buyer, '
        f'and the `shoes` / `outerwear` categories).\n\n'
        f'---\n\n'
    )
    report = orch.make_report(state, 2500, ADD_AT)
    rpt_path = os.path.join(STATE_DIR, f'report_at_{ADD_AT}.md')
    with open(rpt_path, 'w') as f:
        f.write(notice + report)
    next_edits = os.path.join(STATE_DIR, f'edits_round_{ADD_AT}.json')
    prompt = orch.render_prompt(state, 2500, ADD_AT, notice + report, next_edits)
    prompt_path = os.path.join(STATE_DIR, f'PROMPT_at_{ADD_AT}.md')
    with open(prompt_path, 'w') as f:
        f.write(prompt)

    print(f'[init] report   -> {rpt_path}')
    print(f'[init] prompt   -> {prompt_path}')
    print(f'[init] next edits expected at -> {next_edits}')


def cmd_apply(args):
    """Apply edits + run to next checkpoint. Wraps ReportOrchestrator."""
    from edp.ground_truth import set_source
    set_source('llm')
    patch_catalog()
    from edp.orchestrators.report import ReportOrchestrator
    orch = ReportOrchestrator(STATE_DIR)
    orch.run(until=args.until, apply_path=args.apply)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('init')
    a2 = sp.add_parser('apply')
    a2.add_argument('--apply', type=str, required=True)
    a2.add_argument('--until', type=int, required=True)
    args = ap.parse_args()
    if args.cmd == 'init':
        cmd_init()
    elif args.cmd == 'apply':
        cmd_apply(args)


if __name__ == '__main__':
    main()
