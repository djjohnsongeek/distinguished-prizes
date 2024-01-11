from flask import current_app, g
from peewee import MySQLDatabase
from app.models.database import *
from app.models.database import EmailTask

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