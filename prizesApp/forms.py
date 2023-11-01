from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, TextAreaField, DateTimeLocalField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email
from flask_wtf.recaptcha.validators import Recaptcha
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    sweepstakes_id = IntegerField(validators=[DataRequired()])
    age_confirm = BooleanField("I am 18 or older", default=False, validators=[DataRequired()])
    location_confirm = BooleanField("I live in the USA", default=False, validators=[DataRequired()])
    terms_confirm = BooleanField(default=False, validators=[DataRequired()])
    recaptcha = RecaptchaField(validators=[Recaptcha()])

class LoginCredentials(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
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

class ConfirmationForm(FlaskForm):
    sweepstakes_id = IntegerField(validators=[DataRequired()])
    participant_id = IntegerField(validators=[DataRequired()])
    confirmation_guid = StringField(validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    address1 = StringField("Address", validators=[DataRequired()])
    address2 = StringField("Appartment or Suite #")
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zipcode = StringField("Zipcode", validators=[DataRequired()])
    recaptcha = RecaptchaField(validators=[Recaptcha()])