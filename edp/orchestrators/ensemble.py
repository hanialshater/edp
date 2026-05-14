"""
Multi-agent ensemble orchestrator: at each checkpoint we will spawn K=3
subagent draws (independent edit-batch JSONs); after they're written, we
evaluate each on a held-out validation slice and adopt the best mean
config.

This module provides:
  - EnsembleOrchestrator.prepare_round(K)
       writes K prompt files PROMPT_at_<until>_draw{1..K}.md and expects
       the parent (the parallel subagent caller) to populate K
       edits_round_<until>_draw{1..K}.json files
  - EnsembleOrchestrator.select_round(until)
       reads the K JSONs, evaluates each candidate config on the
       validation slice (seed 99991, N=500), picks the best by mean
       reward, applies it, runs the live batch, writes the next prompt
"""
from __future__ import annotations
import argparse
import copy
import json
import os
import sys
import numpy as np

from edp import (make_session_stream, true_page_reward, oracle_reward,
                 EDPPolicy)
from edp.policies.edp import apply_edits
from edp.orchestrators.report import ReportOrchestrator


VALIDATION_SEED = 99991
VALIDATION_N = 500


def evaluate_config(modules, val_stream):
    pol = EDPPolicy(modules=modules)
    rewards = np.zeros(len(val_stream))
    for i, (p, c, f) in enumerate(val_stream):
        rewards[i] = true_page_reward(p, c, pol.select_page(f))
    return float(rewards.mean()), float(rewards.std())


class EnsembleOrchestrator(ReportOrchestrator):

    def prepare_round(self, until: int, K: int = 3,
                      apply_path: str | None = None,
                      seed: int = 42):
        """Run the live batch, write K identical prompt copies."""
        if apply_path:
            state = self.load_state()
            state = self.apply_edits_from_file(state, apply_path)
            self.save_state(state)
        state = self.load_state()
        batch_start = state['session_idx']
        state = self.run_batch(state, until, seed=seed)
        report = self.make_report(state, batch_start, until)
        rpt_path = os.path.join(self.state_dir, f'report_at_{until}.md')
        with open(rpt_path, 'w') as f:
            f.write(report)
        self.save_state(state)
        # Write K prompt copies, each pointing at a different output path
        prompts = []
        for k in range(1, K + 1):
            out_path = os.path.join(self.state_dir,
                                     f'edits_round_{until}_draw{k}.json')
            prompt = self.render_prompt(state, batch_start, until, report, out_path)
            prompt_path = os.path.join(self.state_dir,
                                        f'PROMPT_at_{until}_draw{k}.md')
            with open(prompt_path, 'w') as f:
                f.write(prompt)
            prompts.append(prompt_path)
        rewards = np.array(state['rewards'])
        oracle = np.array(state['oracle'])
        cr = float((oracle - rewards).sum())
        print(f'[ensemble] sessions {batch_start} -> {until}; cum regret = {cr:.2f}')
        for p in prompts:
            print(f'  prompt: {p}')

    def select_round(self, until: int, K: int = 3):
        """
        Read the K candidate edit JSONs, evaluate each on validation slice,
        pick the best mean. Apply the winner to state['modules'] and record
        a diagnostic.
        """
        state = self.load_state()
        # Load each candidate config (apply edits onto current modules)
        candidates = []
        for k in range(1, K + 1):
            path = os.path.join(self.state_dir, f'edits_round_{until}_draw{k}.json')
            if not os.path.exists(path):
                print(f'[select] missing draw {k}: {path}')
                continue
            with open(path) as f:
                data = json.load(f)
            edit_tuples = [
                (e['widget'], e['path'], e.get('from', 0.0),
                 e['to'], e.get('reason', ''))
                for e in data['edits']
            ]
            cfg = apply_edits(state['modules'], edit_tuples)
            candidates.append((k, data, cfg))

        val_stream = make_session_stream(VALIDATION_N, seed=VALIDATION_SEED)
        scored = []
        for k, data, cfg in candidates:
            m, s = evaluate_config(cfg, val_stream)
            scored.append((m, s, k, data, cfg))
        scored.sort(key=lambda x: -x[0])
        best_m, best_s, best_k, best_data, best_cfg = scored[0]

        diag = {
            'all_means': [(k, m, s) for m, s, k, _, _ in scored],
            'best_draw': best_k,
            'best_mean': best_m,
            'best_std': best_s,
        }
        state['modules'] = best_cfg
        state['edit_history'].append({
            'session': state['session_idx'],
            'count': len(best_data['edits']),
            'note': best_data.get('note', '') + f'  [ensemble-best of {len(scored)}: draw {best_k}]',
            'ensemble_diag': diag,
        })
        self.save_state(state)
        print(f'[select] best of {len(scored)} draws at session {state["session_idx"]}: '
              f'draw {best_k} (mean {best_m:.4f}, std {best_s:.4f})')
        for m, s, k, _, _ in scored:
            print(f'  draw {k}: mean={m:.4f}  std={s:.4f}')


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    a1 = sp.add_parser('prepare')
    a1.add_argument('--state-dir', required=True)
    a1.add_argument('--until', type=int, required=True)
    a1.add_argument('--apply', type=str, default=None)
    a1.add_argument('--K', type=int, default=3)
    a2 = sp.add_parser('select')
    a2.add_argument('--state-dir', required=True)
    a2.add_argument('--until', type=int, required=True)
    a2.add_argument('--K', type=int, default=3)
    args = ap.parse_args()
    orch = EnsembleOrchestrator(args.state_dir)
    if args.cmd == 'prepare':
        orch.prepare_round(args.until, K=args.K, apply_path=args.apply)
    elif args.cmd == 'select':
        orch.select_round(args.until, K=args.K)


if __name__ == '__main__':
    main()
