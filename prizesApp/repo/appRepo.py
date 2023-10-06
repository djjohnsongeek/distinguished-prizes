from prizesApp.models.database import *
from prizesApp.forms import SweepstakesForm, SweepstakesEditForm, RegisterForm
from peewee import DoesNotExist
from datetime import datetime


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
    result = True

    model.name = form.name.data
    model.description = form.description.data
    model.start_date = form.start_date.data
    model.end_date = form.end_date.data
    model.max_participants = form.max_participants.data
    if form.image.data:
        model.image = form.image.data.filename

    try:
        model.save()
    except:
        result = False

    return result

def retrieve_sweepstake(id: int) -> Sweepstake:
    try:
        return Sweepstake.get(Sweepstake.id == id)
    except DoesNotExist:
        return None

def retrieve_sweepstakes() -> []:
    return Sweepstake.select().execute()

def retrieve_active_sweeptakes() -> []:
    now = datetime.now()
    return Sweepstake.select().where(now < Sweepstake.end_date and now > Sweepstake.start_date)

def retrieve_inactive_sweepstakes() -> []:
    now = datetime.now()
    return Sweepstake.select().where(now > Sweepstake.end_date)

def retrieve_participants(sweepstakes: Sweepstake):
    return Participant.select().where(Participant.sweepstake == sweepstakes)

def retrieve_participant_by_username(username: str):
    pass

def retrieve_participant_by_email(email: str):
    pass

def add_participant(register_form: RegisterForm, sweepstake: Sweepstake) -> bool:
    return Participant.insert(
        name = register_form.user_name.data,
        email = register_form.email.data,
        sweepstake = sweepstake,
        entry_time = datetime.now()
    ).execute()