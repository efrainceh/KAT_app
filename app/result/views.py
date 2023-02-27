import os
from flask import abort, render_template, send_file, jsonify, url_for, session
from flask_login import login_required, current_user
from . import result
from .. import RESULTS_FOLDER, GUEST
from ..models import Run
from ..helpers import access_denied


@result.route("/<string:kat_runname>", methods=["GET"])
@login_required
def get_result(kat_runname):
    
    run = evaluate_access(current_user, kat_runname, session)

    return render_template("result/result.html", run=run, guest=GUEST)

@result.route("/return_zip/<string:kat_runname>", methods=["GET"])
@login_required
def return_zip(kat_runname):
    extension = ".zip"
    filename = kat_runname + extension
    run = evaluate_access(current_user, kat_runname, session)
    file_path = os.path.join(run.folder, RESULTS_FOLDER, filename)
    return send_file(file_path, download_name=run.user_runname + extension)

@result.route("/return_images/<string:kat_runname>/<string:suffix>", methods=["GET"])
@login_required
def return_images(kat_runname, suffix):
    extension = ".png"
    filename = kat_runname + suffix + extension
    run = evaluate_access(current_user, kat_runname, session)
    file_path = os.path.join(run.folder, RESULTS_FOLDER, filename)
    return send_file(file_path, mimetype="image/png")

@result.route("/image_url/<int:run_id>", methods=["GET"])
@login_required
def image_url(run_id):
    run = Run.query.filter_by(id=run_id).first_or_404()
    # No user access check. The return is an URL that leads to a route that is protected. 
    data = {"img_URL" : url_for('result.return_images', kat_runname=run.kat_runname, suffix='_percentage')}
    return jsonify(data)


def evaluate_access(user, kat_runname, current_session):
    if user.username == GUEST:
        # If no run is going or the URL doesn't match the current run
        if "kat_runname" not in current_session or current_session["kat_runname"] != kat_runname:
            abort(400)
        return Run(kmer_size=current_session["kmer_size"], user_runname=current_session["user_runname"], kat_runname=kat_runname, folder=current_session["folder"], user_id=current_user.id)   
    else:
        run = Run.query.filter_by(kat_runname=kat_runname).first_or_404()
        # Check run is accesible and user has access to it
        if access_denied(run, user):
            abort(400)
        return run
