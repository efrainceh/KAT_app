from flask import Blueprint

main_site = Blueprint("main_site", __name__, template_folder="templates")

from app.endpoints.main_site import views