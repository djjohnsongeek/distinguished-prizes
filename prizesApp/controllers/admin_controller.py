from flask import Blueprint, render_template, request, flash, redirect, url_for
from prizesApp.auth import login_required
from prizesApp.forms import SweepstakesForm, SweepstakesEditForm
from prizesApp.services import admin_service
from prizesApp.repo import appRepo
from prizesApp.util import flash_collection

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

    # Valid POST request
    if sweepstakes_form.validate_on_submit():
        if admin_service.create_sweepstakes(sweepstakes_form):
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
    redirect_url = None

    if request.method == "GET":
        if sweepstake:
            edit_form = SweepstakesEditForm(
                id = sweepstake.id,
                name = sweepstake.name,
                description = sweepstake.description,
                details = sweepstake.details,
                start_date = sweepstake.start_date,
                end_date = sweepstake.end_date,
                max_participants = sweepstake.max_participants,
                image = "Select to replace"
            )
        else:
            flash("Sweepstakes not found", "danger")
            redirect_url = url_for("admin.sweepstakes")

    # POST request with valid data
    elif request.method == "POST" and edit_form.validate():
        if admin_service.update_sweepstakes(edit_form, sweepstake):
            flash("Sweepstakes updated!", "success")
            redirect_url = url_for("admin.sweepstakes")
        else:
            flash("Failed to update sweepstakes.", "danger")

    if redirect_url:
        return redirect(redirect_url)

    return render_template("admin/sweepstakes/edit.html", form=edit_form, image_name=sweepstake.image)

@admin_blueprint.route("/admin/sweepstakes/select-winner/<int:id>", methods=["GET"])
@login_required
def select_winner(id: int):
    errors = admin_service.select_winner(id)

    flash_collection(errors, "danger")
    if len(errors) == 0:
        flash("Winner Selected!", "success")

    return redirect(url_for("admin.sweepstakes"))