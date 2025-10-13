from abc import ABC, abstractmethod

ERROR_NOT_IMPLEMENTED = "function not implemented"


class StockInterface(ABC):
    def __init__(self, ticker):
        self.ticker = ticker

    @abstractmethod
    def can_live_track(self):
        raise Exception(ERROR_NOT_IMPLEMENTED)

    @abstractmethod
    def get_price(self):
        raise Exception(ERROR_NOT_IMPLEMENTED)

    @abstractmethod
    def process_model(self, form, model):
        raise Exception(ERROR_NOT_IMPLEMENTED)
