import os
cwd = os.getcwd()

DB_NAME = ""
DB_USER = ""
DB_PORT = 0
DB_HOST = ""
DB_PASSWORD = ""

LOCKOUT_RANGE_MINUTES = 0
LOCKOUT_DUR_MINUTES = 0
FAILED_LOGIN_THRESHOLD = 0

PHOTOS_DIR = os.path.join(cwd, "")
TEST_PHOTOS_DIR = os.path.join(cwd, "")

# NOTE: Put config in an instance folder