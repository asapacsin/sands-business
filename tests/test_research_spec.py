import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_research_spec as gate  # noqa: E402

SPEC = ROOT / "research" / "RESEARCH_SPEC.md"
REGISTRY = ROOT / "research" / "work.json"


class ResearchSpecGateTest(unittest.TestCase):
    def run_gate(self, text: str, registry: dict | None = None) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "RESEARCH_SPEC.md"
            spec.write_text(text, encoding="utf-8")
            data = registry if registry is not None else json.loads(REGISTRY.read_text(encoding="utf-8"))
            (Path(tmp) / "work.json").write_text(json.dumps(data), encoding="utf-8")
            out = io.StringIO()
            with redirect_stdout(out):
                code = gate.main([str(spec)])
            return code, out.getvalue()

    def test_committed_spec_passes(self):
        code, out = self.run_gate(SPEC.read_text(encoding="utf-8"))
        self.assertEqual(code, 0, out)

    def test_wrong_weighted_score_is_caught(self):
        text = SPEC.read_text(encoding="utf-8").replace("**4.60**", "**4.65**")
        code, out = self.run_gate(text)
        self.assertEqual(code, 1)
        self.assertIn("matrix option 1", out)

    def test_missing_card_field_is_caught(self):
        text = SPEC.read_text(encoding="utf-8").replace(
            "- Completion: templates match", "- Done when: templates match", 1)
        code, out = self.run_gate(text)
        self.assertEqual(code, 1)
        self.assertIn("T01: missing 'Completion:'", out)

    def test_missing_section_is_caught(self):
        text = SPEC.read_text(encoding="utf-8").replace("## 13. Quality assurance", "## Quality assurance")
        code, out = self.run_gate(text)
        self.assertEqual(code, 1)
        self.assertIn("sections 1..15", out)

    def test_registry_dependency_drift_is_caught(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        next(item for item in data["work"] if item["id"] == "T09")["depends_on"] = ["T02"]
        code, out = self.run_gate(SPEC.read_text(encoding="utf-8"), data)
        self.assertEqual(code, 1)
        self.assertIn("T09: registry depends_on", out)

    def test_human_task_must_have_human_owner(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        next(item for item in data["work"] if item["id"] == "T26")["owner"] = "AUTONOMOUS"
        code, out = self.run_gate(SPEC.read_text(encoding="utf-8"), data)
        self.assertEqual(code, 1)
        self.assertIn("T26: HUM task", out)


if __name__ == "__main__":
    unittest.main()
