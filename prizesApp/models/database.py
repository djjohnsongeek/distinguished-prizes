import os
from peewee import *
from datetime import datetime

class BaseModel(Model):
    id = AutoField()

    class Meta:
        legacy_table_names = False

class User(BaseModel):
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    email = CharField(max_length=64, unique=True)
    password_hash = CharField(max_length=320)
    
    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

class Sweepstake(BaseModel):
    name = CharField(max_length=512)
    description = TextField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    max_participants = IntegerField(null=True)
    image = CharField(max_length=512)

    def has_ended(self) -> bool:
        return datetime.now() > self.end_date

    def has_started(self) -> bool:
        return datetime.now() > self.start_date

class Participant(BaseModel):
    name = CharField(max_length=512)
    email = CharField(max_length=512)
    sweepstake = ForeignKeyField(Sweepstake, backref="participants")
    entry_time = DateTimeField()