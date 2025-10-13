from enum import Enum
from app.portfolio.stock_tracker.cache_utils import get_yf_cached_info

class AssetType(Enum):
    ASSET = "Asset"
    STOCK = "Stock"
    GOV_BILL = "GovernmentBill"
    OPTION = "Option"
    CUSTOM = "Custom"


class Currency(Enum):
    EUR = "EUR"
    USD = "USD"
    GBP = "GBp"

    def get_conversion_rate(self, ttl=60):
        ticker = f"{self.name}EUR=X"
        info = get_yf_cached_info(ticker, ttl=ttl)
        rate = info.get("previousClose")
        return rate


class OptionType(Enum):
    CALL = "Call"
    PUT = "Put"


class TransactionType(Enum):
    BUY = "Buy"
    SELL = "Sell"
