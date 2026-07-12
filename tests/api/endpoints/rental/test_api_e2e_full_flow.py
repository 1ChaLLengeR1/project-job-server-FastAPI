"""Test e2e pełnego przepływu rozliczenia miesiąca — scenariusz wg docs/Obliczenia_3.txt.

Wszystko przez HTTP (TestClient), zero fabryk: słowniki -> okres z prefill ->
odczyty -> preview (błąd licznika głównego + propozycje) -> korekty ->
preview z wyliczeniami -> close z korektą jednorazową -> snapshoty ->
reopen -> ponowny close -> delete.

Modyfikacje względem pliku źródłowego (żądanie: różne liczby osób, nie każde
mieszkanie ma dodatki, podział Ja/Ojciec/Mama per składnik):
- osoby: Dudzik 2, Kydr 1, Witek 3, Łukasz 1 (śmieci 35 zł/os. -> 70/35/105/35),
- internet 60 zł tylko Dudzik i Łukasz; garaż 200 zł tylko Dudzik,
- Ojciec bierze czynsze z 3 mieszkań (Dudzik, Kydr, Witek) + garaż,
- Ja bierze czynsz z Pokoju Łukasza + cały prąd, Mama wodę/internet/śmieci,
- recurring: podatek (Ja -90, Ojciec -270, Mama +360), telefon (Ja -25, Mama +25).
"""

from pytest import approx
from sqlalchemy.orm import Session

from api.endpoints.rental.billing.close import router as billing_close_router
from api.endpoints.rental.billing.collection import router as billing_collection_router
from api.endpoints.rental.billing.create import router as billing_create_router
from api.endpoints.rental.billing.delete import router as billing_delete_router
from api.endpoints.rental.billing.one import router as billing_one_router
from api.endpoints.rental.billing.preview import router as billing_preview_router
from api.endpoints.rental.billing.update import router as billing_update_router
from api.endpoints.rental.dictionaries.create import router as dictionaries_create_router
from api.endpoints.rental.family.collection import router as family_collection_router
from api.endpoints.rental.family.create import router as family_create_router
from database.psql.models.rentals import RentalMeterReading
from tests.api.helper import authorized_as, make_client

ROUTERS = (
    dictionaries_create_router,
    family_create_router,
    family_collection_router,
    billing_create_router,
    billing_collection_router,
    billing_one_router,
    billing_update_router,
    billing_preview_router,
    billing_close_router,
    billing_delete_router,
)

# (klucz, nazwa, osoby, czynsz) — osoby wg żądania: 2/1/3/1
APARTMENTS = (
    ("dudzik", "Pokój Państwa Dudzik", 2, 1100.00),
    ("kydr", "Pokój Łukasza Kydra", 1, 1000.00),
    ("witek", "Pokój Witka", 3, 1000.00),
    ("lukasz", "Pokój Łukasza", 1, 1000.00),
)

# odczyty prądu z Obliczenia_3.txt: (ostatnio, teraz)
ELECTRICITY_READINGS = {
    "dudzik": (5621.26, 5938.86),  # 317.6 kWh
    "kydr": (5245.77, 5330.12),  # 84.35 kWh
    "witek": (533.75, 810.93),  # 277.18 kWh
    "lukasz": (3068.36, 3244.96),  # 176.6 kWh
}
MAIN_METER_READING = (23132, 23990)  # różnica 858

# odczyty wody z Obliczenia_3.txt; licznik Pokoju Łukasza jest nadrzędny
WATER_READINGS = {
    "dudzik": (127.954, 135.079),  # 7.125 m3
    "kydr": (89.866, 89.871),  # 0.005 m3
    "witek": (14.483, 22.710),  # 8.227 m3
    "lukasz": (416.766, 434.577),  # 17.811 - (7.125 + 0.005 + 8.227) = 2.454 m3
}

# koszt prądu po korekcie +1 kWh per mieszkanie, stawka 1.05 zł/kWh (jak w pliku)
EXPECTED = {
    #          prąd  woda  media  media+czynsz
    "dudzik": (335.0, 64.0, 729.0, 1829.0),  # 335+64+70+60+200
    "kydr": (90.0, 0.0, 125.0, 1125.0),  # 90+0+35
    "witek": (292.0, 74.0, 471.0, 1471.0),  # 292+74+105
    "lukasz": (186.0, 22.0, 303.0, 1303.0),  # 186+22+35+60
}

EXPECTED_BENEFICIARY_TOTALS = {
    # czynsz Łukasz 1000 + cały prąd 903 - podatek 90 - telefon 25
    "Ja": 1788.0,
    # czynsze 1100+1000+1000 + garaż 200 - podatek 270
    "Ojciec": 3030.0,
    # woda 160 + internet 120 + śmieci 245 + podatek 360 + telefon 25
    "Mama": 910.0,
}


