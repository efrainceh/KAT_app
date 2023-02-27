from flask import Blueprint

user_profile = Blueprint("user_profile", __name__, template_folder="templates", static_folder="static")

from app.user_profile import views