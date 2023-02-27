from . import GUEST
from . import db


def user_already_logged_in(user):
    return user.is_authenticated and user.username != GUEST

def access_denied(run, user):
    return not run.accesible or not run.user_access(user.username)

def change_run_accesibility(run, user):
    if run.accesible and user.username == GUEST:
        run.set_accesibility(False)
        db.session.commit()