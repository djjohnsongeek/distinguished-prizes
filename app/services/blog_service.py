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
    user_id = get_user_id()
    user_session = session.get(user_id, None)

    if post_id not in user_session["votes"]:
        l = user_session["votes"]
        l.append(post_id)
        user_session["votes"] = l
        result = True

    return result

def remove_user_vote(post_id: int):
    print("remvong")
    user_id = get_user_id()
    user_session = session.get(user_id, None)
    user_session["votes"].remove(user_id)