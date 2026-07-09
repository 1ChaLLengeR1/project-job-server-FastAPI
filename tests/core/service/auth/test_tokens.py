import uuid
from datetime import datetime, timedelta, timezone

import jwt

from config.settings import settings
from core.service.auth.tokens import (
    decode_access_token,
    decode_refresh_token,
    encode_access_token,
    encode_refresh_token,
)

USER_ID = str(uuid.uuid4())
OTHER_USER_ID = str(uuid.uuid4())


class TestAccessToken:
    def test_access01_encode_decode_roundtrip(self):
        token = encode_access_token(USER_ID)

        user_id, err, ok = decode_access_token(token)

        assert ok is True and err is None
        assert user_id == USER_ID

    def test_access02_garbage_token_returns_unauthorized(self):
        user_id, err, ok = decode_access_token("abc.def.ghi")

        assert ok is False and user_id is None
        assert err.key_type_error == "Unauthorized"
        assert err.type_error == "invalid_token"

    def test_access03_expired_token_returns_token_expired(self):
        expired = jwt.encode(
            {"id": USER_ID, "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
            settings.secret_key_token,
            algorithm=settings.algorithm,
        )

        user_id, err, ok = decode_access_token(expired)

        assert ok is False
        assert err.type_error == "token_expired"
        assert err.key_type_error == "Unauthorized"

    def test_access04_missing_id_claim_returns_error(self):
        token = jwt.encode(
            {"exp": datetime.now(timezone.utc) + timedelta(hours=1)},
            settings.secret_key_token,
            algorithm=settings.algorithm,
        )

        user_id, err, ok = decode_access_token(token)

        assert ok is False
        assert "id" in err.message

    def test_access05_id_claim_not_uuid_returns_error(self):
        token = jwt.encode(
            {"id": "nie-uuid", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
            settings.secret_key_token,
            algorithm=settings.algorithm,
        )

        user_id, err, ok = decode_access_token(token)

        assert ok is False
        assert "UUID" in err.message

    def test_access06_refresh_token_rejected_as_access(self):
        # inny sekret — refresh token nie może przejść jako access
        token = encode_refresh_token(USER_ID)

        user_id, err, ok = decode_access_token(token)

        assert ok is False
        assert err.key_type_error == "Unauthorized"


class TestRefreshToken:
    def test_refresh01_encode_decode_roundtrip(self):
        token = encode_refresh_token(USER_ID)

        user_id, err, ok = decode_refresh_token(token, USER_ID)

        assert ok is True and err is None
        assert user_id == USER_ID

    def test_refresh02_token_of_other_user_returns_mismatch(self):
        token = encode_refresh_token(USER_ID)

        user_id, err, ok = decode_refresh_token(token, OTHER_USER_ID)

        assert ok is False and user_id is None
        assert err.type_error == "token_mismatch"
        assert err.key_type_error == "Unauthorized"

    def test_refresh03_access_token_rejected_as_refresh(self):
        token = encode_access_token(USER_ID)

        user_id, err, ok = decode_refresh_token(token, USER_ID)

        assert ok is False
        assert err.key_type_error == "Unauthorized"
