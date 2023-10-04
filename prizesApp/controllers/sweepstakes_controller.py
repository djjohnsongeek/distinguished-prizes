from flask import Blueprint, render_template, request, flash
sweepstakes_blueprint = Blueprint("sweepstakes", __name__)
from prizesApp.forms import RegisterForm

@sweepstakes_blueprint.route("/sweepstakes/<int:sweepstakes_id>", methods=["GET"])
def info(sweepstakes_id: int):
    return render_template("sweepstakes/info.html")

@sweepstakes_blueprint.route("/sweepstakes/register/<int:sweepstakes_id>", methods=["GET", "POST"])
def register(sweepstakes_id: int):
    register_form = RegisterForm(sweepstakes_id=sweepstakes_id)
    return render_template("sweepstakes/register.html", form=register_form, sweepstakes_id=sweepstakes_id)