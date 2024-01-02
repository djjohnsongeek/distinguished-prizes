from datetime import datetime
from mailjet_rest import Client
from select_winner import get_db
from app.models.database import EmailTask
import app.services.log_service
from instance.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, MAILJET_API_KEY, MAILJET_SECRET_KEY, MAILJET_SENDER_EMAIL

def send_emails():
    db = get_db()
    db.connect()

    mail_client = get_mail_client()
    email_tasks = get_pending_tasks()
    send_emails(email_tasks, mail_client, db)

    db.close()

def get_mail_client():
    return Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

def get_pending_tasks():
    return EmailTask.select().where(EmailTask.date_sent is None)

def send_emails(EmailTask: email_tasks, mail_client, db):
    for task in email_tasks:
        if send_email(task, mail_client):
            task.date_sent = datetime.now()

        task.send_attempts += 1

    with db.automatic():
        EmailTask.bulk_update(email_tasks, fields=[EmailTask.date_sent, EmailTask.send_attempts], batch_size=50)

def send_email(email_task, mail_client) -> bool:
    result = mail_client.send.create(data=build_request_data(email_task.to, email_task.subject, "", email_task.body))
    return result.status_code == 200

def build_request_data(to: str, subject: str, plain_text: str, html_text):
    return {
        'Messages': [
		    {
			    "From": {
                    "Email": MAILJET_SENDER_EMAIL,
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

if __name__ == '__main__':
    send_emails()