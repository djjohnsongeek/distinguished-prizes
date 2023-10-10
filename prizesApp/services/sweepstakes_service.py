from flask import session
from prizesApp.repo import appRepo
from prizesApp.forms import RegisterForm
from prizesApp.models.database import Sweepstake
from datetime import datetime

def add_participant(form: RegisterForm, sweepstake: Sweepstake) -> []:
    errors = []
    if not form.validate():
        errors.append("Invalid form data.")
    
    if sweepstake is None:
        errors.append("Sweepstakes not found.")
        return errors
    
    if datetime.now() > sweepstake.end_date:
        errors.append("Sweepstakes is over.")
    
    if datetime.now() < sweepstake.start_date:
        errors.append("Sweepstakes has not started.")
    
    participant = appRepo.retrieve_participant_by_email(form.email.data, sweepstake)
    if participant is not None:
        errors.append("You have already signed up for this sweepstakes.")

    if is_client_registered(sweepstake):
        errors.append("You have already signed up for this sweepstakes.")
    
    if len(errors) == 0:
        result = appRepo.add_participant(form, sweepstake)
        if not result:
            errors.append("Failed to register for sweepstakes.")
        else:
            remember_client_registration(sweepstake)

    return errors

def remember_client_registration(sweepstake: Sweepstake):
    session[f"sweepstake_{sweepstake.id}"] = True

def is_client_registered(sweepstake: Sweepstake):
    return session.get(f"sweepstake_{sweepstake.id}", default=False)

def get_sweepstakes() -> {}:
    now = datetime.now()
    recent_sweepstakes = appRepo.retrieve_recent_sweepstakes()

    sorted_sweepstakes = {
        "past": [],
        "current": [],
        "future": []
    }

    for sweepstake in recent_sweepstakes:
        if sweepstake.start_date > now:
            sorted_sweepstakes["future"].append(sweepstake)
        elif sweepstake.end_date < now:
            sorted_sweepstakes["past"].append(sweepstake)
        else:
            sorted_sweepstakes["current"].append(sweepstake)

    return sorted_sweepstakes