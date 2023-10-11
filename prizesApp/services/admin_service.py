import uuid
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
    sweepstake = appRepo.retrieve_sweepstake_with_winners(sweepstake_id)
    if sweepstake is None:
        errors.append("Sweepstake not found.")

    # check for previously selected winners
    if len(sweepstake.winner_confirmations) > 0:
        for confirmation in sweepstake.winner_confirmations:
            if confirmation.confirmed == True:
                errors.append("Winner has been already been confirmed.")
            if confirmation.confirmed == None:
                errors.append("There are still unconfirmed winners")
        


    # check if confirm exists

    winner = appRepo.retrieve_random_participant(sweepstake)
    confirm_guid = str(uuid.uuid4())

    success = appRepo.create_winner_confirmation(sweepstake, winner, confirm_guid)
    print(confirm_guid)


    # TODO
    # send email to customer
    # customer needs to fill out secret form
    print(winner)
    
    return errors