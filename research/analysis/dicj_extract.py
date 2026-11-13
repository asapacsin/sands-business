"""Extract quarterly Macao GGR by game type from DICJ statistics XML (report 3).

Source: https://www.dicj.gov.mo/web/en/information/DadosEstat/<year>/report_en.xml
Units: MOP million. Output: data/processed/market_quarter.csv (long format).
"""
from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "dicj"
OUT = ROOT / "data" / "processed" / "market_quarter.csv"


def num(text: str | None) -> float | None:
    text = (text or "").strip().replace(",", "")
    return None if text in {"", "-"} else float(text)


def extract(year: int) -> list[dict]:
    root = ET.parse(RAW / f"q_{year}.xml").getroot()
    report = next(r for r in root.iter("REPORT") if r.findtext("TITLE", "").startswith("(3)"))
    rows = []
    for record in report.find("DATA").iter("RECORD"):
        cells = [d.text for d in record.findall("DATA")]
        item, values = cells[0].strip(), cells[1:]
        quarterly = values[-5:-1]  # last block = current year Q1..Q4, Total
        for q, value in enumerate(quarterly, start=1):
            v = num(value)
            if v is not None:
                rows.append({"period": f"{year}Q{q}", "item": item, "value_mop_m": v,
                             "source_id": f"DICJ-Q-{year}"})
    return rows


def build() -> list[dict]:
    rows = [r for y in (2023, 2024, 2025, 2026) for r in extract(y)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


if __name__ == "__main__":
    data = build()
    print(len(data), "rows", sorted({r["item"] for r in data}))
    for r in data:
        if r["period"] in ("2025Q4", "2026Q3"):
            print(r)
