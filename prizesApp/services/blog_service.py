from prizesApp.repo import appRepo
from prizesApp.forms import PostForm, PostEditForm
from prizesApp.models.database import Post
from prizesApp.models.dtos import PostModel
from prizesApp.util import parse_boolean_post, parse_int_post
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
        "vote_total": 0,
    }

    post_id = parse_int_post("id", request)
    vote = parse_boolean_post("vote", request)
    post = appRepo.retrieve_post_by_id(post_id)

    if post is None or vote is None:
        response["errors"].append("Vote Failed")
    else:
        response["vote_total"] = appRepo.vote_on_post(vote, post)

    return response