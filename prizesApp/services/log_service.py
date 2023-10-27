from flask import current_app
import os

error_logs_file = os.path.join(current_app.config["LOGS_DIR"], "error_logs.txt")


def log_error(message: str):
    f = open(error_logs_file, "a")
    