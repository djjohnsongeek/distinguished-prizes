
from app.models.database import *
from instance.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.services import email_service, log_service
from app.util import generate_confirmation_url
from datetime import datetime
from peewee import MySQLDatabase, fn
import uuid

db_models = [User, Sweepstake, Participant, Entry, Winner, LoginLog, Post, PageView]

def select_winners():
    db = get_db()
    db.connect()

    # Handle any 'expired' winners
    expired_winners = Winner.select().join(Sweepstake).switch(Winner).join(Participant).where((datetime.now() > Winner.expire_date) & (Winner.confirmed is False))
    for winner in expired_winners:
        expire_winner(winner)

    # Get all Sweepstakes ready for selection
    sweepstakes = Sweepstake.select().where(Sweepstake.end_date <= datetime.now()) 
    for sweepstake in sweepstakes:
        if not winner_selected(sweepstake):
            select_winner(sweepstake)

    db.close()

def get_db():
    db = MySQLDatabase(
        DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    for model in db_models:
        model.bind(db)

    return db

def winner_selected(sweepstake: Sweepstake) -> bool:
    result = False
    for winner in sweepstake.winners:
        if winner.confirmed:
            result = True
            break

        if not winner.confirmed and not winner.expired:
            result = True
            break

    return result

def select_winner(sweepstake: Sweepstake, last_winner_id: int = None):
    while True:
        winning_participant = get_random_winner(sweepstake)
        if winning_participant.id != last_winner_id:
            break

    confirmation_guid = generate_confirmation_uuid()
    result = create_winner(sweepstake, winning_participant, confirmation_guid)
    confirmation_url = generate_confirmation_url("localhost", sweepstake.id, winning_participant.id, confirmation_guid)

    print(confirmation_url)

    # Send selection email to winner (this is not going to work as email_service is VERY dependant on the flask project)
    # move to a queue based email system?
    # email_service.send_selection_email(winning_participant.name, winning_participant.email, sweepstake.name, confirmation_url)
    # send web master notification email

def expire_winner(winner: Winner):
    winner.confirmed = False
    winner.save()

def create_winner(sweepstake: Sweepstake, participant: Participant, guid: str) -> bool:
    new_id = 0
    try:
        new_id = Winner.insert(
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
    except Exception as e:
        log_service.log_error("Failed to selecte a winner for sweepstake", "select_winner.py", { "winner_id": participant.id, "sweepstake_id": sweepstake.id, "e_msg": str(e)})
        pass

    return new_id > 0

def generate_confirmation_uuid() -> str:
    return str(uuid.uuid4())

def get_random_winner(sweepstake_id: int) -> Participant:
    selected_entry = Entry.select().join(Participant).where(Entry.sweepstake.id == sweepstake_id).order_by(fn.Random()).limit(1)
    return selected_entry.participant

if __name__ == '__main__':
    select_winners()