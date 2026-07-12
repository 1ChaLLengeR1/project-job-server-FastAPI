from datetime import datetime, timedelta, timezone

import jwt

from config.settings import settings
from core.service.auth.tokens import encode_access_token
from core.service.contact.token import decode_contact_token, encode_contact_token


class TestContactToken:
    def test_token01_roundtrip_returns_application(self):
        token = encode_contact_token("portfolio")

        application, err, ok = decode_contact_token(token)

        assert ok is True and err is None
        assert application == "portfolio"

    def test_token02_expired_token_rejected(self):
        token = encode_contact_token("portfolio", expires_minutes=-1)

        application, err, ok = decode_contact_token(token)

        assert ok is False and application is None
        assert err.key_type_error == "Unauthorized"
        assert err.type_error == "token_expired"

    def test_token03_wrong_secret_rejected(self):
        now = datetime.now(timezone.utc)
        token = jwt.encode(
            {"application": "portfolio", "exp": now + timedelta(minutes=5)},
            "inny-sekret",
            algorithm=settings.algorithm,
        )

        application, err, ok = decode_contact_token(token)

        assert ok is False
        assert err.type_error == "invalid_token"

    def test_token04_missing_application_claim_rejected(self):
        now = datetime.now(timezone.utc)
        token = jwt.encode(
            {"exp": now + timedelta(minutes=5)},
            settings.secret_key_contact_token,
            algorithm=settings.algorithm,
        )

        application, err, ok = decode_contact_token(token)

        assert ok is False
        assert "application" in err.message

    def test_token05_missing_exp_claim_rejected(self):
        # token bez wygaśnięcia byłby wieczny — wymagamy exp
        token = jwt.encode(
            {"application": "portfolio"},
            settings.secret_key_contact_token,
            algorithm=settings.algorithm,
        )

        application, err, ok = decode_contact_token(token)

        assert ok is False
        assert "exp" in err.message

    def test_token06_access_token_rejected_as_contact_token(self):
        # inny sekret — token usera nie może przejść jako token kontaktowy
        token = encode_access_token("11111111-1111-4111-8111-111111111111")

        application, err, ok = decode_contact_token(token)

        assert ok is False

    def test_token07_application_claim_is_stripped(self):
        token = encode_contact_token("  portfolio  ")

        application, err, ok = decode_contact_token(token)

        assert ok is True
        assert application == "portfolio"
