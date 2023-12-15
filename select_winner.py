
from app.models.database import *
from instance.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.services import email_service, log_service
from datetime import datetime
from peewee import MySQLDatabase, fn
import uuid

db_models = [User, Sweepstake, Participant, Entry, Winner, LoginLog, Post, PageView]

def select_winners():
    db = get_db()
    db.connect()

    print("Testing winner selection!")

    # Get all Sweepstakes ready for selection
    sweepstakes = Sweepstake.select().where(Sweepstake.end_date <= datetime.now())
    for sweepstake in sweepstakes:
        if len(sweepstakes.winners) > 0:
            winning_participant = get_random_winner(sweepstake)
            guid = generate_confirmation_uuid()
            result = create_winner(sweepstake, winning_participant, guid)
                # Send email confirmation to winner

    # Check current winners to see if any are unconfirmed and expired
    # if expired, grab a new random entry
    # double check it is not the same person before ...
    # grab participant infromation
    # create winner entry
    # send email confirmation to the winner

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