from flask import current_app
from app.models.database import Winner, EmailTask
from datetime import datetime

def queue_email(to: str, subject: str, body: str) -> bool:
    EmailTask.insert(
        to=to,
        subject=subject,
        body=body,
        date_created=datetime.now(),
    ).execute()

def send_registration_email(email: str, sweepstake_name: str, end_date: datetime) -> bool:
    body = build_registration_body(sweepstake_name, end_date)
    return queue_email(email, "Registration successful!", body)

def send_selection_email(username: str, email: str, sweepstake_name: str, confirm_url: str) -> bool:
    body = build_selection_body(sweepstake_name, username, confirm_url)
    return queue_email(email, "You have been selected!", body)

def send_confirmation_email(email: str, sweepstake_name: str) -> bool:
    body = build_confirmation_body(sweepstake_name)
    return queue_email(email, "Confirmation Complete!", body)

def send_confirmation_notification(username: str, sweepstake_name: str) -> bool:
    return queue_email(current_app.config["CONTACT_EMAIL"], "Winner Confirmed", f"{username} has filled out the confirmation form for the {sweepstake_name} giveaway")

def send_fullfillment_email(winner: Winner) -> bool:
    return queue_email(winner.participant.email, "Your package has shipped!", build_fullfillment_email(winner))

def build_registration_body(sweepstake_name: str, end_date: datetime):
    body = f"<h3>Your registration for the {sweepstake_name} giveaway was successful!</h3>"\
    f"<span>Selection of the winner will occur promptly after the giveaway ends at {end_date.strftime('%a %d %b %Y, %I:%M%p %Z')}.</span><br/>"\
    f"<span>If you are selected you will a receive an email notification with futher instructions. If you have any questions, please send an email to {current_app.config['CONTACT_EMAIL']}.</span><br/>"\
    f"<strong>May the RNG be ever in your favor.</strong><br/>"
    return body

def build_selection_body(sweepstake_name: str, username: str, confirm_url: str):
    body = f"<h3>Congratulations {username}! You have been selected as the winner of the {sweepstake_name} giveaway!</h3>"\
    f"<span>There is one more step to complete. Please fill out this <a href='{confirm_url}' target='_blank'>confirmation form</a> online.</span><br/>"\
    f"<span>Once filled out the prize will be mailed to you using the address information provided by the confirmation form. Package tracking information will then be emailed to you.<span/><br/>"\
    f"<span>If you are unable to fillout the confirmation form within {current_app.config['CONFIRMATION_FORM_LIMIT']} hours, another winner will be chosen.</span><br/>"\
    f"<span>If you have any questions, send an email to {current_app.config['CONTACT_EMAIL']}.</span><br/>"
    return body

def build_confirmation_body(sweepstake_name: str) -> str:
    body = f"<h3>Congratulations! You are now the confirmed winner of the {sweepstake_name} giveaway!</h3>"\
    f"<span>The next email you get from us will have package tracking information.</span><br/>"\
    f"<span>If you have any questions, send an email to {current_app.config['CONTACT_EMAIL']}.</span><br/>"
    return body

def build_fullfillment_email(winner: Winner) -> str:
    body = f"<h3>Your {winner.sweepstake.name} is on the way!</h3>"\
    f"<span>You can track your package on the <a href='{current_app.config[winner.carrier + '_TRACKING']}'>{winner.carrier} website</a> with the following tracking code: <strong>{winner.tracking_number}</strong><br/>"\
    f"<span>We sincerely hope you enjoy the gift!</span><br/>"\
    f"<span>If you have any questions, send an email to {current_app.config['CONTACT_EMAIL']}.</span><br/>"
    return body