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

Specify provider:
```bash
./scripts/openbb-quote AAPL fmp
```

CLI fallback:
```bash
./scripts/openbb-cli-fallback --file ./my-routine.openbb
```

## Data Providers

### yfinance (Default - Free, No API Key)

Most tools use yfinance by default. Works for quotes, financials, ratios, dividends, estimates, technicals.

### FMP (Optional)

Some tools benefit from FMP for additional data:

| Tool | Without FMP | With FMP (paid) |
|------|-------------|-----------------|
| `openbb-earnings` | Next earnings date (yfinance) | + Historical EPS with beat/miss tracking |
| `openbb-ownership` | Falls back to intrinio/sec | Full institutional ownership data |

Setup:
1. Sign up at [financialmodelingprep.com](https://site.financialmodelingprep.com/register)
2. `export FMP_API_KEY="your_key"`

See [FMP pricing](https://site.financialmodelingprep.com/developer/docs/pricing) for tier details.

## License

MIT
