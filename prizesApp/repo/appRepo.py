from prizesApp.models.database import *
from prizesApp.forms import SweepstakesForm, SweepstakesEditForm, RegisterForm
from peewee import DoesNotExist
from datetime import datetime, timedelta


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
        image = safe_image_name,
        details = sweepstake_form.details.data,
    ).execute()

def create_winner(sweepstake: Sweepstake, participant: Participant, guid: str) -> bool:
    return Winner.insert(
        participant = participant,
        sweepstake = sweepstake,
        selection_date = datetime.now(),
        confirmation_guid = guid,
        confirmation_date = None,
        fullfilled = False,
        fullfilled_date = None,
        firstname = None,
        lastname = None,
        address1 = None,
        address2 = None,
        city = None,
        state = None,
        zipcode = None,
    ).execute()

def update_sweepstake(form: SweepstakesEditForm, model: Sweepstake):
    result = True

    model.name = form.name.data
    model.description = form.description.data
    model.details = form.details.data
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
    return Sweepstake.get_or_none(Sweepstake.id == id)

def retrieve_sweepstake_with_winners(id: int) -> Sweepstake:
    try:
        return Sweepstake.select().join(Winner).where(Sweepstake.id == id).get()
    except DoesNotExist:
        return None

def retrieve_all_winners() -> []:
    return Winner.select().join(Sweepstake).join(Participant).group_by(Winner.id)
        
def retrieve_winners(sweepstake_id: int) -> Winner:
    return Winner.select().join(Sweepstake).where(Sweepstake.id == sweepstake_id)

def retrieve_winner(confirm_guid: str) -> Winner:
    return Winner.get_or_none(Winner.confirmation_guid == confirm_guid)
    
def retrieve_sweepstakes() -> []:
    return Sweepstake.select().execute()

def retrieve_recent_sweepstakes() -> []:
    now = datetime.now()
    time_range = timedelta(weeks=10)
    end = now + time_range
    start = now - time_range
    return Sweepstake.select().where((Sweepstake.start_date > start) & (Sweepstake.start_date < end))

def retrieve_participants(sweepstake: Sweepstake):
    return Participant.select().where(Participant.sweepstake == sweepstake)

def retrieve_participant(participant_id: int) -> Participant:
    return Participant.get_or_none(Participant.id == participant_id)

def retrieve_participant_count(sweepstake: Sweepstake) -> int:
    return Participant.select().join(Sweepstake).where(Sweepstake.id == sweepstake.id).count()

def retrieve_participant_by_email(email: str, sweepstake: Sweepstake):
    return Participant.select().join(Sweepstake).where((Participant.email == email) & (Sweepstake.id == sweepstake.id)).get_or_none()

def retrieve_random_participant(sweepstake: Sweepstake) -> Participant:
    return Participant.select().join(Sweepstake).where(Sweepstake.id == sweepstake.id).order_by(fn.Rand()).limit(1).get()

def add_participant(register_form: RegisterForm, sweepstake: Sweepstake) -> bool:
    return Participant.insert(
        name = register_form.user_name.data,
        email = register_form.email.data,
        sweepstake = sweepstake,
        entry_time = datetime.now()
    ).execute()