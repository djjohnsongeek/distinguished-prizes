from app.repo import appRepo
from app.forms import PostForm, PostEditForm
from app.models.database import Post
from app.models.dtos import PostModel
from app.util import parse_bool_from_request, parse_int_from_request, get_user_id
from flask import Request, session

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

def delete_post(id: int) -> bool:
    post = appRepo.retrieve_post_by_id(id)

    if post is None:
        return False

    appRepo.delete_post(post)

    return True

def get_posts() -> []:
    posts = appRepo.retrieve_posts()
    return posts

def get_post_dtos() -> []:
    posts = appRepo.retrieve_posts()
    return [PostModel(p) for p in posts]

def vote_on_post(request: Request) -> dict:
    errors = []
 
    post_id = parse_int_from_request(request.json, "id")
    vote = parse_bool_from_request(request.json, "vote")
    post = appRepo.retrieve_post_by_id(post_id)

    if post is None or vote is None:
        errors.append("Vote Failed")

    if len(errors) == 0:
        if not record_vote(post_id):
            errors.append("Already voted")

    if len(errors) == 0:
        success = appRepo.vote_on_post(vote, post)
        if not success:
            errors.append("Failed to vote on post")
            remove_user_vote(post_id)

    return { "errors": errors }

def record_vote(post_id: int) -> bool:
    result = False

    if session.get("votes", None) is None:
        session["votes"] = []

    if post_id not in session["votes"]:
        session["votes"].append(post_id)
        result = True

    return result

def remove_user_vote(post_id: int):
    session["votes"].remove(post_id)