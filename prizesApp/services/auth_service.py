
from prizesApp.forms import LoginCredentials
from prizesApp.repo.appRepo import retrieve_user
from werkzeug.security import check_password_hash
from flask import session

def login_user(credentials: LoginCredentials) -> []:
    errors = []
    user = retrieve_user(credentials.email.data)

    if credentials_are_valid(user, credentials.password.data):
        session.clear()
        session["user"] = user.to_dict()
    else:
        errors.append("Username or password is incorrect")

    return errors

def credentials_are_valid(user, password):
    return user is not None and check_password_hash(user.password_hash, password)