# T25 — Reproducibility check

**Reproduced revision:** `586419ede7dcb6525c097a9147fe544b26438515` (2026-11-13), fresh `git clone` into an empty directory.
Later commits that touch only this log do not change any analysed file.

| Mode | Command | Result |
|---|---|---|
| From committed processed data (spec §15.7) | `python3 research/analysis/run_all.py --from-processed` | exit 0; `git diff` on research/data/processed, research/outputs (excl. PNG figures): **0 files changed** |
| Full, from primary sources | `python3 research/analysis/fetch_sources.py` then `python3 research/analysis/run_all.py` | 66/66 sources re-downloaded, 66/66 SHA-256 match the register; exit 0; `git diff` on processed data, outputs and sources (excl. PNG): **0 files changed** |
| CI | `.github/workflows/ci.yml` step "one-command rebuild … byte-identical" | Same `--from-processed` check with `git diff --exit-code` |

History: an earlier run (pre-`586419e`) hit one transient TLS error on a DICJ download; `fetch_sources.py`
now retries (`--retry 5 --retry-all-errors`). PNG figures are regenerated but not hash-compared because
matplotlib output can vary with installed fonts.
