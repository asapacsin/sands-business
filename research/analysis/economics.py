"""Unit economics of reinvestment (spec §8.3) and the public-data return anchor (§8.4)."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def break_even_multiple(tau: float, v: float, promo_reduces_taxable_ggr: bool = False) -> float:
    """Incremental GGR needed per $1 of reinvestment for zero incremental contribution.

    If promotional play reduces taxable GGR, each $1 of promotion also saves tau of tax,
    so its net cost is (1 - tau)."""
    if not 0 <= tau < 1 or not 0 <= v < 1 or tau + v >= 1:
        raise ValueError("need 0 <= tau, v and tau + v < 1")
    promo_cost = (1 - tau) if promo_reduces_taxable_ggr else 1.0
    return promo_cost / (1 - tau - v)


def incremental_contribution(d_ggr: float, promo_cost: float, tau: float, v: float,
                             d_noncasino: float = 0.0, m_noncasino: float = 0.0,
                             room_opportunity_cost: float = 0.0) -> float:
    """ΔΠ = ΔGGR·(1 − τ − v) + ΔNG·m_NG − C_promo − OC_room  (rebates/commissions inside C_promo)."""
    return d_ggr * (1 - tau - v) + d_noncasino * m_noncasino - promo_cost - room_opportunity_cost


def comp_room_opportunity_cost(p_sellout: float, adr_cash: float, c_var: float) -> float:
    """OC = P(sellout)·(ADR − c_var) + (1 − P)·c_var  (displaced cash margin when full, else marginal cost)."""
    if not 0 <= p_sellout <= 1:
        raise ValueError("p_sellout must be in [0, 1]")
    return p_sellout * max(adr_cash - c_var, 0.0) + (1 - p_sellout) * c_var


def mroi(d_contribution_before_promo: float, promo_cost: float) -> float:
    return d_contribution_before_promo / promo_cost if promo_cost else math.inf


def public_anchor(results: dict, assumptions: dict) -> dict:
    """Average return on the post-2Q25 reinvestment increase implied by public data (DERIVED, not causal)."""
    tau, v = assumptions["tau_gaming_tax"]["value"], assumptions["v_variable_cost_share"]["value"]
    mass_q = results["latest"]["market_mass_usd_m"]
    cost_year = results["net_to_gross"]["implied_extra_deductions_usd_m_annualised"]
    out = {}
    for label, share_pts in (("company_definition", assumptions["share_gain_pts_company_definition"]["value"]),
                             ("derived_index", results["tradeoff_vs_2025Q1"][-1]["d_mass_share_index_pts"])):
        for attribution in (1.0, 0.5, 0.3):
            d_ggr_year = share_pts / 100 * mass_q * 4 * attribution
            contrib = d_ggr_year * (1 - tau - v)
            out[f"{label}_attr{attribution}"] = {
                "share_gain_pts": round(share_pts, 2), "attribution": attribution,
                "incremental_ggr_usd_m_yr": round(d_ggr_year), "contribution_before_promo_usd_m_yr": round(contrib),
                "incremental_deductions_usd_m_yr": round(cost_year),
                "average_return_multiple": round(contrib / cost_year, 2),
                "net_contribution_usd_m_yr": round(contrib - cost_year)}
    return out


if __name__ == "__main__":
    a = json.loads((ROOT / "model/assumptions.json").read_text())
    r = json.loads((ROOT / "outputs/results.json").read_text())
    anchor = public_anchor(r, a)
    k = {f"tau{t}_v{vv}_promoTaxDeductible{p}": round(break_even_multiple(t, vv, p), 2)
         for t in (0.35, 0.40) for vv in (0.05, 0.10, 0.20) for p in (False, True)}
    rooms = {p: round(comp_room_opportunity_cost(a["p_sellout_by_property"]["value"][p], adr, a["comp_room_variable_cost_usd"]["value"]), 0)
             for p, adr in {pp: r["hotel_recent"][pp]["adr_mean_post"] for pp in r["hotel_recent"]}.items()}
    out = {"label": "DERIVED + ILLUSTRATIVE; average (not marginal) returns; not causal",
           "break_even_multiple": k, "public_anchor": anchor, "comp_room_opportunity_cost_usd_per_night": rooms}
    (ROOT / "outputs/economics.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))
