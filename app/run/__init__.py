from flask import Blueprint

run = Blueprint("run", __name__, template_folder="templates", static_folder="static")

from app.run import views