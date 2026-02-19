from typing import Optional
from core.data.api.date_nager_at.get import Holiday
import requests


def fetch_date_nager_at_pl(year: int, country: str) -> tuple[Optional[list[Holiday]], Optional[str], bool]:
    try:

        response = requests.get(f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country.upper()}", timeout=10)
        response.raise_for_status()

        holidays = [Holiday.from_dict(item) for item in response.json()]
        return holidays, None, True

    except Exception as e:
        return None, f"fetch_date_nager_at_pl error: {e}.", False
