import os
from uuid import UUID
from typing import List, Dict
from dotenv import load_dotenv
from consumer.data.response import ResponseData

from config.app_config import ENV_MODE

env_file_path = os.path.join('env', f'{ENV_MODE}.env')
load_dotenv(env_file_path)


def is_valid_uuid(uuid: str, version: int = 4) -> bool:
    try:
        uuid_obj = UUID(uuid, version=version)
        return str(uuid_obj) == uuid
    except ValueError:
        return False


def get_env_variable(name_env: str) -> str:
    value = os.getenv(name_env)
    if not value:
        raise Exception(f"Missing required environment variable: {name_env}")
    return value.strip('"').strip("'")


def validate_required_fields(data: Dict, required_fields: List[str]) -> tuple[bool, str]:
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return False, f"Missing field(s): {', '.join(missing_fields)}"

    return True, f""
