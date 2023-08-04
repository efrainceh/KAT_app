import os
import sys

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, __name__))
sys.path.append(os.path.join(APP_PATH, "utils"))

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_session import Session

from app.config import Config
from app.global_variables import GUEST, GUEST_EMAIL, PROJECT_FOLDER


# Create Project Folder if it doesn't exist
project_path = os.path.join(APP_PATH, PROJECT_FOLDER)
if not os.path.isdir(project_path):

    os.mkdir(project_path)

db = SQLAlchemy()
# session = Session()
login_manager = LoginManager()
login_manager.login_view = "main_site.login"

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    
    from app.models import db, login_manager, User, Run
   
    with app.app_context():

        login_manager.init_app(app)
        # session.init_app(app)
        db.init_app(app)
        db.create_all()

        # Add Guest user if it doesn't exist
        if User.query.filter_by(username=GUEST).scalar() is None:

            user = User(username=GUEST, email=GUEST_EMAIL)
            db.session.add(user)
            db.session.commit()

        # Create guest folder if it doesn't exist
        guest_folder = os.path.join(project_path, GUEST)
        if not os.path.isdir(guest_folder):

            os.mkdir(guest_folder)
            
        # db.drop_all()

    from app.endpoints.main_site import main_site
    app.register_blueprint(main_site)
    from app.endpoints.user_profile import user_profile
    app.register_blueprint(user_profile, url_prefix="/profile")
    from app.endpoints.run import run
    app.register_blueprint(run, url_prefix="/run")
    from app.endpoints.result import result
    app.register_blueprint(result, url_prefix="/result")
    from app.endpoints.error import error
    app.register_blueprint(error, url_prefix="/error")

    return app

