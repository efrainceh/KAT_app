from datetime import datetime
from flask import session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager, RUN_END, RUN_GOING

@login_manager.user_loader
def load_user(id):
    user = User.query.get(int(id))
    session["user"] = user.username
    return user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    date_joined = db.Column(db.DateTime, default=datetime.now)
    runs = db.relationship('Run', back_populates='user', lazy='dynamic')

    def set_password(self, password):
       self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Run(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_runname = db.Column(db.String(20))
    kat_runname = db.Column(db.String(20), unique=True, index=True)
    kmer_size = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    folder = db.Column(db.String(100))
    runcode = db.Column(db.Integer, default=RUN_GOING)
    accesible = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='runs')

    def get_date(self):
        return self.date.strftime("%Y/%m/%d, %H:%M")

    def user_access(self, username):
        return self.user.username == username

    def is_finished(self):
        return self.runcode == RUN_END
    
    def set_runcode(self, value):
        self.runcode = value

    def set_accesibility(self, accesibility):
        self.accesible = accesibility
