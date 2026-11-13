"""Analysis pipeline for the randomised reinvestment holdout (spec §8.6, task T20).

Runs on SYNTHETIC data only. With Sands internal data it would take one row per rated player:
stratum, arm, pre-period theo, test-period theo, reinvestment cost, visits, rg_flag.

Estimator: stratified difference in means with CUPED adjustment (pre-period theo covariate);
outcome = incremental contribution per player = Δtheo·(1−τ−v) − Δreinvestment cost.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
Z90 = 1.6448536269514722


def simulate(n_per_stratum: int = 4000, n_strata: int = 6, true_lift_ggr: float = 30.0,
             offer_saving: float = 40.0, seed: int = 0) -> dict:
    """SYNTHETIC. Arm B = reduced offer: saves `offer_saving` per player, loses `true_lift_ggr` theo."""
    rng = np.random.default_rng(seed)
    strata, arm, pre, post, cost = [], [], [], [], []
    for s in range(n_strata):
        scale = 400 * (1 + s)                      # strata by baseline value decile group
        pre_s = rng.gamma(1.5, scale / 1.5, n_per_stratum)
        assign = rng.random(n_per_stratum) < 0.10  # 10% holdout to reduced offer
        noise = rng.normal(0, 0.35 * scale, n_per_stratum)
        post_s = 0.8 * pre_s + 0.2 * scale + noise - assign * true_lift_ggr
        base_cost = 0.12 * pre_s
        strata += [s] * n_per_stratum
        arm += list(assign.astype(int))
        pre += list(pre_s)
        post += list(post_s)  # no clipping: clipping at 0 biases large effects
        cost += list(base_cost - assign * offer_saving)
    return {k: np.asarray(v) for k, v in dict(stratum=strata, arm=arm, pre=pre, post=post, cost=cost).items()}


def estimate(d: dict, tau: float = 0.40, v: float = 0.10) -> dict:
    """Effect of the REDUCED offer vs current, per player: contribution = theo·(1−τ−v) − cost."""
    y = d["post"] * (1 - tau - v) - d["cost"]
    x = d["pre"] * (1 - tau - v)
    effects, variances, weights = [], [], []
    for s in np.unique(d["stratum"]):
        m = d["stratum"] == s
        ys, xs, a = y[m], x[m], d["arm"][m]
        theta = np.cov(ys, xs)[0, 1] / np.var(xs, ddof=1)       # CUPED coefficient
        adj = ys - theta * (xs - xs.mean())
        t, c = adj[a == 1], adj[a == 0]
        effects.append(t.mean() - c.mean())
        variances.append(t.var(ddof=1) / len(t) + c.var(ddof=1) / len(c))
        weights.append(m.sum())
    w = np.asarray(weights) / sum(weights)
    eff = float(np.sum(w * effects))
    se = float(math.sqrt(np.sum(w ** 2 * np.asarray(variances))))
    return {"effect_per_player": eff, "se": se, "ci90": (eff - Z90 * se, eff + Z90 * se)}


def decision(est: dict) -> str:
    """Pre-declared rule (spec §8.6): adopt the reduced/reallocated offer only if the 90% CI lower bound > 0."""
    return "ADOPT" if est["ci90"][0] > 0 else "DO_NOT_ADOPT"


def mde(sd: float, n_treat: int, n_control: int, alpha_z: float = Z90, power_z: float = 0.8416) -> float:
    """Minimum detectable effect for a two-arm comparison (one-sided 5% / 80% power by default)."""
    return (alpha_z + power_z) * sd * math.sqrt(1 / n_treat + 1 / n_control)


def coverage(runs: int = 200, **kw) -> dict:
    tau, v = 0.40, 0.10
    true = kw.get("offer_saving", 40.0) - kw.get("true_lift_ggr", 30.0) * (1 - tau - v)
    hits, adopt = 0, 0
    for seed in range(runs):
        e = estimate(simulate(seed=seed, **kw), tau, v)
        hits += e["ci90"][0] <= true <= e["ci90"][1]
        adopt += decision(e) == "ADOPT"
    return {"true_effect": true, "ci90_coverage": hits / runs, "adopt_rate": adopt / runs, "runs": runs}


if __name__ == "__main__":
    out = {"label": "SYNTHETIC DATA — demonstrates the pipeline only",
           "single_run": {k: (list(v) if isinstance(v, tuple) else v) for k, v in estimate(simulate(seed=1)).items()},
           "coverage_reduced_offer_profitable": coverage(runs=500),
           "coverage_reduced_offer_unprofitable": coverage(runs=500, true_lift_ggr=120.0),
           "mde_example": round(mde(sd=500.0, n_treat=2400, n_control=21600), 2)}
    (ROOT / "outputs/holdout_synthetic_demo.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))
