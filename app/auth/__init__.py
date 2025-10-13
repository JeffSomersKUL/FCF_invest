from flask import Blueprint
from flask_restful import Api
from app import csrf

auth = Blueprint("auth", __name__)
api = Api(auth)
csrf.exempt(auth)

from . import routes
from .routes import (
    Signin,
    Signup,
    VerifyEmail,
    ResendConfirmation,
    Logout,
)

api.add_resource(Signup, "/api/signup", endpoint="signup")
api.add_resource(Signin, "/api/signin", endpoint="signin")
api.add_resource(Logout, "/api/logout", endpoint="logout")
api.add_resource(VerifyEmail, "/api/verify-email", endpoint="verify_email")
api.add_resource(
    ResendConfirmation,
    "/api/resend-confirmation",
    endpoint="resend_confirm_code",
)
