import os
import sys
import json
from openbb import obb

symbol = sys.argv[1] if len(sys.argv) > 1 else "GOOGL"
statement = sys.argv[2] if len(sys.argv) > 2 else "all"
years = int(sys.argv[3]) if len(sys.argv) > 3 else 5

def safe_get(obj, attr, default=None):
    if obj is None:
        return default
    if hasattr(obj, 'model_extra') and obj.model_extra:
        return obj.model_extra.get(attr, default)
    return getattr(obj, attr, default)

def calc_cagr(start, end, years):
    if start and end and start > 0 and end > 0 and years > 0:
        return (end / start) ** (1/years) - 1
    return None

def calc_yoy(current, prior):
    if current and prior and prior != 0:
        return (current - abs(prior)) / abs(prior)
    return None

def fetch_statement(symbol, stmt_type, limit):
    try:
        if stmt_type == 'income':
            return obb.equity.fundamental.income(symbol=symbol, provider='yfinance', limit=limit)
        elif stmt_type == 'balance':
            return obb.equity.fundamental.balance(symbol=symbol, provider='yfinance', limit=limit)
        elif stmt_type == 'cash':
            return obb.equity.fundamental.cash(symbol=symbol, provider='yfinance', limit=limit)
    except:
        return None

def process_income(data):
    if not data or not data.results:
        return None
    
    periods = []
    revenues = []
    net_incomes = []
    
    for item in data.results:
        period = {
            "date": str(safe_get(item, 'period_ending', '')),
            "revenue": safe_get(item, 'total_revenue'),
            "gross_profit": safe_get(item, 'gross_profit'),
            "operating_income": safe_get(item, 'operating_income'),
            "net_income": safe_get(item, 'net_income'),
            "eps_diluted": safe_get(item, 'diluted_earnings_per_share'),
        }
        
        if period['revenue'] and period['revenue'] > 0:
            if period['gross_profit']:
                period['gross_margin'] = round(period['gross_profit'] / period['revenue'], 4)
            if period['net_income']:
                period['net_margin'] = round(period['net_income'] / period['revenue'], 4)
        
        periods.append(period)
        revenues.append(period['revenue'])
        net_incomes.append(period['net_income'])
    
    for i in range(len(periods) - 1):
        periods[i]['revenue_yoy'] = round(calc_yoy(revenues[i], revenues[i+1]), 4) if i < len(revenues)-1 else None
        periods[i]['net_income_yoy'] = round(calc_yoy(net_incomes[i], net_incomes[i+1]), 4) if i < len(net_incomes)-1 else None
    
    return {"periods": periods}

try:
    output = {"symbol": symbol, "statement": statement}
    
    if statement in ['income', 'all']:
        income_data = fetch_statement(symbol, 'income', years)
        output['income'] = process_income(income_data)
    
    print(json.dumps(output, indent=2, default=str))

except Exception as e:
    print(json.dumps({"error": str(e), "symbol": symbol}))
    sys.exit(1)
