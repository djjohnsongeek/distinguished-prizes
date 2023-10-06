from flask import flash

def flash_collection(messages: [], category: str):
    for message in messages:
        flash(message, category)