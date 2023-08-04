import os

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from werkzeug.urls import url_parse

from app import db, project_path
from app.endpoints.main_site import main_site
from app.endpoints.main_site.forms import GuestForm, LoginForm, RegistrationForm
from app.global_variables import GUEST
from app.utils import user_already_logged_in
from app.models import User                 

# IF THE USER IS LOGGED IN AND THEN IT CLICKS THE BACK PAGE BUTTON IT CAN GO TO LOGIN. THEN IT WILL BE REDIRECT 
# WHEN YOU CLICK "SIGN IN" OR "HOME"

@main_site.route('/', methods=["GET", "POST"])
def index():

    return redirect(url_for('main_site.login'))

@main_site.route('/login', methods=["GET", "POST"])
def login():

    if user_already_logged_in(current_user):

        return redirect(url_for('user_profile.profile', username=current_user.username))
    
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):

            login_user(user, remember=form.remember_me.data)
            # Redirect when the user got here from typing an URL that requires a login
            next_page = request.args.get('next')
            # If user got here directly from login, set next to their profile
            if not next_page or url_parse(next_page).netloc != '':

                next_page = url_for('user_profile.profile', username=user.username)

            return redirect(next_page)
        
        else:

            flash("Invalid username or password")
    
    guestForm = GuestForm()

    return render_template("main_site/login.html", form=form, guestForm=guestForm)

@main_site.route('/guest_login', methods=["GET", "POST"])
def guest_login():

    # Handle logged in users that type this URL
    if user_already_logged_in(current_user):

        return redirect(url_for('user_profile.profile', username=current_user.username))
    
    guestForm = GuestForm()
    if guestForm.validate_on_submit():

        user = User.query.filter_by(username=GUEST).first()
        login_user(user)

        return redirect(url_for('run.kat_upload'))

    form = LoginForm()

    return render_template("main_site/login.html", form=form, guestForm=guestForm)

@main_site.route('/register', methods=["GET","POST"])
def register():
    
    if user_already_logged_in(current_user):

        return redirect(url_for('user_profile.profile', username=current_user.username))

    form = RegistrationForm()
    if form.validate_on_submit():

        # Add user to database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
    
        # Create user folder
        user_folder = os.path.join(project_path, form.username.data)

        if not os.path.isdir(user_folder):

            os.mkdir(user_folder)

        flash("Registration complete. Welcome to KAT!")
        
        return redirect(url_for("main_site.register"))

    return render_template("main_site/register.html", form=form)

@main_site.route("/about", methods=["GET"])
def about():
    
    return render_template("main_site/about.html", guest=GUEST)
