import csv
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import economics as E  # noqa: E402
import holdout_analysis as H  # noqa: E402
import scenarios as S  # noqa: E402


class Economics(unittest.TestCase):
    def test_break_even_closed_form(self):
        self.assertAlmostEqual(E.break_even_multiple(0.40, 0.10), 2.0)
        self.assertAlmostEqual(E.break_even_multiple(0.40, 0.10, True), 1.2)
        self.assertAlmostEqual(E.break_even_multiple(0.0, 0.0), 1.0)  # tau = 0 edge case

    def test_break_even_rejects_impossible_inputs(self):
        with self.assertRaises(ValueError):
            E.break_even_multiple(0.6, 0.5)

    def test_contribution_zero_at_break_even(self):
        k = E.break_even_multiple(0.40, 0.10)
        self.assertAlmostEqual(E.incremental_contribution(d_ggr=k * 100, promo_cost=100, tau=0.40, v=0.10), 0.0)

    def test_zero_response_loses_full_cost(self):
        self.assertEqual(E.incremental_contribution(0, 50, 0.4, 0.1), -50)

    def test_comp_room_cost_bounds(self):
        self.assertEqual(E.comp_room_opportunity_cost(1.0, 200, 40), 160)   # full occupancy -> displaced margin
        self.assertEqual(E.comp_room_opportunity_cost(0.0, 200, 40), 40)    # empty -> marginal cost only


class Scenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = S.base_params()
        cls.cs = S.cells(cls.p)

    def test_bau_average_multiple_matches_calibration(self):
        g = sum(S.ggr(c, c["x0"], self.p["b"]) for c in self.cs)
        self.assertAlmostEqual(g / self.p["pool"], self.p["pool_avg_ggr_per_dollar"], places=6)

    def test_equimarginal_property_of_optimum(self):
        xs = S.optimal(self.cs, self.p, self.p["pool"])
        m = [mg for mg, x in zip(S.marginal_ggr_per_dollar(self.cs, xs, self.p), xs) if x > 1e-9]
        self.assertLess((max(m) - min(m)) / max(m), 0.05)

    def test_reallocation_never_reduces_contribution_or_share(self):
        for realloc in (0.1, 0.2, 0.3):
            s = S.scenario(self.p, realloc)
            self.assertGreaterEqual(s["delta_vs_bau"], -1e-6)
            self.assertTrue(s["share_guardrail_ok"])

    def test_illustrative_values_never_in_actual_data(self):
        for path in (ROOT / "data/processed").glob("*.csv"):
            with path.open() as handle:
                self.assertNotIn("ILLUSTRATIVE", handle.read(), path.name)


class Holdout(unittest.TestCase):
    def test_estimator_recovers_effect_and_decision(self):
        cov = H.coverage(runs=60)
        self.assertGreaterEqual(cov["ci90_coverage"], 0.8)
        self.assertEqual(cov["adopt_rate"], 1.0)
        bad = H.coverage(runs=40, true_lift_ggr=120.0)
        self.assertEqual(bad["adopt_rate"], 0.0)

    def test_mde_decreases_with_sample(self):
        self.assertLess(H.mde(500, 4000, 36000), H.mde(500, 1000, 9000))
        self.assertTrue(math.isfinite(H.mde(500, 10, 10)))


if __name__ == "__main__":
    unittest.main()
