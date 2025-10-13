import yfinance as yf
from datetime import datetime, date, timedelta
import time

from .base import StockInterface
from app.portfolio.enums import Currency, OptionType
from .historical_data import (
    populate_historical_data_from_csv,
    get_historical_price,
)

ERROR_STOCK_YAHOO = "stock not found on Yahoo Finance api"

NO_RESULTS_DICT = {"trailingPegRatio": None}


def get_currency_enum(currency):
    if currency == "EUR":
        return Currency.EUR
    elif currency == "USD":
        return Currency.USD
    elif currency == "GBp":
        return Currency.GBP
    return Currency.EUR


class YahooFinanceStock(StockInterface):
    def __init__(self, ticker):
        super().__init__(ticker)
        self.stock = yf.Ticker(ticker)
        print(self.stock)
        self.info = self.stock.info
        print(self.info)

    def get_exchange(self):
        return self.info.get("exchange")

    def get_currency(self):
        return self.info.get("currency")

    def get_long_name(self):
        return self.info.get("longName")

    def get_industry(self):
        return self.info.get("industry")

    def get_yahoo_price(self):
        current_price = self.info.get("currentPrice")
        if not current_price:
            current_price = self.info.get("navPrice")
        if not current_price:
            current_price = self.info.get("bid")
        if not current_price:
            raise Exception("no price found")
        return current_price

    def can_live_track(self):
        try:
            self.get_yahoo_price()
            return True
        except Exception:
            return False
    # TODO: function to long split this
    def get_price(self, date_input=None):
        if date_input:
            if isinstance(date_input, datetime):
                date_input = date.date()

            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())

            if date_input == today:
                yesterday = today - timedelta(days=1)
                hist_data = self.stock.history(start=yesterday, end=today)
                if not hist_data.empty:
                    hist_data_date = hist_data.index[0].date()
                    if hist_data_date == yesterday:
                        yesterday_close = hist_data.iloc[-1]["Close"]
                        if yesterday_close > 0:
                            return yesterday_close

                hist_data = self.stock.history(period="1d")
                if not hist_data.empty:
                    hist_data_date = hist_data.index[0].date()
                    if hist_data_date == today:
                        opening = hist_data.iloc[0]["Open"]
                        if opening > 0:
                            return opening

                raise Exception("No opening price available for today")

            if date_input == start_of_week:
                hist_data = self.stock.history(
                    start=date_input, end=date_input + timedelta(days=1)
                )
                if not hist_data.empty:
                    opening = hist_data.iloc[0]["Open"]
                    if opening > 0:
                        return opening
                raise Exception(
                    f"No opening price available for the beginning of the week ({date_input})"
                )

            else:
                hist_data = self.stock.history(
                    start=date_input, end=date_input + timedelta(days=1)
                )
                if not hist_data.empty:
                    return hist_data.iloc[0]["Close"]
                else:
                    raise Exception(
                        f"No closing price available for the date {date_input}"
                    )

        return self.get_yahoo_price()

    def process_model(self, _, model, fully_update):
        if self.info == NO_RESULTS_DICT:
            raise Exception(ERROR_STOCK_YAHOO)
        self.get_yahoo_price()
        model.currency = get_currency_enum(self.get_currency())
        if not model.exchange or fully_update:
            model.exchange = self.get_exchange()
        if not model.long_name or fully_update:
            model.long_name = self.get_long_name()
        if not model.industry or fully_update:
            model.industry = self.get_industry()


class YahooFinanceOptionStock(YahooFinanceStock):
    def __init__(
        self,
        ticker,
        expiration_date,
        strike_price,
        option_type,
        historical_data,
    ):
        super().__init__(ticker)
        self.expiration_date = expiration_date
        self.strike_price = strike_price
        self.option_type = option_type
        self.historical_data = historical_data

    def get_yahoo_price(self):
        try:
            expiration_str = self.expiration_date.strftime("%Y-%m-%d")
            expirations = self.stock.options
            if expiration_str not in expirations:
                raise Exception(f"expiration date {expiration_str} not found")

            option_chain = self.stock.option_chain(expiration_str)

            if self.option_type == OptionType.CALL:
                options = option_chain.calls
            elif self.option_type == OptionType.PUT:
                options = option_chain.puts

            option = options[options["strike"] == self.strike_price]

            if option.empty:
                raise Exception(f"strike price {self.strike_price} not found")
            last_price = option["lastPrice"].values[0]
            return last_price

        except Exception as e:
            raise Exception(e)

    def get_price(self, date_input=None):
        if date_input:
            if isinstance(date_input, datetime):
                date_input = date_input.date()

            return get_historical_price(self.historical_data, date_input)
        try:
            return self.get_yahoo_price()
        except Exception:
            return get_historical_price(self.historical_data)

    def process_model(self, form, model, fully_update):
        if form.csv_file.data:
            populate_historical_data_from_csv(form.csv_file.data, model.id)
        super().process_model(form, model, fully_update)
