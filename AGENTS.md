# AGENTS.md — OpenBB CLI Tools (OpenClaw Skill)

> Canonical agent instructions for this project. `CLAUDE.md` symlinks here.
> Windsurf workspace rules (`.windsurfrules`) also reference this file.

## Project Overview

OpenClaw skill providing stock market data via OpenBB SDK CLI wrappers. All 18 scripts live in `scripts/` and emit **JSON to stdout**. Errors go to stderr.

- **Language:** Bash (wrappers) + embedded Python (OpenBB SDK calls)
- **Runtime:** Python 3.11+ with `openbb` package, `jq` for multi-ticker
- **Default data provider:** yfinance (free, no API key)
- **Optional provider:** FMP (requires `FMP_API_KEY` env var)

## Repository Structure

```
.
├── AGENTS.md          # Agent instructions (this file)
├── CLAUDE.md          # Symlink → AGENTS.md
├── .windsurfrules     # Windsurf workspace rules (references this file)
├── README.md          # User-facing documentation
├── SKILL.md           # OpenClaw skill manifest (frontmatter + docs)
└── scripts/
    ├── _openbb_common.sh       # Shared helpers (python resolution, retry logic, NixOS LD_LIBRARY_PATH)
    ├── openbb-quote            # Current price, OHLCV (multi-ticker)
    ├── openbb-get-quote        # Current price (single ticker, Python-only)
    ├── openbb-ratios           # P/E, P/S, margins, ROE, debt/equity
    ├── openbb-profile          # Company info
    ├── openbb-growth-profile   # Revenue/earnings growth, margin trends
    ├── openbb-financials       # Income/cash flow statements
    ├── openbb-quality          # Quality score (0-10) with breakdown
    ├── openbb-historical       # YTD/1y/3y/5y price returns
    ├── openbb-valuation        # Fair value estimates
    ├── openbb-volatility       # Beta, std dev, Sharpe
    ├── openbb-technicals       # SMA 50/200, cross signals
    ├── openbb-metrics          # Key valuation multiples
    ├── openbb-ev-ntm           # EV/NTM revenue
    ├── openbb-dividend         # Dividend yield, history, safety
    ├── openbb-estimates        # Analyst targets, recommendations
    ├── openbb-earnings         # Next earnings + EPS history
    ├── openbb-ownership        # Institutional ownership
    └── openbb-cli-fallback     # Raw OpenBB CLI passthrough
```

## Code Conventions

- **Shell style:** `set -euo pipefail` in every script; POSIX-compatible where possible
- **Shared code:** All scripts source `_openbb_common.sh` for `resolve_openbb_python`, `resolve_openbb_provider`, `setup_openbb_ld_library_path`, and `run_openbb_python_with_retry`. This file also auto-sources `.env` from project root for local testing.
- **Python embedding:** Inline heredocs (`<< 'PYTHON'`) executed via `run_openbb_python_with_retry`
- **Environment variables** pass data from Bash → Python (prefixed `_OPENBB_`)
- **Output contract:** Every script prints valid JSON to stdout; never mix stderr into stdout
- **Provider resolution:** CLI arg → `OPENBB_DEFAULT_PROVIDER` env var → `yfinance` (via `resolve_openbb_provider`)
- **Error handling:** Scripts return non-zero on failure; Python exceptions are caught and emitted as `{"symbol": "...", "error": "..."}`

## Key Patterns

### Adding a New Wrapper Script

1. Create `scripts/openbb-<name>` (executable, `#!/usr/bin/env bash`)
2. Add `set -euo pipefail` and source `_openbb_common.sh`
3. Parse ticker + optional provider from args; use `resolve_openbb_provider` for provider resolution
4. Use `run_openbb_python_with_retry` with an inline Python heredoc
5. Output JSON to stdout; errors to stderr
6. Update the tool table in both `README.md` and `SKILL.md`

### Provider Routing

`resolve_openbb_provider` in `_openbb_common.sh` resolves the data provider with this priority:
1. Explicit CLI argument (passed as first param)
2. `OPENBB_DEFAULT_PROVIDER` environment variable
3. Fallback default (second param, typically `yfinance`)

This enables per-command overrides (`openbb-ratios AAPL fmp`) and global overrides (`OPENBB_DEFAULT_PROVIDER=fmp`) for Asian market tickers where yfinance is slow.

### Retry / Rate Limiting

`run_openbb_python_with_retry` handles OpenBB `.build.lock` contention with exponential backoff. Configurable via:
- `OPENBB_RETRY_MAX_ATTEMPTS` (default: 6)
- `OPENBB_RETRY_BASE_DELAY_SEC` (default: 2)

### NixOS Compatibility

`setup_openbb_ld_library_path` auto-detects NixOS and sets `LD_LIBRARY_PATH` for `libstdc++` and `zlib`.

## Development Commands

```bash
# Test a single script
./scripts/openbb-quote AAPL

# Test with specific provider
./scripts/openbb-quote AAPL fmp

# Global provider override (useful for Asian tickers)
OPENBB_DEFAULT_PROVIDER=fmp ./scripts/openbb-quote 7203.T

# Multi-ticker
./scripts/openbb-quote AAPL MSFT GOOGL

# Financial statements (type + years)
./scripts/openbb-financials GOOGL income 5

# Validate JSON output
./scripts/openbb-ratios MSFT | jq .

# Check all scripts are executable
ls -la scripts/openbb-*
```

## Important Constraints

- **Do not** hardcode API keys. Use environment variables (`FMP_API_KEY`, `OPENBB_PYTHON`, `OPENBB_DEFAULT_PROVIDER`).
- **Do not** print non-JSON to stdout in wrapper scripts.
- **Do not** modify `_openbb_common.sh` without testing all scripts that source it.
- **Do not** add Python package imports beyond what `openbb` provides without updating `README.md` requirements.
- **Prefer** `yfinance` as default provider (free, no key required).
- **Keep** `SKILL.md` frontmatter in sync with `README.md` tool table when adding/removing scripts.
- **ShellCheck** clean: run `shellcheck scripts/*` before committing.

## Command Selection Policy

1. Use `openbb-*` wrapper scripts first — they provide stable JSON contracts.
2. Use `openbb-cli-fallback` only when no wrapper covers the endpoint.
3. If a fallback pattern repeats, promote it to a dedicated wrapper.

## GitHub Hygiene

- PR title default: `type(scope): imperative summary`.
- Issue title defaults:
  - Feature: `feat: <capability> (for <surface>)`
  - Bug: `bug: <symptom> when <condition>`
  - Tracking: `TODO: <cleanup> after <dependency>`
- PR body required sections: `What`, `Why`, `Tests`, `AI Assistance`.
- `Tests` should be exact commands (for this repo, include script invocations and `shellcheck` where relevant).
