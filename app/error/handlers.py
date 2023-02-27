from flask import render_template
from .. import db
from app.error import error

@error.app_errorhandler(400)
def not_found_error(error):
    return render_template("error/400.html"), 400

@error.app_errorhandler(404)
def not_found_error(error):
    return render_template("error/404.html"), 404

@error.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("error/500.html"), 505





