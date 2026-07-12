from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.concurrency import run_in_threadpool

from core.data.user import UserData
from core.repository.psql.user.one import one_user_by_id_psql
from core.service.auth.tokens import decode_access_token


class JWTBasicAuthenticationMiddleware(HTTPBearer):
    """Dependency FastAPI (nie klasyczne ASGI middleware).

    Przepływ: Bearer token → dekodowanie JWT (service auth) → claim `id` walidowany jako UUID →
    pobranie usera z DB → weryfikacja roli względem `roles` → zwrot danych usera.

    - `roles=None` — wystarczy poprawny token (każdy zalogowany user),
    - `roles=["admin"]` — wpuszcza admina (i superadmina — superadmin przechodzi każdy check),
    - 401 — problem z tokenem, 403 — brak uprawnień.
    """

    def __init__(self, roles: list[str] | None = None, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.roles = roles

    async def __call__(self, request: Request) -> UserData:
        try:
            credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        except HTTPException as err:
            raise HTTPException(status_code=401, detail=err.detail) from err

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Bearer token not provided.")

        user_id, err, ok = decode_access_token(credentials.credentials)
        if not ok:
            raise HTTPException(status_code=401, detail=err.message)

        # sync ORM w async dependency - przez threadpool, żeby nie blokować event loopu
        user, _, ok = await run_in_threadpool(one_user_by_id_psql, user_id)
        if not ok or user is None:
            raise HTTPException(status_code=401, detail="User from token does not exist.")

        if self.roles and user.type != "superadmin" and user.type not in self.roles:
            raise HTTPException(status_code=403, detail=f"User '{user.username}' has no permission.")

        return UserData(id=user.id, username=user.username, type=user.type)
