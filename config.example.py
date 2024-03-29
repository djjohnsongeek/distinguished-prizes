# Place config in the instance directory

import os
cwd = os.getcwd()

DB_NAME = ""
DB_USER = ""
DB_PORT = 0
DB_HOST = ""
DB_PASSWORD = ""

# LOCKOUT_DUR_MINUTES must be > LOCKOUT RANGE
LOCKOUT_RANGE_MINUTES = 0
LOCKOUT_DUR_MINUTES = 0
FAILED_LOGIN_THRESHOLD = 0

CONTACT_EMAIL = ""
MAILJET_API_KEY = ""
MAILJET_SECRET_KEY = ""
MAILJET_SENDER_EMAIL = ""

RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""

CONFIRMATION_FORM_LIMIT = 48
USPS_TRACKING = "https://tools.usps.com/go/TrackConfirmAction_input"
UPS_TRACKING = "https://www.ups.com/track"
FEDEX_TRACKING = "https://www.fedex.com/en-us/tracking.html"

PHOTOS_DIR = os.path.join(cwd, "")
TEST_PHOTOS_DIR = os.path.join(cwd, "")
LOG_FILE_PATH = os.path.join(cwd, "instance", "error_logs.txt")

USER_COOKIE_KEY = "dp-user-id"
TRAFFIC_SOURCES = ["reddit", "discord", "other", "facebook", "twitter", "youtube"]

REGISTRATION_FREQUENCY_HRS = 24

# NOTE: Put config in an instance folder