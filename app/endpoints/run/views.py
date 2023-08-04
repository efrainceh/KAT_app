import os
import random
import string
import threading

from flask import abort, current_app, jsonify, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db, project_path
from app.endpoints.run import run
from app.endpoints.run.forms import KatRunForm
from app.global_variables import GUEST, RUN_END
from app.kat_wrapper import KAT
from app.models import Run
from app.utils import FlaskSaveFiles


@run.route("/kat_upload", methods=["GET", "POST"])
@login_required
def kat_upload():

    form = KatRunForm()
    if form.validate_on_submit():

        # A random name is created so that we can retrieve the run and avoid folder name clashes.
        name_length = 20
        kat_runname = random_project_name(name_length)
        
        # Create run folder. This folder will contain other folders where input and output files are be saved.
        run_folder = os.path.join(project_path, form.run_name.data, kat_runname)

        if not os.path.isdir(run_folder):

            os.mkdir(run_folder)

        # Save files to folders.
        save_files = FlaskSaveFiles(current_app)
        save_files.save(run_folder, form.samples.data, form.references.data)

        # Save user and run info to the session
        # session["kat_runname"] = kat_runname
        # session["user_runname"] = form.run_name.data
        # session["kmer_size"] = form.kmer_size.data
        # session["folder"] = run_folder
        # session["user_id"] = current_user.id

        # Add run to the database.
        new_run = Run(kmer_size=form.kmer_size.data, user_runname=form.run_name.data, \
                  kat_runname=kat_runname, folder=run_folder, \
                    user_id=current_user.id)
        db.session.add(new_run)
        db.session.commit()
       
    
        return redirect(url_for("run.kat_run", kat_runname=kat_runname))
    
    return render_template("run/kat_upload.html", form=form, guest=GUEST)

@run.route("/run_kat/<string:kat_runname>", methods=["GET"])
@login_required
def kat_run(kat_runname):

    if user_existing_run(current_app._get_current_object(), kat_runname):

            return redirect(url_for("result.get_result", kat_runname=kat_runname))
    
    # If this is a new run coming from kat_upload
    # This thread runs the KAT executable. It will update the run_state in the db once it finishes
    thread_kat = threading.Thread(target=run_KAT_thread, args=(current_app._get_current_object(), kat_runname))
    thread_kat.start()

    current_run = Run.query.filter_by(kat_runname=kat_runname).first()

    return render_template("run/in_progress.html", run=current_run, guest=GUEST)

@run.route("/runcode/<string:kat_runname>", methods=["GET"])
@login_required
def runcode(kat_runname):

    current_run = Run.query.filter_by(kat_runname=kat_runname).first()
    print("runcode: ", current_run.get_run_state())
    data = {"run_state" : current_run.get_run_state(), "next_URL" : url_for("result.get_result", kat_runname=kat_runname)}

    return jsonify(data)

def run_KAT_thread(app, kat_runname):

    with app.app_context():

        current_run = Run.query.filter_by(kat_runname=kat_runname).first()
        kat = KAT()
        run_state = kat.run(current_run.kmer_size, current_run.kat_runname, current_run.folder)
        current_run.set_run_state(run_state)
        db.session.commit()

        state = Run.query.filter_by(kat_runname=current_run.kat_runname).first().get_run_state()
        print("finished: ", state)


# def commit_new_run(app, current_session):
     
#     with app.app_context():

#         new_run = Run(kmer_size=current_session["kmer_size"], user_runname=current_session["user_runname"], \
#                   kat_runname=current_session["kat_runname"], folder=current_session["folder"], \
#                     user_id=current_session["user_id"])
#         db.session.add(new_run)
#         db.session.commit()        

def user_existing_run(app, kat_runname):

    if current_user.username == GUEST:

        abort(400)
        # If no run is going or the URL doesn't match the current run
        # if "kat_runname" not in session or session["kat_runname"] != kat_runname:
            
        #     abort(400)
    
    else:

        with app.app_context():

            kat_run = Run.query.filter_by(kat_runname=kat_runname).first_or_404()

            # If this run is not users then abort
            if not kat_run.user_access(current_user.username):

                abort(400)

            # If run is users and is finished, return true so the view can be redirected
            if kat_run.user_access(current_user.username) and kat_run.get_run_state() == RUN_END:
                
                return True
    
    return False

def random_project_name(size):

    symbols = string.ascii_letters + string.digits
    project_name = ""

    while(len(project_name) < size):

        project_name += random.choice(symbols)

    return project_name