from datetime import datetime

from core.data.response import Error


def application_gateway_calendar_create(year: int) -> tuple[dict | None, Error | None, bool, int]:
    try:
        current_year = datetime.now().year
        min_year = 2000
        max_year = current_year + 10

        if year < min_year or year > max_year:
            return None, Error(message=f"Year must be between {min_year} and {max_year}"), False, 400

        result = {
            "year": year,
        }
        return result, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 417
