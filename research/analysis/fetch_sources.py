"""Re-download every raw source registered in sources/source_register.csv (SEC EDGAR, DICJ) and
verify SHA-256 where recorded. A generic User-Agent is used, as SEC asks automated clients to identify
themselves; replace it with your own contact before heavy use."""
import csv
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "independent-research-script contact@example.com"
DEST = {"LVS-ER": "data/raw/lvs/{d}_ex991.htm"}

for row in csv.DictReader(open(ROOT / "sources/source_register.csv")):
    sid, url = row["source_id"], row["url"]
    if sid.startswith("LVS-ER-"):
        out = ROOT / f"data/raw/lvs/{sid[7:]}_ex991.htm"
    elif sid.startswith("DICJ-Q-"):
        out = ROOT / f"data/raw/dicj/q_{sid[7:]}.xml"
    elif "-ER-" in sid:
        op, d = sid.split("-ER-")
        out = ROOT / f"data/raw/peers/{op.lower()}_{d}.htm"
    else:
        continue
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        subprocess.run(["curl", "-s", "-L", "--retry", "5", "--retry-all-errors", "--retry-delay", "2", "-A", UA, url, "-o", str(out)], check=True)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    expected = row.get("sha256_of_downloaded_file")
    status = "ok" if not expected or expected == digest else "HASH MISMATCH (source may have been re-published)"
    print(sid, status)
