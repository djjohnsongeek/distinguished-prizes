from prizesApp.models.database import *
from prizesApp.forms import SweepstakesForm, SweepstakesEditForm
from peewee import DoesNotExist


def retrieve_user(email: str) -> User:
    try:
        return User.get(User.email == email)
    except DoesNotExist:
        return None

def create_sweepstake(sweepstake_form: SweepstakesForm, safe_image_name: str) -> bool:
    return Sweepstake.insert(
        name = sweepstake_form.name.data,
        description = sweepstake_form.description.data,
        start_date = sweepstake_form.start_date.data,
        end_date = sweepstake_form.end_date.data,
        max_participants = sweepstake_form.max_participants.data,
        image = safe_image_name
    ).execute()

def update_sweepstake(form: SweepstakesEditForm, model: Sweepstake):
    model.name = form.name.data
    model.description = form.description.data
    model.start_date = form.start_date.data
    model.end_date = form.end_date.data
    model.max_participants = form.max_participants.data
    model.image = form.image.data.filename
    # TODO figure out file uploads

    try:
        model.save()
    except:
        return False

    return True

def retrieve_sweepstake(id: int) -> Sweepstake:
    try:
        return Sweepstake.get(Sweepstake.id == id)
    except DoesNotExist:
        return None

def retrieve_sweepstakes() -> []:
    return Sweepstake.select().execute()