from datetime import date

import pytest

from core.service.calendar.holidays import fetch_public_holidays
from core.service.calendar.response import Holiday


class TestHolidayResponse:
    def test_holiday01_from_dict_maps_api_fields(self):
        holiday = Holiday.from_dict(
            {
                "date": "2030-05-01",
                "localName": "Święto Pracy",
                "name": "Labour Day",
                "countryCode": "PL",
                "fixed": True,
                "global": True,
                "counties": None,
                "launchYear": None,
                "types": ["Public"],
            }
        )

        assert holiday.local_name == "Święto Pracy"
        assert holiday.country_code == "PL"
        assert holiday.global_ is True

    def test_holiday02_date_object_parses_iso_string(self):
        holiday = Holiday.from_dict(
            {
                "date": "2030-12-25",
                "localName": "x",
                "name": "x",
                "countryCode": "PL",
                "fixed": True,
                "global": True,
                "counties": None,
                "launchYear": None,
                "types": [],
            }
        )

        assert holiday.date_object == date(2030, 12, 25)


class TestFetchPublicHolidays:
    @pytest.mark.api_integration
    def test_fetch01_returns_polish_holidays(self):
        result, err, ok = fetch_public_holidays(2030, "PL")

        assert ok is True and err is None
        assert len(result) >= 10
        assert any(holiday.date == "2030-05-01" for holiday in result)

    @pytest.mark.api_integration
    def test_fetch02_invalid_country_returns_external_service_error(self):
        result, err, ok = fetch_public_holidays(2030, "XX")

        assert ok is False and result is None
        assert err.key_type_error == "ExternalService"
