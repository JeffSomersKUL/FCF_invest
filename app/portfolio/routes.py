from flask import render_template, jsonify
from flask_login import current_user
from enum import Enum

from . import portfolio, get_balances_all
from app.portfolio.enums import Currency
from app.portfolio.stock_models import Asset
from app.portfolio.platform_balance import get_safe_asset_price


def replace_currency_enums(data):
    if isinstance(data, dict):
        return {
            replace_currency_enums(k): replace_currency_enums(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [replace_currency_enums(item) for item in data]
    elif isinstance(data, set):
        return {replace_currency_enums(item) for item in data}
    elif isinstance(data, Enum):
        return data.value
    else:
        return data


def serialize_open_assets(platform_balances):
    for platform_balance in platform_balances["open_assets"]:
        platform_balance["asset"] = str(platform_balance["asset"])
        platform_balance["platform"] = str(platform_balance["platform"].name)
    return platform_balances


@portfolio.route("/")
def main():
    if current_user.is_authenticated:
        platform_balances = get_balances_all()
        platform_balances = replace_currency_enums(platform_balances)
        platform_balances = serialize_open_assets(platform_balances)
        return render_template(
            "portfolio-login.html",
            balance=platform_balances,
            usd_rate=Currency.USD.get_conversion_rate(),
            gbp_rate=Currency.GBP.get_conversion_rate(),
        )
    else:
        return render_template("portfolio.html")


@portfolio.route("/asset/<string:asset_id>")
def get_asset_value(asset_id):
    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({"status": "error", "message": "Asset not found"}), 404

    price, live_trackable = get_safe_asset_price(asset)

    return jsonify(
        {
            "status": "success",
            "asset_id": asset_id,
            "price": price,
            "live_trackable": live_trackable,
        }
    )
