from prizesApp.repo import appRepo
from prizesApp.forms import PostForm, PostEditForm
from prizesApp.models.database import Post
from prizesApp.models.dtos import PostModel
from datetime import datetime, timedelta


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