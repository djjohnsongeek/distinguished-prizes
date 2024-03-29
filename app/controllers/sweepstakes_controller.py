from flask import Blueprint, render_template, flash, redirect, url_for, request
sweepstakes_blueprint = Blueprint("sweepstakes", __name__)
from app.forms import RegisterForm, ConfirmationForm
from app.repo import appRepo
from app.services import sweepstakes_service
from app.util import flash_collection, capture_page_view

@sweepstakes_blueprint.route("/sweepstakes/<int:sweepstakes_id>", methods=["GET"])
def info(sweepstakes_id: int):
    sweepstake = appRepo.retrieve_sweepstake(sweepstakes_id)
    entry_count = appRepo.retireve_entry_count(sweepstake)
    winner = appRepo.retrieve_confirmed_winner(sweepstake)

    if sweepstake is None:
        flash("Sweepstakes not found :(", "danger")
        return redirect(url_for("index.home"))

    capture_page_view(request, "sweepstake-info")
    return render_template("sweepstakes/info.html", sweepstakes=sweepstake, entry_count=entry_count, winner=winner)

@sweepstakes_blueprint.route("/sweepstakes/register/<int:sweepstakes_id>", methods=["GET"])
def register_get(sweepstakes_id: int):
    sweepstakes = appRepo.retrieve_sweepstake(sweepstakes_id)

    if sweepstakes is None:
        flash("Sweepstakes not found :(", "danger")
        return redirect(url_for("index.home"))

    capture_page_view(request, "sweepstake-register")
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

@sweepstakes_blueprint.route("/sweepstakes/confirmation/<int:participant_id>/<int:sweepstakes_id>/<uuid:confirmation_guid>", methods=["GET", "POST"])
def confirm_get(sweepstakes_id: int, participant_id: int, confirmation_guid: str):
    errors = sweepstakes_service.validate_confirmation(sweepstakes_id, participant_id, confirmation_guid)
    if len(errors) > 0:
        return render_template("error.html", error_message=errors[0])

    confirm_form = ConfirmationForm(sweepstakes_id=sweepstakes_id, participant_id=participant_id, confirmation_guid=confirmation_guid)
    return render_template("sweepstakes/confirm.html", form=confirm_form)

@sweepstakes_blueprint.route("/sweepstakes/confirmation", methods=["POST"])
def confirm_post():
    form = ConfirmationForm()
    errors = sweepstakes_service.complete_confirmation(form)

    flash_collection(errors, "danger")
    if len(errors) == 0:
        flash("Your claim has been confirmed!", "success")
        return redirect(url_for("index.home"))
    else:
        return render_template("sweepstakes/confirm.html", form=form)