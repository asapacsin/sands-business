"""Decision simulation (spec §8.4): allocate the incremental reinvestment pool across
property x tier cells with diminishing-returns response curves.

ALL RESPONSE PARAMETERS ARE ILLUSTRATIVE. Outputs are not Sands forecasts. The model shows how the
decision depends on assumptions and which assumptions flip the conclusion.
"""
from __future__ import annotations

import copy
import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROPS = ["Venetian", "Londoner", "Parisian", "Plaza_FourSeasons", "SandsMacao"]


def base_params() -> dict:
    a = json.loads((ROOT / "model/assumptions.json").read_text())
    r = json.loads((ROOT / "outputs/results.json").read_text())
    panel = pd.read_csv(ROOT / "data/processed/sands_panel.csv")
    recent = panel[(panel.unit.isin(PROPS)) & (panel.period.isin(["2025Q4", "2026Q1", "2026Q2", "2026Q3"]))]
    mass = recent.groupby("unit").mass_win.sum()
    return {
        "pool": r["net_to_gross"]["implied_extra_deductions_usd_m_annualised"],  # DERIVED, US$m/yr
        "property_weight": (mass / mass.sum()).to_dict(),                          # DERIVED
        "tiers": a["tiers"]["value"],                                             # ILLUSTRATIVE
        "pool_avg_ggr_per_dollar": 2.0,  # ILLUSTRATIVE: average exactly at break-even (anchor range 0.72-4.28)
        "dispersion": 1.0, "b": a["curvature_b"]["value"],
        "tau": a["tau_gaming_tax"]["value"], "v": a["v_variable_cost_share"]["value"],
        "promo_tax_deductible": False,
    }


def cells(p: dict) -> list[dict]:
    """Cell response: dGGR(x) = A (1 - exp(-b x / x0)); A set so that dGGR(x0)/x0 = multiple."""
    tiers = p["tiers"]
    raw = {t: v["response_multiple_at_current"] for t, v in tiers.items()}
    mean = sum(tiers[t]["pool_share"] * raw[t] for t in tiers)
    out = []
    for prop, w in p["property_weight"].items():
        for t, v in tiers.items():
            rel = 1 + p["dispersion"] * (raw[t] / mean - 1)          # dispersion scales spread around 1
            multiple = max(p["pool_avg_ggr_per_dollar"] * rel, 0.0)
            x0 = p["pool"] * w * v["pool_share"]
            A = multiple * x0 / (1 - math.exp(-p["b"]))
            out.append({"property": prop, "tier": t, "x0": x0, "A": A})
    return out


def ggr(cell: dict, x: float, b: float) -> float:
    return cell["A"] * (1 - math.exp(-b * x / cell["x0"])) if cell["x0"] > 0 else 0.0


def contribution(cs: list[dict], xs: list[float], p: dict) -> float:
    promo_net = (1 - p["tau"]) if p["promo_tax_deductible"] else 1.0
    return sum(ggr(c, x, p["b"]) * (1 - p["tau"] - p["v"]) - x * promo_net for c, x in zip(cs, xs))


def optimal(cs: list[dict], p: dict, budget: float, steps: int = 4000) -> list[float]:
    """Greedy equimarginal allocation (concave curves => optimal) under a fixed budget."""
    xs, dx = [0.0] * len(cs), budget / steps
    for _ in range(steps):
        gains = [ggr(c, x + dx, p["b"]) - ggr(c, x, p["b"]) for c, x in zip(cs, xs)]
        i = max(range(len(cs)), key=gains.__getitem__)
        xs[i] += dx
    return xs


def marginal_ggr_per_dollar(cs, xs, p):
    return [c["A"] * p["b"] / c["x0"] * math.exp(-p["b"] * x / c["x0"]) for c, x in zip(cs, xs)]


def scenario(p: dict, realloc: float) -> dict:
    cs = cells(p)
    bau = [c["x0"] for c in cs]
    opt = optimal(cs, p, sum(bau))
    xs = [(1 - realloc) * b + realloc * o for b, o in zip(bau, opt)]
    g_bau = sum(ggr(c, x, p["b"]) for c, x in zip(cs, bau))
    g_new = sum(ggr(c, x, p["b"]) for c, x in zip(cs, xs))
    return {"contribution_bau": contribution(cs, bau, p), "contribution": contribution(cs, xs, p),
            "delta_vs_bau": contribution(cs, xs, p) - contribution(cs, bau, p),
            "ggr_bau": g_bau, "ggr": g_new, "share_guardrail_ok": g_new >= g_bau - 1e-6,
            "allocation": {f"{c['property']}|{c['tier']}": round(x, 2) for c, x in zip(cs, xs)}}


SCENARIOS = {  # name: (reallocation fraction, dispersion multiplier)  — all ILLUSTRATIVE
    "baseline_bau": (0.0, 1.0),
    "conservative": (0.10, 0.5),
    "expected": (0.20, 1.0),
    "optimistic": (0.30, 1.5),
}


