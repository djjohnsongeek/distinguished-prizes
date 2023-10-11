from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField, TextAreaField, DateTimeLocalField, BooleanField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    sweepstakes_id = IntegerField(validators=[DataRequired()])
    age_confirm = BooleanField("I am 18 or older", default=False, validators=[DataRequired()])
    location_confirm = BooleanField("I live in the USA", default=False, validators=[DataRequired()])
    terms_confirm = BooleanField(default=False, validators=[DataRequired()])
    # TODO need to add recaptia

class LoginCredentials(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])

class SweepstakesForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    start_date = DateTimeLocalField("Start Time", validators=[DataRequired()], format="%Y-%m-%dT%H:%M")
    end_date = DateTimeLocalField("End Time", validators=[DataRequired()], format="%Y-%m-%dT%H:%M")
    max_participants = IntegerField("Max Participants")
    image = FileField("Upload Image", validators=[FileAllowed(["jpg", "png"], "Images Only")])
    details = StringField("Details", validators=[DataRequired()])

class SweepstakesEditForm(SweepstakesForm):
    id = IntegerField(None, validators=[DataRequired()])