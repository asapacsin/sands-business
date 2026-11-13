# T25 — Reproducibility check (2026-11-13)

Procedure: `git clone` of the committed repository into an empty directory →
`python3 research/analysis/fetch_sources.py` → `python3 research/analysis/run_all.py` →
SHA-256 comparison of every regenerated data and output file with the committed versions.

| Step | Result |
|---|---|
| Source re-download (66 registered sources: 16 LVS, 46 peer, 4 DICJ) | 66/66 downloaded, 66/66 SHA-256 match the source register |
| First attempt | One DICJ download failed with a TLS connect error (curl exit 35). Fixed by adding `--retry 5 --retry-all-errors` to `fetch_sources.py`; rerun clean |
| `run_all.py` | exit 0 |
| Regenerated files compared (processed CSVs, outputs JSON, output tables, fact verification) | 18/18 byte-identical |
| Figures (PNG) | Regenerated; not hash-compared (matplotlib embeds build metadata) |
