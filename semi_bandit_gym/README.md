# `semi_bandit_gym`

A correctness-first structured-bandit harness for EDP research.

The browser Berlin52 demo is useful for intuition. It is not a trustworthy
algorithm harness. This package makes the experiment contract explicit:

```text
hidden world -> environment -> agent -> exact solver -> evaluator -> renderer
```

The first environment is a **route-level contextual combinatorial semi-bandit**:

- **action**: one complete Hamiltonian tour;
- **feedback**: one labelled noisy cost for each selected edge;
- **public context**: edge features plus route-position / rush features;
- **hidden world**: fixed expected-cost law, with no day-to-day drift;
- **evaluation**: exact time-indexed TSP oracle on 4-12 nodes.

## Agent-like API

The API intentionally looks like Gym while preserving semi-bandit feedback
instead of collapsing everything into one scalar reward.

```python
observation = env.reset(seed=42)

while True:
    action = agent.plan(observation)
    result = env.step(action)
    agent.update(result.feedback)
    observation = result.observation
    if result.terminated:
        break
```

`result.feedback` contains one `EdgeFeedback` record for every selected tour
edge. It never exposes unselected edge costs, hidden expected costs, or oracle
values. `ExactOracle` is evaluator-only and should not be passed to the agent.

## Run

```bash
python -m unittest discover -s tests -v
python examples/run_contextual_tsp.py
```

## Correctness contract

The test suite checks:

1. only selected route edges are observed;
2. malformed tours are rejected;
3. the fixed hidden city has no daily drift when observation noise is zero;
4. the exact Held-Karp oracle matches brute force on a small world;
5. a contextual LCB agent beats an edge-only baseline when route position truly
   changes costs.

## Why tiny exact worlds come before Berlin52

Berlin52 is a good visual stress test but a poor correctness oracle: browser
heuristics, approximate routes, animation state, and rendering can all mask a
semantic error. The tiny environment keeps the action space small enough to
solve exactly, so an observed convergence claim can be tied to a testable
contract before it becomes a polished interactive story.
