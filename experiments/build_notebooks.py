"""Generate the example notebooks under notebooks/ from verified code.

Run once: python experiments/build_notebooks.py
Outputs notebooks/01_quickstart.ipynb, 02_explainability.ipynb,
03_custom_policy.ipynb. Cells are not pre-executed (no kernel in this
image); every code cell has been run as a plain script first.
"""
from __future__ import annotations
import pathlib
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

OUT = pathlib.Path(__file__).resolve().parent.parent / 'notebooks'
OUT.mkdir(exist_ok=True)

PREAMBLE = (
    "import os, sys\n"
    "# notebooks live in notebooks/; make the repo root importable\n"
    "sys.path.insert(0, os.path.abspath('..'))\n"
)


def md(*lines):
    return new_markdown_cell('\n'.join(lines))


def code(src):
    return new_code_cell(src.strip('\n'))


def write(name, cells):
    nb = new_notebook(cells=cells, metadata={
        'kernelspec': {'display_name': 'Python 3', 'language': 'python',
                       'name': 'python3'},
        'language_info': {'name': 'python'},
    })
    p = OUT / name
    nbf.write(nb, str(p))
    print(f'wrote {p}')


# ---------------------------------------------------------------------------
# 01 — quickstart: the Gym-like env/agent API
# ---------------------------------------------------------------------------
quickstart = [
    md('# 1. Quickstart: the Gym-like env / agent API',
       '',
       'This notebook shows the environment/algorithm split added in '
       '`edp/env.py` and `edp/agents.py`. The same `PageCompositionEnv` '
       'and `run_episode` runner drive three very different policies — a '
       'deterministic GAM (EDP-static), an online contextual bandit '
       '(LinTS), and the LLM-prior + SGD fusion (Bayesian-EDP) — with no '
       'policy-specific loop code.'),
    code(PREAMBLE),
    code(
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "from edp.env import PageCompositionEnv\n"
        "from edp.agents import EDPAgent, BanditAgent, BayesianEDPAgent, run_episode\n"
        "from edp.policies.edp import EDPPolicy\n"
        "from edp.policies.bandit import BanditPolicy\n"
        "from edp.policies.bayesian_edp import BayesianEDPPolicy"
    ),
    md('## The environment',
       '',
       '`PageCompositionEnv` owns the session stream and the production '
       'reward stack: page-level attribution, multi-day delay (`delay=500` '
       'sessions), and observation noise (`noise_sigma=0.20`). Each '
       'observation exposes the fashion `category` and the 14 raw '
       'behavioural signals in `feat`; the persona is hidden because it is '
       'the latent the reward depends on.'),
    code(
        "env = PageCompositionEnv(n=2000, seed=42, source='parametric',\n"
        "                         delay=500, noise_sigma=0.20)\n"
        "obs = env.reset()\n"
        "print('category :', obs.category)\n"
        "print('feat keys:', sorted(obs.feat)[:6], '...')\n"
        "print('index    :', obs.index)"
    ),
    md('## One episode, three policies',
       '',
       'The runner is identical for every agent. An agent only has to '
       'implement `act(obs) -> (page, payload)`, `learn(reward, payload)`, '
       'and `maybe_checkpoint(index)`.'),
    code(
        "def fresh():\n"
        "    return PageCompositionEnv(n=2000, seed=42, source='parametric',\n"
        "                              delay=500, noise_sigma=0.20)\n"
        "\n"
        "runs = {}\n"
        "e = fresh(); runs['EDP-static']   = (run_episode(e, EDPAgent(EDPPolicy())), e)\n"
        "e = fresh(); runs['LinTS-warm']   = (run_episode(e,\n"
        "        BanditAgent(BanditPolicy(ctx_dim=7, alpha=0.3, seed=7), context='warm')), e)\n"
        "e = fresh(); runs['Bayesian-EDP'] = (run_episode(e,\n"
        "        BayesianEDPAgent(BayesianEDPPolicy(lr=5e-4, lam=2.0, prior_sigma=0.3))), e)\n"
        "\n"
        "for name, (out, e) in runs.items():\n"
        "    print(f'{name:14s} regret% = {out[\"regret_pct\"]:.2f}')"
    ),
    md('## Cumulative regret over the episode',
       '',
       'The environment records the oracle and the realised reward per '
       'session, so the cumulative-regret curve is just '
       '`cumsum(oracle - reward)`. EDP-static and Bayesian-EDP track the '
       'oracle closely from session 0 (the LLM-authored prior is competent '
       'with zero data); the bandit pays an exploration tax that never '
       'amortises under page-level reward.'),
    code(
        "plt.figure(figsize=(8, 5))\n"
        "for name, (out, e) in runs.items():\n"
        "    cum = np.cumsum(e.oracles - e.rewards)\n"
        "    plt.plot(cum, label=name, lw=2)\n"
        "plt.xlabel('session'); plt.ylabel('cumulative regret')\n"
        "plt.title('Cumulative regret (parametric, production conditions)')\n"
        "plt.legend(); plt.grid(alpha=0.3); plt.show()"
    ),
    md('## Switching the simulator',
       '',
       "Pass `source='llm'` to swap the parametric 8-persona simulator for "
       'the LLM-driven 14-persona × 6-category one. Nothing else changes.'),
    code(
        "e = PageCompositionEnv(n=2000, seed=42, source='llm',\n"
        "                       delay=500, noise_sigma=0.20)\n"
        "out = run_episode(e, EDPAgent(EDPPolicy()))\n"
        "print('EDP-static on LLM-persona, regret% =', round(out['regret_pct'], 2))"
    ),
]

