from flask import Blueprint, render_template, request, flash, redirect, url_for
from prizesApp.auth import login_required
from prizesApp.forms import SweepstakesForm, SweepstakesEditForm
from prizesApp.services import admin_service
from prizesApp.repo import appRepo

admin_blueprint = Blueprint("admin", __name__)

@admin_blueprint.route("/admin", methods=["GET"])
@login_required
def index():
    return render_template("admin/index.html")

@admin_blueprint.route("/admin/sweepstakes", methods=["GET"])
@login_required
def sweepstakes():
    sweepstakes = appRepo.retrieve_sweepstakes()
    return render_template("admin/sweepstakes/index.html", sweepstakes=sweepstakes)

@admin_blueprint.route("/admin/sweepstakes/create", methods=["GET", "POST"])
@login_required
def create_sweepstakes():
    sweepstakes_form = SweepstakesForm()

    if sweepstakes_form.validate_on_submit():
        errors = admin_service.create_sweepstakes(sweepstakes_form)
        if len(errors) == 0:
            flash("Sweepstakes created!", "success")
            return redirect(url_for("admin.sweepstakes"))
        else:
            flash("Failed to create sweepstakes.", "danger")

    return render_template("/admin/sweepstakes/create.html", form=sweepstakes_form)

@admin_blueprint.route("/admin/sweepstakes/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_sweepstakes(id: int):
    edit_form = SweepstakesEditForm()
    sweepstake = appRepo.retrieve_sweepstake(id)

    if edit_form.validate_on_submit():
        if admin_service.update_sweepstakes(edit_form, sweepstake):
            flash("Sweepstakes updated!", "success")
            return redirect(url_for("admin.sweepstakes"))
        else:
            flash("Failed to update sweepstakes.", "danger")

    if request.method == "GET":
        if sweepstake:
            edit_form = SweepstakesEditForm(
                id = sweepstake.id,
                name = sweepstake.name,
                description = sweepstake.description,
                start_date = sweepstake.start_date,
                end_date = sweepstake.end_date,
                max_participants = sweepstake.max_participants,
                image = "Replace Image?"
            )
        else:
            flash("Sweepstakes not found", "danger")
            return redirect(url_for("admin.sweepstakes"))

    return render_template("admin/sweepstakes/edit.html", form=edit_form, image_name=sweepstake.image)