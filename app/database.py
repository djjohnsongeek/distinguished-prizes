import click
import os
import shutil
from datetime import datetime, timedelta
from flask import current_app, g
from werkzeug.security import generate_password_hash
from peewee import MySQLDatabase
from app.models.database import *

db_models = [User, Sweepstake, Participant, Entry, Winner, LoginLog, Post, PageView, EmailTask]

def get_db() -> MySQLDatabase:
    if 'db' not in g:
        config = current_app.config
        g.db = MySQLDatabase(
            config["DB_NAME"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            host=config["DB_HOST"],
            port=config["DB_PORT"]
        )

        for model in db_models:
            model.bind(g.db)

    return g.db

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

#region Initialize Database
def init_db():
    db = get_db()
    db.connect()

    # Prepare db schema
    db.drop_tables(db_models)
    db.create_tables(db_models)

    # Clear out photos directory
    for filename in os.listdir(current_app.config["PHOTOS_DIR"]):
        path = os.path.join(current_app.config["PHOTOS_DIR"], filename)
        if os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                print(f"Failed to remove {path}. Reason: {e}")


    # Update the photos directory
    for filename in os.listdir(current_app.config["TEST_PHOTOS_DIR"]):
        src_path = os.path.join(current_app.config["TEST_PHOTOS_DIR"], filename)
        dest_path = os.path.join(current_app.config["PHOTOS_DIR"], filename)
        if os.path.isfile(src_path):
            try:
                shutil.copyfile(src_path, dest_path)
            except Exception as e:
                print(f"Failed to move {src_path}. Reason: {e}")
                
    # Add Super/Admin user
    User.insert(
        first_name = "Daniel",
        last_name = "Johnson",
        email = "danieleejohnson@gmail.com",
        password_hash = generate_password_hash("password"),
    ).execute()

    range = timedelta(days=30)

    start = datetime.now().replace(day=1)
    end = start.replace(day=28)

    start_past = start - range
    end_past = end - range

    start_future = start + range
    end_future = end + range

    # Add test sweepstakes
    Sweepstake.insert_many([
        {
            "name": "Nintendo Switch",
            "description": "Switch to the incredible experience of gaming on the go!",
            "start_date": start,
            "end_date": end,
            "max_participants": 32,
            "details": "item1 item2 item3",
            "daily_entries": True,
            "image": "ccf84ed0-0658-4a4d-9b16-d2339d5ec152.jpg",
        },
        {
            "name": "Xbox Series X",
            "description": "Xbox has Xtreem perfomance!",
            "start_date": start_past,
            "end_date": end_past,
            "max_participants": 32,
            "details": "item1 item2 item3",
            "daily_entries": True,
            "image": "d05b21b8-72c2-4e6a-b131-36443813ade7.png",
        },
        {
            "name": "Playstation 5",
            "description": "Play all day on this incredible gaming station!",
            "start_date": start_future,
            "end_date": end_future,
            "max_participants": 32,
            "details": "item1 item2 item3",
            "daily_entries": True,
            "image": "ed5d99ea-3e81-4b6d-b581-63867632dea6.jpg",
        }
    ]).execute()
    db.close()
#endregion

#region Select Winners
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
    confirmation_url = generate_confirmation_url(current_app.config["SITE_DOMAIN"], sweepstake.id, winning_participant.id, confirmation_guid)
    email_service.send_selection_email(winning_participant.name, winning_participant.email, sweepstake.name, confirmation_url)
    email_service.send_confirmation_notification(winning_participant.name, sweepstake.name)

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
#endregion


def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(select_winners_command)
 
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database Initialized ...")

@click.command("select-winners")
def select_winners_command():
    select_winners()
    click.echo("Winner selection complete ...")