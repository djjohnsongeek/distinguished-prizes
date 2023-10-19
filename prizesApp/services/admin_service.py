import uuid
from datetime import datetime
from flask import Request
from prizesApp.models.database import Sweepstake, Participant
from prizesApp.forms import SweepstakesEditForm, SweepstakesForm
from prizesApp.repo import appRepo
from prizesApp.services import file_service

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


def select_winner(sweepstake_id: int) -> []:
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
        winner = appRepo.retrieve_random_participant(sweepstake)
        confirm_guid = str(uuid.uuid4())

        success = appRepo.create_winner(sweepstake, winner, confirm_guid)

        if not success:
            errors.append("Failed to select winner.")

        print(f"localhost:5000/sweepstakes/confirmation/{sweepstake.id}/{winner.id}/{confirm_guid}")

    # TODO
    # send email to customer with confirmation link
   
    return errors

def mark_fullfilled(request: Request) -> []:
    errors = []


def parse_fullfill_request(request) -> {}:

    errors = []

    tracking_number = request.form.get("tracking_number", None)
    try:
        winner_id = int(request.form.get("winner_id", None))
    except:
        winner_id = None
    carrier = request.form.get("carrier", None)

    if tracking_number is None or tracking_number.strip() == "":
        errors.add("Invalid Tracking Number")

    if winner_id is None or winner_id == 0:
        errors.Add("Invalid Winner")

    if carrier not in ["UPS", "USPS", "FEDEX"]:
        errors.add("Invalid Carrier")

    return errors