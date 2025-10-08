import os
from pathlib import Path
from typing import List
from fastapi import UploadFile
from config.app_config import DOWNLOAD, TMP, FILE


def save_files_tmp(upload_files: List[UploadFile]) -> List[str] | dict:
    try:

        file_dir = FILE
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        saved_files = []
        for upload_file in upload_files:
            file_path = os.path.join(file_dir, upload_file.filename)
            with open(file_path, "wb") as tmp_file:
                content = upload_file.file.read()
                tmp_file.write(content)

            os.chmod(file_path, 0o777)
            saved_files.append(file_path)

        return saved_files

    except Exception as e:
        return {"error": str(e)}


def check_files_size(upload_files: List[UploadFile]) -> int:
    sum_size = 0
    for upload_file in upload_files:
        sum_size += upload_file.size

    return sum_size
