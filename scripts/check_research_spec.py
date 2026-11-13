#!/usr/bin/env python3
"""Deterministic gate for research/RESEARCH_SPEC.md.

Checks structure, not research quality: the 15 required sections in order,
complete task cards, a recomputed decision-matrix score, and agreement with
the task registry (research/work.json). Exit 0 = pass, 1 = findings.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Research objective and intended audience",
    "Candidate Sands China business decisions",
    "Decision-selection matrix and justification",
    "Final research question and testable hypotheses",
    "External casino case-study research plan",
    "Macau / Sands competitive and financial research plan",
    "Public datasets and source-verification strategy",
    "Analytical methods, metrics, equations and model requirements",
    "Framework for transferring external case-study lessons to Sands",
    "Proposed report outline and principal figures/tables",
    "Implementation and reproducibility plan",
    "Potential findings, competing explanations and limitations",
    "Quality assurance and evidence-verification checklist",
    "Milestones and step-by-step execution tasks",
    "Acceptance criteria for the completed research",
]
CARD_FIELDS = ("Inputs:", "Procedure:", "Output:", "Dependencies:", "Completion:")
CARD_RE = re.compile(r"^\*\*(T\d{2}) — (.+?)\*\* \((PUB|INT|HUM)[^)]*\)\s*$", re.M)
SCORE_TOLERANCE = 0.005


def check_sections(text: str) -> list[str]:
    found = re.findall(r"^## (\d+)\. (.+)$", text, re.M)
    errors = []
    if [int(n) for n, _ in found] != list(range(1, 16)):
        errors.append(f"expected sections 1..15 in order, found {[n for n, _ in found]}")
    for (number, title), required in zip(found, REQUIRED_SECTIONS):
        if not title.strip().startswith(required):
            errors.append(f"section {number} title '{title}' does not start with '{required}'")
    if not re.search(r"^## Prioritized execution backlog", text, re.M):
        errors.append("missing '## Prioritized execution backlog'")
    return errors


def task_cards(text: str) -> dict[str, dict]:
    cards = {}
    matches = list(CARD_RE.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find("\n## ", match.end())
        body = text[match.end(): end if end != -1 else len(text)]
        deps_line = re.search(r"Dependencies:\s*(.+)", body)
        deps = re.findall(r"T\d{2}", deps_line.group(1)) if deps_line else []
        cards[match.group(1)] = {"body": body, "class": match.group(3), "depends_on": deps}
    return cards


def check_cards(cards: dict[str, dict]) -> list[str]:
    errors = []
    if not cards:
        return ["no task cards found"]
    for task_id, card in cards.items():
        for field in CARD_FIELDS:
            if field not in card["body"]:
                errors.append(f"{task_id}: missing '{field}'")
        for dep in card["depends_on"]:
            if dep not in cards:
                errors.append(f"{task_id}: unknown dependency {dep}")
    return errors


def check_matrix(text: str) -> list[str]:
    """Recompute weighted scores of the decision-selection matrix."""
    section = re.search(r"^## 3\..*?(?=^## 4\.)", text, re.M | re.S)
    if not section:
        return ["section 3 not found for matrix check"]
    weights, columns, stated = [], [], None
    for line in section.group(0).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        weight = re.search(r"\((0\.\d+)\)", cells[0]) if cells else None
        if weight:
            weights.append(float(weight.group(1)))
            columns.append([int(re.match(r"\d", c).group(0)) for c in cells[1:]])
        elif cells and "Weighted score" in cells[0]:
            stated = [float(re.sub(r"[^\d.]", "", c)) for c in cells[1:]]
    if not weights or stated is None:
        return ["decision matrix weights or weighted-score row not found"]
    errors = []
    if abs(sum(weights) - 1.0) > 1e-9:
        errors.append(f"matrix weights sum to {sum(weights)}, expected 1.0")
    for option in range(len(stated)):
        computed = sum(w * row[option] for w, row in zip(weights, columns))
        if abs(computed - stated[option]) > SCORE_TOLERANCE:
            errors.append(f"matrix option {option + 1}: stated {stated[option]} != computed {computed:.2f}")
    return errors


def check_registry(cards: dict[str, dict], registry_path: Path) -> list[str]:
    data = json.loads(registry_path.read_text(encoding="utf-8"))
    items = {item["id"]: item for item in data.get("work", [])}
    errors = []
    if set(items) != set(cards):
        errors.append(f"registry/spec task mismatch: only in spec {sorted(set(cards) - set(items))}, "
                      f"only in registry {sorted(set(items) - set(cards))}")
    for task_id in set(items) & set(cards):
        if sorted(items[task_id]["depends_on"]) != sorted(cards[task_id]["depends_on"]):
            errors.append(f"{task_id}: registry depends_on {items[task_id]['depends_on']} "
                          f"!= spec {cards[task_id]['depends_on']}")
        if cards[task_id]["class"] == "HUM" and not items[task_id]["owner"].startswith("HUMAN_"):
            errors.append(f"{task_id}: HUM task must have a HUMAN_* owner in the registry")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--registry", type=Path, help="defaults to work.json beside the spec")
    args = parser.parse_args(argv)
    text = args.spec.read_text(encoding="utf-8")
    cards = task_cards(text)
    registry = args.registry or args.spec.with_name("work.json")
    errors = check_sections(text) + check_cards(cards) + check_matrix(text) + check_registry(cards, registry)
    for error in errors:
        print("FAIL: " + error)
    if not errors:
        print(f"PASS: 15 sections, {len(cards)} task cards, matrix scores and registry consistent")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
