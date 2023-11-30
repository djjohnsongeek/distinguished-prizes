from flask import current_app
from datetime import datetime

def log_error(message: str, area: str, context: dict):
    with open(current_app.config["LOG_FILE_PATH"], "a") as f:
        line = f"{datetime.now()}, {area}, {message}, {context}\n"
        f.write(line)