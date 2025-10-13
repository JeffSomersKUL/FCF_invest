from flask import redirect, url_for, request, abort
from flask_admin import AdminIndexView, expose
from flask_login import current_user
from functools import wraps
from sqlalchemy import desc
from datetime import datetime

from app import db
from app.user.models import User
from app.main.models import ContactFormData
from .base_view import BaseAdmin
from app.portfolio import get_balance


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


class IndexView(AdminIndexView):
    @expose("/")
    @admin_required
    def index(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Query user count and contact forms
        user_count = db.session.query(User).count()
        users = db.session.query(User).all()
        contact_forms_query = db.session.query(ContactFormData).order_by(
            desc(ContactFormData.date_created)
        )

        if start_date:
            contact_forms_query = contact_forms_query.filter(
                ContactFormData.date_created >= start_date
            )
        if end_date:
            contact_forms_query = contact_forms_query.filter(
                ContactFormData.date_created <= end_date
            )
        contact_forms = contact_forms_query.all()

        platform_balances, all_currencies = get_balance(
            include_intermediate_sums=True,
            start_date=start_date,
            end_date=end_date,
        )

        return self.render(
            "admin/index.html",
            user_count=user_count,
            users=users,
            contact_forms=contact_forms,
            platform_balances=platform_balances,
            currencies=all_currencies,
        )


class UserAdmin(BaseAdmin):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = [
        "password_hash",
        "email",
        "date_created",
    ]
    can_create = False
    can_delete = False


class MemberAdmin(BaseAdmin):
    column_list = ["email", "fname", "lname", "investments", "current"]
    form_columns = ["email", "fname", "lname", "current"]
    can_create = True
    can_edit = True
    can_delete = True


class InvestmentAdmin(BaseAdmin):
    column_list = ["member", "date", "amount", "stocks_received"]
    can_create = True
    can_edit = True
    can_delete = True


class MemberTransferAdmin(BaseAdmin):
    pass
