from flask import redirect, url_for, request, abort
from flask_admin import AdminIndexView, expose, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from functools import wraps
from app import db
from app.models import User, ContactFormData
from sqlalchemy import desc


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    @admin_required
    def index(self):
        user_count = db.session.query(User).count()
        users = db.session.query(User).all()
        contact_forms = (
            db.session.query(ContactFormData)
            .order_by(desc(ContactFormData.date_created))
            .all()
        )

        return self.render(
            "admin/index.html",
            user_count=user_count,
            users=users,
            contact_forms=contact_forms,
        )

    @expose("/delete_message/<int:message_id>")
    @admin_required
    def delete_contact_form(self, message_id):
        message = ContactFormData.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
        return redirect(url_for("admin.index"))


class UserAdmin(ModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = [
        "password_hash",
        "email",
        "date_created",
    ]
    can_create = False
    can_delete = False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class MemberAdmin(ModelView):
    column_list = ["id", "email", "fname", "lname", "current"]
    form_columns = ["email", "current"]
    can_create = True
    can_edit = True
    can_delete = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
