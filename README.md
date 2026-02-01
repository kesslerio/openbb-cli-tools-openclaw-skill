# OpenBB CLI Tools

Bash wrapper scripts for the [OpenBB SDK](https://openbb.co/) providing quick CLI access to stock data.

## Requirements

- Python 3.11+ with OpenBB SDK installed
- NixOS: scripts handle `LD_LIBRARY_PATH` automatically
- API keys: yfinance (free, default), FMP (optional, for earnings/ownership)

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
| `openbb-earnings` | EPS history, beat rate | FMP (paid) |
| `openbb-ownership` | Institutional ownership | FMP (paid) |

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
3. (Optional) Set `FMP_API_KEY` for earnings/ownership data

## License

MIT
