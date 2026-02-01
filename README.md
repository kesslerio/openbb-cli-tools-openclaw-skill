# OpenBB CLI Tools

Bash wrapper scripts for the [OpenBB SDK](https://openbb.co/) providing quick CLI access to stock data.

## Requirements

- Python 3.11+ with OpenBB SDK installed
- `jq` (used by `openbb-quote` for multi-ticker support)
- NixOS: scripts handle `LD_LIBRARY_PATH` automatically
- Optional: FMP API key for enhanced data (see below)

## Tools

| Script | Description | Default Provider |
|--------|-------------|------------------|
| `openbb-quote` | Current price, OHLCV | yfinance (supports fmp, intrinio) |
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

**Note:** `openbb-get-quote` also exists as a simpler Python alternative to `openbb-quote`.

## Usage

```bash
openbb-quote AAPL
openbb-quote AAPL MSFT GOOGL        # Multiple tickers
openbb-quote AAPL fmp               # Specify provider
openbb-ratios MSFT
openbb-financials GOOGL income 5   # 5 years of income statements
openbb-historical NVDA 1y
```

All output is JSON.

## Installation

1. Install OpenBB SDK: `pip install openbb`
2. Install jq: `apt install jq` / `brew install jq` / `nix-shell -p jq`
3. Add scripts to PATH: `export PATH="/path/to/scripts:$PATH"`
4. (Optional) Set `FMP_API_KEY` for enhanced earnings/ownership data (see below)

## Data Providers

### yfinance (Default - Free, No API Key)

Most tools use yfinance by default, which is free and requires no API key. Works for:
- Price quotes, OHLCV data
- Financial statements (income, balance sheet, cash flow)
- Key ratios and metrics
- Dividend history
- Analyst estimates and recommendations
- Technical indicators
- Next earnings date

### FMP (Financial Modeling Prep)

Some tools benefit from FMP for additional data. Some tools fall back to FMP automatically.

#### Getting an FMP API Key

1. Sign up at [financialmodelingprep.com](https://site.financialmodelingprep.com/register)
2. Get your API key from the dashboard
3. Set the environment variable:
   ```bash
   export FMP_API_KEY="your_api_key_here"
   ```

See [FMP pricing](https://site.financialmodelingprep.com/developer/docs/pricing) for current tier limits and features.

#### What Each Tool Uses

| Tool | Without FMP | With FMP (paid) |
|------|-------------|-----------------|
| `openbb-quote` | yfinance (default) | Can specify `fmp` as provider arg |
| `openbb-estimates` | yfinance, then tries fmp fallback | Enhanced estimates data |
| `openbb-earnings` | Next earnings date (yfinance) | + Historical EPS with beat/miss tracking |
| `openbb-ownership` | Falls back to intrinio/sec | Full institutional ownership data |

#### Recommendation

- **Most users**: The yfinance-based tools cover typical needs (quotes, financials, ratios, dividends, estimates)
- **Active traders**: Consider FMP for earnings surprise tracking
- **Institutional analysis**: FMP provides richer ownership data

## License

MIT
