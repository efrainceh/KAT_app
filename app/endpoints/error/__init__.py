from flask import Blueprint

error = Blueprint("error", __name__, template_folder="templates")

from app.endpoints.error import handlers



