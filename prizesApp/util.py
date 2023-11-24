from flask import flash, Request

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

def parse_boolean_post(request: Request, key: str) -> bool:
    value = request.form.get(key, None)

    if value is not None:
        value = value.lower()

        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            value = None

    return value

def parse_int_post(request: Request, key: str) -> int:
    value = request.form.get(key, None)

    if value is not None:
        try:
            value = int(value)
        except:
            value = None

    return value