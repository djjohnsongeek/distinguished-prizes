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

    winner_confirmations = appRepo.retrieve_winner_confirmations(sweepstake.id)

    if datetime.now() <= sweepstake.end_date:
        errors.append("Sweepstakes has not yet ended.")

    print(winner_confirmations)
    print(sweepstake.__dict__)

    # check for previously selected winners
    for confirmation in winner_confirmations:
        if confirmation.confirmed == True:
            errors.append("Winner has been already been confirmed.")
            break

        if confirmation.confirmed == None:
            errors.append("There are still unconfirmed winners")
            break

    if len(errors) == 0:
        winner = appRepo.retrieve_random_participant(sweepstake)
        confirm_guid = str(uuid.uuid4())
        success = appRepo.create_winner_confirmation(sweepstake, winner, confirm_guid)

        print(winner)
        print(confirm_guid)


    # TODO
    # send email to customer
    # customer needs to fill out secret form

    
    return errors