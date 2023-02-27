from flask import Blueprint

result = Blueprint("result", __name__, template_folder="templates")

from app.result import views