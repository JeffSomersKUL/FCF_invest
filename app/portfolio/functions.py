from collections import defaultdict

from app import db
from .platform_models import Platform, AssetTrade
from . import PlatformBalanceCalculator


def get_balance(
    start_date=None,
    end_date=None,
    include_intermediate_sums=False,
    with_price=False,
    with_invested=False,
    with_opening=False,
    with_begin_week=False,
    with_sell_cost=False,
):
    platforms = db.session.query(Platform).all()
    platform_balances = []
    all_currencies = set()

    for platform in platforms:
        calculator = PlatformBalanceCalculator(
            platform,
            include_intermediate_costs=include_intermediate_sums,
            start_date=start_date,
            end_date=end_date,
        )
        balances = calculator.balance_by_currency
        open_assets = calculator.get_open_assets(
            with_price, with_invested, with_opening, with_begin_week, with_sell_cost
        )

        intermediate_sums = calculator.intermediate_sums

        platform_balances.append(
            {
                "platform": platform,
                "balances": balances,
                "open_assets": open_assets,
                "intermediate_sums": intermediate_sums,
            }
        )
        all_currencies.update(balances.keys())
    all_currencies = sorted(all_currencies, key=lambda c: c.value)

    return platform_balances, all_currencies


def get_balances_all():
    platform_balances, _ = get_balance(
        with_price=False,
        with_invested=True,
        with_opening=False,
        with_begin_week=False,
        with_sell_cost=True,
    )

    combined_balances = defaultdict(float)
    combined_open_assets = []

    for platform_data in platform_balances:
        for currency, amount in platform_data["balances"].items():
            combined_balances[currency] += amount

        combined_open_assets.extend(platform_data["open_assets"])

    return {
        "balances": dict(combined_balances),
        "open_assets": combined_open_assets,
    }

