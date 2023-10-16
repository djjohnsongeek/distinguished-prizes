import click
import os
import shutil
from datetime import datetime, timedelta
from flask import current_app, g
from werkzeug.security import generate_password_hash
from peewee import MySQLDatabase
from prizesApp.models.database import *

db_models = [User, Sweepstake, Participant, Winner]

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
            "name": "Test Current",
            "description": " Test Current Description",
            "start_date": start,
            "end_date": end,
            "max_participants": 32,
            "details": "item1 item2 item3",
            "image": "ccf84ed0-0658-4a4d-9b16-d2339d5ec152.jpg",
        },
        {
            "name": "Test Past",
            "description": " Test Past Description",
            "start_date": start_past,
            "end_date": end_past,
            "max_participants": 32,
            "details": "item1 item2 item3",
            "image": "d05b21b8-72c2-4e6a-b131-36443813ade7.png",
        },
        {
            "name": "Test Future",
            "description": " Test Future Description",
            "start_date": start_future,
            "end_date": end_future,
            "max_participants": 32,
            "details": "item1 item2 item3",
            "image": "ed5d99ea-3e81-4b6d-b581-63867632dea6.jpg",
        }
    ]).execute()

    # Add participans
    Participant.insert_many([
        {
            "name": "daniel",
            "email": "daniel@gmail.com",
            "sweepstake": Sweepstake.get_by_id(2),
            "entry_time": datetime.now()
        },
        {
            "name": "jack",
            "email": "jack@gmail.com",
            "sweepstake": Sweepstake.get_by_id(2),
            "entry_time": datetime.now()
        },
        {
            "name": "jill",
            "email": "jill@gmail.com",
            "sweepstake": Sweepstake.get_by_id(2),
            "entry_time": datetime.now()
        },
        {
            "name": "jane",
            "email": "jane@gmail.com",
            "sweepstake": Sweepstake.get_by_id(2),
            "entry_time": datetime.now()
        },
        {
            "name": "john",
            "email": "john@gmail.com",
            "sweepstake": Sweepstake.get_by_id(2),
            "entry_time": datetime.now()
        }
    ]).execute()
    
    db.close()

def init_app(app):
    app.cli.add_command(init_db_command)
 
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database Initialized ...")