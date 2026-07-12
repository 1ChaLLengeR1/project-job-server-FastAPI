import uuid
from types import SimpleNamespace

import jwt as jwt_lib
from starlette.requests import Request

from config.rate_limit import (
    RATE_LIMIT_AUTH,
    RATE_LIMIT_READ,
    RATE_LIMIT_WRITE,
    auth_or_ip_key,
    limiter,
    rate_limit_exceeded_handler,
)
from config.settings import settings


def make_request(headers: dict | None = None, client_ip: str = "1.2.3.4") -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/",
        "query_string": b"",
        "scheme": "http",
        "server": ("testserver", 80),
        "client": (client_ip, 50000),
        "headers": [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()],
    }
    return Request(scope)


class TestRateLimitConstants:
    def test_constants01_expected_values(self):
        assert RATE_LIMIT_AUTH == "10/minute"
        assert RATE_LIMIT_READ == "120/minute"
        assert RATE_LIMIT_WRITE == "60/minute"

    def test_constants02_limiter_has_global_default(self):
        assert limiter._default_limits  # 200/second globalnie


class TestAuthOrIpKey:
    def test_key01_bearer_token_gives_user_key(self):
        user_id = str(uuid.uuid4())
        token = jwt_lib.encode({"id": user_id}, settings.secret_key_token, algorithm=settings.algorithm)
        request = make_request({"Authorization": f"Bearer {token}"})

        assert auth_or_ip_key(request) == f"user:{user_id}"

    def test_key02_no_header_falls_back_to_ip(self):
        request = make_request(client_ip="5.6.7.8")

        assert auth_or_ip_key(request) == "5.6.7.8"

    def test_key03_garbage_token_falls_back_to_ip(self):
        request = make_request({"Authorization": "Bearer abc.def.ghi"}, client_ip="5.6.7.8")

        assert auth_or_ip_key(request) == "5.6.7.8"

    def test_key04_token_without_id_claim_falls_back_to_ip(self):
        token = jwt_lib.encode({"sub": "x"}, settings.secret_key_token, algorithm=settings.algorithm)
        request = make_request({"Authorization": f"Bearer {token}"}, client_ip="5.6.7.8")

        assert auth_or_ip_key(request) == "5.6.7.8"

    def test_key05_signature_is_not_verified(self):
        # klucz limitera nie weryfikuje podpisu — autoryzację robi middleware
        user_id = str(uuid.uuid4())
        token = jwt_lib.encode({"id": user_id}, "zupelnie-inny-sekret", algorithm=settings.algorithm)
        request = make_request({"Authorization": f"Bearer {token}"})

        assert auth_or_ip_key(request) == f"user:{user_id}"


class TestRateLimitExceededHandler:
    def test_handler01_returns_429_with_envelope(self):
        exc = SimpleNamespace(detail="10 per 1 minute")

        response = rate_limit_exceeded_handler(make_request(), exc)

        assert response.status_code == 429
        import json

        body = json.loads(response.body)
        assert body["status"] == "ERROR"
        assert body["status_code"] == 429
        assert body["data"]["type_error"] == "rate_limit_exceeded"
        assert "10 per 1 minute" in body["data"]["message"]
