import uuid
from datetime import datetime
from flask import Request
from app.models.database import Sweepstake, Participant, Winner
from app.forms import SweepstakesEditForm, SweepstakesForm
from app.repo import appRepo
from app.services import file_service, email_service

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

        if winner.confirmed == None and not winner.expired:
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


def get_site_traffic_data():
    data = {
        "siteTraffic": [],
        "siteTrafficSrcs": [],
        "siteTrafficPages": []
    }

    page_views = appRepo.retrieve_site_traffic()

    # split into days
    data_by_day = {}
    traffic_srcs = {}
    traffic_pages = {}
    for page_view in page_views:
        if page_view.timestamp.day not in data_by_day:
            data_by_day[page_view.timestamp.day] = []

        if page_view.source not in traffic_srcs:
            traffic_srcs[page_view.source] = 0

        if page_view.page not in traffic_pages:
            traffic_pages[page_view.page] = 0

        data_by_day[page_view.timestamp.day].append(page_view)
        traffic_srcs[page_view.source] += 1
        traffic_pages[page_view.page] += 1

    #load site traffic data
    for key, value in data_by_day.items():


        # Determine number of unique views
        user_uuid = ""
        unique_views = 0
        for page_view in value:

            # Increment unique view count
            if page_view.user_uuid != user_uuid:
                unique_views += 1
                user_uuid = page_view.user_uuid


        data["siteTraffic"].append([
            value[0].timestamp.strftime("%m/%d/%Y"), unique_views, len(value)
        ])

    # load traffic source data
    for key, value in traffic_srcs.items():
        data["siteTrafficSrcs"].append([
            key, value
        ])

    # load page traffic data
    for key, value in traffic_pages.items():
        data["siteTrafficPages"].append([
            key, value
        ])

    return data