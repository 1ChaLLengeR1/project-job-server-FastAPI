APP_DESCRIPTION = """
Backend FastAPI do codziennej pracy (kalendarz pracy, zadania, zaległe płatności,
logi, kalkulatory, generowanie PDF).

## Format odpowiedzi (envelope)

Każda odpowiedź API ma jednolity kształt:

```json
{
  "status": "SUCCESS | ERROR",
  "status_code": 200,
  "data": { },
  "additional": null
}
```

## Autoryzacja

Endpointy chronione wymagają nagłówka `Authorization: Bearer {access_token}`
(token z `/authentication/login`). Refresh token odświeża sesję przez
nagłówek `x-refresh-token`.

## Konwencje

- Daty i czasy w formacie **ISO 8601**.
- Identyfikatory to **UUID v4**.
- Rate limit: 200 żądań/sekundę na adres IP (HTTP 429 po przekroczeniu).
"""
