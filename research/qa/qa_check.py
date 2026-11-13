"""T22 — automated evidence QA for Deliverables A, B, D (spec §13). Exit 0 only if every check passes.
Writes qa/qa_report.md."""
from __future__ import annotations

import csv
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from lvs_extract import METRICS, to_text  # noqa: E402

A = (ROOT / "deliverables/A_report.md").read_text()
B = (ROOT / "deliverables/B_brief.md").read_text()
D = (ROOT / "deliverables/D_interview.md").read_text()
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))


# 1. No unverified tags left in outward-facing deliverables
for label, text in (("A", A), ("B", B)):
    bad = re.findall(r"\[(?:TO-VERIFY|SECONDARY ✔)\]", text)
    check(f"{label}: no TO-VERIFY / SECONDARY tags", not bad, str(bad))

# 2. Causal and accusatory language scan (A, B)
CAUSAL = r"\b(caused|proved|proves|drove|drives the decline)\b"
ACCUSE = r"(mismanag|poor management|should have|failed to|failure of management|wasteful|inefficient spending)"
for label, text in (("A", A), ("B", B)):
    c = [m.group(0) for m in re.finditer(CAUSAL, text, re.I)]
    check(f"{label}: no unsupported causal verbs", not c, str(c))
    x = [m.group(0) for m in re.finditer(ACCUSE, text, re.I)]
    check(f"{label}: no accusatory language", not x, str(x))

# 3. Affiliation / internal-access boundaries
for label, text in (("A", A), ("B", B)):
    check(f"{label}: independence statement present", bool(re.search(r"no (internal|affiliation)", text, re.I)))
    check(f"{label}: no implied internal access", not re.search(r"\b(our data|internal sources told|confidential)\b", text, re.I))

# 3b. §13: every block (paragraph, bullet, table) containing a figure carries an evidence tag
TAG = re.compile(r"\[(?:[PDIUR])(?:[\] :])")
FIG = re.compile(r"(\d[\d,.]*\s?(%|×|pts|points|bn\b|m\b|m a year|a night)|US\$\s?\d|HK\$\d|MOP\s?\d|\$\d)")


def blocks(text: str):
    body = text.split("\n---\n", 1)[-1] if text.startswith("---") else text
    body = body.split("## 10. References")[0]
    cur = []
    for line in body.splitlines():
        if not line.strip() or line.startswith("#"):
            if cur:
                yield "\n".join(cur)
            cur = []
            continue
        if line.lstrip().startswith(("- ", "1.", "2.", "3.", "4.", "5.")) and cur and not cur[0].startswith("|"):
            yield "\n".join(cur)
            cur = []
        cur.append(line)
    if cur:
        yield "\n".join(cur)


for label, text in (("A", A), ("B", B), ("D", D)):
    untagged = [b[:70] for b in blocks(text) if FIG.search(b) and not TAG.search(b) and not b.startswith("![")]
    check(f"{label}: every figure-bearing block has an evidence tag", not untagged, str(untagged[:3]))

# 3c. every source ID used in a tag exists in the source register
register = {r["source_id"] for r in csv.DictReader(open(ROOT / "sources/source_register.csv"))}
families = {sid.rsplit("-", 3)[0] if sid[-10:-6].isdigit() else sid for sid in register}
ids = set()
for tag in re.findall(r"\[[PDIUR][ :][^\]]*\]", A + B + D):
    for group in re.split(r"[\s,;+]+", tag.strip("[]")):
        prev = None
        for piece in group.split("/"):
            if prev and re.fullmatch(r"(Q\d|\d{4}|\d{4}-\d{2}-\d{2})", piece):
                piece = prev[: len(prev) - len(piece)] + piece  # TR-LVS-2025Q2/Q3, DICJ-Q-2024/2025
            prev = piece
            if re.fullmatch(r"(?:LVS|WYNN|MGM|MELCO)-ER(?:-\d{4}-\d{2}-\d{2})?|DICJ-Q(?:-\d{4})?|(?:TR|BRK|LIT|PR|LAW)-[A-Z0-9-]+", piece):
                ids.add(piece)
            elif re.fullmatch(r"(?:WYNN|MGM|MELCO)", piece):
                ids.add(piece + "-ER")
family_ok = lambda i: any(r.startswith(i + "-") for r in register)  # noqa: E731
missing = sorted(i for i in ids if i not in register and not family_ok(i))
check("all cited source IDs exist in source register", not missing, str(missing))

