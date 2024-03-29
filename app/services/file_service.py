import os, uuid
from flask import current_app
from werkzeug.utils import secure_filename

def save_file(file, required=False) -> bool:
    if required and not file:
        return False
    
    result = True
    original_filename = file.filename
    overwrite_filename(file)
    path = os.path.join(current_app.config["PHOTOS_DIR"], file.filename)
    try:
        file.save(path)
    except:
        file.filename = original_filename
        result = False
    return result

def overwrite_filename(file):
    extension = get_file_extension(file.filename)
    new_filename = str(uuid.uuid4()) + extension
    file.filename = secure_filename(new_filename)

def get_file_extension(filename: str) -> str:
    name, extension = os.path.splitext(filename)
    return extension