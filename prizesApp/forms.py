from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    sweepstakes_id = IntegerField(validators=[DataRequired()])
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
    image = FileField("Upload Image", validators=[FileRequired(), FileAllowed(["jpg", "png"], "Images Only")])

class SweepstakesEditForm(SweepstakesForm):
    id = IntegerField(None, validators=[DataRequired()])