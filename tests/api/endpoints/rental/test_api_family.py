from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from api.endpoints.rental.family.collection import router as collection_router
from api.endpoints.rental.family.create import router as create_router
from api.endpoints.rental.family.delete import router as delete_router
from api.endpoints.rental.family.one import router as one_router
from api.endpoints.rental.family.update import router as update_router
from database.psql.models.logs import Logs
from database.psql.models.rentals import RentalAllocationRule, RentalBeneficiary
from tests.api.helper import authorized_as, make_client
from tests.core.repository.psql.rental.helper import (
    make_allocation_rule,
    make_apartment,
    make_beneficiary,
    make_beneficiary_settlement,
    make_beneficiary_settlement_item,
    make_billing_period,
)
from tests.core.repository.psql.user.helper import create_test_user


class TestApiRentalBeneficiaries:
    def test_beneficiary01_create_returns_201_and_saves_row(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/beneficiaries/create", json={"name": "Ojciec"}, headers=headers)

        assert response.status_code == 201
        assert response.json()["data"]["name"] == "Ojciec"
        assert db_session.query(RentalBeneficiary).count() == 1

    def test_beneficiary02_create_duplicate_name_returns_409(self, db_session: Session):
        make_beneficiary(db_session, name="Mama")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post("/rentals/beneficiaries/create", json={"name": "Mama"}, headers=headers)

        assert response.status_code == 409

    def test_beneficiary03_collection_filters_by_is_active(self, db_session: Session):
        make_beneficiary(db_session, name="Ja")
        make_beneficiary(db_session, name="Były wspólnik", is_active=False)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            active_rows = client.get("/rentals/beneficiaries/collection", params={"is_active": True}, headers=headers)

        rows = active_rows.json()["data"]
        assert len(rows) == 1 and rows[0]["name"] == "Ja"

    def test_beneficiary04_one_update_delete(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Mama")
        client = make_client(db_session, one_router, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            one = client.get(f"/rentals/beneficiaries/one/{beneficiary.id}", headers=headers)
            updated = client.put(
                f"/rentals/beneficiaries/update/{beneficiary.id}",
                json={"name": "Mama (emerytura)", "is_active": True},
                headers=headers,
            )
            deleted = client.delete(f"/rentals/beneficiaries/delete/{beneficiary.id}", headers=headers)
            missing = client.get(f"/rentals/beneficiaries/one/{uuid4()}", headers=headers)

        assert one.status_code == 200
        assert updated.status_code == 200 and updated.json()["data"]["name"] == "Mama (emerytura)"
        assert deleted.status_code == 200
        assert missing.status_code == 404

    def test_beneficiary05_no_token_401_and_role_user_403(self, db_session: Session):
        client = make_client(db_session, create_router)

        no_token = client.post("/rentals/beneficiaries/create", json={"name": "x"})
        with authorized_as("user") as headers:
            wrong_role = client.post("/rentals/beneficiaries/create", json={"name": "x"}, headers=headers)

        assert no_token.status_code == 401
        assert wrong_role.status_code == 403


class TestApiRentalAllocationRules:
    def test_rule01_create_recurring_returns_201(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Ja")
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/allocation_rules/create",
                json={
                    "beneficiary_id": str(beneficiary.id),
                    "component": "recurring",
                    "mode": "fixed_amount",
                    "amount": -90.00,
                    "description": "podatek",
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )

        assert response.status_code == 201
        body = response.json()["data"]
        assert body["amount"] == -90.00 and body["description"] == "podatek"
        assert db_session.query(RentalAllocationRule).count() == 1

    def test_rule02_create_invalid_component_returns_422(self, db_session: Session):
        client = make_client(db_session, create_router)

        with authorized_as("superadmin") as headers:
            response = client.post(
                "/rentals/allocation_rules/create",
                json={
                    "beneficiary_id": str(uuid4()),
                    "component": "gaz",
                    "mode": "full",
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )

        assert response.status_code == 422

    def test_rule03_collection_filters_by_beneficiary(self, db_session: Session):
        beneficiary = make_beneficiary(db_session, name="Mama")
        make_allocation_rule(db_session, beneficiary=beneficiary, component="water", mode="full", amount=None)
        make_allocation_rule(db_session)
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/rentals/allocation_rules/collection",
                params={"beneficiary_id": str(beneficiary.id)},
                headers=headers,
            )

        rows = response.json()["data"]
        assert len(rows) == 1 and rows[0]["component"] == "water"

    def test_rule04_one_update_delete(self, db_session: Session):
        apartment = make_apartment(db_session)
        rule = make_allocation_rule(db_session, apartment=apartment, amount=1000.00)
        client = make_client(db_session, one_router, update_router, delete_router)

        with authorized_as("superadmin") as headers:
            one = client.get(f"/rentals/allocation_rules/one/{rule.id}", headers=headers)
            updated = client.put(
                f"/rentals/allocation_rules/update/{rule.id}",
                json={
                    "apartment_id": str(apartment.id),
                    "component": "rent",
                    "mode": "fixed_amount",
                    "amount": 1100.00,
                    "description": "czynsz Dudzik",
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )
            deleted = client.delete(f"/rentals/allocation_rules/delete/{rule.id}", headers=headers)

        assert one.status_code == 200
        assert updated.status_code == 200 and updated.json()["data"]["amount"] == 1100.00
        assert deleted.status_code == 200

    def test_rule05_create_writes_audit_log(self, db_session: Session):
        user = create_test_user(db_session, type="superadmin")
        beneficiary = make_beneficiary(db_session)
        client = make_client(db_session, create_router)

        with authorized_as("superadmin", user_id=str(user.id)) as headers:
            client.post(
                "/rentals/allocation_rules/create",
                json={
                    "beneficiary_id": str(beneficiary.id),
                    "component": "electricity",
                    "mode": "full",
                    "start_date": "2026-01-01",
                },
                headers=headers,
            )

        log = db_session.query(Logs).filter(Logs.description == "rental:create_allocation_rule").first()
        assert log is not None and log.username == user.username


class TestApiRentalBeneficiarySettlements:
    def test_beneficiary_settlements01_collection_filters_by_period(self, db_session: Session):
        period = make_billing_period(db_session, period_month=date(2026, 6, 1))
        settlement = make_beneficiary_settlement(db_session, period=period, total_amount=1790.00)
        make_beneficiary_settlement_item(db_session, beneficiary_settlement=settlement)
        make_beneficiary_settlement(db_session, period=make_billing_period(db_session, period_month=date(2026, 7, 1)))
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/rentals/beneficiary_settlements/collection", params={"period_id": str(period.id)}, headers=headers
            )

        rows = response.json()["data"]
        assert len(rows) == 1
        assert rows[0]["total_amount"] == 1790.00
        assert rows[0]["items"][0]["description"] == "czynsz - Pokój Państwa Dudzik"

    def test_beneficiary_settlements02_invalid_uuid_returns_400(self, db_session: Session):
        client = make_client(db_session, collection_router)

        with authorized_as("superadmin") as headers:
            response = client.get(
                "/rentals/beneficiary_settlements/collection", params={"period_id": "not-a-uuid"}, headers=headers
            )

        assert response.status_code == 400