def run() -> dict:
    base = base_params()
    results = {"label": "ILLUSTRATIVE - not Sands forecasts", "pool_usd_m_yr": round(base["pool"], 1),
               "property_weight": {k: round(v, 3) for k, v in base["property_weight"].items()}, "scenarios": {}}
    for name, (realloc, disp) in SCENARIOS.items():
        p = dict(base, dispersion=disp)
        s = scenario(p, realloc)
        results["scenarios"][name] = {k: (round(v, 1) if isinstance(v, float) else v) for k, v in s.items() if k != "allocation"}
        results["scenarios"][name]["reallocation_fraction"] = realloc
        results["scenarios"][name]["dispersion"] = disp
    cs = cells(base)
    bau = [c["x0"] for c in cs]
    mg = marginal_ggr_per_dollar(cs, bau, base)
    k_star = 1 / (1 - base["tau"] - base["v"])
    results["marginal_at_bau"] = {f"{c['property']}|{c['tier']}": round(m, 2) for c, m in zip(cs, mg)}
    results["cells_below_break_even_at_bau"] = sum(m < k_star for m in mg)
    results["break_even_multiple"] = round(k_star, 2)

    # budget-level question: where is total pool marginal return = k*? (expected dispersion)
    budgets = [base["pool"] * f for f in [0.25, 0.5, 0.75, 1.0, 1.25]]
    curve = []
    for B in budgets:
        xs = optimal(cs, base, B, steps=1500)
        curve.append({"pool_fraction": round(B / base["pool"], 2), "contribution": round(contribution(cs, xs, base), 1)})
    results["optimal_pool_curve"] = curve

    # sensitivity: expected scenario delta and BAU level; one-at-a-time swings
    swings = {"tau": ("tau", 0.35, 0.40), "v": ("v", 0.05, 0.20),
              "pool_avg_ggr_per_dollar": ("pool_avg_ggr_per_dollar", 0.72, 4.28),
              "curvature_b": ("b", 0.5, 3.0), "tier_dispersion": ("dispersion", 0.5, 1.5),
              "promo_tax_deductible": ("promo_tax_deductible", False, True)}
    sens = []
    for label, (key, lo, hi) in swings.items():
        row = {"parameter": label, "low": lo, "high": hi}
        for side, val in (("low", lo), ("high", hi)):
            p = dict(base)
            p[key] = val
            s = scenario(p, 0.20)
            row[f"delta_{side}"] = round(s["delta_vs_bau"], 1)
            row[f"bau_level_{side}"] = round(s["contribution_bau"], 1)
        sens.append(row)
    results["sensitivity"] = sens
    results["sign_flips_bau_level"] = [r["parameter"] for r in sens if (r["bau_level_low"] > 0) != (r["bau_level_high"] > 0)]
    (ROOT / "outputs/scenario_results.json").write_text(json.dumps(results, indent=2))
    pd.DataFrame(sens).to_csv(ROOT / "outputs/tables/sensitivity_tornado.csv", index=False)

    # figures
    fig, ax = plt.subplots(figsize=(7, 3.6))
    names = list(results["scenarios"])
    vals = [results["scenarios"][n]["delta_vs_bau"] for n in names]
    ax.bar(names, vals, color=["#9aa5b1", "#c9d6e3", "#1f4e79", "#7a9cc6"])
    for i, v in enumerate(vals):
        ax.text(i, v, f"{v:.0f}", ha="center", va="bottom", fontsize=8)
    ax.set_ylabel("Δ contribution vs BAU (US$m/yr)")
    ax.set_title("F7. Reallocation scenarios — ILLUSTRATIVE, not Sands forecasts", fontsize=9)
    fig.tight_layout()
    fig.savefig(ROOT / "outputs/figures/F7_scenarios.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    order = sorted(sens, key=lambda r: abs(r["bau_level_high"] - r["bau_level_low"]))
    for i, r in enumerate(order):
        lo, hi = r["bau_level_low"], r["bau_level_high"]
        ax.barh(i, hi - lo, left=min(lo, hi) if hi >= lo else hi, color="#1f4e79" if hi >= lo else "#c0504d")
        ax.barh(i, 0)
    ax.set_yticks(range(len(order)), [f"{r['parameter']} ({r['low']}→{r['high']})" for r in order], fontsize=7)
    base_bau = results["scenarios"]["baseline_bau"]["contribution_bau"]
    ax.axvline(base_bau, color="black", lw=0.8)
    ax.axvline(0, color="grey", ls="--", lw=0.8)
    ax.set_xlabel("Net contribution of incremental reinvestment pool at BAU (US$m/yr)")
    ax.set_title("F8. Sensitivity: which assumptions flip the sign (ILLUSTRATIVE)", fontsize=9)
    fig.tight_layout()
    fig.savefig(ROOT / "outputs/figures/F8_tornado.png", dpi=150)
    plt.close(fig)

    tau_grid = [0.35, 0.37, 0.39, 0.40]
    fig, ax = plt.subplots(figsize=(6, 3.4))
    for vv in (0.05, 0.10, 0.20):
        ax.plot(tau_grid, [1 / (1 - t - vv) for t in tau_grid], marker="o", label=f"v={vv}, promo not deductible")
        ax.plot(tau_grid, [(1 - t) / (1 - t - vv) for t in tau_grid], ls="--", label=f"v={vv}, promo deductible")
    ax.axhline(1, color="grey", lw=0.6)
    ax.set_xlabel("Effective gaming tax rate τ")
    ax.set_ylabel("Break-even incremental GGR per $1")
    ax.set_title("F6. Break-even multiple k* (DERIVED formula)", fontsize=9)
    ax.legend(fontsize=6)
    fig.tight_layout()
    fig.savefig(ROOT / "outputs/figures/F6_break_even.png", dpi=150)
    plt.close(fig)
    return results


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: r[k] for k in ("pool_usd_m_yr", "scenarios", "cells_below_break_even_at_bau",
                                         "optimal_pool_curve", "sign_flips_bau_level", "sensitivity")}, indent=1))
