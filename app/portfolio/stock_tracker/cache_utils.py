import yfinance as yf
import time

def get_yf_cached_info(ticker, ttl=600):
    if not hasattr(get_yf_cached_info, "_cache"):
        get_yf_cached_info._cache = {}
    _yf_cache = get_yf_cached_info._cache
    now = time.time()
    cache_entry = _yf_cache.get((ticker, ttl))
    if cache_entry:
        cached_time, data = cache_entry
        if now - cached_time < ttl:
            return data
    ticker_data = yf.Ticker(ticker)
    info = ticker_data.info
    _yf_cache[(ticker, ttl)] = (now, info)
    return info 