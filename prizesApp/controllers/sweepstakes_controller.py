from flask import Blueprint, render_template, request, flash, redirect, url_for
sweepstakes_blueprint = Blueprint("sweepstakes", __name__)
from prizesApp.forms import RegisterForm
from prizesApp.repo import appRepo
from prizesApp.services import sweepstakes_service
from prizesApp.util import flash_collection

@sweepstakes_blueprint.route("/sweepstakes/<int:sweepstakes_id>", methods=["GET"])
def info(sweepstakes_id: int):
    sweepstakes = appRepo.retrieve_sweepstake(sweepstakes_id)

    if sweepstakes is None:
        flash("Sweepstakes not found :(", "danger")
        return redirect(url_for("index.home"))

    return render_template("sweepstakes/info.html", sweepstakes=sweepstakes)

@sweepstakes_blueprint.route("/sweepstakes/register/<int:sweepstakes_id>", methods=["GET"])
def register_get(sweepstakes_id: int):
    sweepstakes = appRepo.retrieve_sweepstake(sweepstakes_id)

    if sweepstakes is None:
        flash("Sweepstakes not found :(", "danger")
        return redirect(url_for("index.home"))

    register_form = RegisterForm(sweepstakes_id=sweepstakes_id)
    return render_template(
        "sweepstakes/register.html",
        form=register_form,
        sweepstakes_id=sweepstakes_id,
        sweepstakes_name=sweepstakes.name
    )

@sweepstakes_blueprint.route("/sweepstakes/register", methods=["POST"])
def register_post():
    register_form = RegisterForm()
    sweepstake = appRepo.retrieve_sweepstake(register_form.sweepstakes_id.data)
    errors = sweepstakes_service.add_participant(register_form, sweepstake)
    if len(errors) == 0:
        flash("You have been successfully registered!", "success")
        return redirect(url_for("index.home"))
    
    flash_collection(errors, "danger")
    return render_template(
        "sweepstakes/register.html",
        form=register_form,
        sweepstakes_id=register_form.sweepstakes_id.data,
        sweepstakes_name=sweepstake.name
    ) 
