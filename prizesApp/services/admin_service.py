import uuid
from datetime import datetime
from flask import Request
from prizesApp.models.database import Sweepstake, Participant, Winner
from prizesApp.forms import SweepstakesEditForm, SweepstakesForm
from prizesApp.repo import appRepo
from prizesApp.services import file_service, email_service

def create_sweepstakes(form: SweepstakesForm) -> bool:
    f = form.image.data
    result = file_service.save_file(f, True)

    if result:
        result = appRepo.create_sweepstake(form, f.filename)

    return result

def update_sweepstakes(form: SweepstakesEditForm, sweepstake: Sweepstake) -> bool:
    if form.image.data:
        file_service.save_file(form.image.data)

    return appRepo.update_sweepstake(form, sweepstake)


def select_winner(sweepstake_id: int, request: Request) -> []:
    errors = []
    sweepstake = appRepo.retrieve_sweepstake(sweepstake_id)

    if sweepstake is None:
        errors.append("Sweepstake not found.")
        return errors

    winners = appRepo.retrieve_winners(sweepstake.id)

    if datetime.now() <= sweepstake.end_date:
        errors.append("Sweepstakes has not yet ended.")

    # check for previously selected winners
    for winner in winners:
        if winner.confirmed == True:
            errors.append("A winner has already been chosen. (Confirmed)")
            break

        if winner.confirmed == None:
            errors.append("A winner has already been chosen. (Unconfirmed)")
            break

    if len(errors) == 0:
        selected_participant = appRepo.retrieve_random_participant(sweepstake)
        confirm_guid = str(uuid.uuid4())

        success = appRepo.create_winner(sweepstake, selected_participant, confirm_guid)

        if not success:
            errors.append("Failed to select winner.")
        else:
            confirm_url = f"{request.url_root}sweepstakes/confirmation/{sweepstake.id}/{selected_participant.id}/{confirm_guid}"
            sent = email_service.send_selection_email(
                selected_participant.name,
                selected_participant.email, 
                sweepstake.name,
                confirm_url
            )

            print(sent)
   
    return errors

def mark_fullfilled(request: Request) -> []:
    data = parse_fullfill_request(request)
    winner = appRepo.retrieve_winner_by_id(data["winner_id"])
    errors = validate_fullfill_data(data, winner)

    if len(errors) == 0:
        success = appRepo.update_winner_fullfillment(winner, data)
        if not success:
            errors.append("Failed to update winner with fullfillment information.")
        else:
            sent = email_service.send_fullfillment_email(winner)

    return errors

def parse_fullfill_request(request: Request) -> {}:
    tracking_number = request.form.get("tracking_number", None)
    try:
        winner_id = int(request.form.get("winner_id", None))
    except:
        winner_id = 0
    carrier = request.form.get("carrier", None)

    return { "carrier": carrier, "tracking_number": tracking_number, "winner_id": winner_id}

def validate_fullfill_data(data: {}, winner: Winner) -> []:
    errors = []

    if data["tracking_number"] is None or data["tracking_number"].strip() == "":
        errors.append("Invalid Tracking Number")

    if data["winner_id"] == 0 or winner is None:
        errors.append("Invalid Winner")

    if data["carrier"] not in ["UPS", "USPS", "FEDEX"]:
        errors.append("Invalid Carrier")

    return errors