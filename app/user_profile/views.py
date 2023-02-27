import os
import shutil
from flask import abort, render_template, redirect, url_for, jsonify, jsonify
from flask_login import login_required, logout_user, current_user
from . import user_profile
from .. import db, PROJECT_PATH, GUEST, RUN_END
from ..models import User, Run
from ..helpers import access_denied


@user_profile.route('/<string:username>', methods=["GET"])
@login_required
def profile(username):

    # Verify that the user exists
    user = User.query.filter_by(username=username).first_or_404()

    # Handle guest user typing URL: '/guest'
    if current_user.username == GUEST:
        return redirect(url_for('main_site.login'))
    
    # Handle registered, logged in user typing another user's URL
    if current_user.username != username:
        abort(400)

    # Show profile
    runs = Run.query.filter_by(user_id=current_user.id, runcode=RUN_END).all()
    if runs is None:
        runs = []
    return render_template("user_profile/profile.html", runs=runs)

@user_profile.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_site.login"))

@user_profile.route("/redirect", methods=["GET"])
@login_required
def user_redirect():
    return redirect(url_for("user_profile.profile", username=current_user.username))

@user_profile.route("/delete_user", methods=["DELETE"])
@login_required
def delete_user():

    # Quick out anyone trying to delete Guest user
    if current_user.username == GUEST:
        abort(400)

    # Capture user before logging out
    user = User.query.filter_by(id=current_user.id).first_or_404()
    logout_user()

    # Delete folder and database entry
    user_folder = os.path.join(PROJECT_PATH, user.username)
    if os.path.exists(user_folder) and os.path.isdir(user_folder):
        shutil.rmtree(user_folder)
    db.session.delete(user)
    db.session.commit()
    
    data = {"next_URL" : url_for("main_site.login")}
    return jsonify(data)

@user_profile.route("/delete_run/<string:run_id>", methods=["DELETE"])
@login_required
def delete_run(run_id):

    # Check run exists and user has access to it
    run = Run.query.filter_by(id=int(run_id)).first_or_404()
    if access_denied(run, current_user):
        abort(400)

    # Delete folder and database entry
    if os.path.exists(run.folder) and os.path.isdir(run.folder):
        shutil.rmtree(run.folder)
    db.session.delete(run)
    db.session.commit()

    return jsonify(data={"code" : 200})
