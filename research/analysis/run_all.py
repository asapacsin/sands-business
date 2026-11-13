"""One command to regenerate every processed dataset, table, figure and model output from raw sources.

Usage: python3 research/analysis/run_all.py   (raw filings must be present: see fetch_sources.py)
"""
import runpy
from pathlib import Path

HERE = Path(__file__).parent
for step in ["lvs_extract", "dicj_extract", "panel", "peers_extract", "public_analysis", "economics", "scenarios",
             "holdout_analysis", "verify_facts"]:
    print(f"== {step}")
    runpy.run_path(str(HERE / f"{step}.py"), run_name="__main__")
