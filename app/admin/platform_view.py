from flask_ckeditor import CKEditorField
from flask_admin.contrib.sqla.filters import (
    DateBetweenFilter,
    DateGreaterFilter,
    DateSmallerFilter,
    BaseSQLAFilter,
    FilterEqual,
)
from sqlalchemy import or_

from app.portfolio.platform_models import AssetTrade
from app.portfolio.stock_models import Asset, AssetType, Stock
from .base_view import BaseAdmin


class AssetTypeFilter(FilterEqual):
    def __init__(self, column, name):
        super().__init__(column, name)

    def get_options(self, view):
        return [(choice.name, choice.value) for choice in AssetType]


class FilterStockTicker(BaseSQLAFilter):
    def apply(self, query, value, alias=None):
        return query.join(Stock, Stock.id == AssetTrade.asset_id).filter(
            or_(
                Stock.ticker.ilike(f"%{value}%"),
                Stock.long_name.ilike(f"%{value}%"),
            )
        )

    def operation(self):
        return "Stock Ticker/Name is"


class PlatformBaseAdmin(BaseAdmin):

    column_filters = ["platform"]


class PlatformAdmin(BaseAdmin):
    form_columns = ["name"]


class AssetTradeAdmin(PlatformBaseAdmin):
    form_columns = [
        "asset",
        "platform",
        "price_per_stock",
        "quantity",
        "date",
        "transaction_type",
        "transaction_cost",
        "information",
    ]
    column_list = [
        "asset",
        "platform",
        "price_per_stock",
        "quantity",
        "date",
        "transaction_type",
        "currency",
        "transaction_cost",
    ]

    column_formatters = {
        "currency": lambda v, c, model, p: model.asset.currency.value,
    }

    form_overrides = {"information": CKEditorField}

    column_filters = [
        AssetTypeFilter(Asset.type, name="Asset Type"),
        FilterStockTicker(AssetTrade.asset_id, name="Stock Ticker/Name"),
        "platform",
        DateBetweenFilter(AssetTrade.date, "Date Range"),
        DateGreaterFilter(AssetTrade.date, "After Date"),
        DateSmallerFilter(AssetTrade.date, "Before Date"),
    ]

    column_default_sort = ("date", True)

    create_template = "admin/editor-transaction.html"
    edit_template = "admin/editor-transaction.html"
