"""Build the Sands property-quarter analysis panel and derived market-share series.

All derived quantities are labelled DERIVED and computed only from:
  - LVS earnings releases (property gaming volumes, win rates, revenues, EBITDA, hotel KPIs)
  - DICJ quarterly GGR by game type
FX: DICJ states 1 HKD = 1.03 MOP; HKD is pegged in the 7.75-7.85 band to USD. We use
MOP_PER_USD = 7.80 * 1.03 = 8.034 (documented assumption; sensitivity < 1% for the band).
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
MOP_PER_USD = 7.80 * 1.03
PROPS = ["Venetian", "Londoner", "Parisian", "Plaza_FourSeasons", "SandsMacao"]
TREATMENT_START = "2025Q2"  # reinvestment increase announced on the Q2 2025 call (from late April 2025)


def load_property() -> dict:
    data = defaultdict(dict)
    for r in csv.DictReader(open(PROC / "property_quarter.csv")):
        if r["basis"] == "reported":
            data[(r["property"], r["period"])][r["metric"]] = float(r["value"])
    return data


def load_market() -> dict:
    market = defaultdict(dict)
    for r in csv.DictReader(open(PROC / "market_quarter.csv")):
        market[r["period"]][r["item"]] = float(r["value_mop_m"])
    out = {}
    for period, items in market.items():
        total = sum(items.values())
        vip = items.get("VIP Baccarat", 0.0)
        out[period] = {"market_ggr_usd_m": total / MOP_PER_USD,
                       "market_vip_usd_m": vip / MOP_PER_USD,
                       "market_mass_usd_m": (total - vip) / MOP_PER_USD}
    return out


def property_row(p: dict) -> dict:
    g = lambda k: p.get(k, 0.0)
    rolling_win = g("rolling_volume") * g("rolling_win_pct") / 100
    table_mass_win = g("nonrolling_drop") * g("nonrolling_win_pct") / 100
    slot_win = g("slot_handle") * g("slot_hold_pct") / 100
    mass_win = table_mass_win + slot_win
    gross_win = rolling_win + mass_win
    return {
        "net_revenue": g("net_revenue"), "adj_property_ebitda": g("adj_property_ebitda"),
        "rev_casino": g("rev_casino"), "rev_rooms": g("rev_rooms"),
        "rev_noncasino": g("net_revenue") - g("rev_casino"),
        "rolling_win": rolling_win, "mass_table_win": table_mass_win, "slot_win": slot_win,
        "mass_win": mass_win, "gross_win": gross_win,
        "net_to_gross_gap": gross_win - g("rev_casino"),
        "nonrolling_drop": g("nonrolling_drop"), "nonrolling_win_pct": g("nonrolling_win_pct"),
        "rolling_volume": g("rolling_volume"), "rolling_win_pct": g("rolling_win_pct"),
        "occupancy_pct": p.get("occupancy_pct"), "adr": p.get("adr"), "revpar": p.get("revpar"),
    }


def build() -> list[dict]:
    prop, market = load_property(), load_market()
    periods = sorted({period for _, period in prop if period in market})
    rows = []
    for period in periods:
        total = defaultdict(float)
        for name in PROPS:
            if (name, period) not in prop:
                continue
            r = property_row(prop[(name, period)])
            for k, v in r.items():
                if v is not None and k not in ("occupancy_pct", "adr", "revpar", "nonrolling_win_pct", "rolling_win_pct"):
                    total[k] += v
            rows.append({"period": period, "unit": name, **r})
        m = market[period]
        t = dict(total)
        t["nonrolling_win_pct"] = 100 * t["mass_table_win"] / t["nonrolling_drop"] if t["nonrolling_drop"] else None
        t["rolling_win_pct"] = 100 * t["rolling_win"] / t["rolling_volume"] if t["rolling_volume"] else None
        rows.append({"period": period, "unit": "SandsMacao5_total", **t, **m,
                     "mass_share_pct_derived": 100 * t["mass_win"] / m["market_mass_usd_m"],
                     "ggr_share_pct_derived": 100 * t["gross_win"] / m["market_ggr_usd_m"]})
    for r in rows:
        r["ebitda_margin_pct"] = 100 * r["adj_property_ebitda"] / r["net_revenue"] if r["net_revenue"] else None
        r["gap_pct_of_gross_win"] = 100 * r["net_to_gross_gap"] / r["gross_win"] if r["gross_win"] else None
        r["post_treatment"] = int(r["period"] >= TREATMENT_START)
        r["evidence_label"] = "DERIVED (LVS-ER + DICJ)"
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("period", "unit"), k))
    with (PROC / "sands_panel.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    for r in build():
        if r["unit"] == "SandsMacao5_total":
            print(r["period"], f"rev {r['net_revenue']:.0f} ebitda {r['adj_property_ebitda']:.0f} "
                  f"margin {r['ebitda_margin_pct']:.1f}% mass_share {r['mass_share_pct_derived']:.1f}% "
                  f"ggr_share {r['ggr_share_pct_derived']:.1f}% gap {r['gap_pct_of_gross_win']:.1f}% "
                  f"mkt_mass {r['market_mass_usd_m']:.0f}")
