"""Extract Macao property-quarter data from Las Vegas Sands earnings releases (8-K Ex.99.1).

Each release reports the current quarter and the prior-year quarter for every Macao property.
We keep the current-quarter value as primary and the prior-year value for cross-checks
(restatement detection). Output: data/processed/property_quarter.csv (long format).
"""
from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "lvs"
OUT = ROOT / "data" / "processed" / "property_quarter.csv"

PROPERTIES = {
    "The Venetian Macao": "Venetian",
    "The Londoner Macao": "Londoner",
    "Sands Cotai Central": "Londoner",  # pre-rebrand name, if present
    "The Parisian Macao": "Parisian",
    "The Plaza Macao and Four Seasons Macao": "Plaza_FourSeasons",
    "The Plaza Macao and Four Seasons Hotel Macao": "Plaza_FourSeasons",
    "Sands Macao": "SandsMacao",
}
METRICS = [
    ("Casino", "rev_casino", "usd_m"),
    ("Rooms", "rev_rooms", "usd_m"),
    ("Food and beverage", "rev_fnb", "usd_m"),
    ("Mall", "rev_mall", "usd_m"),
    ("Convention, retail and other", "rev_other", "usd_m"),
    ("Net revenues", "net_revenue", "usd_m"),
    ("Adjusted Property EBITDA", "adj_property_ebitda", "usd_m"),
    ("Rolling Chip volume", "rolling_volume", "usd_m"),
    ("Rolling Chip win %", "rolling_win_pct", "pct"),
    ("Non-Rolling Chip drop", "nonrolling_drop", "usd_m"),
    ("Non-Rolling Chip win %", "nonrolling_win_pct", "pct"),
    ("Slot handle", "slot_handle", "usd_m"),
    ("Slot hold %", "slot_hold_pct", "pct"),
    ("Occupancy %", "occupancy_pct", "pct"),
    (r"Average daily (?:room )?rate \(ADR\)", "adr", "usd"),
    (r"Revenue per available room \(RevPAR\)", "revpar", "usd"),
]
NUM = r"\(?-?[\d,]+(?:\.\d+)?\)?|—|-"


def to_text(path: Path) -> str:
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?i)</(tr|p|div)>", "\n", t)
    t = re.sub(r"(?i)</t[dh]>", " | ", t)
    t = html.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"[ \xa0​]+", " ", t)
    t = re.sub(r"(\|\s*)+", "| ", t)
    return re.sub(r"\n\s*\n+", "\n", t)


def parse_num(token: str) -> float | None:
    token = token.strip()
    if token in {"—", "-", ""}:
        return 0.0
    negative = token.startswith("(")
    value = float(token.strip("()").replace(",", ""))
    return -value if negative else value


def quarter_of(text: str) -> tuple[int, int]:
    m = re.search(r"Three Months Ended \| [^|]*?\| (March|June|September|December) 31?0?,? \| \(Dollars in millions\) \| (\d{4})", text)
    if not m:
        m = re.search(r"(March|June|September|December) \d{1,2}, \| \(Dollars in millions\) \| (\d{4})", text)
    month, year = m.group(1), int(m.group(2))
    return year, {"March": 1, "June": 2, "September": 3, "December": 4}[month]


def extract(path: Path) -> list[dict]:
    text = to_text(path).replace("\n", " ")
    rows = []
    for m in re.finditer(r"Three Months Ended \| (The [^|]+?|Sands Macao|Sands Cotai Central) \| (March|June|September|December) \d{1,2}, \| \(Dollars in millions\) \| (\d{4}) \| (\d{4}) \| Change \|", text):
        name, month, cur_year, prior_year = m.group(1).strip(), m.group(2), int(m.group(3)), int(m.group(4))
        if name not in PROPERTIES:
            continue
        quarter = {"March": 1, "June": 2, "September": 3, "December": 4}[month]
        block = text[m.end(): m.end() + 2500]
        block = block.split("Three Months Ended")[0]
        for label, key, unit in METRICS:
            pattern = label if label.startswith("Average") or label.startswith("Revenue per") else re.escape(label)
            mm = re.search(pattern + r"(?:\(\d\))?\s*\|\s*(?:\$ \|\s*)?(" + NUM + r")\s*\|\s*(?:% \|\s*)?(?:\$ \|\s*)?(" + NUM + r")", block, re.I)
            if not mm:
                continue
            for year, token in ((cur_year, mm.group(1)), (prior_year, mm.group(2))):
                rows.append({"property": PROPERTIES[name], "year": year, "quarter": quarter,
                             "period": f"{year}Q{quarter}", "metric": key, "value": parse_num(token), "unit": unit,
                             "basis": "reported" if year == cur_year else "prior_year_comparative",
                             "source_id": f"LVS-ER-{path.name[:10]}"})
    return rows


def build() -> list[dict]:
    rows = []
    for path in sorted(RAW.glob("*_ex991.htm")):
        rows.extend(extract(path))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: (r["property"], r["period"], r["metric"], r["basis"])))
    return rows


if __name__ == "__main__":
    data = build()
    reported = [r for r in data if r["basis"] == "reported"]
    print(len(data), "rows;", len(reported), "reported;",
          sorted({r["period"] for r in reported}), sorted({r["property"] for r in reported}))
    print(json.dumps(sorted({r["metric"] for r in reported})))