# ---------------------------------------------------------------------------
# 02 — open-box explainability
# ---------------------------------------------------------------------------
explain = [
    md('# 2. Open-box explainability: one decision, fully traced',
       '',
       'Every page choice an EDP makes factors into readable curves. This '
       'notebook reproduces the trace behind Figure 9 of the paper for a '
       'single session: 14 raw signals → 7 latent problem scores → a '
       'slot-1 score that decomposes additively across candidate widgets.'),
    code(PREAMBLE),
    code(
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "from edp.env import PageCompositionEnv\n"
        "from edp.policies.edp import make_problem_shapes, make_modules, score_problems\n"
        "from edp.config import PROBLEMS, N_SLOTS"
    ),
    md('## Pick a size-anxious session',
       '',
       'We scan the stream for a `size_anxious_new` session so the trace '
       'has a clear dominant problem. (The env hides the persona at serving '
       'time; here we read the stream directly only to choose an '
       'illustrative example.)'),
    code(
        "env = PageCompositionEnv(n=200, seed=42, source='parametric')\n"
        "env.reset()\n"
        "# env._stream is (persona, category, feat) — used here only to pick an example\n"
        "persona, category, feat = next(s for s in env._stream if s[0] == 'size_anxious_new')\n"
        "print('persona  :', persona)\n"
        "print('category :', category)"
    ),
    md('## Step 1 — raw signals',
       '',
       'The size-anxious persona concentrates mass on `size_chart`, low '
       '`size_conf`, and `return_hist`.'),
    code(
        "sig_names = ['size_conf','price_sens','return_hist','style_stretch','new',\n"
        "             'mobile','size_chart','tab_switch','zoom','price_dwell',\n"
        "             'cart_osc','wishlist','return_view','revisit']\n"
        "vals = [feat.get(s, 0.0) for s in sig_names]\n"
        "plt.figure(figsize=(10, 3))\n"
        "plt.bar(sig_names, vals, color='#4C72B0'); plt.ylim(0, 1)\n"
        "plt.xticks(rotation=45, ha='right'); plt.ylabel('signal value')\n"
        "plt.title('Step 1: 14 raw behavioural signals'); plt.tight_layout(); plt.show()"
    ),
    md('## Step 2 — Layer-1 problem fingerprint',
       '',
       '`score_problems` runs the PWL shape functions and produces the 7-d '
       'problem fingerprint. F3.2 (size anxiety) dominates.'),
    code(
        "shapes = make_problem_shapes()\n"
        "problems = score_problems(feat, shapes)\n"
        "for p, v in sorted(problems.items(), key=lambda kv: -kv[1]):\n"
        "    print(f'{p:5s} {v:.3f}')"
    ),
    md('## Step 3 — slot-1 score decomposition',
       '',
       'For slot 1, each widget score is '
       '`base + Σ on_rem·remaining + Σ on_cov·coverage − slot_decay·0`. '
       'The winner wins on its on-remaining slope against F3.2, not on a '
       'high base.'),
    code(
        "modules = make_modules()\n"
        "remaining = dict(problems); coverage = {p: 0.0 for p in PROBLEMS}\n"
        "rows = []\n"
        "for name, mod in modules.items():\n"
        "    base = mod['base']\n"
        "    rem  = sum(w * remaining.get(p, 0.0) for p, w in mod.get('on_rem', {}).items())\n"
        "    cov  = sum(w * coverage.get(p, 0.0) for p, w in mod.get('on_cov', {}).items())\n"
        "    rows.append((name, base, rem, cov, base + rem + cov))\n"
        "rows.sort(key=lambda r: -r[-1])\n"
        "top = rows[:5]\n"
        "print(f'{\"widget\":22s} {\"base\":>6s} {\"on_rem\":>7s} {\"total\":>7s}')\n"
        "for name, base, rem, cov, tot in top:\n"
        "    print(f'{name:22s} {base:6.2f} {rem:7.2f} {tot:7.2f}')"
    ),
    code(
        "names = [r[0] for r in top]\n"
        "bases = np.array([r[1] for r in top]); rems = np.array([r[2] for r in top])\n"
        "covs  = np.array([r[3] for r in top]); tots = np.array([r[4] for r in top])\n"
        "x = np.arange(len(names))\n"
        "plt.figure(figsize=(9, 4))\n"
        "plt.bar(x, bases, label='base', color='#7F7F7F')\n"
        "plt.bar(x, rems, bottom=bases, label='on_remaining', color='#C44E52')\n"
        "plt.bar(x, covs, bottom=bases+rems, label='on_coverage', color='#55A868')\n"
        "plt.scatter(x, tots, color='black', zorder=5, label='total')\n"
        "plt.xticks(x, names, rotation=15); plt.ylabel('score contribution')\n"
        "plt.title(f'Step 3: slot-1 decomposition (winner = {names[0]})')\n"
        "plt.legend(); plt.tight_layout(); plt.show()"
    ),
    md('The whole decision is 14 + 7 + (22 scored widgets) named numbers. '
       'No SHAP, no surrogate model — the trace *is* the policy.'),
]

