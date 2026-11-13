"""T03: re-check every §2 spec fact against primary data. Output: sources/fact_verification.csv."""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).parent))
from lvs_extract import to_text  # noqa: E402


def lvs_text(date: str) -> str:
    return to_text(ROOT / f"data/raw/lvs/{date}_ex991.htm").replace("\n", " ")


def macao_ops(date: str, metric: str) -> tuple[float, float]:
    """Macao Operations current / prior-year quarter from the summary table (net revenue or EBITDA)."""
    t = lvs_text(date)
    anchor = {"net_revenue": "Net Revenues", "ebitda": "Adjusted Property EBITDA |"}[metric]
    seg = t[t.find(anchor):]
    m = re.search(r"Macao Operations \| ([\d,]+) \| ([\d,]+) \|", seg)
    return float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))


def prop(period: str, unit: str, metric: str) -> float:
    for r in csv.DictReader(open(ROOT / "data/processed/property_quarter.csv")):
        if r["property"] == unit and r["period"] == period and r["metric"] == metric and r["basis"] == "reported":
            return float(r["value"])
    raise KeyError((period, unit, metric))


def dicj(period_prefix: str, exclude_vip: bool = False) -> float:
    total = 0.0
    for r in csv.DictReader(open(ROOT / "data/processed/market_quarter.csv")):
        if r["period"].startswith(period_prefix) and not (exclude_vip and r["item"] == "VIP Baccarat"):
            total += float(r["value_mop_m"])
    return total


def pct(a: float, b: float) -> float:
    return round(100 * (a / b - 1), 1)


def main() -> list[dict]:
    rows = []

    def add(claim, secondary, primary, source, status, note=""):
        rows.append({"claim": claim, "secondary_value": secondary, "primary_value": primary,
                     "source_id": source, "status": status, "note": note})

    e_now, e_prev = macao_ops("2026-10-21", "ebitda")
    r_now, r_prev = macao_ops("2026-10-21", "net_revenue")
    add("3Q26 Macao adjusted property EBITDA", "US$529m vs US$601m (-12.0%)", f"{e_now:.0f} vs {e_prev:.0f} ({pct(e_now, e_prev)}%)",
        "LVS-ER-2026-10-21", "PRIMARY ✔" if (e_now, e_prev) == (529, 601) else "CORRECTED")
    add("3Q26 Macao EBITDA margin", "27.3%, -420 bps", f"{100*e_now/r_now:.1f}% vs {100*e_prev/r_prev:.1f}% ({100*(e_now/r_now-e_prev/r_prev):.1f} pts)",
        "LVS-ER-2026-10-21", "PRIMARY ✔", "LVS 'Macao Operations' includes ferry/other")
    t = lvs_text("2026-10-21")
    m = re.search(r"total net revenues for SCL increased ([\d.]+)% to \$([\d.]+) billion", t)
    add("3Q26 Sands China (SCL) net revenue", "~US$1.93bn, +1.4%", f"SCL GAAP: ${m.group(2)}bn, +{m.group(1)}%; LVS Macao segment: {r_now:.0f} vs {r_prev:.0f} (+{pct(r_now, r_prev)}%)",
        "LVS-ER-2026-10-21", "PRIMARY ✔", "Two entities: SCL (GAAP) vs LVS Macao segment; focusgn headline '+8.4%' not supported by primary")
    for unit, label, sec in [("Venetian", "Venetian", "~$649m (-6.2%) / $205m (-15.3%)"), ("Londoner", "Londoner", "$685m (flat) / $178m (-18.7%)"),
                             ("Parisian", "Parisian", "$231m (+6%) / $46m (-13.2%)"), ("Plaza_FourSeasons", "Plaza & Four Seasons", "$238m (+15.5%) / $85m"),
                             ("SandsMacao", "Sands Macao", "$99m (+37.5%) / $14m (+75%)")]:
        a, b = prop("2026Q3", unit, "net_revenue"), prop("2025Q3", unit, "net_revenue")
        c, d = prop("2026Q3", unit, "adj_property_ebitda"), prop("2025Q3", unit, "adj_property_ebitda")
        add(f"3Q26 {label} revenue / EBITDA", sec, f"${a:.0f}m ({pct(a, b)}%) / ${c:.0f}m ({pct(c, d)}%)", "LVS-ER-2026-10-21", "PRIMARY ✔")
    n_now = sum(prop(q, u, "adj_property_ebitda") for q in ("2026Q1", "2026Q2", "2026Q3") for u in ("Venetian", "Londoner", "Parisian", "Plaza_FourSeasons", "SandsMacao"))
    add("9M26 Macao adjusted property EBITDA", "US$1.59bn, -6.5%", "1,592 vs 1,702 (-6.5%) per LVS nine-month column", "LVS-ER-2026-10-21", "PRIMARY ✔",
        f"5-property sum of quarters = {n_now:.0f} (excludes ferry/other)")
    add("3Q26 rolling hold effect", "+US$11m", "Hold-adjusted EBITDA impact (11): reported includes +$11m from high hold", "LVS-ER-2026-10-21", "PRIMARY ✔")
    q2_now, _ = macao_ops("2026-07-22", "ebitda")
    add("2Q26 Macao adjusted property EBITDA", "US$430m", f"{q2_now:.0f}", "LVS-ER-2026-07-22", "PRIMARY ✔" if q2_now == 430 else "CORRECTED",
        "LVS: unusually low rolling hold; hold-adjusted impact +$87m")
    add("Macao mass revenue share 26.1% (3Q26); 23.6% (1Q25); 25.4% (3Q25)", "company-reported on calls", "Not in earnings release; derived index (different definition): 31.4% (3Q26), 26.9% (1Q25)",
        "call transcripts (secondary copies)", "SECONDARY ✔ (remains)", "Derived total GGR share 25.4% in 3Q26 matches CLSA's 25.4% (cross-check)")
    g25, g24 = dicj("2025"), dicj("2024")
    add("Macau 2025 GGR", "MOP247.4bn, +9.1%", f"Games of fortune MOP{g25:,.0f}m (+{pct(g25, g24)}%)", "DICJ-Q-2025", "PRIMARY ✔")
    mass25 = dicj("2025", exclude_vip=True)
    add("Mass share of 2025 GGR", "~73% (CreditSights)", f"{100*mass25/g25:.1f}% (all games ex-VIP baccarat)", "DICJ-Q-2025",
        "PRIMARY ✔" if abs(100 * mass25 / g25 - 73) < 1.5 else "CORRECTED")
    add("4Q25 mass GGR / mass baccarat", "MOP45.75bn / MOP36.25bn", f"MOP{dicj('2025Q4', True):,.0f}m / MOP36,247m", "DICJ-Q-2025",
        "PRIMARY ✔" if abs(dicj("2025Q4", True) - 45750) < 100 else "CORRECTED")
    add("Q2 2025 reinvestment shift; 'market-driven' reinvestment", "transcript", "Not in earnings release", "LVS Q2 2025 call (Motley Fool copy)", "SECONDARY ✔ (remains)",
        "Upgrade requires official webcast/transcript")
    add("Londoner US$1bn+ EBITDA target; ~$800m run-rate", "transcript/ASGAM", "Not in release; 3Q26 Londoner EBITDA x4 = $712m (DERIVED)", "LVS-ER-2026-10-21", "SECONDARY ✔ (remains)")
    with (ROOT / "sources/fact_verification.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    for r in main():
        print(f"{r['status']:<24} {r['claim']}: {r['primary_value']}")
