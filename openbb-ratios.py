import sys
import json
from openbb import obb
import yfinance as yf

symbol = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

def safe_get(obj, attr, default=None):
    if obj is None:
        return default
    if hasattr(obj, 'model_extra') and obj.model_extra:
        return obj.model_extra.get(attr, default)
    return getattr(obj, attr, default)

try:
    result = obb.equity.fundamental.metrics(symbol=symbol, provider='yfinance')
    if not result or not result.results:
        print(json.dumps({"error": "No data found", "symbol": symbol}))
        sys.exit(1)
    
    data = result.results[0]
    
    # Get forward P/E directly from yfinance (not exposed by OpenBB)
    ticker = yf.Ticker(symbol)
    info = ticker.info
    forward_pe = info.get('forwardPE')
    
    output = {
        "symbol": symbol,
        "pe_ratio": safe_get(data, 'pe_ratio'),
        "forward_pe": forward_pe,
        "profit_margin": safe_get(data, 'profit_margin'),
        "return_on_equity": safe_get(data, 'return_on_equity'),
        "debt_to_equity": safe_get(data, 'debt_to_equity'),
        "current_ratio": safe_get(data, 'current_ratio'),
    }
    print(json.dumps(output, indent=2))
except Exception as e:
    print(json.dumps({"error": str(e), "symbol": symbol}))
    sys.exit(1)