# ---------------------------------------------------------------------------
# 03 — writing a custom policy
# ---------------------------------------------------------------------------
custom = [
    md('# 3. Writing a custom policy',
       '',
       'Any object with `act` / `learn` / `maybe_checkpoint` is a valid '
       'agent. Here we write a trivial baseline — always place the six '
       'highest-`base` widgets — and run it through the same environment '
       'and runner as the built-in policies.'),
    code(PREAMBLE),
    code(
        "from edp.env import PageCompositionEnv\n"
        "from edp.agents import run_episode\n"
        "from edp.policies.edp import make_modules\n"
        "from edp.config import N_SLOTS\n"
        "\n"
        "class TopBaseAgent:\n"
        "    '''Always place the N_SLOTS widgets with the highest base prior.'''\n"
        "    def __init__(self):\n"
        "        m = make_modules()\n"
        "        self.page = sorted(m, key=lambda w: -m[w]['base'])[:N_SLOTS]\n"
        "    def act(self, obs):\n"
        "        return self.page, None      # payload=None -> no learning signal\n"
        "    def learn(self, reward, payload):\n"
        "        pass\n"
        "    def maybe_checkpoint(self, index):\n"
        "        pass"
    ),
    code(
        "env = PageCompositionEnv(n=2000, seed=42, source='parametric')\n"
        "out = run_episode(env, TopBaseAgent())\n"
        "print('TopBaseAgent regret% =', round(out['regret_pct'], 2))"
    ),
    md('## A learning custom policy',
       '',
       'To learn online, return a `payload` from `act` (anything you need '
       'to attribute the delayed reward later) and update in `learn`. The '
       'environment hands each matured `(reward, payload)` pair back to '
       '`learn` once the delay elapses. Below, an epsilon-greedy-ish '
       'placeholder records the running mean reward per first-slot widget.'),
    code(
        "import random\n"
        "from edp.catalog import WIDGETS\n"
        "from edp.config import N_SLOTS\n"
        "\n"
        "class GreedyFirstSlot:\n"
        "    def __init__(self, seed=0):\n"
        "        self.mean = {w: 0.0 for w in WIDGETS}\n"
        "        self.n = {w: 0 for w in WIDGETS}\n"
        "        self.rng = random.Random(seed)\n"
        "    def act(self, obs):\n"
        "        if self.rng.random() < 0.1:           # explore\n"
        "            first = self.rng.choice(WIDGETS)\n"
        "        else:                                  # exploit best mean\n"
        "            first = max(self.mean, key=self.mean.get)\n"
        "        rest = [w for w in WIDGETS if w != first][:N_SLOTS - 1]\n"
        "        page = [first] + rest\n"
        "        return page, first                     # payload = the slot-1 arm\n"
        "    def learn(self, reward, first):\n"
        "        self.n[first] += 1\n"
        "        self.mean[first] += (reward - self.mean[first]) / self.n[first]\n"
        "    def maybe_checkpoint(self, index):\n"
        "        pass\n"
        "\n"
        "env = PageCompositionEnv(n=3000, seed=42, source='parametric')\n"
        "out = run_episode(env, GreedyFirstSlot(seed=1))\n"
        "print('GreedyFirstSlot regret% =', round(out['regret_pct'], 2))"
    ),
    md('Neither toy is competitive with the built-in policies — that is the '
       'point. The env/agent boundary lets you drop in any idea and measure '
       'it against the same oracle, under the same production reward stack, '
       'with three lines of glue.'),
]

write('01_quickstart.ipynb', quickstart)
write('02_explainability.ipynb', explain)
write('03_custom_policy.ipynb', custom)
