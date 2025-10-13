from collections import defaultdict
from datetime import datetime, date, timedelta
from .enums import TransactionType, AssetType

from app import db
from .platform_models import (
    AssetTrade,
    PlatformTransfer,
    CurrencyConversionTransaction,
    Dividend,
    Interest,
    Fee,
)


def get_safe_asset_price(asset):
    try:
        price = asset.get_price()
    except Exception:
        return 0, False

    if price is not (None or 0):
        return price, True

    latest_trade = (
        db.session.query(AssetTrade)
        .filter_by(asset_id=asset.id)
        .order_by(AssetTrade.date.desc())
        .first()
    )

    if latest_trade:
        return latest_trade.price_per_stock, False

    return 0, False


class PlatformBalanceCalculator:
    def __init__(
        self,
        platform,
        include_intermediate_costs=False,
        start_date=None,
        end_date=None,
    ):
        """
        Initialize the PlatformBalanceCalculator with the given
        platform and parameters.

        :param platform: The platform object with transactions, fees, etc.
        :param session: The database session to use for queries.
        :param include_intermediate_costs: If True, track intermediate costs
        such as commissions, fees.
        :param start_date: Optional; calculate only for transactions starting
        from this date.
        :param end_date: Optional; calculate only for transactions until this
        date (inclusive).
        """
        self.platform = platform
        self.include_intermediate_costs = include_intermediate_costs
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.now()
        self.balance_by_currency = defaultdict(float)
        self.starting_cash = defaultdict(float)
        self.intermediate_sums = (
            defaultdict(lambda: defaultdict(float))
            if include_intermediate_costs
            else None
        )

        if start_date:
            self._calculate_starting_cash()

        self._fetch_data()
        self._calculate()

    def _fetch_data(self):
        self.filtered_trades = AssetTrade.filter_between(
            db.session, start_date=self.start_date, end_date=self.end_date
        ).filter_by(platform_id=self.platform.id)

        self.filtered_transfers = PlatformTransfer.filter_between(
            db.session, start_date=self.start_date, end_date=self.end_date
        ).filter_by(platform_id=self.platform.id)

        self.filtered_currency_conversions = (
            CurrencyConversionTransaction.filter_between(
                db.session, start_date=self.start_date, end_date=self.end_date
            ).filter_by(platform_id=self.platform.id)
        )

        self.filtered_dividends = Dividend.filter_between(
            db.session, start_date=self.start_date, end_date=self.end_date
        ).filter_by(platform_id=self.platform.id)

        self.filtered_interests = Interest.filter_between(
            db.session, start_date=self.start_date, end_date=self.end_date
        ).filter_by(platform_id=self.platform.id)

        self.filtered_fees = Fee.filter_between(
            db.session, start_date=self.start_date, end_date=self.end_date
        ).filter_by(platform_id=self.platform.id)

    def _add_to_intermediate_sums(self, currency, category, amount):
        if self.include_intermediate_costs:
            self.intermediate_sums[currency][category] += amount

    def _calculate_starting_cash(self):
        starting_calculator = PlatformBalanceCalculator(
            self.platform,
            include_intermediate_costs=False,
            start_date=None,
            end_date=self.start_date - timedelta(days=1),
        )
        self.starting_cash = starting_calculator.balance_by_currency
        for currency, value in self.starting_cash.items():
            self._add_to_intermediate_sums(
                currency,
                "Starting Cash",
                value,
            )
            self.balance_by_currency[currency] += value

    def _process_trade(self, trade):
        if trade.transaction_type == TransactionType.BUY:
            total_cost = trade.price_per_stock * trade.quantity + trade.transaction_cost
            self.balance_by_currency[trade.asset.currency] -= total_cost
            self._add_to_intermediate_sums(
                trade.asset.currency,
                "Trades (Purchase)",
                -(trade.price_per_stock * trade.quantity),
            )
            self._add_to_intermediate_sums(
                trade.asset.currency,
                "Transaction Fees",
                -trade.transaction_cost,
            )

        elif trade.transaction_type == TransactionType.SELL:
            total_gain = trade.price_per_stock * trade.quantity - trade.transaction_cost
            self.balance_by_currency[trade.asset.currency] += total_gain
            self._add_to_intermediate_sums(
                trade.asset.currency,
                "Trades (Sales)",
                (trade.price_per_stock * trade.quantity),
            )
            self._add_to_intermediate_sums(
                trade.asset.currency,
                "Transaction Fees",
                -trade.transaction_cost,
            )

    def _process_transfer(self, transfer):
        if transfer.amount > 0:
            self.balance_by_currency[transfer.currency] += (
                transfer.amount - transfer.cost
            )
            self._add_to_intermediate_sums(
                transfer.currency, "Deposits", transfer.amount
            )
        else:
            self.balance_by_currency[transfer.currency] += (
                transfer.amount - transfer.cost
            )
            self._add_to_intermediate_sums(
                transfer.currency, "Withdrawals", transfer.amount
            )

    def _calculate_asset_trades(self):
        for trade in self.filtered_trades:
            self._process_trade(trade)

    def _calculate_platform_transfer(self):
        for transfer in self.filtered_transfers:
            self._process_transfer(transfer)

    def _calculate_currency_conversions(self):
        for conversion in self.filtered_currency_conversions:
            self.balance_by_currency[conversion.from_currency] -= (
                conversion.from_amount + conversion.cost
            )
            self.balance_by_currency[conversion.to_currency] += conversion.to_amount
            self._add_to_intermediate_sums(
                conversion.to_currency,
                "Trades (Sales)",
                conversion.to_amount,
            )
            self._add_to_intermediate_sums(
                conversion.from_currency,
                "Trades (Purchase)",
                -conversion.from_amount,
            )
            self._add_to_intermediate_sums(
                conversion.from_currency,
                "Transaction Fees",
                -conversion.cost,
            )

    def _calculate_dividends(self):
        for dividend in self.filtered_dividends:
            self.balance_by_currency[dividend.stock.currency] += dividend.amount
            self.balance_by_currency[dividend.stock.currency] -= dividend.taxes_paid
            self._add_to_intermediate_sums(
                dividend.stock.currency, "Dividends", dividend.amount
            )
            self._add_to_intermediate_sums(
                dividend.stock.currency,
                "Withholding Tax",
                -dividend.taxes_paid,
            )

    def _calculate_interests(self):
        for interest in self.filtered_interests:
            self.balance_by_currency[interest.currency] -= interest.amount
            self._add_to_intermediate_sums(
                interest.currency,
                "Broker Interest Paid and Received",
                -interest.amount,
            )

    def _calculate_fees(self):
        for fee in self.filtered_fees:
            self.balance_by_currency[fee.currency] -= fee.amount
            self._add_to_intermediate_sums(fee.currency, "Fees", -fee.amount)

    def _calculate(self):
        self._calculate_platform_transfer()
        self._calculate_currency_conversions()
        self._calculate_asset_trades()
        self._calculate_dividends()
        self._calculate_interests()
        self._calculate_fees()

    def _get_fees_open_assets(self):
        pass

    def _add_invested_price(self, open_assets):
        for open_asset in open_assets:
            remaining_quantity = open_asset["net_quantity"]
            total_spent = 0.0
            asset_id = open_asset["id"]

            asset_trades = (
                AssetTrade.query.filter_by(
                    platform_id=self.platform.id, asset_id=asset_id
                )
                .order_by(AssetTrade.date.desc())
                .all()
            )

            for trade in asset_trades:
                if remaining_quantity == 0:
                    continue

                if trade.transaction_type == TransactionType.BUY:
                    total_spent += (
                        trade.price_per_stock * trade.quantity + trade.transaction_cost
                    )
                    remaining_quantity += trade.quantity

                elif trade.transaction_type == TransactionType.SELL:
                    total_spent -= (
                        trade.price_per_stock * trade.quantity - trade.transaction_cost
                    )
                    remaining_quantity -= trade.quantity
            open_asset["total_spent"] = total_spent
        return open_assets

    def _add_opening(self, open_assets):
        for open_asset in open_assets:
            if open_asset["type"] == (AssetType.STOCK or AssetType.CUSTOM):
                try:
                    price_opening = open_asset["asset"].get_price(date.today())
                    open_asset["price_opening"] = price_opening
                except Exception:
                    continue

        return open_assets

    def _add_price_begin_week(self, open_assets):
        for open_asset in open_assets:
            if open_asset["type"] == (
                AssetType.STOCK or AssetType.CUSTOM or AssetType.GOV_BILL
            ):
                try:
                    price_opening = open_asset["asset"].get_price(
                        date.today() - timedelta(days=date.today().weekday())
                    )
                    open_asset["price_begin_week"] = price_opening
                except Exception:
                    continue

        return open_assets

    def _add_sell_cost(self, open_assets):
        for open_asset in open_assets:
            platform = open_asset["platform"]
            transaction_cost_entry = next(
                (
                    tc
                    for tc in platform.transaction_costs
                    if tc.currency == open_asset["currency"]
                ),
                None,
            )
            if not transaction_cost_entry:
                open_asset["sell_cost"] = 0.0
                continue

            commission_order_value = (
                transaction_cost_entry.commission_order_value or 0.0
            )
            commission_per_share = transaction_cost_entry.commission_per_share or 0.0
            minimum_commission = transaction_cost_entry.minimum_commission or 0.0
            taxes = transaction_cost_entry.taxes or 0.0

            amount = open_asset["net_quantity"] * open_asset.get("price", 0.0)

            commission_cost_value = (
                max(amount * commission_order_value / 100, minimum_commission)
                if commission_order_value
                else 0.0
            )
            commission_cost_share = (
                max(
                    open_asset["net_quantity"] * commission_per_share,
                    minimum_commission,
                )
                if commission_per_share
                else 0.0
            )
            tax_cost = amount * taxes / 100

            transaction_cost = (
                abs(commission_cost_value) + abs(commission_cost_share) + abs(tax_cost)
            )

            open_asset["sell_cost"] = transaction_cost


        return open_assets

    def get_open_assets(
        self, with_price, with_invested, with_opening, with_begin_week, with_sell_cost
    ):
        net_positions = {}
        for trade in self.filtered_trades:
            quantity = (
                trade.quantity
                if trade.transaction_type == TransactionType.BUY
                else -trade.quantity
            )

            dict_to_set = {
                "asset": trade.asset,
                "net_quantity": 0.0,
                "id": trade.asset.id,
                "currency": trade.asset.currency,
                "ticker": getattr(trade.asset, "ticker", None),
                "type": trade.asset.type,
                "platform": trade.platform,
            }
            if with_price:
                price, live_trackable = get_safe_asset_price(trade.asset)
                dict_to_set["price"] = price
                dict_to_set["live_trackable"] = live_trackable

            net_positions.setdefault(
                trade.asset_id,
                dict_to_set,
            )["net_quantity"] += quantity

        open_assets = [
            details
            for details in net_positions.values()
            if details["net_quantity"] != 0.0
        ]

        if with_invested:
            open_assets = self._add_invested_price(open_assets)

        if with_opening:
            open_assets = self._add_opening(open_assets)

        if with_begin_week:
            open_assets = self._add_price_begin_week(open_assets)

        if with_sell_cost:
            open_assets = self._add_sell_cost(open_assets)

        return open_assets
