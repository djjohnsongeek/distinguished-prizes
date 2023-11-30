from mailjet_rest import Client
from flask import current_app
from app.models.database import Winner
from app.services import log_service
from datetime import datetime

def get_mail_client():
    api_key = current_app.config["MAILJET_API_KEY"]
    secret_key = current_app.config["MAILJET_SECRET_KEY"]
    return Client(auth=(api_key, secret_key), version='v3.1')

def get_customer_contact() -> str:
    return current_app.config["CONTACT_EMAIL"]

def send_email(to: str, subject: str, body: str) -> bool:
    mail_client = get_mail_client()
    result = mail_client.send.create(data=build_request_data(to, subject, "", body))

    if result.status_code != 200:
        log_service.log_error("Failed to send email", "Email Service", { "to": to, "subject": subject, "result": result.json() })

    return result.status_code == 200

def build_email_body(form_data: dict) -> str:
    body = "<h3>A Customer filled out your contact form<h3/>"
    for key, value in form_data.items():
        if len(value) > 0:
            body += f"<strong>{key}</strong><br/>"
            body += f"{value}<br/>"
    return body

def build_request_data(to: str, subject: str, plain_text: str, html_text):
    return {
        'Messages': [
		    {
			    "From": {
                    "Email": current_app.config["MAILJET_SENDER_EMAIL"],
                    "Name": "Distinguished Prizes"
				},
                "To": [
                    {
                        "Email": to,
                        "Name": to,
                    }
                ],
                "Subject": subject,
                "TextPart": plain_text,
                "HTMLPart": html_text,
			}
		]
    }

def send_registration_email(email: str, sweepstake_name: str, end_date: datetime) -> bool:
    body = build_registration_body(sweepstake_name, end_date)
    return send_email(email, "Registration successful!", body)

def send_selection_email(username: str, email: str, sweepstake_name: str, confirm_url: str) -> bool:
    body = build_selection_body(sweepstake_name, username, confirm_url)
    return send_email(email, "You have been selected!", body)

def send_confirmation_email(email: str, sweepstake_name: str) -> bool:
    body = build_confirmation_body(sweepstake_name)
    return send_email(email, "Confirmation Complete!", body)

def send_confirmation_notification(username: str, sweepstake_name: str) -> bool:
    return send_email(current_app.config["CONTACT_EMAIL"], "Winner Confirmed", f"{username} has filled out the confirmation form for the {sweepstake_name} giveaway")

def send_fullfillment_email(winner: Winner) -> bool:
    return send_email(winner.participant.email, "Your package has shipped!", build_fullfillment_email(winner))

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