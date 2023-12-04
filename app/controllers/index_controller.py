from flask import Blueprint, render_template, request, send_from_directory, current_app, jsonify, session
from app.services import sweepstakes_service, blog_service
from app.util import capture_page_view
index_blueprint = Blueprint("index", __name__)

@index_blueprint.route("/", methods=["GET"])
def home():
    capture_page_view(request, "home")
    sweepstakes = sweepstakes_service.get_sweepstakes()
    return render_template("home.html", sweepstakes=sweepstakes)

@index_blueprint.route("/About", methods=["GET"])
def about():
    capture_page_view(request, "about")
    return render_template("about.html")

@index_blueprint.route("/News", methods=["GET"])
def news():
    capture_page_view(request, "news")
    posts = blog_service.get_post_dtos()
    return render_template("news.html", posts=posts)

@index_blueprint.route("/Image/<filename>", methods=["GET"])
def download_image(filename):
    return send_from_directory(current_app.config["PHOTOS_DIR"], filename)

@index_blueprint.route("/posts/vote", methods=["POST"])
def vote():
    print(session)
    response = blog_service.vote_on_post(request)
    print(session)
    return jsonify(response)