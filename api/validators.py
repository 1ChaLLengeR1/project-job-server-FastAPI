from uuid import UUID


def is_valid_uuid(value: str, version: int = 4) -> bool:
    try:
        return str(UUID(value, version=version)) == value
    except ValueError:
        return False


def validate_uuid(value: str) -> str:
    """Do użycia w Pydantic field_validator — rzuca ValueError."""
    if not is_valid_uuid(value):
        raise ValueError(f"'{value}' nie jest poprawnym UUID v4")
    return value


def validate_non_empty_str(value: str) -> str:
    """Do użycia w Pydantic field_validator — rzuca ValueError."""
    if not value or not value.strip():
        raise ValueError("Pole nie może być puste")
    return value.strip()


def validate_required_fields(data: dict, required_fields: list[str]) -> tuple[bool, str]:
    missing = [field for field in required_fields if field not in data]
    if missing:
        return False, f"Missing field(s): {', '.join(missing)}"
    return True, ""
