import requests

from api.response import ApiErrorData
from core.service.calendar.response import Holiday


def fetch_public_holidays(year: int, country: str = "PL") -> tuple[list[Holiday] | None, ApiErrorData | None, bool]:
    """Pobiera dni ustawowo wolne z zewnętrznego API date.nager.at."""
    try:
        response = requests.get(
            f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country.upper()}", timeout=10
        )
        response.raise_for_status()

        holidays = [Holiday.from_dict(item) for item in response.json()]
        return holidays, None, True
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="fetch_public_holidays",
            type_error="external_service_error",
            key_type_error="ExternalService",
        ), False
