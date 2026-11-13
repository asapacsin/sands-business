"""Public-data analysis for tasks T09-T12 (property decomposition, hotel KPIs, net-to-gross
reinvestment proxy, share-margin trade-off with peer comparison).

Writes outputs/tables/*.csv, outputs/figures/*.png and outputs/results.json.
Everything here is DESCRIPTIVE or quasi-experimental with weak identification (n = 4 operators
with SEC filings). Nothing in this file is a causal estimate.
"""
from __future__ import annotations

import json
import re
import statistics as st
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PROC, TAB, FIG = ROOT / "data/processed", ROOT / "outputs/tables", ROOT / "outputs/figures"
sys.path.insert(0, str(Path(__file__).parent))
from lvs_extract import to_text  # noqa: E402

PRE = [f"{y}Q{q}" for y, q in [(2023, 3), (2023, 4), (2024, 1), (2024, 2), (2024, 3), (2024, 4), (2025, 1)]]
POST = [f"{y}Q{q}" for y, q in [(2025, 2), (2025, 3), (2025, 4), (2026, 1), (2026, 2), (2026, 3)]]
PROPS = ["Venetian", "Londoner", "Parisian", "Plaza_FourSeasons", "SandsMacao"]
COLORS = {"sands": "#1f4e79", "wynn": "#9aa5b1", "mgm": "#c9a227", "melco": "#7a8b6f",
          "Venetian": "#1f4e79", "Londoner": "#c0504d", "Parisian": "#9bbb59", "Plaza_FourSeasons": "#8064a2", "SandsMacao": "#4bacc6"}


def hold_impacts() -> pd.Series:
    """LVS-reported hold-adjustment impact; read from data/processed/hold_impacts.csv (built from raw by
    extract_hold_impacts) so analysis can run from committed processed data alone."""
    path = PROC / "hold_impacts.csv"
    if not path.exists():
        extract_hold_impacts()
    h = pd.read_csv(path, index_col="period")["hold_adj_impact_usd_m"]
    h.name = "hold_adj_impact"
    return h


def extract_hold_impacts() -> None:
    """LVS-reported impact on Macao Adjusted Property EBITDA of hold-adjusting rolling win % (from raw)."""
    out = {}
    for path in sorted((ROOT / "data/raw/lvs").glob("*_ex991.htm")):
        text = to_text(path).replace("\n", " ")
        m = re.search(r"impact on Adjusted Property EBITDA for hold-adjusted win percentage: \| Three Months Ended \| "
                      r"(March|June|September|December) 3\d, \| (\d{4}) \| \d{4} \| Macao Operations \| \$ \| (\(?[\d,]+\)?|—)", text)
        if m:
            q = {"March": 1, "June": 2, "September": 3, "December": 4}[m.group(1)]
            tok = m.group(3)
            val = 0.0 if tok == "—" else (-1 if tok.startswith("(") else 1) * float(tok.strip("()").replace(",", ""))
            out[f"{m.group(2)}Q{q}"] = val
    pd.DataFrame({"period": list(out), "hold_adj_impact_usd_m": list(out.values()),
                  "source_id": [f"LVS-ER (quarter {k})" for k in out]}).sort_values("period").to_csv(
        PROC / "hold_impacts.csv", index=False)


