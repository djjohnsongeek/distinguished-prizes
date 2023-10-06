from prizesApp.repo import appRepo
from prizesApp.forms import RegisterForm

def add_participant(form: RegisterForm) -> bool:
    if not form.validate():
        return False

    sweepstakes = appRepo.retrieve_sweepstake(form.sweepstakes_id.data)
    if sweepstakes is None:
        return False

    result = appRepo.add_participant(form, sweepstakes)

    return result