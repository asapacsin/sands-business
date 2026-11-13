import csv
import unittest
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = list(csv.DictReader(open(ROOT / "data/processed/property_quarter.csv")))


def table(basis):
    out = {}
    for r in ROWS:
        if r["basis"] == basis:
            out[(r["property"], r["period"], r["metric"])] = float(r["value"])
    return out


class PropertyQuarterIntegrity(unittest.TestCase):
    def test_every_row_has_source(self):
        self.assertTrue(all(r["source_id"].startswith("LVS-ER-") for r in ROWS))

    def test_categories_sum_to_net_revenue(self):
        t = table("reported")
        cats = ("rev_casino", "rev_rooms", "rev_fnb", "rev_mall", "rev_other")
        for (prop, period, metric), value in t.items():
            if metric != "net_revenue":
                continue
            total = sum(t.get((prop, period, c), 0.0) for c in cats)
            self.assertLessEqual(abs(total - value), 3, f"{prop} {period}: {total} vs {value}")

    def test_reported_matches_next_year_comparative(self):
        rep, comp = table("reported"), table("prior_year_comparative")
        mismatches = [(k, rep[k], comp[k]) for k in rep.keys() & comp.keys()
                      if abs(rep[k] - comp[k]) > max(2, 0.02 * abs(rep[k]))]
        # restatements must be rare and are reported in notes/restatements.md
        self.assertLessEqual(len(mismatches), 10, mismatches[:10])

    def test_pinned_values_q3_2026(self):
        t = table("reported")
        self.assertEqual(t[("Venetian", "2026Q3", "net_revenue")], 649)
        self.assertEqual(t[("Londoner", "2026Q3", "adj_property_ebitda")], 178)
        self.assertEqual(t[("Venetian", "2026Q3", "occupancy_pct")], 98.3)


if __name__ == "__main__":
    unittest.main()
