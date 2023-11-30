from app.repo import appRepo
from app.forms import PostForm, PostEditForm
from app.models.database import Post
from app.models.dtos import PostModel
from app.util import parse_bool_from_request, parse_int_from_request
from datetime import datetime, timedelta
from flask import Request


def create_post(form: PostForm) -> []:
    errors = []
    if form.validate():
        success = appRepo.create_post(form)
        if not success:
            errors.append("Failed to created post.")
    else:
        errors.append("Invalid form.")

    return errors

def update_post(form: PostEditForm, post: Post) -> bool:
    if not post:
        return False

    return appRepo.update_post(form, post)

def get_posts() -> []:
    posts = appRepo.retrieve_posts()
    return posts

def get_post_dtos() -> []:
    posts = appRepo.retrieve_posts()
    return [PostModel(p) for p in posts]


def vote_on_post(request: Request) -> dict:
    response = {
        "errors": [],
    }
 
    post_id = parse_int_from_request(request.json, "id")
    vote = parse_bool_from_request(request.json, "vote")
    post = appRepo.retrieve_post_by_id(post_id)

    if post is None or vote is None:
        response["errors"].append("Vote Failed")
    else:
        success = appRepo.vote_on_post(vote, post)
        if not success:
            response.errors.append("Failed to vote on post")

    return response