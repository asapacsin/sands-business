#!/usr/bin/env python3
"""Independent read-only reviewer adapter using a separate Claude Code CLI session.

Set AI_NATIVE_REVIEWER_CMD="python3 scripts/claude_reviewer.py". The reviewer session gets only
Read/Grep/Glob and read-only git/python Bash (no Edit/Write); this wrapper writes the result JSON.
Limitation: same model family as a Claude executor; it is a fresh, context-free session, not a
different vendor. Set AI_NATIVE_REVIEWER_MODEL to choose another model.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

PROMPT = """You are an independent, skeptical, READ-ONLY reviewer. You did not write this work.
Review packet (JSON): {packet}
1. Read the packet: it holds the contract (goal, acceptance), gate results and the source fingerprint.
2. Inspect the actual repository files the contract covers (research/**). Spot-check claims against data:
   e.g. compare numbers in research/deliverables/A_report.md and B_brief.md with research/outputs/*.json,
   research/data/processed/*.csv and research/sources/*.csv; check that cited sources exist in
   research/sources/source_register.csv; look for fabricated references, unlabelled illustrative numbers,
   causal over-claims, implied affiliation with Sands China, and acceptance criteria in research/RESEARCH_SPEC.md §15.
3. Verdict PASS only if acceptance is met and you found no material defect. REWORK for fixable defects
   (list them precisely). NOT_VERIFIED if you could not check.
Reply with ONLY one JSON object, no prose:
{{"verdict": "PASS|REWORK|BLOCKED|NOT_VERIFIED", "reviewed_fingerprint": "{fp}", "reviewed_contract_hash": "{ch}",
  "findings": [{{"severity": "high|medium|low", "file": "...", "issue": "...", "evidence": "..."}}], "next_action": "..."}}"""


def main() -> int:
    packet_path = Path(os.environ["AI_NATIVE_REVIEW_PACKET"])
    result_path = Path(os.environ["AI_NATIVE_REVIEW_RESULT"])
    packet = json.loads(packet_path.read_text())
    fp = packet["snapshot"]["fingerprint"]
    ch = packet["contract_hash"]
    argv = ["claude", "-p", PROMPT.format(packet=packet_path, fp=fp, ch=ch),
            "--allowedTools", "Read,Grep,Glob,Bash(git diff:*),Bash(git log:*),Bash(git show:*),Bash(python3 -c:*)",
            "--disallowedTools", "Edit,Write,NotebookEdit", "--output-format", "text"]
    if os.environ.get("AI_NATIVE_REVIEWER_MODEL"):
        argv += ["--model", os.environ["AI_NATIVE_REVIEWER_MODEL"]]
    proc = subprocess.run(argv, capture_output=True, text=True, timeout=1500)
    match = re.search(r"\{.*\}", proc.stdout, re.S)
    if proc.returncode != 0 or not match:
        sys.stderr.write(proc.stderr[-2000:] + proc.stdout[-2000:])
        return 1
    result = json.loads(match.group(0))
    result_path.write_text(json.dumps(result, indent=2))
    (result_path.parent / "reviewer_transcript.txt").write_text(proc.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