class TestApiRentalE2EFullMonthFlow:
    def _post(self, client, headers, url, payload):
        response = client.post(url, json=payload, headers=headers)
        assert response.status_code == 201, f"{url}: {response.text}"
        return response.json()["data"]

    def _setup_dictionaries(self, client, headers) -> dict:
        """Słowniki przez API: mieszkania, najemcy, najmy, koszty, liczniki, beneficjenci, reguły."""
        ids = {"apartments": {}, "meters": {}, "beneficiaries": {}}

        for key, name, persons, rent in APARTMENTS:
            apartment = self._post(client, headers, "/rentals/apartments/create", {"name": name})
            ids["apartments"][key] = apartment["id"]
            tenant = self._post(client, headers, "/rentals/tenants/create", {"first_name": name.split()[-1]})
            self._post(
                client,
                headers,
                "/rentals/tenancies/create",
                {
                    "apartment_id": apartment["id"],
                    "tenant_id": tenant["id"],
                    "rent_amount": rent,
                    "persons_count": persons,
                    "start_date": "2026-01-01",
                },
            )

        smieci = self._post(
            client, headers, "/rentals/cost_types/create", {"name": "śmieci", "charge_type": "per_person"}
        )
        internet = self._post(
            client, headers, "/rentals/cost_types/create", {"name": "internet", "charge_type": "fixed"}
        )
        garaz = self._post(client, headers, "/rentals/cost_types/create", {"name": "garaż", "charge_type": "fixed"})
        ids["cost_types"] = {"śmieci": smieci["id"], "internet": internet["id"], "garaż": garaz["id"]}

        # śmieci 35 zł/os. wszędzie; internet tylko Dudzik i Łukasz; garaż tylko Dudzik
        costs = [(key, smieci["id"], 35.00) for key in ids["apartments"]]
        costs += [("dudzik", internet["id"], 60.00), ("lukasz", internet["id"], 60.00)]
        costs += [("dudzik", garaz["id"], 200.00)]
        for apartment_key, cost_type_id, amount in costs:
            self._post(
                client,
                headers,
                "/rentals/apartment_costs/create",
                {
                    "apartment_id": ids["apartments"][apartment_key],
                    "cost_type_id": cost_type_id,
                    "amount": amount,
                    "start_date": "2026-01-01",
                },
            )

        main_meter = self._post(
            client, headers, "/rentals/meters/create", {"media_type": "electricity", "name": "licznik główny"}
        )
        ids["meters"]["main"] = main_meter["id"]
        for key in ids["apartments"]:
            electricity = self._post(
                client,
                headers,
                "/rentals/meters/create",
                {"media_type": "electricity", "apartment_id": ids["apartments"][key]},
            )
            water = self._post(
                client,
                headers,
                "/rentals/meters/create",
                {
                    "media_type": "water",
                    "apartment_id": ids["apartments"][key],
                    "is_master": key == "lukasz",  # woda Pokoju Łukasza jest licznikiem nadrzędnym
                },
            )
            ids["meters"][f"{key}_electricity"] = electricity["id"]
            ids["meters"][f"{key}_water"] = water["id"]

        for name in ("Ja", "Ojciec", "Mama"):
            beneficiary = self._post(client, headers, "/rentals/beneficiaries/create", {"name": name})
            ids["beneficiaries"][name] = beneficiary["id"]

        rules = [
            # Ja: czynsz z Pokoju Łukasza + cały prąd + podatek/telefon
            ("Ja", "rent", "full", "lukasz", None, None, "czynsz"),
            ("Ja", "electricity", "full", None, None, None, "prąd"),
            ("Ja", "recurring", "fixed_amount", None, None, -90.00, "podatek"),
            ("Ja", "recurring", "fixed_amount", None, None, -25.00, "telefon"),
            # Ojciec: czynsze z 3 mieszkań + garaż + podatek
            ("Ojciec", "rent", "full", "dudzik", None, None, "czynsz"),
            ("Ojciec", "rent", "full", "kydr", None, None, "czynsz"),
            ("Ojciec", "rent", "full", "witek", None, None, "czynsz"),
            ("Ojciec", "cost_type", "full", None, "garaż", None, "garaż"),
            ("Ojciec", "recurring", "fixed_amount", None, None, -270.00, "podatek"),
            # Mama: woda + internet + śmieci + podatek/telefon
            ("Mama", "water", "full", None, None, None, "woda"),
            ("Mama", "cost_type", "full", None, "internet", None, "internet"),
            ("Mama", "cost_type", "full", None, "śmieci", None, "śmieci"),
            ("Mama", "recurring", "fixed_amount", None, None, 360.00, "podatek"),
            ("Mama", "recurring", "fixed_amount", None, None, 25.00, "telefon"),
        ]
        for beneficiary, component, mode, apartment_key, cost_type_name, amount, description in rules:
            self._post(
                client,
                headers,
                "/rentals/allocation_rules/create",
                {
                    "beneficiary_id": ids["beneficiaries"][beneficiary],
                    "component": component,
                    "mode": mode,
                    "apartment_id": ids["apartments"][apartment_key] if apartment_key else None,
                    "cost_type_id": ids["cost_types"][cost_type_name] if cost_type_name else None,
                    "amount": amount,
                    "description": description,
                    "start_date": "2026-01-01",
                },
            )
        return ids

    def _fill_readings(self, client, headers, ids, period_id) -> dict:
        """Wpisanie odczytów 'Ostatnio'/'Teraz' w prefillowane szkielety odczytów."""
        readings = client.get(f"/rentals/readings/collection/{period_id}", headers=headers).json()["data"]
        assert len(readings) == 9  # licznik główny + 4x prąd + 4x woda
        assert all(reading["previous_value"] == 0 for reading in readings)  # brak historii -> prefill 0

        reading_by_meter = {reading["meter_id"]: reading["id"] for reading in readings}
        values = {ids["meters"]["main"]: MAIN_METER_READING}
        for key, (previous, current) in ELECTRICITY_READINGS.items():
            values[ids["meters"][f"{key}_electricity"]] = (previous, current)
        for key, (previous, current) in WATER_READINGS.items():
            values[ids["meters"][f"{key}_water"]] = (previous, current)

        for meter_id, (previous, current) in values.items():
            response = client.put(
                f"/rentals/readings/update/{reading_by_meter[meter_id]}",
                json={"previous_value": previous, "current_value": current, "error_correction": 0},
                headers=headers,
            )
            assert response.status_code == 200
        return reading_by_meter

    def _settlements_by_key(self, preview_data, ids) -> dict:
        apartment_key_by_id = {apartment_id: key for key, apartment_id in ids["apartments"].items()}
        return {
            apartment_key_by_id[entry["apartment_id"]]: entry["settlement"] for entry in preview_data["settlements"]
        }

    def test_e2e01_full_month_flow(self, db_session: Session):
        client = make_client(db_session, *ROUTERS)

        with authorized_as("superadmin") as headers:
            ids = self._setup_dictionaries(client, headers)

            # --- okres z rachunkiem prądu i ręczną stawką 1.05 zł/kWh (jak "koszt" w pliku) ---
            period = self._post(
                client,
                headers,
                "/rentals/periods/create",
                {
                    "period_month": "2026-06-01",
                    "electricity_bill_amount": 899.48,
                    "electricity_rate": 1.05,
                    "electricity_rate_is_manual": True,
                    "water_rate": 9.00,
                },
            )
            period_id = period["id"]
            reading_by_meter = self._fill_readings(client, headers, ids, period_id)

            # --- preview 1: błąd licznika głównego z propozycją podziału ---
            preview = client.post(
                f"/rentals/periods/preview/{period_id}", json={"adjustments": []}, headers=headers
            ).json()["data"]
            assert preview["electricity_rate"] == 1.05
            assert preview["electricity_total_consumption"] == approx(855.73)
            main_error = preview["main_meter_error"]
            assert main_error["main_difference"] == approx(858)
            assert main_error["error"] == approx(2.27)  # "Błąd_między_licznikami" z pliku
            assert len(main_error["proposals"]) == 4

            # --- ręczna korekta: +1 kWh per mieszkanie (jak "Bład_Licznika: 1" w pliku) ---
            for key, (previous, current) in ELECTRICITY_READINGS.items():
                reading_id = reading_by_meter[ids["meters"][f"{key}_electricity"]]
                response = client.put(
                    f"/rentals/readings/update/{reading_id}",
                    json={"previous_value": previous, "current_value": current, "error_correction": 1},
                    headers=headers,
                )
                assert response.status_code == 200

            # --- preview 2: pełne wyliczenie per mieszkanie i podział rodzinny ---
            preview = client.post(
                f"/rentals/periods/preview/{period_id}", json={"adjustments": []}, headers=headers
            ).json()["data"]
            assert preview["electricity_total_consumption"] == approx(859.73)
            assert preview["warnings"] == []

            settlements = self._settlements_by_key(preview, ids)
            for key, (electricity, water, media, total) in EXPECTED.items():
                assert settlements[key]["electricity_cost"] == electricity, key
                assert settlements[key]["water_cost"] == water, key
                assert settlements[key]["total_media_amount"] == media, key
                assert settlements[key]["total_amount"] == total, key
            # zużycie wody licznika nadrzędnego = odczyt - suma pozostałych mieszkań
            assert settlements["lukasz"]["water_consumption"] == approx(2.454)
            # "prąd dla mnie" z pliku: suma kosztów prądu wszystkich mieszkań
            assert sum(EXPECTED[key][0] for key in EXPECTED) == 903.0

            beneficiary_totals = {
                entry["beneficiary_name"]: entry["total_amount"] for entry in preview["beneficiaries"]
            }
            assert beneficiary_totals == EXPECTED_BENEFICIARY_TOTALS

            # --- close z korektą jednorazową: rabat -200 zł dla Dudzika (jak "- 200" w pliku) ---
            closed = client.post(
                f"/rentals/periods/close/{period_id}",
                json={"adjustments": [{"apartment_id": ids["apartments"]["dudzik"], "name": "rabat", "amount": -200}]},
                headers=headers,
            )
            assert closed.status_code == 200
            closed_data = closed.json()["data"]
            assert closed_data["period"]["status"] == "closed"
            closed_settlements = self._settlements_by_key(closed_data, ids)
            assert closed_settlements["dudzik"]["total_media_amount"] == 529.0  # 729 - 200, "Razem" z pliku
            assert closed_settlements["dudzik"]["total_amount"] == 1629.0

            # --- snapshoty rozliczeń mieszkań w bazie ---
            saved = client.get(
                "/rentals/settlements/collection", params={"period_id": period_id}, headers=headers
            ).json()["data"]
            assert len(saved) == 4
            saved_dudzik = next(row for row in saved if row["apartment_id"] == ids["apartments"]["dudzik"])
            assert saved_dudzik["rent_amount"] == 1100.0 and saved_dudzik["total_amount"] == 1629.0
            item_amounts = sorted(item["amount"] for item in saved_dudzik["items"])
            assert item_amounts == [-200.0, 60.0, 70.0, 200.0]  # rabat, internet, śmieci 2x35, garaż
            rabat = next(item for item in saved_dudzik["items"] if item["amount"] == -200.0)
            assert rabat["kind"] == "adjustment" and rabat["cost_type_id"] is None

            # --- snapshoty podziału rodzinnego ---
            beneficiary_rows = client.get(
                "/rentals/beneficiary_settlements/collection", params={"period_id": period_id}, headers=headers
            ).json()["data"]
            beneficiary_name_by_id = {v: k for k, v in ids["beneficiaries"].items()}
            saved_totals = {
                beneficiary_name_by_id[row["beneficiary_id"]]: row["total_amount"] for row in beneficiary_rows
            }
            assert saved_totals == EXPECTED_BENEFICIARY_TOTALS
            items_count = {beneficiary_name_by_id[row["beneficiary_id"]]: len(row["items"]) for row in beneficiary_rows}
            # Ja: czynsz + 4x prąd + podatek + telefon; Ojciec: 3x czynsz + 4x garaż (w tym 0 zł) + podatek;
            # Mama: 4x woda + 4x internet + 4x śmieci + podatek + telefon
            assert items_count == {"Ja": 7, "Ojciec": 8, "Mama": 14}
            saved_ojciec = next(
                row for row in beneficiary_rows if beneficiary_name_by_id[row["beneficiary_id"]] == "Ojciec"
            )
            garage_amounts = [
                item["amount"] for item in saved_ojciec["items"] if item["description"].startswith("garaż")
            ]
            assert sorted(garage_amounts) == [0.0, 0.0, 0.0, 200.0]  # garaż ma tylko Dudzik

            # --- zamknięty okres: edycja zablokowana, reopen kasuje snapshoty ---
            blocked_update = client.put(
                f"/rentals/periods/update/{period_id}",
                json={"electricity_rate_is_manual": True, "water_rate": 9.00},
                headers=headers,
            )
            assert blocked_update.status_code == 409

            reopened = client.post(f"/rentals/periods/reopen/{period_id}", headers=headers)
            assert reopened.status_code == 200 and reopened.json()["data"]["status"] == "draft"
            assert (
                client.get("/rentals/settlements/collection", params={"period_id": period_id}, headers=headers).json()[
                    "data"
                ]
                == []
            )
            assert (
                client.get(
                    "/rentals/beneficiary_settlements/collection", params={"period_id": period_id}, headers=headers
                ).json()["data"]
                == []
            )

            # --- ponowny close bez rabatu: odczyty przetrwały reopen, Dudzik wraca do 729 zł ---
            reclosed = client.post(f"/rentals/periods/close/{period_id}", json={"adjustments": []}, headers=headers)
            assert reclosed.status_code == 200
            reclosed_settlements = self._settlements_by_key(reclosed.json()["data"], ids)
            assert reclosed_settlements["dudzik"]["total_media_amount"] == 729.0

            # --- pełne wycofanie okresu ---
            deleted = client.delete(f"/rentals/periods/delete/{period_id}", headers=headers)
            assert deleted.status_code == 200
            assert client.get(f"/rentals/periods/one/{period_id}", headers=headers).status_code == 404
            assert db_session.query(RentalMeterReading).count() == 0
