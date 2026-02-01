# OpenBB CLI Tools

Bash wrapper scripts for the [OpenBB SDK](https://openbb.co/) providing quick CLI access to stock data.

## Requirements

- Python 3.11+ with OpenBB SDK installed
- NixOS: scripts handle `LD_LIBRARY_PATH` automatically
- API keys: yfinance (free, default), FMP (optional, see below)

## Tools

| Script | Description | Provider |
|--------|-------------|----------|
| `openbb-quote` | Current price, OHLCV | yfinance |
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
| `openbb-estimates` | Analyst targets, recommendations | yfinance |
| `openbb-earnings` | EPS history, beat rate | FMP |
| `openbb-ownership` | Institutional ownership | FMP |

## Usage

```bash
openbb-quote AAPL
openbb-ratios MSFT
openbb-financials GOOGL income 5  # 5 years of income statements
openbb-historical NVDA 1y
```

All output is JSON.

## Installation

1. Install OpenBB SDK: `pip install openbb`
2. Add scripts to PATH: `export PATH="/path/to/scripts:$PATH"`
3. (Optional) Set `FMP_API_KEY` for earnings/ownership data (see below)

## Data Providers

### yfinance (Default - Free)

Most tools use yfinance, which is free and requires no API key. Works for:
- Price quotes, OHLCV data
- Financial statements (income, balance sheet, cash flow)
- Key ratios and metrics
- Dividend history
- Analyst estimates and recommendations
- Technical indicators

### FMP (Financial Modeling Prep)

Two tools require FMP: `openbb-earnings` and `openbb-ownership`.

#### Getting an FMP API Key

1. Sign up at [financialmodelingprep.com](https://site.financialmodelingprep.com/register)
2. Get your API key from the dashboard
3. Set the environment variable:
   ```bash
   export FMP_API_KEY="your_api_key_here"
   ```

#### FMP Tier Comparison

| Feature | Free Tier | Paid Tier (~$20-30/mo) |
|---------|-----------|------------------------|
| Earnings calendar (upcoming dates) | ✅ | ✅ |
| Historical EPS (beat/miss history) | ❌ | ✅ |
| Institutional ownership | ❌ | ✅ |
| API rate limits | 250/day | Higher |
| Historical data depth | Limited | Full |

#### What Each Tool Needs

| Tool | Free FMP | Paid FMP | Notes |
|------|----------|----------|-------|
| `openbb-earnings` | Partial | Full | Free tier gets earnings calendar only; paid tier adds historical EPS with beat/miss tracking |
| `openbb-ownership` | ❌ | ✅ | Requires paid FMP subscription |

#### Recommendation

- **Most users**: The 14 yfinance-based tools cover typical needs (quotes, financials, ratios, dividends, estimates)
- **Active traders**: Consider paid FMP for earnings surprise tracking
- **Institutional analysis**: Paid FMP required for ownership data

## License

MIT
