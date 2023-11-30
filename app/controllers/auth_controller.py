from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from app.forms import LoginCredentials
from app.services import auth_service
auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/admin/login", methods=["GET", "POST"])
def login():
    # If user is logged in, move them along
    if session.get("user") is not None:
        return redirect(url_for("admin.index"))

    login_form = LoginCredentials()

    if request.method == "POST":
        errors = auth_service.login_user(login_form)
        for error in errors:
            flash(error, "danger")
        if not errors:
            return redirect(url_for("admin.index"))

    return render_template("admin/login.html", form=login_form)

@auth_blueprint.route("/admin/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Logout Successful!", "success")
    return redirect(url_for("auth.login"))