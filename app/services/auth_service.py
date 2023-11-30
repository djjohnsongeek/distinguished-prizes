
from app.forms import LoginCredentials
from app.repo.appRepo import retrieve_user, log_login_attempt, retrieve_failed_login_count, lock_account
from app.models.database import User, LoginLog
from werkzeug.security import check_password_hash
from flask import session, current_app
from datetime import datetime

def login_user(credentials: LoginCredentials) -> []:
    errors = []
    user = retrieve_user(credentials.email.data)

    if login_valid(user, credentials.password.data):
        session.clear()
        session["user"] = user.to_dict()
    else:
        errors.append("Login Failed")

    # Log attempts, lockout if needed
    if user is not None:
        log_login_attempt(user, len(errors) == 0)
        failed_count = retrieve_failed_login_count(user)
        if failed_count >= current_app.config["FAILED_LOGIN_THRESHOLD"]:
            lock_account(user)

    return errors

def login_valid(user, password):
    login_valid = user is not None and check_password_hash(user.password_hash, password)

    if login_valid:
        locked_out = user.lockout_time is not None and user.lockout_time >= datetime.now()
        login_valid = not locked_out
    
    return login_valid