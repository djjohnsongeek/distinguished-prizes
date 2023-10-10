from prizesApp.models.database import Sweepstake
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

    winner = appRepo.retrieve_random_participant(sweepstake)

    # TODO
    # Update sweepstake's winner field
    # send email to customer
    print(winner)
    
    return errors