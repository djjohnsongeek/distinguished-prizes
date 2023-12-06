from flask import session, current_app
from app.services import email_service, log_service
from app.repo import appRepo
from app.forms import RegisterForm, ConfirmationForm
from app.models.database import Sweepstake
from datetime import datetime, timedelta, time

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
        cut_off_time = determine_entry_cutoff_time(participant.entry_time)
        if datetime.now() <= cut_off_time:
            errors.append(f"You cannot sign up for this sweepstakes yet. You will be able to enter again after {cut_off_time}")

    # TODO make sure username is unique to email
    # if form.user_name.data != participant.name:
    #     form.user_name.errors.append("Username does not match email.")
    #     errors.append("This username is already in use. Please pick a different one.")
    
    if len(errors) == 0:
        result = appRepo.add_participant(form, sweepstake)
        if not result:
            errors.append("Failed to register for sweepstakes.")
        else:
            sent = email_service.send_registration_email(form.email.data, sweepstake.name, sweepstake.end_date)
            # TODO log if email fails

    return errors

def determine_entry_cutoff_time(last_entry_time: datetime):
    cutt_off = datetime.combine(last_entry_time, time.max)
    return cutt_off

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

def validate_confirmation(participant_id: int, sweepstakes_id: int, confirm_guid: str) -> []:
    errors = []
    participant = appRepo.retrieve_participant(participant_id)
    sweepstake = appRepo.retrieve_sweepstake(sweepstakes_id)
    winner = appRepo.retrieve_winner(confirm_guid)

    if participant is None or sweepstake is None or winner is None:
        errors.append("Not Found.")
        return errors
    
    expiration_date = winner.selection_date + timedelta(hours=int(current_app.config['CONFIRMATION_FORM_LIMIT']))

    if (winner.participant.id != participant.id or winner.sweepstake.id != sweepstake.id):
        errors.append("Invalid data.")

    if winner.confirmed:
        errors.append("This prize has already been claimed.")
    
    if datetime.now() > expiration_date:
        errors.append("The confirmation form has expired.")
            
    return errors

def complete_confirmation(form: ConfirmationForm) -> []:
    errors = []
    if form.validate():
        errors = validate_confirmation(form.sweepstakes_id.data, form.participant_id.data, form.confirmation_guid.data)
    else:
        errors.append("Form filled out incorrectly.")

    if len(errors) == 0:
        winner = appRepo.retrieve_winner(form.confirmation_guid.data)
        if not appRepo.update_winner(form, winner):
            errors.append("An unexpected error occured. Please try again.")
            error_context = {
                "errors": errors,
                "winner_name": winner.participant.name,
                "winner_email": winner.participant.email,
                "winner_id": winner.id,
                "participant_id": winner.participant.id,
                "sweepstake_id": winner.sweepstake.id
            }
            log_service.log_error("Winner confirmation failed", "services.sweepstakes_service.complete_confirmation", error_context)
        else:
            email_service.send_confirmation_email(winner.participant.email, winner.sweepstake.name)
            email_service.send_confirmation_notification(winner.participant.name, winner.sweepstake.name)
    return errors
