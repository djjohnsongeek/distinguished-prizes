from flask import Blueprint, render_template, request, flash, send_from_directory, current_app, jsonify
from prizesApp.services import sweepstakes_service, blog_service
index_blueprint = Blueprint("index", __name__)

@index_blueprint.route("/", methods=["GET"])
def home():
    sweepstakes = sweepstakes_service.get_sweepstakes()
    return render_template("home.html", sweepstakes=sweepstakes)

@index_blueprint.route("/About", methods=["GET"])
def about():
    return render_template("about.html")

@index_blueprint.route("/News", methods=["GET"])
def news():
    posts = blog_service.get_post_dtos()
    return render_template("news.html", posts=posts)

@index_blueprint.route("/Image/<filename>", methods=["GET"])
def download_image(filename):
    return send_from_directory(current_app.config["PHOTOS_DIR"], filename)

@index_blueprint.route("/posts/vote", methods=["POST"])
def vote():
    response = blog_service.vote_on_post(request)
    return jsonify(response)