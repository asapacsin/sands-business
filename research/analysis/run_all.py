"""Regenerate quantitative outputs with one command.

  python3 research/analysis/run_all.py                   # full: raw filings -> processed -> outputs
  python3 research/analysis/run_all.py --from-processed  # committed processed data -> all outputs
The full mode needs raw filings (python3 research/analysis/fetch_sources.py); --from-processed needs
only what is committed in research/data/processed/.
"""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).parent
FULL = ["lvs_extract", "dicj_extract", "panel", "peers_extract", "hold", "public_analysis", "economics",
        "scenarios", "holdout_analysis", "verify_facts"]
PROCESSED = ["panel", "public_analysis", "economics", "scenarios", "holdout_analysis"]
for step in (PROCESSED if "--from-processed" in sys.argv else FULL):
    print(f"== {step}")
    if step == "hold":
        sys.path.insert(0, str(HERE))
        import public_analysis
        public_analysis.extract_hold_impacts()
        continue
    runpy.run_path(str(HERE / f"{step}.py"), run_name="__main__")
