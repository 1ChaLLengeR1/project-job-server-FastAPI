from fastapi import HTTPException, Request

from core.service.contact.token import decode_contact_token

CONTACT_TOKEN_HEADER = "X-Contact-Token"


class ContactTokenAuthenticationMiddleware:
    """Dependency FastAPI dla publicznego endpointu kontaktowego (nie klasyczne ASGI middleware).

    Przepływ: nagłówek `X-Contact-Token` → weryfikacja podpisu HS256 wspólnym sekretem
    (service contact) → zwrot claimu `application` (identyfikator frontendu/backendu nadawcy).

    W odróżnieniu od JWTBasicAuthenticationMiddleware nie ma tu usera ani ról —
    token potwierdza jedynie, że nadawca zna wspólny sekret i z jakiej aplikacji pisze.
    Dla klientów server-to-server to pełnoprawna autoryzacja; dla frontendów
    przeglądarkowych filtr antybotowy (sekret w bundlu JS jest do wyciągnięcia),
    dlatego endpoint ma dodatkowo restrykcyjny rate limit per IP.
    """

    async def __call__(self, request: Request) -> str:
        token = request.headers.get(CONTACT_TOKEN_HEADER)
        if not token:
            raise HTTPException(status_code=401, detail="Contact token not provided.")

        application, err, ok = decode_contact_token(token)
        if not ok:
            raise HTTPException(status_code=401, detail=err.message)

        return application
