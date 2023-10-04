from prizesApp.models.database import Sweepstake
from prizesApp.forms import SweepstakesEditForm, SweepstakesForm
from prizesApp.repo import appRepo
from prizesApp.services import file_service

def create_sweepstakes(form: SweepstakesForm) -> []:
    f = form.image.data
    errors = file_service.save_file(f)

    if len(errors) == 0:
        result = appRepo.create_sweepstake(form, f.filename)
        if not result:
            errors.append("Failed to create sweepstakes.")

    return errors

def update_sweepstakes(form: SweepstakesEditForm, sweepstake: Sweepstake) -> bool:

    # TODO Save file



    return appRepo.update_sweepstake(form, sweepstake)