import click
from flask import current_app, g
from werkzeug.security import generate_password_hash
from peewee import MySQLDatabase
from prizesApp.models.database import *

db_models = [User, Sweepstake, Participant]

def get_db() -> MySQLDatabase:
    if 'db' not in g:
        config = current_app.config
        g.db = MySQLDatabase(
            config["DB_NAME"],
            user=config["DB_USER"],
            password=config["DB_PASSWORD"],
            host=config["DB_HOST"],
            port=config["DB_PORT"]
        )

        for model in db_models:
            model.bind(g.db)

    return g.db

def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.connect()

    db.drop_tables(db_models)
    db.create_tables(db_models)

    User.insert(
        first_name = "Daniel",
        last_name = "Johnson",
        email = "danieleejohnson@gmail.com",
        password_hash = generate_password_hash("password"),
    ).execute()

    # admin_role = Role.create(
    #     name = "Admin"
    # )
    
    # AppUser.insert(
    #     first_name = "Daniel",
    #     last_name = "Johnson",
    #     email = "danieleejohnson@gmail.com",
    #     role = admin_role,
    #     last_login = None,
    #     password_hash = generate_password_hash("password"),
    #     lockout_end = None,
    # ).execute()

    # Carousel.insert_many([
    #     {
    #         "name": "Connect",
    #         "sub_heading": "We want to get to know you.",
    #         "description": "Your perspective and preference flow out of who you are as a person. Your age and stage, previous experiences and even future objectives matter as we have a conversation about your painting needs. We prefer to meet in person but are happy to call, text and email to connect with you.",
    #         "animation_type": "fade",
    #         "interval_length": 3000
    #     },
    #     {
    #         "name": "Reimagine",
    #         "sub_heading": "We want to hear your ideas and speak into them.",
    #         "description": "Color and sheen selection can be a daunting task. Warm and welcoming or minimal and modern? Form and function or classic and collected? From a conversation about your big idea to a color filled picture of your space, we want to help you reimagine a new place to live!",
    #         "animation_type": "fade",
    #         "interval_length": 3000
    #     },
    #     {
    #         "name": "Redeem",
    #         "sub_heading": "We want to bring life back into your space",
    #         "description": "You can relax and watch the transformation! Our team will take great care to protect your floors and furniture, to fill in the holes and cracks, repair damaged walls and trim, prime the stains, sand out the bumps, and bring your space to life with a fresh coat of quality paint! Our satisfaction is fulfilled as your home is redeemed!",
    #         "animation_type": "fade",
    #         "interval_length": 3000
    #     }]).execute()

    # AppConfig.insert_many([
    #     {
    #         "name": "Site Email",
    #         "system_name": "ContactEmail",
    #         "value": "danieleejohnson@gmail.com",
    #         "desc": "Contact email displayed to customers. Also the target of all contact form submissions.",
    #     },
    #     {
    #         "name": "Site Phone Number",
    #         "system_name": "ContactPhone",
    #         "value": "3366550315",
    #         "desc": "Contact phone number displayed to customers.",
    #     },
    #     {
    #         "name": "Mail Jet API Key",
    #         "system_name": "MailJetApiKey",
    #         "value": "0f96ec8ef99595a3a23a539db62c7152",
    #         "desc": "Mail Jet Service uses this api key to send emails.",
    #     },
    #     {
    #         "name": "Mail Jet Secret Key",
    #         "system_name": "MailJetSecretKey",
    #         "value": "9b127ab90896781f0f39bccf4cf6cac7",
    #         "desc": "Mail Jet Services uses this secrety key to send emails.",
    #     },
    #     {
    #         "name": "Mail Jet Sender Email",
    #         "system_name": "MailJetSenderEmail",
    #         "value": "admin@fortheking.dev",
    #         "desc": "All Mail Jet Emails will be sent from this email address.",
    #     }
    # ]).execute()

    # AppStyle.insert_many([
    #     {
    #         "name": "Nav Link Font",
    #         "description": "Font style for the navigation bar.",
    #         "class_name": ".nav-links-font",
    #         "font_id": 1
    #     },
    #     {
    #         "name": "Headings Font",
    #         "description": "Font style for major headings",
    #         "class_name": ".headings-font",
    #         "font_id": 0
    #     },
    #     {
    #         "name": "Sub Headings Font",
    #         "description": "Font style for sub headings.",
    #         "class_name": ".sub-headings-font",
    #         "font_id": 0
    #     },
    #     {
    #         "name": "Main Copy Font",
    #         "description": "Font style for general text content.",
    #         "class_name": ".copy-font",
    #         "font_id": 0
    #     },
    #     {
    #         "name": "Video Overly Font",
    #         "description": "Font style for text overly on the video.",
    #         "class_name": ".video-overlay-font",
    #         "font_id": 0
    #     },
    #     {
    #         "name": "Footer Font",
    #         "description": "Font style for footer text.",
    #         "class_name": ".footer-font",
    #         "font_id": 0
    #     },
    #     {
    #         "name": "Banner Font",
    #         "description": "Font style for the call to action banner",
    #         "class_name": ".banner-font",
    #         "font_id": 0
    #     }
    # ]).execute()
    
    db.close()

def init_app(app):
    app.cli.add_command(init_db_command)
 
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database Initialized ...")