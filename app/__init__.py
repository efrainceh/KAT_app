import os
import sys

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, __name__))
sys.path.append(os.path.join(APP_PATH, "utils"))

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from kat_variables import RESULTS_FOLDER, ALLOWED_EXTENSIONS
from flask_save_files import FlaskSaveFiles
from KAT_wrapper import run_KAT_thread, random_project_name
from .config import Config


# Global variables
PROJECT_PATH = os.path.join(APP_PATH, "projects")
GUEST = "guest"             # Guest username registered to the database
RUN_END = 0                 # Returncode from KAT indicating the program ended succesfully
RUN_GOING = 1               # Indicates a run that hasn't finished

db = SQLAlchemy()
session = Session()
login_manager = LoginManager()
login_manager.login_view = "main_site.login"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from app.models import db, login_manager, User, Run
    with app.app_context():
        login_manager.init_app(app)
        session.init_app(app)
        db.init_app(app)
        db.create_all()
        # user = User(username=GUEST, email="guest@gmail.com")
        # user.set_password("myprecious")
        # db.session.add(user)
        # db.session.commit()
        # Create user folder
        user_folder = os.path.join(PROJECT_PATH, GUEST)
        if not os.path.isdir(user_folder):
            os.mkdir(user_folder)
        #db.drop_all()

    from app.main_site import main_site
    app.register_blueprint(main_site)
    from app.user_profile import user_profile
    app.register_blueprint(user_profile, url_prefix="/profile")
    from app.run import run
    app.register_blueprint(run, url_prefix="/run")
    from app.result import result
    app.register_blueprint(result, url_prefix="/result")
    from app.error import error
    app.register_blueprint(error, url_prefix="/error")

    return app

