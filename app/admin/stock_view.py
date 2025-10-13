from flask import flash, current_app, has_app_context
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_admin.contrib.sqla.filters import (
    DateBetweenFilter,
    DateGreaterFilter,
    DateSmallerFilter,
    FilterEqual,
)
from markupsafe import Markup
from flask_wtf.file import FileAllowed, FileField
from wtforms import ValidationError

from app import db
from app.portfolio.enums import AssetType, OptionType, Currency
from app.portfolio.stock_models import Stock, HistoricalData
from .base_view import BaseAdmin


class StockAdmin(BaseAdmin):
    form_columns = [
        "ticker",
        "trade_type",
        "long_name",
        "exchange",
        "industry",
    ]
    column_list = [
        "ticker",
        "long_name",
        "currency",
        "exchange",
        "industry",
        "type",
        "trade_type",
        "historical_data",
    ]

    column_filters = ["currency"]

    column_formatters = {
        "ticker": lambda v, c, model, p: StockAdmin.format_ticker(model),
        "historical_data": lambda v, c, model, p: StockAdmin.format_historical_data(
            model
        ),
    }

    form_args = {
        "long_name": {
            "label": "Long Name (Optional)",
            "render_kw": {"placeholder": "Enter long name (Optional)"},
        },
        "exchange": {
            "label": "Exchange (Optional)",
            "render_kw": {"placeholder": "Enter exchange (Optional)"},
        },
        "industry": {
            "label": "Industry (Optional)",
            "render_kw": {"placeholder": "Enter industry (Optional)"},
        },
    }

    column_searchable_list = ["ticker"]

    @staticmethod
    def format_historical_data(stock):
        if stock.historical_data:
            return True
        return False

    @staticmethod
    def format_ticker(stock):
        if stock.type == AssetType.CUSTOM and not stock.historical_data:
            return Markup(f'<span style="color: red;">{stock.ticker}</span>')
        else:
            return stock.ticker

    def get_query(self):
        return self.session.query(Stock).filter(Stock.type == AssetType.STOCK)

    def get_count_query(self):
        return self.session.query(db.func.count("*")).filter(
            Stock.type == AssetType.STOCK
        )

    def create_model(self, form):
        return self.save_model(form, is_create=True)

    def update_model(self, form, model):
        fully_update = not form.ticker.data == model.ticker
        return self.save_model(
            form, model=model, is_create=False, fully_update=fully_update
        )

    def check_model_ticker(self, model):
        if model.type != (AssetType.OPTION or AssetType.GOV_BILL):
            existing_stock = (
                Stock.query.filter_by(ticker=model.ticker)
                .filter(Stock.type != AssetType.OPTION)
                .first()
            )
            if existing_stock and existing_stock.id != model.id:
                raise ValidationError(
                    f"A stock with ticker '{model.ticker}' already exists"
                )

    def set_type(self, model):
        model.type = AssetType.STOCK

    def preprocess_form(self, form):
        pass

    def save_model(self, form, model=None, is_create=True, fully_update=False):
        self.preprocess_form(form)
        if is_create:
            model = self.model()
        form.populate_obj(model)
        self.set_type(model)

        try:
            self.check_model_ticker(model)
            if is_create:
                self.session.add(model)
                db.session.flush()  # makes sure the model already gets an id
            stock_instance = model.get_stock_instance()
            stock_instance.process_model(form, model, fully_update)
        except ValidationError as e:
            self.session.rollback()
            flash(f"Error processing stock: {e}", "error")
            return False
        except Exception as e:
            self.session.rollback()
            flash(f"Error processing stock: {e}", "error")
            return False

        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            flash(f"Database error: {e}")
            return False

        return model


class OptionStockAdmin(StockAdmin):
    form_columns = [
        "ticker",
        "expiration_date",
        "strike_price",
        "option_type",
        "trade_type",
        "long_name",
        "exchange",
        "industry",
        "trade_type",
        "csv_file",
    ]

    form_extra_fields = {
        "csv_file": FileField(
            "Historical Data (CSV)",
            validators=[FileAllowed(["csv"], "CSV files only!")],
        )
    }

    def get_query(self):
        return self.session.query(Stock).filter(Stock.type == AssetType.OPTION)

    def get_count_query(self):
        return self.session.query(db.func.count("*")).filter(
            Stock.type == AssetType.OPTION
        )

    def preprocess_form(self, form):
        form.option_type.data = OptionType[form.option_type.data]

    def set_type(self, model):
        model.type = AssetType.OPTION


class CustomStockAdmin(StockAdmin):
    form_columns = [
        "ticker",
        "currency",
        "exchange",
        "long_name",
        "industry",
        "trade_type",
        "meta_data",
        "csv_file",
    ]

    column_list = [
        "ticker",
        "long_name",
        "price",
        "currency",
        "exchange",
        "industry",
        "type",
        "trade_type",
        "historical_data",
    ]

    form_args = {}

    form_extra_fields = {
        "csv_file": FileField(
            "Historical Data (CSV)",
            validators=[FileAllowed(["csv"], "CSV files only!")],
        )
    }

    def format_price(self, context, model, name):
        stock_instance = model.get_stock_instance()

        can_live_track = stock_instance.can_live_track()

        try:
            price = stock_instance.get_price()
        except Exception:
            price = None

        if can_live_track:
            return Markup(f'<span style="color: green;">{price}</span>')
        else:
            return price

    column_formatters = (
        StockAdmin.column_formatters.copy()
    )
    column_formatters.update(
        {
            "price": lambda view, context, model, name: view.format_price(
                context, model, name
            )
        }
    )

    def get_query(self):
        return self.session.query(Stock).filter(Stock.type == AssetType.CUSTOM)

    def get_count_query(self):
        return self.session.query(db.func.count("*")).filter(
            Stock.type == AssetType.CUSTOM
        )

    def preprocess_form(self, form):
        form.currency.data = Currency[form.currency.data]

    def set_type(self, model):
        model.type = AssetType.CUSTOM


class GovBillAdmin(BaseAdmin):
    column_list = [
        "issuer",
        "face_value",
        "maturity_date",
        "discount_rate",
        "price",
        "currency",
    ]

    form_columns = [
        "issuer",
        "face_value",
        "maturity_date",
        "discount_rate",
        "currency",
    ]

    column_formatters = {
        "price": lambda v, c, model, p: model.get_price(),
    }


def get_all_tickers_with_historical_data():
    unique_tickers = (
        db.session.query(Stock.ticker.distinct().label("ticker"))
        .join(HistoricalData, Stock.id == HistoricalData.stock_id)
        .order_by(Stock.ticker.asc())
        .all()
    )
    return [(stock.ticker, stock.ticker) for stock in unique_tickers]


class HistoricalDataAdmin(BaseAdmin):
    form_columns = [
        "stock",
        "date",
        "price",
    ]
    column_list = [
        "stock",
        "date",
        "price",
    ]

    column_filters = [
        DateBetweenFilter(HistoricalData.date, "Date Range"),
        DateGreaterFilter(HistoricalData.date, "After Date"),
        DateSmallerFilter(HistoricalData.date, "Before Date"),
    ]
    can_set_page_size = True

    column_searchable_list = [
        "stock.ticker",
        "stock.long_name",
    ]
