from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, date
from abc import abstractmethod

from app import db
from . import YahooFinanceStock, Custom, YahooFinanceOptionStock
from .enums import Currency, OptionType, AssetType


class Asset(db.Model):
    __tablename__ = "asset"
    __mapper_args__ = {
        "polymorphic_identity": AssetType.ASSET,
        "polymorphic_on": "type",
    }
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(AssetType), nullable=False)
    currency = db.Column(db.Enum(Currency), nullable=False, default=Currency.EUR)

    # Relationships
    trades = db.relationship("AssetTrade", back_populates="asset")

    @abstractmethod
    def get_price(self, date_input=None):
        return None


class Stock(Asset):
    __tablename__ = "stock"
    __mapper_args__ = {"polymorphic_identity": AssetType.STOCK}

    id = db.Column(db.Integer, db.ForeignKey("asset.id"), primary_key=True)
    trade_type_id = db.Column(db.Integer, db.ForeignKey("trade_type.id"))
    ticker = db.Column(db.String(20), nullable=False)
    exchange = db.Column(db.String(30), nullable=True)
    long_name = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(200), nullable=True)
    meta_data = db.Column(JSON, nullable=True)

    # Define relationships
    dividends = db.relationship("Dividend", back_populates="stock", lazy=True)
    historical_data = db.relationship(
        "HistoricalData",
        back_populates="stock",
        cascade="all, delete-orphan",
        lazy=True,
    )
    trade_type = db.relationship("TradeType", back_populates="stocks")

    def __repr__(self):
        return self.long_name or self.ticker

    def get_stock_instance(self):
        return YahooFinanceStock(self.ticker)

    def get_price(self, date_input=None):
        return self.get_stock_instance().get_price(date_input)


class OptionStock(Stock):
    __tablename__ = "option_stock"
    __mapper_args__ = {"polymorphic_identity": AssetType.OPTION}

    id = db.Column(db.Integer, db.ForeignKey("stock.id"), primary_key=True)
    expiration_date = db.Column(db.Date, nullable=False)
    strike_price = db.Column(db.Float, nullable=False)
    option_type = db.Column(db.Enum(OptionType), nullable=False)

    def __repr__(self):
        expiration_str = self.expiration_date.strftime("%d%m%y")
        option_type_str = "C" if self.option_type == OptionType.CALL else "P"
        strike_price_str = f"{int(self.strike_price * 1000):08d}"

        return f"{self.ticker}{expiration_str}{option_type_str}{strike_price_str}"

    def get_stock_instance(self):
        return YahooFinanceOptionStock(
            self.ticker,
            self.expiration_date,
            self.strike_price,
            self.option_type,
            self.historical_data,
        )


class CustomStock(Stock):
    __tablename__ = "custom_stock"
    __mapper_args__ = {"polymorphic_identity": AssetType.CUSTOM}

    id = db.Column(db.Integer, db.ForeignKey("stock.id"), primary_key=True)

    def get_stock_instance(self):
        return Custom(self.ticker, self.historical_data, self.meta_data)


class GovBill(Asset):
    __tablename__ = "government_bill"
    __mapper_args__ = {"polymorphic_identity": AssetType.GOV_BILL}

    id = db.Column(db.Integer, db.ForeignKey("asset.id"), primary_key=True)
    issuer = db.Column(db.String(100), nullable=False)
    face_value = db.Column(db.Float, nullable=False)
    maturity_date = db.Column(db.Date, nullable=False)
    discount_rate = db.Column(db.Float, nullable=False)

    def get_time_to_maturity(self, date_input=None):
        if date_input is None:
            input_date = datetime.today().date()
        elif isinstance(date_input, datetime):
            input_date = input_date.date()
        elif not isinstance(date_input, date):
            raise TypeError("input_date must be a date or datetime instance")

        days_to_maturity = (self.maturity_date - input_date).days
        return days_to_maturity / 365.0

    def get_price(self, date_input=None):
        time_to_maturity = self.get_time_to_maturity(date_input)

        if time_to_maturity <= 0:
            return self.face_value

        current_value = self.face_value / (1 + self.discount_rate) ** time_to_maturity

        return current_value

    def __repr__(self):
        return f"GovBill {self.issuer} by {self.maturity_date}"


class HistoricalData(db.Model):
    __table_args__ = (db.UniqueConstraint("stock_id", "date", name="_stock_date_uc"),)

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define relationships
    stock = db.relationship("Stock", back_populates="historical_data")

    @classmethod
    def add_or_update_data(cls, stock_id, date, price):
        existing_data = cls.query.filter_by(stock_id=stock_id, date=date).first()
        if existing_data:
            existing_data.price = price
        else:
            new_data = cls(stock_id=stock_id, date=date, price=price)
            db.session.add(new_data)

    def __repr__(self):
        return f"<HistoricalData {self.date} for {self.stock_id}>"
