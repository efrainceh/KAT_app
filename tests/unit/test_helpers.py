from app.utils.helpers import *
from app.models import User, Run


def test_user_logged_in():
    """
        GIVEN a User model
        WHEN the user is ......
        THEN function should return true
    """
    
    username = "Efrain"
    email = "efrain@gmail.com"
    user = User(username=username, email=email)
    assert user_already_logged_in(user)


# define test for not authenticated

def test_user_is_guest():
    """
        GIVEN a User model
        WHEN the user is guest
        THEN function should return false
    """

    username = "guest"
    email = "guest@gmail.com"
    user = User(username=username, email=email)
    assert not user_already_logged_in(user)

# def test_access_denied():
#     """
#         GIVEN a User model
#         WHEN the user is guest
#         THEN function should return false
#     """

#     kmer_size = 10
#     user_runname = "runname"
#     kat_runname = "kat_runname"
#     folder = "project_folder"
#     user_id = 5
#     run = Run(kmer_size=kmer_size, user_runname=user_runname, kat_runname=kat_runname, \
#                   folder=folder, user_id=user_id)
#     assert 
#     return not run.accesible or not run.user_access(user.username)
