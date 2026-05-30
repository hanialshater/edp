#!/usr/bin/env python3
"""EDP harness for the Post-6 'run it for real' test.

Reproduces the paper's §5.4 ablation in miniature, in sync with the live widget
in blog/05-edp/index.html:

  - Loads the SAME POLICY JSON and the SAME 6 personas from the post.
  - Defines a hidden ground-truth oracle: each persona has an ideal set of
    widgets (the modules that address its dominant problems). Page reward =
    overlap of the composed page with that ideal set, with slot-decay weighting.
  - Regret = (oracle_reward - policy_reward), averaged over personas, in %.

Two editor channels, mirroring the paper:
  * report  : a STRUCTURED diagnostic — per-persona regret + which widget
              families are over/under-served + the addressable edit paths.
  * opro    : SCORE-ONLY — just the scalar total regret and the last edits.

A subagent (the LLM) reads one channel and emits typed scalar edits to the
policy (e.g. set modules.size_guide.on_rem.F32 = 2.4). apply_edits() applies
them; evaluate() re-scores. The point: structured context lets the editor
reason about WHICH curve to nudge; score-only does not.

CLI:
    python3 edp_harness.py report          # print the structured diagnostic
    python3 edp_harness.py opro            # print the score-only view
    python3 edp_harness.py eval            # print current regret table
    python3 edp_harness.py apply '<edits-json>'   # apply edits, print new regret
        edits = [{"path":"modules.size_guide.on_rem.F32","value":2.4,"reason":"..."}]
    python3 edp_harness.py reset           # restore policy to the post's baseline
State persists in edp_state.json so a multi-round agent run is reproducible.
"""
import sys, os, re, json, copy

HERE = os.path.dirname(os.path.abspath(__file__))
POST = os.path.join(HERE, "..", "05-edp", "index.html")
STATE = os.environ.get("EDP_STATE", os.path.join(HERE, "edp_state.json"))
N_SLOTS = 6

