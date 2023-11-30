from flask import flash, Request, current_app, session
from app.repo import appRepo
import uuid

def flash_collection(messages: [], category: str):
    for message in messages:
        flash(message, category)

def parse_boolean_arg(request: Request, key: str) -> bool:
    value = request.args.get(key, None)

    if value is not None:
        value = value.lower()

        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            value = None

    return value

def parse_bool_from_request(requestPayload: dict, key: str) -> bool:
    value = requestPayload.get(key, None)

    if value is not None:
        value = value.lower()

        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            value = None

    return value

def parse_int_from_request(requestPayload: dict, key: str) -> int:
    value = requestPayload.get(key, None)

    if value is not None:
        try:
            value = int(value)
        except:
            value = None

    return value

def get_user_id():
    config = current_app.config

    userId = session.get(config["USER_COOKIE_KEY"], None)

    if userId is None:
        session[config["USER_COOKIE_KEY"]] = str(uuid.uuid4())
        userId = session[config["USER_COOKIE_KEY"]]
    
    return userId

def capture_page_view(request: Request, page: str):
    source = request.args.get("source", "other")
    if source not in current_app.config["TRAFFIC_SOURCES"]:
        source = "other"

    user_id = get_user_id()

    appRepo.record_view(user_id, source, page)