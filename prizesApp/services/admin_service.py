import uuid
from datetime import datetime
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

        print(sweepstake.__dict__)
        print(winner.__dict__)

        print(f"localhost:5000/sweepstakes/confirmation/{sweepstake.id}/{winner.id}/{confirm_guid}")

    # TODO
    # send email to customer with confirmation link
   
    return errors