from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app.models import User, Run

class TestUser:

    username = "Efrain"
    email = "efrain@gmail.com"
    password = "hakkuna_matata"

    def test_new_user(self):
        """
            GIVEN a User model
            WHEN a new User is created
            THEN check username and email
        """
        user = User(username=self.username, email=self.email)
        assert user.username == self.username
        assert user.email == self.email

    def test_user_set_password(self):
        """
            GIVEN a User model
            WHEN a User creates a password
            THEN check password
        """

        user = User(username=self.username, email=self.email)
        user.set_password(self.password)
        assert user.check_password(self.password)

    
    


class TestRun():

    kmer_size = 10
    user_runname = "runname"
    kat_runname = "kat_runname"
    folder = "project_folder"
    user_id = 5

    def test_new_run(self):

        run = Run(kmer_size=self.kmer_size, user_runname=self.user_runname, kat_runname=self.kat_runname, \
                  folder=self.folder, user_id=self.user_id)
        assert run.kmer_size == self.kmer_size
        assert run.user_runname == self.user_runname
        assert run.kat_runname == self.kat_runname
        assert run.folder == self.folder
        assert run.user_id == self.user_id