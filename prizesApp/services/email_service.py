from mailjet_rest import Client
from flask import current_app

def get_mail_client():
    api_key = current_app.config["MAILJET_API_KEY"]
    secret_key = current_app.config["MAILJET_SECRET_KEY"]
    return Client(auth=(api_key, secret_key), version='v3.1')

def get_sender_email() -> str:
    return current_app.config["MAILJET_SENDER_EMAIL"]

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
                    "Email": get_sender_email(),
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

def send_registration_email(email: str, pw: str):
    body = build_registration_body(email, pw)
    send_email(email, "DT Painting Account", body)

def build_registration_body(email: str, pw: str):
    body = "<h3>You have been given user privileges to DT Painting Pro</h3>"
    body += "<strong>User Name</strong><br/>"
    body += f"<span>{email}</span><br/>"
    body += "<strong>Password</strong><br/>"
    body += f"<span>{pw}</span><br/>"

    return body