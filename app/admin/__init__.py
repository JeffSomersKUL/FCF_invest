from flask import Blueprint, current_app
from flask_admin import Admin
from .stock_view import (
    StockAdmin,
    HistoricalDataAdmin,
    OptionStockAdmin,
    CustomStockAdmin,
    GovBillAdmin,
)
from .platform_view import PlatformAdmin, AssetTradeAdmin, PlatformBaseAdmin
from .index_view import (
    IndexView,
    UserAdmin,
    MemberAdmin,
    InvestmentAdmin,
    MemberTransferAdmin,
)
from .schedule_view import ScheduledTaskAdmin, SchedulerJobsView
from .base_view import BaseAdmin, LogView
from app.user.models import User, Member, MemberInvestment, MemberTransfer
from app.portfolio.platform_models import (
    Platform,
    AssetTrade,
    PlatformTransfer,
    CurrencyConversionTransaction,
    Expense,
    Dividend,
    Fee,
    Interest,
    TradeType,
    TransactionCost
)
from app.portfolio.stock_models import (
    Stock,
    HistoricalData,
    OptionStock,
    CustomStock,
    GovBill,
)
from app.scheduler.models import ScheduledTask
from app import db

admin_bp = Blueprint("admin_bp", __name__)


def create_admin(app):
    admin = Admin(app, index_view=IndexView(), template_mode="bootstrap3")
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(MemberAdmin(Member, db.session, category="Member"))
    admin.add_view(
        MemberTransferAdmin(MemberTransfer, db.session, category="Member")
    )
    admin.add_view(
        InvestmentAdmin(MemberInvestment, db.session, category="Member")
    )
    admin.add_view(StockAdmin(Stock, db.session, category="Stock Management"))
    admin.add_view(
        OptionStockAdmin(OptionStock, db.session, category="Stock Management")
    )
    admin.add_view(
        CustomStockAdmin(CustomStock, db.session, category="Stock Management")
    )
    admin.add_view(
        GovBillAdmin(GovBill, db.session, category="Stock Management")
    )
    admin.add_view(
        BaseAdmin(TradeType, db.session, category="Stock Management")
    )
    admin.add_view(
        HistoricalDataAdmin(
            HistoricalData, db.session, category="Stock Management"
        )
    )
    admin.add_view(
        PlatformAdmin(Platform, db.session, category="Portfolio Management")
    )
    admin.add_view(
        PlatformBaseAdmin(
            PlatformTransfer, db.session, category="Portfolio Management"
        )
    )
    admin.add_view(
        PlatformBaseAdmin(
            CurrencyConversionTransaction,
            db.session,
            category="Portfolio Management",
        )
    )
    admin.add_view(
        AssetTradeAdmin(
            AssetTrade, db.session, category="Portfolio Management"
        )
    )
    admin.add_view(
        PlatformBaseAdmin(
            Dividend, db.session, category="Portfolio Management"
        )
    )
    admin.add_view(
        PlatformBaseAdmin(
            Interest, db.session, category="Portfolio Management"
        )
    )
    admin.add_view(BaseAdmin(Fee, db.session, category="Portfolio Management"))
    admin.add_view(
        BaseAdmin(Expense, db.session, category="Portfolio Management")
    )
    admin.add_view(
        BaseAdmin(TransactionCost, db.session, category="Portfolio Management")
    )
    admin.add_view(
        ScheduledTaskAdmin(ScheduledTask, db.session, category="Scheduler")
    )
    admin.add_view(
        SchedulerJobsView(name="Scheduled Jobs", category="Scheduler")
    )
    admin.add_view(
        LogView(
            log_file=app.config["SCHEDULER_LOG_FILE"],
            title="Scheduler logs",
            name="Scheduler log",
            category="Scheduler",
            endpoint="scheduler_log",
        )
    )
    admin.add_view(
        LogView(
            log_file=app.config["FLASK_LOG_FILE"],
            title="Flask application logs",
            name="Flask log",
            endpoint="flask_log",
        )
    )