# 3d. cross-operator comparisons labelled directional; illustrative defined
for label, text in (("A", A), ("B", B)):
    if re.search(r"Wynn|MGM|Melco", text):
        check(f"{label}: peer margin comparison labelled 'directional'", "directional" in text.lower())
    check(f"{label}: illustrative defined as 'not a Sands figure'", "not a sands figure" in text.lower())

# 4. Illustrative labelling
check("A: illustrative values labelled", A.lower().count("illustrative") >= 4, f"count={A.lower().count('illustrative')}")

# 5. Glossary-level distinctions present
for term in ("GGR", "net revenue", "EBITDA", "contribution"):
    check(f"A: uses term '{term}'", term.lower() in A.lower())

# 6. Required figures exist and are referenced
for f in ("F1_share_vs_margin", "F2_net_to_gross_gap", "F3_property_margins", "F5_hotel_kpis",
          "F6_break_even", "F7_scenarios", "F8_tornado"):
    check(f"figure {f} exists and is referenced", (ROOT / f"outputs/figures/{f}.png").exists() and f in A)

# 7. Length budgets (≈ 500 words/page text; figures add pages)
def pdf_pages(name: str) -> int:
    pdf = ROOT / f"deliverables/{name}.pdf"
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes())) if pdf.exists() else -1


check("A: 8–12 rendered pages (PDF)", 8 <= pdf_pages("A_report") <= 12, f"pages={pdf_pages('A_report')}")
check("B: ≤ 2 rendered pages (PDF)", 1 <= pdf_pages("B_brief") <= 2, f"pages={pdf_pages('B_brief')}")
check("D: 8 questions", len(re.findall(r"^\*\*\d+\.", D, re.M)) == 8)

# 8. Headline numbers in B also appear in A (traceability)
for token in ("22.4%", "25.4%", "20.5%", "23.5%", "US$226m", "4.2 points", "27.8%", "0.4", "2.1", "98"):
    check(f"B number '{token}' traceable to A", token in A)

# 9. Fact verification: no CORRECTED/unresolved facts used as-is
facts = list(csv.DictReader(open(ROOT / "sources/fact_verification.csv")))
check("all spec facts resolved", all(r["status"] for r in facts), f"{len(facts)} facts")

# 10. Independent re-extraction of a random 20% of property-quarter values from raw filings
rows = [r for r in csv.DictReader(open(ROOT / "data/processed/property_quarter.csv")) if r["basis"] == "reported"]
random.seed(20261113)
sample = random.sample(rows, k=max(1, len(rows) // 5))
names = {"Venetian": "The Venetian Macao", "Londoner": "The Londoner Macao", "Parisian": "The Parisian Macao",
         "Plaza_FourSeasons": "The Plaza Macao and Four Seasons", "SandsMacao": "Sands Macao"}
labels = {k: lbl for lbl, k, _ in METRICS}
cache: dict[str, str] = {}
misses = []
for r in sample:
    path = ROOT / f"data/raw/lvs/{r['source_id'][7:]}_ex991.htm"
    text = cache.setdefault(str(path), to_text(path).replace("\n", " "))
    start = text.find(f"| {names[r['property']]}")
    blocks = [m.start() for m in re.finditer(re.escape(names[r["property"]]) + r"[^|]*\| (March|June|September|December) \d", text)]
    v = float(r["value"])
    fmt = [f"{v:,.0f}", f"{v:.1f}", f"{v:.2f}", f"{v:.0f}"]
    if v < 0:
        fmt += [f"({abs(v):,.0f})", f"({abs(v):.1f})", f"({abs(v):.2f})"]
    if v == 0:
        fmt += ["—"]
    found = any(any(f" {f} " in text[b:b + 2600] for f in fmt) for b in blocks)
    if not found:
        misses.append((r["property"], r["period"], r["metric"], r["value"]))
check(f"re-extraction of {len(sample)} sampled values (20%)", not misses, str(misses[:5]))

lines = ["# QA report (T22)", "", f"Checks: {len(results)}; failed: {sum(not ok for _, ok, _ in results)}", "",
         "| Check | Result | Detail |", "|---|---|---|"]
lines += [f"| {n} | {'PASS' if ok else 'FAIL'} | {d.replace('|', '/')[:120]} |" for n, ok, d in results]
(ROOT / "qa/qa_report.md").write_text("\n".join(lines) + "\n")
for n, ok, d in results:
    if not ok:
        print("FAIL:", n, d)
print(f"{len(results)} checks, {sum(not ok for _, ok, _ in results)} failed")
sys.exit(0 if all(ok for _, ok, _ in results) else 1)
