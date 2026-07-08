from uuid import UUID


def is_valid_uuid(uuid: str, version: int = 4) -> bool:
    try:
        uuid_obj = UUID(uuid, version=version)
        return str(uuid_obj) == uuid
    except ValueError:
        return False


def validate_required_fields(data: dict, required_fields: list[str]) -> tuple[bool, str]:
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return False, f"Missing field(s): {', '.join(missing_fields)}"

    return True, ""
