
from app.models.database import *
from instance.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
from app.services import email_service

db_models = [User, Sweepstake, Participant, Entry, Winner, LoginLog, Post, PageView]

def select_winners():
    db = get_db()
    db.connect()

    print("Testing winner selection!")

    # Get all Sweepstakes ready for selection
        # end date must be less than now()
        # filter out any sweepstaks that already have winnser (confirmed our not)
    # Grab random entries with the sweepstakes id
    # Grab participant information for that entry
    # Create winner entry
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

if __name__ == '__main__':
    select_winners()