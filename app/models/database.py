import os
from peewee import *
from datetime import datetime, timedelta
from flask import current_app

class BaseModel(Model):
    id = AutoField()

    class Meta:
        legacy_table_names = False

class User(BaseModel):
    first_name = CharField(max_length=32)
    last_name = CharField(max_length=32)
    email = CharField(max_length=64, unique=True)
    password_hash = CharField(max_length=320)
    lockout_time = DateTimeField(null=True)
    
    def to_dict(self) -> dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

class LoginLog(BaseModel):
    user = ForeignKeyField(User, backref="login_logs")
    time = DateTimeField()
    success = BooleanField()

class Sweepstake(BaseModel):
    name = CharField(max_length=512)
    description = TextField()
    start_date = DateTimeField()
    end_date = DateTimeField()
    max_participants = IntegerField(null=True)
    image = CharField(max_length=512)
    details = CharField(max_length=512)
    daily_entries = BooleanField(null=False)

    def has_ended(self) -> bool:
        return datetime.now() > self.end_date

    def has_started(self) -> bool:
        return datetime.now() > self.start_date

class Participant(BaseModel):
    name = CharField(max_length=512)
    email = CharField(max_length=512)

    def __str__(self):
        return f"name: {self.name}, email: {self.email}"

class Entry(BaseModel):
    participant = ForeignKeyField(Participant, backref="entries")
    sweepstake = ForeignKeyField(Sweepstake, backref="entries")
    entry_time = DateTimeField()

class Winner(BaseModel):
    participant = ForeignKeyField(Participant)
    sweepstake = ForeignKeyField(Sweepstake, backref="winners")
    selection_date = DateTimeField(null=False)
    confirmation_guid = CharField(max_length=64)
    confirmation_date = DateTimeField(null=True)
    confirmed = BooleanField(default=False)
    fullfilled = BooleanField(null=False, default=False)
    fullfilled_date = DateTimeField(null=True)
    tracking_number = CharField(max_length=32, null=True)
    carrier = CharField(max_length=8, null=True)
    firstname = CharField(max_length=64, null=True)
    lastname = CharField(max_length=64, null=True)
    address1 = CharField(max_length=64, null=True)
    address2 = CharField(max_length=64, null=True)
    city = CharField(max_length=64, null=True)
    state = CharField(max_length=16, null=True)
    zipcode = CharField(max_length=5, null=True)

    def expire_date(self) -> datetime:
        return self.selection_date + timedelta(hours=current_app.config["CONFIRMATION_FORM_LIMIT"])

    def expired(self) -> bool:
        return datetime.now() >= self.expire_date()

    def selection_status(self) -> str:
        return f"Selected on {self.selection_date}"

    def confirmed_status(self) -> str:
        status_str = ""

        if self.confirmed == False and self.expired():
            status_str = "Unconfirmed. Confirmation window expired."
        elif self.confirmed == False:
            status_str = "Confirmation Pending"
        elif self.confirmed == True:
            status_str = f"Confirmed on {self.confirmation_date}"

        return status_str
    
    def fullfilled_status(self) -> str:
        status_str = ""
        if self.fullfilled:
            status_str = f"Fullfilled on {self.fullfilled_date}"
        else:
            status_str = "Not Fullfilled"
        
        return status_str

class Post(BaseModel):
    edit_date = DateTimeField(null=False)
    likes = IntegerField(null=False, default=0)
    dislikes = IntegerField(null=False, default=0)
    title = CharField(max_length=512, null=False)
    content = TextField(null=False)

class PageView(BaseModel):
    timestamp = DateTimeField(null=True)
    page = CharField(max_length=32)
    user_uuid = UUIDField()
    source = CharField(max_length=32)

class EmailTask(BaseModel):
    subject = CharField(max_length=128, null=False)
    body = TextField(null=False)
    to = CharField(max_length=512, null=False)
    date_created = DateTimeField(null=False)
    date_sent = DateTimeField(null=True)
    send_attempts = IntegerField(null=False, default=0)