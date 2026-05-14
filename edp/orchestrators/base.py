"""
Shared orchestrator scaffolding: state load/save, batch run, edit application.

Subclasses (report.py, opro.py) override render_prompt() to control what
the LLM agent sees at each checkpoint.
"""
from __future__ import annotations
import json
import os
import sys
import argparse
import numpy as np
from typing import Optional

from edp import (make_session_stream, true_page_reward, oracle_reward,
                 EDPPolicy)
from edp.policies.edp import make_modules, apply_edits


class Orchestrator:
    """Base class for live-agent EDP evolution orchestrators."""

    def __init__(self, state_dir: str):
        self.state_dir = state_dir
        os.makedirs(self.state_dir, exist_ok=True)

    def state_path(self):
        return os.path.join(self.state_dir, 'state.json')

    def load_state(self):
        if not os.path.exists(self.state_path()):
            return {
                'session_idx': 0,
                'modules': make_modules(),
                'rewards': [],
                'oracle': [],
                'sessions': [],         # list of (persona, category) per session
                'recent_logs': [],
                'edit_history': [],
            }
        with open(self.state_path()) as f:
            return json.load(f)

    def save_state(self, state):
        with open(self.state_path(), 'w') as f:
            json.dump(state, f)

    def run_batch(self, state, until_idx, seed=42):
        stream = make_session_stream(until_idx, seed=seed)
        policy = EDPPolicy(modules=state['modules'])
        rewards = list(state['rewards'])
        oracle = list(state['oracle'])
        sessions = list(state['sessions'])
        new_logs = []
        start = state['session_idx']
        for i in range(start, until_idx):
            persona, category, feat = stream[i]
            page = policy.select_page(feat)
            r = true_page_reward(persona, category, page)
            o = oracle_reward(persona, category)
            rewards.append(r)
            oracle.append(o)
            sessions.append([persona, category])
            new_logs.append({
                'i': i, 'persona': persona, 'category': category,
                'page': page,
                'reward': round(r, 4), 'oracle': round(o, 4),
                'regret': round(o - r, 4),
            })
        state['session_idx'] = until_idx
        state['rewards'] = rewards
        state['oracle'] = oracle
        state['sessions'] = sessions
        state['recent_logs'] = new_logs
        return state

    def apply_edits_from_file(self, state, path, **extras):
        with open(path) as f:
            data = json.load(f)
        edit_tuples = [
            (e['widget'], e['path'], e.get('from', 0.0),
             e['to'], e.get('reason', ''))
            for e in data['edits']
        ]
        state['modules'] = apply_edits(state['modules'], edit_tuples)
        state['edit_history'].append({
            'session': state['session_idx'],
            'count': len(edit_tuples),
            'note': data.get('note', ''),
            **extras,
        })
        return state

    def render_prompt(self, state, batch_start, batch_end, report_text,
                      out_path) -> str:
        """Subclasses override to build the prompt content."""
        raise NotImplementedError

    def make_report(self, state, batch_start, batch_end) -> str:
        """Subclasses override; OPRO returns a minimal one."""
        raise NotImplementedError

    def run(self, until: int, apply_path: Optional[str] = None,
            reset: bool = False, seed: int = 42):
        if reset and os.path.exists(self.state_path()):
            os.remove(self.state_path())

        state = self.load_state()
        batch_start = state['session_idx']

        if apply_path:
            if batch_start == 0:
                print('Cannot apply edits before any sessions have run.')
                sys.exit(1)
            state = self.apply_edits_from_file(state, apply_path)
            print(f'Applied edits from {apply_path}.')

        state = self.run_batch(state, until, seed=seed)
        report = self.make_report(state, batch_start, until)
        rpt_path = os.path.join(self.state_dir, f'report_at_{until}.md')
        with open(rpt_path, 'w') as f:
            f.write(report)
        self.save_state(state)

        next_edits = os.path.join(self.state_dir, f'edits_round_{until}.json')
        prompt = self.render_prompt(state, batch_start, until, report,
                                     next_edits)
        prompt_path = os.path.join(self.state_dir, f'PROMPT_at_{until}.md')
        with open(prompt_path, 'w') as f:
            f.write(prompt)

        rewards = np.array(state['rewards'])
        oracle = np.array(state['oracle'])
        cum_regret = float((oracle - rewards).sum())
        print(f'\n[{self.__class__.__name__}] sessions {batch_start} -> {until}')
        print(f'  cum regret so far: {cum_regret:.2f}')
        print(f'  state    -> {self.state_path()}')
        print(f'  report   -> {rpt_path}')
        print(f'  prompt   -> {prompt_path}')
        print(f'  next     -> {next_edits}')
        return state


def cli_main(orchestrator_factory):
    """Build an argparse-driven CLI for a given orchestrator class."""
    ap = argparse.ArgumentParser()
    ap.add_argument('--until', type=int, required=True)
    ap.add_argument('--apply', type=str, default=None)
    ap.add_argument('--reset', action='store_true')
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--state-dir', type=str, required=True)
    args = ap.parse_args()
    orch = orchestrator_factory(args.state_dir)
    orch.run(until=args.until, apply_path=args.apply,
             reset=args.reset, seed=args.seed)
