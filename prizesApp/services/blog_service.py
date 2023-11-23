from prizesApp.repo import appRepo
from prizesApp.forms import PostForm
from prizesApp.models.database import Post
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

def get_posts() -> []:
    posts = appRepo.retrieve_posts()
    return posts