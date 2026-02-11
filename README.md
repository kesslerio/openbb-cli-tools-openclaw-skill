# OpenBB Stock Data Skill 📈

OpenClaw skill for fetching stock market data via OpenBB SDK.

## Installation

```bash
# Clone to your skills directory
git clone https://github.com/kesslerio/openbb-cli-tools-openclaw-skill ~/.openclaw/skills/openbb

# Or symlink if cloned elsewhere
ln -s /path/to/openbb-cli-tools-openclaw-skill ~/.openclaw/skills/openbb
```

## Requirements

- Python 3.11+ with OpenBB SDK: `pip install openbb`
- `jq` for multi-ticker support
- (Optional) FMP API key for enhanced earnings/ownership data

## Local Configuration (.env)

Scripts automatically source a `.env` file from the project root for local testing:

```bash
# Copy the example and edit
cp .env.example .env

# Add your API keys and preferences
# FMP_API_KEY=your_key_here
# OPENBB_DEFAULT_PROVIDER=fmp
```

All environment variables are gitignored and sourced by `scripts/_openbb_common.sh`.

## Tools

| Script | Description | Default Provider |
|--------|-------------|------------------|
| `openbb-quote` | Current price, OHLCV (multi-ticker) | yfinance (supports fmp, intrinio) |
| `openbb-get-quote` | Current price (single ticker, Python) | yfinance |
| `openbb-ratios` | P/E, P/S, margins, ROE, debt/equity | yfinance |
| `openbb-profile` | Company info (name, sector, employees) | yfinance |
| `openbb-growth-profile` | Revenue/earnings growth, margin trends | yfinance |
| `openbb-financials` | Income/cash flow statements | yfinance |
| `openbb-quality` | Quality score (0-10) with breakdown | yfinance |
| `openbb-historical` | YTD/1y/3y/5y price returns | yfinance |
| `openbb-valuation` | Fair value estimates | yfinance |
| `openbb-volatility` | Beta, standard deviation, Sharpe | yfinance |
| `openbb-technicals` | SMA 50/200, cross signals | yfinance |
| `openbb-metrics` | Key valuation multiples | yfinance |
| `openbb-ev-ntm` | EV/NTM revenue | yfinance |
| `openbb-dividend` | Dividend yield, history, safety | yfinance |
| `openbb-estimates` | Analyst targets, recommendations | yfinance (falls back to fmp) |
| `openbb-earnings` | Next earnings + EPS history | yfinance + FMP |
| `openbb-ownership` | Institutional ownership | fmp (falls back to intrinio, sec) |
| `openbb-cli-fallback` | Raw OpenBB CLI passthrough for uncovered endpoints | OpenBB CLI |

## Command Policy

1. Use `openbb-*` wrappers first for automation and stable JSON contracts.
2. Use `openbb-cli-fallback` only when wrappers do not cover the requested endpoint/workflow.
3. If fallback usage repeats, promote it into a new dedicated wrapper.

## Usage

All scripts output JSON:

```bash
./scripts/openbb-quote AAPL
./scripts/openbb-ratios MSFT
./scripts/openbb-financials GOOGL income 5  # 5 years
./scripts/openbb-historical NVDA 1y
```

Multiple tickers:
```bash
./scripts/openbb-quote AAPL MSFT GOOGL
```

Specify provider per-command:
```bash
./scripts/openbb-quote AAPL fmp
./scripts/openbb-ratios 7203.T fmp
```

Override default provider globally (useful for Asian market tickers):
```bash
export OPENBB_DEFAULT_PROVIDER=fmp
./scripts/openbb-quote 7203.T
./scripts/openbb-ratios 7203.T
```

CLI fallback:
```bash
./scripts/openbb-cli-fallback --file ./my-routine.openbb
```

## Data Providers

### Provider Selection

All scripts respect the `OPENBB_DEFAULT_PROVIDER` environment variable. The resolution order is:

1. **CLI argument** (e.g., `openbb-ratios AAPL fmp`) — highest priority
2. **`OPENBB_DEFAULT_PROVIDER` env var** — global override
3. **`yfinance`** — default fallback (free, no API key)

Most scripts accept an optional `[provider]` CLI argument; `openbb-financials` and `openbb-historical` currently rely on `OPENBB_DEFAULT_PROVIDER` only.

### yfinance (Default - Free, No API Key)

Most tools use yfinance by default. Works for quotes, financials, ratios, dividends, estimates, technicals.

### FMP (Optional)

Some tools benefit from FMP for additional data:

| Tool | Without FMP | With FMP (paid) |
|------|-------------|------------------|
| `openbb-earnings` | Next earnings date (yfinance) | + Historical EPS with beat/miss tracking |
| `openbb-ownership` | Falls back to intrinio/sec | Full institutional ownership data |

Setup:
1. Sign up at [financialmodelingprep.com](https://site.financialmodelingprep.com/register)
2. `export FMP_API_KEY="your_key"`

See [FMP pricing](https://site.financialmodelingprep.com/developer/docs/pricing) for tier details.

### Asian Market Tickers (.T, .TW, .HK)

yfinance supports Asian exchange tickers but can be slow (~9s per call through OpenBB subprocess). Alternative providers may offer better latency:

| Provider | Package | Asian Market Coverage | Notes |
|----------|---------|----------------------|-------|
| FMP | `openbb-fmp` | Global equities incl. Japan/Taiwan/HK | Paid API key required |
| Tiingo | `openbb-tiingo` | US + some intl EOD | Worth testing for `.T`/`.TW` support |
| Alpha Vantage | `openbb-alphavantage` | Global equities, FX | Free tier is rate-limited |
| Polygon.io | `openbb-polygon` | US-focused, limited intl | May not cover `.T`/`.TW` |

To use FMP for Asian tickers:
```bash
# Per-command
./scripts/openbb-quote 7203.T fmp

# Global override
export OPENBB_DEFAULT_PROVIDER=fmp
./scripts/openbb-quote 7203.T
./scripts/openbb-ratios 2330.TW
./scripts/openbb-financials 9988.HK income 3
```

> **Note:** Finnhub is not a supported OpenBB provider (no `openbb-finnhub` package). It would require a custom provider extension — see [#14](https://github.com/kesslerio/openbb-cli-tools-openclaw-skill/issues/14).

## License

MIT
