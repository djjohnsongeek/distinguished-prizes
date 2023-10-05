from flask import Blueprint, render_template, request, flash, send_from_directory, current_app
from prizesApp.repo import appRepo
index_blueprint = Blueprint("index", __name__)

@index_blueprint.route("/", methods=["GET"])
def home():
    sweepstakes = appRepo.retrieve_active_sweeptakes()
    return render_template("home.html", sweepstakes=sweepstakes)

@index_blueprint.route("/About", methods=["GET"])
def about():
    return render_template("about.html")

@index_blueprint.route("/News", methods=["GET"])
def news():
    return render_template("news.html")

@index_blueprint.route("/Image/<filename>", methods=["GET"])
def download_image(filename):
    return send_from_directory(current_app.config["PHOTOS_DIR"], filename)