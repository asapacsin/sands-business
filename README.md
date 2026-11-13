# sands-business

Independent business research on Sands China using public information only, run under the
[AI-native engineering](https://github.com/asapacsin/ai-native-engineering) practice
(installed from upstream commit `1a161b8`).

> Not affiliated with, endorsed by, or using internal information from Sands China Ltd. or Las Vegas Sands Corp.

## Start here

| What | Where |
|---|---|
| Research specification (decision, methods, task cards, acceptance) | [`research/RESEARCH_SPEC.md`](research/RESEARCH_SPEC.md) |
| Task backlog (dependency frontier) | [`research/work.json`](research/work.json) |
| Task contract for the spec | [`contracts/research-spec.json`](contracts/research-spec.json) |
| Agent operating contract | [`AGENTS.md`](AGENTS.md), [`CLAUDE.md`](CLAUDE.md) |
| AI-native method and enforcement docs | [`docs/`](docs/) |

## Verify

```bash
python3 -m unittest discover -s tests
python3 scripts/check_research_spec.py research/RESEARCH_SPEC.md
python3 scripts/frontier.py next --registry research/work.json
python3 scripts/ai_native.py cycle --repo . --contract contracts/research-spec.json
```

The `cycle` command returns `NOT_VERIFIED` (exit 4) until an independent read-only reviewer CLI is
configured in `AI_NATIVE_REVIEWER_CMD` — see [`docs/INTEGRATION.md`](docs/INTEGRATION.md). Passing
gates alone is not a PASS.

## Installed AI-native components

- `scripts/` — controller (`ai_native.py`), deterministic control plane, governance, frontier,
  supervisor, pre-tool guard, Codex bridge; plus `check_research_spec.py` (project gate).
- `.claude/settings.json` — PreToolUse guard and Stop hook. Both are **off** unless
  `AI_NATIVE_GUARD_ENABLED=1` / `AI_NATIVE_STOP_ENABLED=1` (and `AI_NATIVE_CONTRACT_PATH`) are set.
  Hook commands use `$CLAUDE_PROJECT_DIR` so they work from any working directory.
- `.github/workflows/ci.yml` — runs controller tests and the research-spec gates.
- Upstream `adapters/` (Aurel/Android) and `scripts/publish.ps1` were not copied; they do not apply here.
