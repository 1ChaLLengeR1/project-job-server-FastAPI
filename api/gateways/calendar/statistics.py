from fastapi import Request
from typing import Optional, cast
from datetime import datetime
from core.data.response import Error


def application_gateway_calendar_statistics(
        request: Request
) -> tuple[Optional[dict], Optional[Error], bool, int]:
    try:

        year = request.query_params.get('year')

        if not year:
            return None, Error(
                message="Year and month are required"
            ), False, 400

        try:
            year = int(year)
        except ValueError:
            return None, Error(
                message="Year and month must be integers"
            ), False, 400

        current_year = datetime.now().year
        min_year = 2000
        max_year = current_year + 10

        if year < min_year or year > max_year:
            return None, Error(
                message=f"Year must be between {min_year} and {max_year}"
            ), False, 400

        result = {
            "year": year,
        }
        return result, None, True, 200

    except Exception as e:
        return None, Error(message=str(e)), False, 417
