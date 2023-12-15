from flask import session, current_app
from app.services import email_service, log_service
from app.repo import appRepo
from app.forms import RegisterForm, ConfirmationForm
from app.models.database import Sweepstake, Participant, Entry
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
    
    errors, participant = retrieve_or_create_participant(form)

    if len(errors) > 0:
        return errors

    latest_entry = appRepo.retrieve_latest_entry(sweepstake, participant)
    if not participant_can_enter(latest_entry):
        errors.append(f"You can only enter for this sweepstakes every {current_app.config['REGISTRATION_FREQUENCY_HRS']} hours")

    if len(errors) == 0:
        if not appRepo.create_entry(sweepstake, participant):
            errors.append("Failed to register for sweepstakes.")
        else:
            sent = email_service.send_registration_email(form.email.data, sweepstake.name, sweepstake.end_date)
            log_service.log_error(f"Failed ot sent registration email to {form.email.data}", "sweepstate_service.add_participant()", None)

    return errors

def retrieve_or_create_participant(form: RegisterForm) -> ([], Participant):
    errors = []
    participant = appRepo.retrieve_participant_by_email(form.email.data)

    if participant is None:
        if appRepo.username_exists(form.user_name.data):
            errors.append("The provided username already exists")
        else:
            participant = appRepo.create_participant(form)

    if participant is None:
        errors.append("Failed to retrieve or create participant.")

    return (errors, participant)

def participant_can_enter(latest_entry: Entry) -> bool:
    if latest_entry is None:
        return True

    cut_off = latest_entry.entry_time + timedelta(hours=current_app.config["REGISTRATION_FREQUENCY_HRS"])
    return datetime.now() > cut_off

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
