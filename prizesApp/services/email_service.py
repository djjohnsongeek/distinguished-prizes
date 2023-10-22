from mailjet_rest import Client
from flask import current_app
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

def build_registration_body(sweepstake_name: str, end_date: datetime):
    body = f"<h3>Your registration for the {sweepstake_name} giveaway is complete!</h3>"
    body += f"<span>Selection of the winner will occur promptly after the giveaway ends at {end_date} EST.</span><br/>"
    body += f"<span>If you are selected you will a receive an email notification. This notification email will contain a link to a confirmation form that must be filled out within <strong>{current_app.config['CONFIRMATION_FORM_LIMIT']} hours</strong>.</span><br/>"
    body += f"<span>Once filled out the prize will mailed to you using the address information provided in the confirmation form. Package tracking information will then be provided.<span/><br/>"
    body += f"<span>If you are unable to fillout the confirmation form within 48 hours, another winner will be chosen :(.</span><br/>"
    body += f"<strong>May the odds be ever in your favor.</strong><br/>"
    body += f"<span>If you have any questions, send an email to {current_app.config['CONTACT_EMAIL']}."

    return body