# ---------------------------------------------------------------- load post data
def _extract(html, name):
    # find `const NAME = {` then take the brace-balanced object that follows
    m = re.search(r'const\s+%s\s*=\s*\{' % name, html)
    if not m:
        raise SystemExit(f"could not find {name} in the post")
    start = m.end() - 1          # index of the opening brace
    depth = 0
    for i in range(start, len(html)):
        c = html[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return json.loads(_js_to_json(html[start:i+1]))
    raise SystemExit(f"unbalanced braces extracting {name}")

def _js_to_json(s):
    """Normalize a JS object literal (single-quoted / bare keys) to JSON."""
    s = re.sub(r"'([^']*)'", r'"\1"', s)                 # 'k' -> "k"
    s = re.sub(r'([{,]\s*)([A-Za-z_]\w*)\s*:', r'\1"\2":', s)  # bareKey: -> "bareKey":
    s = re.sub(r',\s*([}\]])', r'\1', s)                 # strip trailing commas
    return s

def load_post():
    html = open(POST).read()
    policy = _extract(html, "POLICY")
    personas = _extract(html, "PERSONAS")
    return policy, personas

BASE_POLICY, PERSONAS = load_post()
PROB_LABELS = {"F32":"size anxiety","F33":"quality deficit","F41":"comparison",
               "F43":"outfit visualization","F45":"price-quality",
               "F46":"return hesitation","F51":"decision paralysis"}

# ---------------------------------------------------------------- the EDP solver
# (identical math to compose() / scoreProblems() in the post's JS)
def pwl(x, bps, vals):
    if x <= bps[0]: return vals[0]
    if x >= bps[-1]: return vals[-1]
    for i in range(len(bps) - 1):
        if x <= bps[i+1]:
            t = (x - bps[i]) / (bps[i+1] - bps[i])
            return vals[i] + t * (vals[i+1] - vals[i])
    return vals[-1]

def score_problems(policy, feat):
    out = {}
    for prob, sigs in policy["shapes"].items():
        s = w = 0.0
        for sig, c in sigs.items():
            x = feat.get("size_conf", 0) if sig == "size_conf_inv" else feat.get(sig, 0)
            s += c["weight"] * pwl(x, c["bps"], c["vals"]); w += c["weight"]
        out[prob] = max(0.0, min(1.0, s / max(w, 1e-9)))
    return out

def compose(policy, feat):
    problems = score_problems(policy, feat)
    remaining = dict(problems); coverage = {p: 0.0 for p in policy["shapes"]}
    used, page = set(), []
    for slot in range(N_SLOTS):
        best, best_s = None, -1e9
        for name, m in policy["modules"].items():
            if name in used: continue
            s = m["base"]
            for p, c in m.get("on_rem", {}).items(): s += c * remaining.get(p, 0)
            for p, c in m.get("on_cov", {}).items(): s += c * coverage.get(p, 0)
            s -= m["slot_decay"] * slot
            if s > best_s: best_s, best = s, name
        page.append(best); used.add(best)
        for p, a in policy["modules"][best].get("addr", {}).items():
            remaining[p] = max(0.0, remaining.get(p, 0) - a)
            coverage[p] = min(1.0, coverage.get(p, 0) + a)
    return page, problems

# ---------------------------------------------------------------- hidden oracle
# Ground truth the policy is NOT told: for each persona, the "ideal" page is the
# top modules by how well they address that persona's dominant problems. Reward
# is slot-decayed overlap of the composed page with that ideal ranking.
SLOT_W = [1.0, 0.85, 0.72, 0.6, 0.5, 0.42]

def persona_problem_intensity(persona_feat):
    return score_problems(BASE_POLICY, persona_feat)

def module_value_for(policy, name, intensity):
    """How much this module truly helps this persona = Σ addr_p * intensity_p."""
    m = policy["modules"][name]
    return sum(a * intensity.get(p, 0) for p, a in m.get("addr", {}).items())

def oracle_page(policy, intensity):
    ranked = sorted(policy["modules"], key=lambda n: -module_value_for(policy, n, intensity))
    return ranked[:N_SLOTS]

def page_reward(policy, page, intensity):
    return sum(SLOT_W[i] * module_value_for(policy, w, intensity) for i, w in enumerate(page))

def evaluate(policy):
    """Per-persona regret % and aggregates."""
    rows = {}
    for pname, feat in PERSONAS.items():
        intensity = persona_problem_intensity(feat)
        page, _ = compose(policy, feat)
        opt = oracle_page(policy, intensity)
        r_pol = page_reward(policy, page, intensity)
        r_opt = page_reward(policy, opt, intensity)
        regret = 0.0 if r_opt <= 1e-9 else max(0.0, (r_opt - r_pol) / r_opt)
        rows[pname] = {"regret_pct": round(100*regret, 2), "page": page,
                       "oracle": opt, "intensity": {p: round(v,2) for p,v in intensity.items()}}
    mean = round(sum(r["regret_pct"] for r in rows.values()) / len(rows), 2)
    return {"mean_regret_pct": mean, "personas": rows}

# ---------------------------------------------------------------- diagnostics
def dominant_problems(intensity, k=2):
    return [p for p, _ in sorted(intensity.items(), key=lambda kv: -kv[1])[:k]]

def structured_report(policy):
    ev = evaluate(policy)
    lines = ["STRUCTURED DIAGNOSTIC REPORT (EDP editor sees this)",
             f"aggregate mean regret: {ev['mean_regret_pct']}%\n",
             "per-persona breakdown (regret, dominant problems, what the page",
             "served vs what the oracle wanted):"]
    for pname, r in sorted(ev["personas"].items(), key=lambda kv: -kv[1]["regret_pct"]):
        dom = dominant_problems(r["intensity"])
        served = set(r["page"]); ideal = set(r["oracle"])
        missing = [w for w in r["oracle"] if w not in served]
        wasted = [w for w in r["page"] if w not in ideal]
        lines.append(f"\n- {pname}: regret {r['regret_pct']}%  dominant={dom} "
                     f"({', '.join(PROB_LABELS[p] for p in dom)})")
        lines.append(f"    page served : {r['page']}")
        lines.append(f"    oracle wants: {r['oracle']}")
        if missing: lines.append(f"    UNDER-SERVED (in oracle, not on page): {missing}")
        if wasted:  lines.append(f"    OVER-SERVED  (on page, not in oracle): {wasted}")
    # addressable knobs for the under-served modules
    lines.append("\naddressable edit paths (raise on_rem to promote a module for its problem):")
    knobs = set()
    for r in ev["personas"].values():
        for w in r["oracle"]:
            for p in policy["modules"][w].get("on_rem", {}):
                knobs.add(f"modules.{w}.on_rem.{p}  (currently {policy['modules'][w]['on_rem'][p]})")
    for k in sorted(knobs)[:24]:
        lines.append("  " + k)
    return "\n".join(lines)

def opro_view(policy):
    ev = evaluate(policy)
    st = load_state()
    lines = ["SCORE-ONLY VIEW (OPRO editor sees ONLY this)",
             f"current aggregate regret: {ev['mean_regret_pct']}%",
             "\nhistory of (edit_batch, resulting_regret):"]
    if not st["history"]:
        lines.append("  (none yet)")
    for h in st["history"]:
        lines.append(f"  round {h['round']}: {len(h['edits'])} edits -> regret {h['regret']}%")
    lines.append("\nYou may propose typed scalar edits of the form "
                 "modules.<name>.<field>.<problem> = value. You are NOT told which "
                 "persona or widget is mis-served.")
    return "\n".join(lines)

# ---------------------------------------------------------------- edit + state
def set_path(policy, path, value):
    cur = policy; parts = path.split(".")
    for p in parts[:-1]:
        if p not in cur: raise KeyError(f"bad path segment {p!r} in {path}")
        cur = cur[p]
    cur[parts[-1]] = float(value)

def apply_edits(policy, edits):
    applied = []
    for e in edits:
        try:
            set_path(policy, e["path"], e["value"]); applied.append(e["path"])
        except (KeyError, ValueError) as ex:
            applied.append(f"FAILED {e.get('path')}: {ex}")
    return applied

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"policy": copy.deepcopy(BASE_POLICY), "history": [], "round": 0}

def save_state(st):
    json.dump(st, open(STATE, "w"), indent=0)

# ---------------------------------------------------------------- CLI
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "eval"
    st = load_state()
    pol = st["policy"]
    if cmd == "reset":
        save_state({"policy": copy.deepcopy(BASE_POLICY), "history": [], "round": 0})
        print("reset to baseline. regret:", evaluate(BASE_POLICY)["mean_regret_pct"], "%")
    elif cmd == "report":
        print(structured_report(pol))
    elif cmd == "opro":
        print(opro_view(pol))
    elif cmd == "eval":
        ev = evaluate(pol)
        print(f"mean regret: {ev['mean_regret_pct']}%")
        for p, r in sorted(ev["personas"].items(), key=lambda kv:-kv[1]["regret_pct"]):
            print(f"  {p:20s} {r['regret_pct']:6.2f}%")
    elif cmd == "apply":
        edits = json.loads(sys.argv[2])
        applied = apply_edits(pol, edits)
        st["round"] += 1
        ev = evaluate(pol)
        st["history"].append({"round": st["round"], "edits": edits,
                              "regret": ev["mean_regret_pct"]})
        save_state(st)
        print(f"applied {len(applied)} edits -> mean regret {ev['mean_regret_pct']}%")
        for a in applied: print("  ", a)
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
