# sands-business — agent instructions

@AGENTS.md

## Project

Independent, public-information business research on Sands China (Macao): a data-driven
study of mass-market customer reinvestment allocation. The governing document is
[`research/RESEARCH_SPEC.md`](research/RESEARCH_SPEC.md); the backlog is `research/work.json`.

## Project-specific rules

- Pick work with `python3 scripts/frontier.py next --registry research/work.json`; do not invent tasks.
- Every factual claim carries an evidence label (`[PRIMARY ✔]`, `[SECONDARY ✔]`, `[TO-VERIFY]`,
  `[ILLUSTRATIVE]`, `[DERIVED]`). Never recall financial figures from memory as facts.
- Never imply affiliation with, internal access to, or endorsement by Sands China / Las Vegas Sands.
- Nothing is sent to anyone outside this repo without explicit human approval (task T26).
- Before claiming a task done, run its gates:
  `python3 scripts/check_research_spec.py research/RESEARCH_SPEC.md`,
  `python3 scripts/frontier.py check --registry research/work.json`,
  `python3 -m unittest discover -s tests`.
