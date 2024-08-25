from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__)

from . import routes

def create_admin(app):
    from flask_admin import Admin
    from .routes import MyAdminIndexView, UserAdmin, MemberAdmin
    from app.models import User, Member
    from app import db

    admin = Admin(
        app, index_view=MyAdminIndexView(), template_mode="bootstrap3"
    )
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(MemberAdmin(Member, db.session))
