from app import db
from .enums import Currency, TransactionType


class DateFilterMixin:
    @classmethod
    def filter_between(cls, session, start_date=None, end_date=None):
        """
        Filter the records between the given start_date and end_date. The model
        that uses this class needs to have a 'date' field, which can be either
        a Date or DateTime type.

        :param session: The database session to use for the query.
        :param start_date: The start date for filtering (inclusive).
        :param end_date: The end date for filtering (inclusive).
        :return: A query object filtered by the date range.
        """
        query = session.query(cls)

        if start_date:
            query = query.filter(cls.date >= start_date)

        if end_date:
            query = query.filter(cls.date <= end_date)

        return query


class Platform(db.Model):
    __tablename__ = "platform"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Define relationships
    transfers = db.relationship(
        "PlatformTransfer", back_populates="platform", lazy=True
    )
    trades = db.relationship("AssetTrade", back_populates="platform", lazy=True)
    currency_conversion_transactions = db.relationship(
        "CurrencyConversionTransaction", back_populates="platform", lazy=True
    )
    dividends = db.relationship("Dividend", back_populates="platform", lazy=True)
    interests = db.relationship("Interest", back_populates="platform", lazy=True)
    fees = db.relationship("Fee", back_populates="platform", lazy=True)
    transaction_costs = db.relationship(
        "TransactionCost", back_populates="platform", lazy=True
    )

    def __repr__(self):
        return self.name


class AssetTrade(DateFilterMixin, db.Model):
    __tablename__ = "asset_transaction"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey("asset.id"), nullable=False)
    price_per_stock = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    transaction_cost = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.DateTime, nullable=False)
    information = db.Column(db.Text, nullable=True)

    # Define relationships
    asset = db.relationship("Asset", back_populates="trades")
    platform = db.relationship("Platform", back_populates="trades")

    def __repr__(self):
        return f"<AssetTrade {self.asset} {self.transaction_type} {self.quantity}>"


class TradeType(db.Model):
    __tablename__ = "trade_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    # Define relationships
    stocks = db.relationship("Stock", back_populates="trade_type")

    def __repr__(self):
        return self.name


class PlatformTransfer(DateFilterMixin, db.Model):
    __tablename__ = "platform_transfer"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Enum(Currency), nullable=False)
    cost = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.DateTime, nullable=False)

    # Define relationships
    platform = db.relationship("Platform", back_populates="transfers")

    def __repr__(self):
        return f"<PlatformTransfer to {self.platform.name} {self.amount}>"


class CurrencyConversionTransaction(DateFilterMixin, db.Model):
    __tablename__ = "currency_conversion_transaction"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    from_amount = db.Column(db.Float, nullable=False)
    to_amount = db.Column(db.Float, nullable=False)
    from_currency = db.Column(db.Enum(Currency), nullable=False)
    to_currency = db.Column(db.Enum(Currency), nullable=False)
    cost = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.DateTime, nullable=False)

    # Define relationships
    platform = db.relationship(
        "Platform", back_populates="currency_conversion_transactions"
    )  # This line connects to Platform

    def __repr__(self):
        return f"<CurrencyConversionTransaction from {self.from_currency.value} to {self.to_currency.value}: {self.from_amount} => {self.to_amount}>"


class Expense(DateFilterMixin, db.Model):
    __tablename__ = "club_expense"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return self.description


class Fee(DateFilterMixin, db.Model):
    __tablename__ = "fee"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Enum(Currency), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Define relationships
    platform = db.relationship("Platform", back_populates="fees")

    def __repr__(self):
        return self.description


class Dividend(DateFilterMixin, db.Model):
    __tablename__ = "dividend"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    taxes_paid = db.Column(db.Float, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False)

    # Define relationships
    stock = db.relationship("Stock", back_populates="dividends")
    platform = db.relationship("Platform", back_populates="dividends")

    def __repr__(self):
        return f"<Dividend {self.amount} received from {self.stock.ticker} on {self.platform.name}>"


class Interest(DateFilterMixin, db.Model):
    __tablename__ = "interest"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(db.Integer, db.ForeignKey("platform.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.Enum(Currency), nullable=False)
    date = db.Column(db.Date, nullable=False)

    # Define relationships
    platform = db.relationship("Platform", back_populates="interests")

    def __repr__(self):
        return self.description


class TransactionCost(db.Model):
    __tablename__ = "transaction_cost"

    id = db.Column(db.Integer, primary_key=True)
    platform_id = db.Column(
        db.Integer, db.ForeignKey("platform.id"), nullable=False
    )
    currency = db.Column(db.Enum(Currency), nullable=False)
    commission_order_value = db.Column(db.Float, nullable=True)
    commission_per_share = db.Column(db.Float, nullable=True)
    minimum_commission = db.Column(db.Float, nullable=True)
    taxes = db.Column(db.Float, nullable=True)

    # Define relationships
    platform = db.relationship("Platform", back_populates="transaction_costs")
