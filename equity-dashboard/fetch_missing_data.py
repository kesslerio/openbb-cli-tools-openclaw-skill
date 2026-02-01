#!/usr/bin/env python3
"""
Phase 2: Fetch Missing Data for Q3/25 Stocks

Uses OpenBB to batch-fetch missing metrics for stocks with incomplete data.
"""

import os
import subprocess
import json
import sys
from datetime import datetime

# Stocks with missing Q3/25 or Q4/25 data
STOCKS_TO_UPDATE = [
    "AMPL", "DKNG", "DOCN", "DOCU", "DT", "EA", "ETSY", "EXPE", "FROG", "FSLY",
    "FTNT", "GLBE", "GME", "GTLB", "NET", "NFLX", "NOW", "OKTA", "OSTK", "PAYC",
    "ROKU", "S", "SHOP", "SNAP", "SNOW", "SPOT", "SQ", "TEAM", "TTD", "TWLO",
    "U", "UBER", "W", "WDAY", "ZI", "ZM", "ZS"
]

OUTPUT_FILE = "/home/art/clawd/reports/equity/phase2_updates.json"

def run_openbb(command):
    """Run OpenBB command and return parsed JSON."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        pass
    return {}

def fetch_stock_data(ticker):
    """Fetch missing data for a single stock."""
    data = {"ticker": ticker, "timestamp": datetime.now().isoformat()}
    
    # Get quote data
    quote = run_openbb(f"openbb-quote {ticker}")
    data["price"] = quote.get("price")
    data["prev_close"] = quote.get("prev_close")
    
    # Get ratios
    ratios = run_openbb(f"openbb-ratios {ticker}")
    data["trailing_pe"] = ratios.get("pe_ratio")
    data["forward_pe"] = ratios.get("forward_pe")
    data["profit_margin"] = ratios.get("profit_margin")
    data["operating_margin"] = ratios.get("operating_margin")
    data["gross_margin"] = ratios.get("gross_margin")
    
    # Get growth
    growth = run_openbb(f"openbb-growth-profile {ticker}")
    data["revenue_growth"] = growth.get("revenue_growth")
    data["earnings_growth"] = growth.get("earnings_growth")
    
    return data

def main():
    print(f"Phase 2: Fetching data for {len(STOCKS_TO_UPDATE)} stocks...", flush=True)
    
    results = []
    for i, ticker in enumerate(STOCKS_TO_UPDATE):
        print(f"[{i+1}/{len(STOCKS_TO_UPDATE)}] {ticker}...", end=" ", flush=True)
        data = fetch_stock_data(ticker)
        fields = len([v for v in data.values() if v])
        print(f"{fields} fields", flush=True)
        results.append(data)
    
    # Save results
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone! Saved to {OUTPUT_FILE}", flush=True)

if __name__ == "__main__":
    main()
