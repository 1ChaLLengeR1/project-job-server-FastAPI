from fastapi import Header, HTTPException

from api.validators import is_valid_uuid
from core.data.user import UserData
from core.repository.psql.user.one import one_user_by_id_psql
from core.service.auth.tokens import decode_refresh_token


class JWTRefreshAuthenticationMiddleware:
    """Dependency FastAPI dla odświeżania sesji refresh tokenem.

    Przepływ: `user_id` z path (walidacja UUID) + nagłówek `X-Refresh-Token` →
    weryfikacja tokenu (podpis, wygaśnięcie, zgodność claimu `id` z user_id) →
    pobranie usera z DB → zwrot danych usera.

    400 — niepoprawny format user_id, 401 — problem z tokenem lub user nie istnieje.
    """

    async def __call__(
        self,
        user_id: str,
        x_refresh_token: str = Header(alias="X-Refresh-Token", description="Refresh token"),
    ) -> UserData:
        if not is_valid_uuid(user_id):
            raise HTTPException(status_code=400, detail="User_id nie jest poprawnego formatu uuid.")

        _, err, ok = decode_refresh_token(x_refresh_token, user_id)
        if not ok:
            raise HTTPException(status_code=401, detail=err.message)

        user, _, ok = one_user_by_id_psql(user_id)
        if not ok or user is None:
            raise HTTPException(status_code=401, detail="User from token does not exist.")

        return UserData(id=user.id, username=user.username, type=user.type)
