import os
import uuid
from fastapi import UploadFile

TEMP_DIR = "temp"

def save_temp_file(upload_file: UploadFile) -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)
    file_path = os.path.join(TEMP_DIR, f"{uuid.uuid4().hex}_{upload_file.filename}")
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return file_path

