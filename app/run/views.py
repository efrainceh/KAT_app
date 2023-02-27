import os
import polling2
import shutil
import threading
from flask import abort, render_template, redirect, url_for, current_app, jsonify, session
from flask_login import login_required, current_user
from . import run
from .. import db, PROJECT_PATH, GUEST, RUN_END, RUN_GOING, FlaskSaveFiles, run_KAT_thread, random_project_name
from ..models import Run
from .forms import KatRunForm


# Global Variable to keep track of when each run is finished
runcodes = {}

@run.route("/kat_upload", methods=["GET", "POST"])
@login_required
def kat_upload():
    form = KatRunForm()
    if form.validate_on_submit():
        # A random name is created so that we can retrieve the run and avoid folder name clashes.
        kat_runname = random_project_name(20)
        
        # Create run folder. This folder will contain other folders where input and output files are be saved.
        run_folder = os.path.join(PROJECT_PATH, session["user"], kat_runname)
        if not os.path.isdir(run_folder):
            os.mkdir(run_folder)

        # Save files to folders.
        save_files = FlaskSaveFiles(current_app)
        save_files.save(run_folder, form.samples.data, form.references.data)

        if current_user.username == GUEST:
            # Everything is saved in the session, not in the database.
            session["kat_runname"] = kat_runname
            session["user_runname"] = form.run_name.data
            session["kmer_size"] = form.kmer_size.data
            session["folder"] = run_folder
            return redirect(url_for("run.kat_run", kat_runname=kat_runname))
        else:
            # For registered users, everything is saved in the database, not in the session. 
            run = Run(kmer_size=form.kmer_size.data, user_runname=form.run_name.data, kat_runname=kat_runname, folder=run_folder, user_id=current_user.id)
            db.session.add(run)
            db.session.commit()
            return redirect(url_for("run.kat_run", kat_runname=kat_runname))
  
    return render_template("run/kat_upload.html", form=form, guest=GUEST)

@run.route("/run_kat/<string:kat_runname>", methods=["GET"])
@login_required
def kat_run(kat_runname):

    if current_user.username == GUEST:
        # If no run is going or the URL doesn't match the current run
        if "kat_runname" not in session or session["kat_runname"] != kat_runname:
            abort(400)
        # Create guest user run object
        run = Run(kmer_size=session["kmer_size"], user_runname=session["user_runname"], kat_runname=kat_runname, folder=session["folder"], user_id=current_user.id)
    else:
        run = Run.query.filter_by(kat_runname=kat_runname).first_or_404()

        # If this run is not users then abort
        if not run.user_access(current_user.username):
            abort(400)

        # If run is users and is finished, then redirect to result page
        if run.user_access(current_user.username) and run.is_finished():
            return redirect(url_for("result.get_result", kat_runname=kat_runname))


    # If this is a new run coming from kat_upload
    global runcodes
    runcodes[kat_runname] = RUN_GOING
    thread_kat = threading.Thread(daemon=True, target=run_KAT_thread, args=(run.kmer_size, run.kat_runname, run.folder, runcodes, kat_runname))
    thread_kat.start()

    thread_end_run_cleanup = threading.Thread(daemon=True, target=end_run_cleanup, args=(run))
    thread_end_run_cleanup.start()

    return render_template("run/in_progress.html", run=run, guest=GUEST)

@run.route("/runcode/<string:kat_runname>", methods=["GET"])
@login_required
def runcode(kat_runname):

    global runcodes
    # Once the subprocess running in thread_kat is finished, the function in thread_end_run_cleanup function will delete
    # kat_runname from the runcodes dictionary. Since there will still be some async calls to this route left in the javascript
    # queue, we need to check for the presence of kat_runname in order to handle these additional calls.  
    if kat_runname in runcodes:
        data = {"runcode" : runcodes[kat_runname], "next_URL" : url_for("result.get_result", kat_runname=kat_runname)}
    else:
         data = {"runcode" : RUN_END, "next_URL" : url_for("result.get_result", kat_runname=kat_runname)}

    return jsonify(data)

def end_run_cleanup(run):
    global runcodes
    polling2.poll(lambda: runcodes[run.kat_runname] == RUN_END, step=60, timeout=86400)
    del runcodes[run.kat_runname]
    if run.user == GUEST:
        if os.path.exists(run.folder) and os.path.isdir(run.folder):
            shutil.rmtree(run.folder)
    else:    
        run.set_runcode = RUN_END
        db.session.commit()
   
    