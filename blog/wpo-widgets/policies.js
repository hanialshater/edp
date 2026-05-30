// Policy library: alternative widget-selection strategies.
// Each policy implements `select(feat, modules)` returning the same shape as
// the orchestrator's compose() — { page, problems, remaining, coverage }.
//
// We keep these in one file so the Policies tab can iterate the registry,
// run simulations, and present metrics side by side.

(function () {
  const PROBLEMS = window.__POLICIES_BOOT_PROBLEMS = ['F32','F33','F41','F43','F45','F46','F51'];

  // Helper: apply a widget's addressing to remaining/coverage state.
  function applyAddr(mod, remaining, coverage) {
    for (const p in (mod.addr || {})) {
      remaining[p] = Math.max(0, remaining[p] - mod.addr[p]);
      coverage[p] = Math.min(1, coverage[p] + mod.addr[p]);
    }
  }

  // Standard initial state for compose: detect problems, init remaining/coverage.
  function initState(feat) {
    const problems = window.scoreProblems(feat);
    return {
      problems,
      remaining: { ...problems },
      coverage: Object.fromEntries(PROBLEMS.map(p => [p, 0])),
    };
  }

  // ─── Policies ──────────────────────────────────────────────────────────

  // v-greedy: the orchestrator's own compose(), parameterized by module set.
  function greedy(feat, modules, n = 6) {
    return window.compose(feat, modules, n);
  }

  // Random: shuffle, take 6. Worst-case baseline.
  function random(feat, modules, n = 6) {
    const s = initState(feat);
    const names = Object.keys(modules).sort(() => Math.random() - 0.5).slice(0, n);
    const page = names.map((name, slot) => {
      const mod = modules[name];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      applyAddr(mod, s.remaining, s.coverage);
      return { slot, name, score, scores: {} };
    });
    return { page, ...s };
  }

  // Base-only: rank by static base score, ignore problems entirely.
  // Models a system that hasn't learned per-session signals.
  function baseOnly(feat, modules, n = 6) {
    const s = initState(feat);
    const names = Object.keys(modules)
      .sort((a, b) => modules[b].base - modules[a].base)
      .slice(0, n);
    const page = names.map((name, slot) => {
      const mod = modules[name];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      applyAddr(mod, s.remaining, s.coverage);
      return { slot, name, score, scores: {} };
    });
    return { page, ...s };
  }

  // ε-greedy: greedy with epsilon chance of a random pick per slot.
  // Models a bandit that exploits but still explores.
  function epsilonGreedy(feat, modules, n = 6, epsilon = 0.15) {
    const s = initState(feat);
    const page = [];
    const used = new Set();
    for (let slot = 0; slot < n; slot++) {
      const avail = Object.keys(modules).filter(name => !used.has(name));
      let pick;
      if (Math.random() < epsilon) {
        pick = avail[Math.floor(Math.random() * avail.length)];
      } else {
        let bestName = avail[0], bestScore = -Infinity;
        avail.forEach(name => {
          const sc = window.scoreModule(modules[name], s.remaining, s.coverage, slot);
          if (sc > bestScore) { bestScore = sc; bestName = name; }
        });
        pick = bestName;
      }
      const mod = modules[pick];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      page.push({ slot, name: pick, score, scores: {} });
      used.add(pick);
      applyAddr(mod, s.remaining, s.coverage);
    }
    return { page, ...s };
  }

  // Thompson sampling: noisy greedy where noise scales with widget uncertainty.
  // Widgets with strong addr have low uncertainty (the system has learned them);
  // widgets with low addr/no addr get high noise (exploring).
  function thompson(feat, modules, n = 6) {
    const s = initState(feat);
    const page = [];
    const used = new Set();
    for (let slot = 0; slot < n; slot++) {
      let bestName = null, bestScore = -Infinity;
      Object.keys(modules).filter(name => !used.has(name)).forEach(name => {
        const mod = modules[name];
        const baseScore = window.scoreModule(mod, s.remaining, s.coverage, slot);
        const addrSum = Object.values(mod.addr || {}).reduce((a, b) => a + b, 0);
        // High addr → low uncertainty (small noise); low addr → high noise.
        const uncertainty = 1 / (1 + addrSum * 4);
        const noise = (Math.random() - 0.5) * uncertainty * 2.2;
        const sc = baseScore + noise;
        if (sc > bestScore) { bestScore = sc; bestName = name; }
      });
      const mod = modules[bestName];
      const score = window.scoreModule(mod, s.remaining, s.coverage, slot);
      page.push({ slot, name: bestName, score, scores: {} });
      used.add(bestName);
      applyAddr(mod, s.remaining, s.coverage);
    }
    return { page, ...s };
  }

  // ─── Policy registry ───────────────────────────────────────────────────

  window.POLICIES = {
    v1_greedy: {
      id: 'v1_greedy', name: 'v1 · Greedy', short: 'v1',
      color: '#94a3b8',
      desc: 'Baseline greedy submodular composition over the v1 module config.',
      modules: () => window.modulesV1,
      select: (feat) => greedy(feat, window.modulesV1, 6),
    },
    v3_greedy: {
      id: 'v3_greedy', name: 'v3 · Evolved', short: 'v3',
      color: '#fbbf24',
      desc: 'Greedy over the v3 config (new on_cov synergies + base adjustments).',
      modules: () => window.modulesV3,
      select: (feat) => greedy(feat, window.modulesV3, 6),
    },
    random: {
      id: 'random', name: 'Random', short: 'rand',
      color: '#fb7185',
      desc: 'Shuffle the registry and take the first 6. Lower bound — no learning, no signals.',
      modules: () => window.modulesV3,
      select: (feat) => random(feat, window.modulesV3, 6),
    },
    base_only: {
      id: 'base_only', name: 'Top-by-base', short: 'base',
      color: '#a78bfa',
      desc: 'Rank by static base score alone — ignores session signals entirely. The "popular widgets" trap.',
      modules: () => window.modulesV3,
      select: (feat) => baseOnly(feat, window.modulesV3, 6),
    },
    epsilon_greedy: {
      id: 'epsilon_greedy', name: 'ε-greedy bandit', short: 'ε-grd',
      color: '#34d399',
      desc: 'Greedy with 15% per-slot random exploration. Trades short-term score for learning surface.',
      modules: () => window.modulesV3,
      select: (feat) => epsilonGreedy(feat, window.modulesV3, 6, 0.15),
    },
    thompson: {
      id: 'thompson', name: 'Thompson sampling', short: 'thomp',
      color: '#60a5fa',
      desc: 'Sample widget rewards from posterior — explores well-supported widgets less, novel ones more.',
      modules: () => window.modulesV3,
      select: (feat) => thompson(feat, window.modulesV3, 6),
    },
  };

  // ─── Simulation engine ─────────────────────────────────────────────────
  // Run N trials. Each trial: sample a persona (uniformly by default), run the
  // policy, collect metrics. For policies with stochasticity (random / ε-grd /
  // thompson) we repeat per trial to average out.

  window.simulatePolicies = function (n = 200) {
    const policies = window.POLICIES;
    const personaKeys = Object.keys(window.PERSONAS);
    const SIGNALS = window.SIGNALS;

    const out = {};
    for (const pid in policies) {
      out[pid] = {
        coverageSum: 0,        // sum of coverage values per page (max 7)
        residualSum: 0,        // sum of remaining problem mass
        problemSum: 0,         // sum of initial problem intensity (for normalisation)
        clicksProj: 0,         // projected clicks (simulated)
        atbProj: 0,            // projected ATB (simulated)
        widgetCounts: {},      // how often each widget appears
        slotScoreSum: 0,       // sum of widget scores landed in page
        trials: 0,
      };
    }

    const TYPE_CTR = {
      outfit: 6.8, decision: 5.4, compare: 4.6, premium: 4.1,
      returns: 3.8, size: 3.2, price: 2.9, default: 2.3,
    };

    for (let t = 0; t < n; t++) {
      const persona = personaKeys[t % personaKeys.length];
      const feat = {};
      SIGNALS.forEach(s => {
        feat[s.id] = window.PERSONAS[persona].vals[s.id] ?? s.default;
        // small jitter so coverage isn't perfectly identical across trials
        feat[s.id] = Math.max(0, Math.min(1, feat[s.id] + (Math.random() - 0.5) * 0.05));
      });
      for (const pid in policies) {
        const result = policies[pid].select(feat);
        const modules = policies[pid].modules();
        const r = out[pid];
        const totalCov = Object.values(result.coverage).reduce((a, b) => a + b, 0);
        const totalRem = Object.values(result.remaining).reduce((a, b) => a + b, 0);
        const totalProb = Object.values(result.problems).reduce((a, b) => a + b, 0);
        r.coverageSum += totalCov;
        r.residualSum += totalRem;
        r.problemSum  += totalProb;
        // Estimated CTR per slot from widget type
        let clicks = 0, atb = 0, scoreSum = 0;
        result.page.forEach(entry => {
          const mod = modules[entry.name];
          const ctr = TYPE_CTR[mod.type] || 3;
          clicks += ctr / 100;
          atb += ctr / 100 * 0.18; // 18% click-to-atb base
          scoreSum += entry.score;
          r.widgetCounts[entry.name] = (r.widgetCounts[entry.name] || 0) + 1;
        });
        r.clicksProj += clicks;
        r.atbProj += atb;
        r.slotScoreSum += scoreSum;
        r.trials += 1;
      }
    }

    // Compute final per-policy metrics
    const final = {};
    for (const pid in out) {
      const r = out[pid];
      const trials = r.trials;
      const coverageRate = r.problemSum > 0 ? (r.coverageSum / r.problemSum) : 0;
      const widgetNames = Object.keys(r.widgetCounts);
      const totalPicks = widgetNames.reduce((a, k) => a + r.widgetCounts[k], 0);
      // Entropy of widget mix
      let entropy = 0;
      widgetNames.forEach(k => {
        const p = r.widgetCounts[k] / totalPicks;
        if (p > 0) entropy -= p * Math.log2(p);
      });
      const maxEntropy = Math.log2(widgetNames.length);
      const diversity = maxEntropy > 0 ? entropy / Math.log2(22) : 0; // normalised against full registry

      final[pid] = {
        ...policies[pid],
        trials,
        avgCoverage: r.coverageSum / trials,
        avgResidual: r.residualSum / trials,
        coverageRate, // 0..1
        avgClicks: r.clicksProj / trials,
        avgAtb: r.atbProj / trials,
        avgScore: r.slotScoreSum / trials,
        diversity, // 0..1
        widgetCounts: r.widgetCounts,
        widgetVariety: widgetNames.length,
      };
    }
    return final;
  };
})();