def main() -> dict:
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(PROC / "sands_panel.csv")
    ops = pd.read_csv(PROC / "operator_quarter.csv")
    total = panel[panel.unit == "SandsMacao5_total"].set_index("period").sort_index()
    props = panel[panel.unit.isin(PROPS)]
    results: dict = {"evidence_label": "DERIVED from LVS-ER, peer ERs, DICJ; descriptive"}

    # ---------- T09 property decomposition ----------
    def yoy(period_now: str, period_prev: str) -> pd.DataFrame:
        a = props[props.period == period_now].set_index("unit")
        b = props[props.period == period_prev].set_index("unit")
        cols = ["net_revenue", "rev_casino", "rev_noncasino", "adj_property_ebitda"]
        d = (a[cols] - b[cols]).add_prefix("d_")
        d["margin_now"], d["margin_prev"] = a.ebitda_margin_pct, b.ebitda_margin_pct
        d["d_margin_pts"] = d.margin_now - d.margin_prev
        # EBITDA bridge: volume effect at prior margin vs margin effect
        d["ebitda_from_revenue_at_prior_margin"] = d.d_net_revenue * b.ebitda_margin_pct / 100
        d["ebitda_from_margin_change"] = a.net_revenue * d.d_margin_pts / 100
        return d.round(1)

    bridge = yoy("2026Q3", "2025Q3")
    bridge.to_csv(TAB / "T3_property_bridge_2026Q3_vs_2025Q3.csv")
    results["bridge_2026Q3"] = bridge[["d_net_revenue", "d_adj_property_ebitda", "d_margin_pts",
                                       "ebitda_from_margin_change"]].to_dict(orient="index")
    margins = props.pivot(index="period", columns="unit", values="ebitda_margin_pct").sort_index()
    margins.round(1).to_csv(TAB / "property_margin_by_quarter.csv")
    pre_m, post_m = margins.loc[PRE].mean(), margins.loc[POST].mean()
    results["property_margin_pre_post"] = pd.DataFrame({"pre": pre_m, "post": post_m, "change": post_m - pre_m}).round(1).to_dict(orient="index")

    fig, ax = plt.subplots(figsize=(8, 4.2))
    for p in PROPS:
        ax.plot(margins.index, margins[p], marker="o", ms=3, label=p, color=COLORS[p])
    ax.axvline(PRE[-1], color="grey", ls="--", lw=0.8)
    ax.text(PRE[-1], ax.get_ylim()[1] * 0.97, " reinvestment push (2Q25)", fontsize=8, color="grey")
    ax.set_ylabel("Adjusted property EBITDA margin (%)")
    ax.set_title("F3. Sands China property EBITDA margins (LVS releases, US GAAP non-GAAP measure)", fontsize=9)
    ax.tick_params(axis="x", rotation=60, labelsize=7)
    ax.legend(fontsize=7, ncol=3)
    fig.tight_layout()
    fig.savefig(FIG / "F3_property_margins.png", dpi=150)
    plt.close(fig)

    mix = props[props.period == "2026Q3"].set_index("unit")
    mix_tab = pd.DataFrame({c: 100 * props[props.period == "2026Q3"].set_index("unit")[c] / mix.net_revenue
                            for c in ["rev_casino", "rev_rooms", "rev_noncasino"]}).round(1)
    mix_tab.to_csv(TAB / "F4_revenue_mix_2026Q3_pct.csv")

    # ---------- T10 hotel KPIs ----------
    hotel = props.pivot(index="period", columns="unit", values="occupancy_pct").sort_index()
    adr = props.pivot(index="period", columns="unit", values="adr").sort_index()
    hotel.to_csv(TAB / "hotel_occupancy_by_quarter.csv")
    adr.to_csv(TAB / "hotel_adr_by_quarter.csv")
    recent = POST
    results["hotel_recent"] = {p: {"occupancy_mean_post": round(hotel.loc[recent, p].mean(), 1),
                                   "occupancy_min_post": round(hotel.loc[recent, p].min(), 1),
                                   "adr_mean_post": round(adr.loc[recent, p].mean(), 0)} for p in PROPS if p in hotel}
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    for p in PROPS:
        ax[0].plot(hotel.index, hotel[p], marker="o", ms=3, label=p, color=COLORS[p])
        ax[1].plot(adr.index, adr[p], marker="o", ms=3, label=p, color=COLORS[p])
    ax[0].set_title("Occupancy %", fontsize=9)
    ax[1].set_title("ADR (US$)", fontsize=9)
    for a in ax:
        a.tick_params(axis="x", rotation=60, labelsize=6)
    ax[0].legend(fontsize=6)
    fig.suptitle("F5. Hotel KPIs by property (LVS releases)", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "F5_hotel_kpis.png", dpi=150)
    plt.close(fig)

    # ---------- T11 net-to-gross gap (reinvestment proxy) ----------
    gap = props.pivot(index="period", columns="unit", values="gap_pct_of_gross_win").sort_index()
    gap["Portfolio"] = total.gap_pct_of_gross_win
    gap.round(1).to_csv(TAB / "net_to_gross_gap_pct.csv")
    pre_gap, post_gap = total.loc[PRE, "gap_pct_of_gross_win"].mean(), total.loc[POST, "gap_pct_of_gross_win"].mean()
    post_gross = total.loc[POST, "gross_win"].sum()
    results["net_to_gross"] = {
        "pre_mean_pct": round(pre_gap, 2), "post_mean_pct": round(post_gap, 2),
        "change_pts": round(post_gap - pre_gap, 2),
        "post_period_gross_win_usd_m": round(post_gross, 0),
        "implied_extra_deductions_usd_m_post_period": round((post_gap - pre_gap) / 100 * post_gross, 0),
        "implied_extra_deductions_usd_m_annualised": round((post_gap - pre_gap) / 100 * post_gross / len(POST) * 4, 0),
        "caveat": "Gap = implied gross win minus net casino revenue. It contains rebates, commissions, discounts, "
                  "loyalty deferrals and comps allocated to other departments - not promotions alone. Gross win is "
                  "approximated from drop x win% (LVS 'non-rolling win %' is calculated on drop).",
        "by_property_pre_post": {p: [round(gap.loc[PRE, p].mean(), 1), round(gap.loc[POST, p].mean(), 1)] for p in PROPS},
    }

    # ---------- T12 share-margin trade-off and peer comparison ----------
    holds = hold_impacts()
    total = total.join(holds)
    total["ebitda_hold_adj"] = total.adj_property_ebitda + total.hold_adj_impact.fillna(0)
    total["margin_hold_adj"] = 100 * total.ebitda_hold_adj / total.net_revenue
    total[["net_revenue", "adj_property_ebitda", "ebitda_margin_pct", "hold_adj_impact", "margin_hold_adj",
           "mass_share_pct_derived", "ggr_share_pct_derived", "gap_pct_of_gross_win", "market_mass_usd_m"]].round(2).to_csv(TAB / "sands_portfolio_quarterly.csv")

    m = ops.pivot(index="period", columns="operator", values="margin_pct").sort_index()

    def did(pre: list[str], post: list[str], donors: list[str], col: str = "sands") -> float:
        d_sands = m.loc[post, col].mean() - m.loc[pre, col].mean()
        d_peer = st.mean(m.loc[post, d].mean() - m.loc[pre, d].mean() for d in donors)
        return d_sands - d_peer

    donors = ["wynn", "mgm", "melco"]
    main_did = did(PRE, POST, donors)
    loo = {f"without_{d}": round(did(PRE, POST, [x for x in donors if x != d]), 2) for d in donors}
    placebo = {}
    allq = list(m.index)
    for fake in ["2024Q2", "2024Q3", "2024Q4"]:
        i = allq.index(fake)
        placebo[fake] = round(did(allq[max(0, i - 4):i], allq[i:allq.index("2025Q2")], donors), 2)
    m_hold = m.copy()
    m_hold["sands"] = total.margin_hold_adj
    d_hold = (m_hold.loc[POST, "sands"].mean() - m_hold.loc[PRE, "sands"].mean()) - st.mean(
        m.loc[POST, d].mean() - m.loc[PRE, d].mean() for d in donors)
    results["margin_did"] = {
        "definition": "Change in mean EBITDA(R) margin, post (2025Q2-2026Q3) minus pre (2023Q3-2025Q1); Sands minus mean of peers",
        "sands_change_pts": round(m.loc[POST, "sands"].mean() - m.loc[PRE, "sands"].mean(), 2),
        "peer_changes_pts": {d: round(m.loc[POST, d].mean() - m.loc[PRE, d].mean(), 2) for d in donors},
        "did_pts": round(main_did, 2), "did_hold_adjusted_sands_pts": round(d_hold, 2),
        "leave_one_out": loo,
        "did_excluding_2026Q2_pts": round(did(PRE, [q for q in POST if q != "2026Q2"], donors), 2),
        "hold_adjustment_available_quarters": sorted(holds.index.tolist()), "placebo_did_pts": placebo,
        "identification": "Weak: 3 donors with different EBITDA vs EBITDAR definitions; treatment coincides with "
                          "Londoner room-inventory return (mid-2025) and satellite-casino closures (end-2025).",
    }

    base = "2025Q1"
    tradeoff = []
    for q in POST:
        d_share = total.loc[q, "mass_share_pct_derived"] - total.loc[base, "mass_share_pct_derived"]
        d_margin_rel = (m.loc[q, "sands"] - m.loc[base, "sands"]) - st.mean(m.loc[q, d] - m.loc[base, d] for d in donors)
        tradeoff.append({"period": q, "d_mass_share_index_pts": round(d_share, 2),
                         "d_margin_vs_peers_pts": round(d_margin_rel, 2),
                         "d_margin_hold_adj_vs_peers_pts": round((total.loc[q, "margin_hold_adj"] - total.loc[base, "margin_hold_adj"]) - st.mean(m.loc[q, d] - m.loc[base, d] for d in donors), 2),
                         "d_gap_pts": round(total.loc[q, "gap_pct_of_gross_win"] - total.loc[base, "gap_pct_of_gross_win"], 2)})
    pd.DataFrame(tradeoff).to_csv(TAB / "share_margin_tradeoff_vs_2025Q1.csv", index=False)
    results["tradeoff_vs_2025Q1"] = tradeoff

    fig, ax1 = plt.subplots(figsize=(8, 4.2))
    ax1.plot(total.index, total.mass_share_pct_derived, color="#1f4e79", marker="o", ms=3, label="Sands mass win share (derived index, %)")
    ax1.plot(total.index, total.ggr_share_pct_derived, color="#1f4e79", ls=":", marker="o", ms=3, label="Sands total GGR share (derived, %)")
    ax1.set_ylabel("Share of Macao GGR (%)")
    ax2 = ax1.twinx()
    for op in ["sands"] + donors:
        ax2.plot(m.index, m[op], color=COLORS[op], lw=1.6 if op == "sands" else 1, ls="-" if op == "sands" else "--",
                 label=f"{op} margin %")
    ax2.set_ylabel("EBITDA(R) margin (%)")
    ax1.axvline(PRE[-1], color="grey", ls="--", lw=0.8)
    ax1.tick_params(axis="x", rotation=60, labelsize=7)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, fontsize=6, loc="lower left", ncol=2)
    ax1.set_title("F1. Sands share (derived from LVS volumes / DICJ) vs operator margins", fontsize=9)
    fig.tight_layout()
    fig.savefig(FIG / "F1_share_vs_margin.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 3.8))
    for p in PROPS + ["Portfolio"]:
        ax.plot(gap.index, gap[p], marker="o", ms=3, lw=2 if p == "Portfolio" else 1,
                color="black" if p == "Portfolio" else COLORS[p], label=p)
    ax.axvline(PRE[-1], color="grey", ls="--", lw=0.8)
    ax.set_ylabel("% of implied gross win")
    ax.set_title("F2. Net-to-gross gap: implied gross win not booked as casino revenue (reinvestment proxy)", fontsize=9)
    ax.tick_params(axis="x", rotation=60, labelsize=7)
    ax.legend(fontsize=6, ncol=3)
    fig.tight_layout()
    fig.savefig(FIG / "F2_net_to_gross_gap.png", dpi=150)
    plt.close(fig)

    results["latest"] = {"period": "2026Q3", **total.loc["2026Q3", ["net_revenue", "adj_property_ebitda", "ebitda_margin_pct",
                                                                    "margin_hold_adj", "mass_share_pct_derived",
                                                                    "ggr_share_pct_derived", "gap_pct_of_gross_win",
                                                                    "market_mass_usd_m"]].round(2).to_dict()}
    (ROOT / "outputs/results.json").write_text(json.dumps(results, indent=2, default=float))
    return results


if __name__ == "__main__":
    r = main()
    print(json.dumps({k: r[k] for k in ("net_to_gross", "margin_did", "latest")}, indent=1, default=float))
    print(json.dumps(r["property_margin_pre_post"], indent=0))
    print(json.dumps(r["hotel_recent"]))
    print(json.dumps(r["tradeoff_vs_2025Q1"]))
