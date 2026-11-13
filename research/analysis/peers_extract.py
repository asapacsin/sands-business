"""Extract Macau segment revenue and property EBITDA(R) for SEC-filing Macau peers.

Definitions differ and are recorded per row (definition column). Comparisons are DIRECTIONAL.
  Wynn  : Wynn Palace + Wynn Macau; "Operating revenues" and "Adjusted Property EBITDAR" (US$ m)
  MGM   : MGM China segment net revenues and Segment Adjusted EBITDAR (US$ thousands -> m)
  Melco : City of Dreams (Macau) + Studio City + Altira; total operating revenues, Adjusted EBITDA
Galaxy Entertainment and SJM Holdings do not file with the SEC: documented gap (see notes).
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "peers"
OUT = ROOT / "data" / "processed" / "operator_quarter.csv"
sys.path.insert(0, str(Path(__file__).parent))
from lvs_extract import to_text  # noqa: E402

QWORD = {"first": 1, "second": 2, "third": 3, "fourth": 4}
MONTHQ = {"March": 1, "June": 2, "September": 3, "December": 4}
AMT = r"\$\s?([\d,]+(?:\.\d+)?) million"


def wynn(text: str) -> dict:
    out = {}
    for prop in ("Wynn Palace", "Wynn Macau"):
        for key, pat in (("net_revenue", rf"Operating revenues from {prop} were {AMT} for the (\w+) quarter of (\d{{4}})"),
                         ("ebitda", rf"Adjusted Property EBITDAR from {prop} was {AMT} for the (\w+) quarter of (\d{{4}})")):
            m = re.search(pat, text)
            if m:
                period = f"{m.group(3)}Q{QWORD[m.group(2).lower()]}"
                out.setdefault(period, {}).setdefault(key, 0.0)
                out[period][key] += float(m.group(1).replace(",", ""))
                out[period].setdefault("_parts", set()).add((prop, key))
    return {p: v for p, v in out.items() if len(v.pop("_parts")) == 4}


def mgm(text: str) -> dict:
    nums = re.findall(r"MGM China \| ([\d,]+) \| (\(?[\d,]+\)?) \|", text)
    m = re.search(r"Three Months Ended (March|June|September|December) 3\d, \| (\d{4})", text)
    if len(nums) < 2 or not m:
        return {}
    period = f"{m.group(2)}Q{MONTHQ[m.group(1)]}"
    return {period: {"net_revenue": float(nums[0][0].replace(",", "")) / 1000,
                     "ebitda": float(nums[1][0].replace(",", "")) / 1000}}


def melco(text: str) -> dict:
    m = re.search(r"For the quarter ended (March|June|September|December) 3\d, (\d{4}), total operating revenues", text)
    if not m:
        return {}
    period = f"{m.group(2)}Q{MONTHQ[m.group(1)]}"
    rev = ebitda = 0.0
    parts = 0
    for prop, possessive in (("City of Dreams", "City of Dreams’"), ("Studio City", "Studio City’s"), ("Altira Macau", "Altira Macau’s")):
        r = re.search(rf"total operating revenues at {prop} were US\$([\d,.]+) million", text, re.I)
        e = (re.search(rf"{possessive} (negative )?Adjusted EBITDA was US\$([\d,.]+) million", text)
             or re.search(rf"{prop} generated (negative )?Adjusted EBITDA of US\$([\d,.]+) million", text))
        if r and e:
            parts += 1
            rev += float(r.group(1).replace(",", ""))
            ebitda += (-1 if e.group(1) else 1) * float(e.group(2).replace(",", ""))
    return {period: {"net_revenue": rev, "ebitda": ebitda}} if parts == 3 else {}


# Preliminary 4Q25 financial-statement exhibit filed a day before the full release (MGM-ER-2026-02-05); not used.
EXCLUDED = {"mgm_2026-02-04.htm"}

DEFINITIONS = {"wynn": "Operating revenues; Adjusted Property EBITDAR (Wynn Palace + Wynn Macau)",
               "mgm": "Segment net revenues; Segment Adjusted EBITDAR (MGM China)",
               "melco": "Total operating revenues; Adjusted EBITDA (CoD Macau + Studio City + Altira)"}


def build() -> list[dict]:
    rows = {}
    for path in sorted(RAW.glob("*.htm")):
        if path.name in EXCLUDED:
            continue
        operator = path.name.split("_")[0]
        text = to_text(path).replace("\n", " ")
        for period, vals in {"wynn": wynn, "mgm": mgm, "melco": melco}[operator](text).items():
            rows[(operator, period)] = {"operator": operator, "period": period,
                                        "net_revenue_usd_m": round(vals["net_revenue"], 1),
                                        "ebitda_usd_m": round(vals["ebitda"], 1),
                                        "margin_pct": round(100 * vals["ebitda"] / vals["net_revenue"], 2),
                                        "definition": DEFINITIONS[operator],
                                        "source_id": f"{operator.upper()}-ER-{path.stem.split('_')[1]}"}
    sands = [r for r in csv.DictReader(open(ROOT / "data/processed/sands_panel.csv")) if r["unit"] == "SandsMacao5_total"]
    for r in sands:
        rows[("sands", r["period"])] = {"operator": "sands", "period": r["period"],
                                         "net_revenue_usd_m": round(float(r["net_revenue"]), 1),
                                         "ebitda_usd_m": round(float(r["adj_property_ebitda"]), 1),
                                         "margin_pct": round(float(r["ebitda_margin_pct"]), 2),
                                         "definition": "Net revenues; Adjusted Property EBITDA (5 Macao properties, excl. ferry/other)",
                                         "source_id": "LVS-ER (see property_quarter.csv)"}
    out = sorted(rows.values(), key=lambda r: (r["operator"], r["period"]))
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)
    return out


if __name__ == "__main__":
    data = build()
    for op in ("sands", "wynn", "mgm", "melco"):
        series = [r for r in data if r["operator"] == op]
        print(op, len(series), [(r["period"], r["margin_pct"]) for r in series][-6:])
