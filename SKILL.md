---
name: openbb
description: "Stock market data via OpenBB SDK. Get quotes, financials, ratios, dividends, earnings, estimates, ownership, technicals, and valuations. Use when user asks about stocks, tickers (AAPL, MSFT, etc.), stock prices, financial ratios, P/E, dividends, analyst targets, or equity research."
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["jq"],"env":[]}}}
---

# OpenBB Stock Data Skill 📈

Fetch stock market data using OpenBB SDK CLI wrappers. All output is JSON.

## Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `openbb-quote` | Current price, OHLCV (multi-ticker) | `openbb-quote AAPL` |
| `openbb-get-quote` | Current price (single ticker) | `openbb-get-quote AAPL` |
| `openbb-ratios` | P/E, margins, ROE, debt | `openbb-ratios MSFT` |
| `openbb-financials` | Income/cash flow statements | `openbb-financials GOOGL income 5` |
| `openbb-growth-profile` | Revenue/earnings growth | `openbb-growth-profile NVDA` |
| `openbb-dividend` | Yield, history, safety | `openbb-dividend JNJ` |
| `openbb-estimates` | Analyst targets, recommendations | `openbb-estimates TSLA` |
| `openbb-earnings` | Next earnings + EPS history | `openbb-earnings AMZN` |
| `openbb-quality` | Quality score (0-10) | `openbb-quality META` |
| `openbb-valuation` | Fair value estimates | `openbb-valuation NFLX` |
| `openbb-volatility` | Beta, Sharpe, drawdown | `openbb-volatility AMD` |
| `openbb-technicals` | SMA 50/200, cross signals | `openbb-technicals SPY` |
| `openbb-historical` | Price returns (1y/3y/5y) | `openbb-historical AAPL 1y` |
| `openbb-metrics` | Key valuation multiples | `openbb-metrics COST` |
| `openbb-ev-ntm` | EV/NTM revenue | `openbb-ev-ntm CRM` |
| `openbb-profile` | Company info | `openbb-profile DIS` |
| `openbb-ownership` | Institutional ownership | `openbb-ownership AAPL` |
| `openbb-cli-fallback` | Raw OpenBB CLI passthrough for uncovered cases | `openbb-cli-fallback --help` |

## Command Selection Policy

1. Use wrapper scripts first (`openbb-quote`, `openbb-ratios`, etc.).
2. Use `openbb-cli-fallback` only if wrappers do not cover the requested endpoint/workflow.
3. Treat CLI output as non-stable text output unless you explicitly control the routine and output format.

## Usage Patterns

### Single Stock Query
```bash
# Get current quote
<skill>/scripts/openbb-quote AAPL

# Get key ratios
<skill>/scripts/openbb-ratios AAPL
```

### Multiple Tickers
```bash
# openbb-quote supports multiple tickers
<skill>/scripts/openbb-quote AAPL MSFT GOOGL
```

### Specify Provider
```bash
# Default is yfinance (free), can specify fmp/intrinio
<skill>/scripts/openbb-quote AAPL fmp
```

### Financial Statements
```bash
# Income statement, 5 years
<skill>/scripts/openbb-financials AAPL income 5

# Cash flow statement, 3 years  
<skill>/scripts/openbb-financials AAPL cash 3
```

### CLI Fallback (Uncovered Endpoints)
```bash
# Run a routine file through OpenBB CLI
<skill>/scripts/openbb-cli-fallback --file ./my-routine.openbb
```

## Data Providers

### Provider Selection

All scripts respect the `OPENBB_DEFAULT_PROVIDER` environment variable. Resolution order:

1. **CLI argument** (e.g., `openbb-ratios AAPL fmp`) — highest priority
2. **`OPENBB_DEFAULT_PROVIDER` env var** — global override
3. **`yfinance`** — default fallback (free, no API key)

Most scripts accept an optional `[provider]` CLI argument; `openbb-financials` and `openbb-historical` currently rely on `OPENBB_DEFAULT_PROVIDER` only.

### yfinance (Default - Free, No API Key)
All tools use yfinance by default. Works for quotes, financials, ratios, dividends, estimates, technicals.

### FMP (Optional - Enhanced Data)
Some tools benefit from FMP for additional data:

| Tool | Without FMP | With FMP |
|------|-------------|----------|
| `openbb-earnings` | Next earnings date only | + Historical EPS with beat/miss |
| `openbb-ownership` | Falls back to intrinio/sec | Full institutional data |
| `openbb-estimates` | yfinance consensus | Enhanced estimates |

**Setup FMP (optional):**
1. Sign up at [financialmodelingprep.com](https://site.financialmodelingprep.com/register)
2. Set environment variable: `export FMP_API_KEY="your_key"`

See [FMP pricing](https://site.financialmodelingprep.com/developer/docs/pricing) for tier details.

### Asian Market Tickers (.T, .TW, .HK)

yfinance supports Asian exchange tickers but can be slow (~9s per call). Use `OPENBB_DEFAULT_PROVIDER` or per-command provider arg for better latency:

```bash
# Per-command
<skill>/scripts/openbb-quote 7203.T fmp

# Global override for batch queries
export OPENBB_DEFAULT_PROVIDER=fmp
<skill>/scripts/openbb-quote 7203.T
<skill>/scripts/openbb-ratios 2330.TW
```

## Output Formatting

All scripts output JSON. When presenting to users:

**For chat channels:** Summarize key metrics in natural language, e.g.:
> AAPL is trading at $259.48 (+0.46%). P/E: 32.9, Dividend yield: 0.4%. Analysts rate it a BUY with average target $291 (+12% upside).

**For detailed analysis:** Format as markdown table or structured list.

## Common Workflows

### Quick Stock Check
User: "How's Apple doing?"
```bash
<skill>/scripts/openbb-quote AAPL
<skill>/scripts/openbb-ratios AAPL
```

### Dividend Analysis
User: "Is JNJ a good dividend stock?"
```bash
<skill>/scripts/openbb-dividend JNJ
<skill>/scripts/openbb-financials JNJ cash 3  # Check FCF coverage
```

### Earnings Preview
User: "When does GOOGL report earnings?"
```bash
<skill>/scripts/openbb-earnings GOOGL
<skill>/scripts/openbb-estimates GOOGL
```

### Valuation Check
User: "Is NVDA overvalued?"
```bash
<skill>/scripts/openbb-valuation NVDA
<skill>/scripts/openbb-ratios NVDA
<skill>/scripts/openbb-growth-profile NVDA
```

## Requirements

- Python 3.11+ with OpenBB SDK (`pip install openbb`)
- `jq` (used by openbb-quote for multi-ticker support)
- NixOS: Scripts handle `LD_LIBRARY_PATH` automatically

## Troubleshooting

**"No such file" errors:** Ensure OpenBB venv exists at `/home/art/.local/venvs/openbb/`

**Empty results:** Some endpoints need paid FMP subscription. Check the "Data Providers" section.

**Timeout:** Some queries are slow on first run (SDK initialization). Retry usually works.

**Need an endpoint not covered by wrappers:** Use `openbb-cli-fallback --file <routine.openbb>` as temporary fallback, then add a dedicated wrapper for repeat usage.

**OpenBB build lock contention (`.build.lock`):**
- `openbb-quote` now retries automatically with exponential backoff when another OpenBB process is building extensions.
- Tune behavior with environment variables:
  - `OPENBB_RETRY_MAX_ATTEMPTS` (default: `6`)
  - `OPENBB_RETRY_BASE_DELAY_SEC` (default: `2`)
