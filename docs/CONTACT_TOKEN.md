# Token kontaktowy (X-Contact-Token) — instrukcja dla klientów

Publiczny endpoint `POST /contact/messages/create` nie wymaga JWT usera.
Zamiast tego każdy request musi mieć nagłówek **`X-Contact-Token`** —
krótkożyciowy token **JWT HS256** podpisany wspólnym sekretem
(`SECRET_KEY_CONTACT_TOKEN` z env backendu).

Wymagane claimy:

| Claim | Znaczenie |
|---|---|
| `application` | identyfikator aplikacji nadawcy (np. `"portfolio"`) — ląduje w kolumnie `contact_messages.application`; NIE przesyła się go w payloadzie |
| `exp` | wygaśnięcie — token bez `exp` jest odrzucany (zalecane 5 minut) |
| `iat` | data wystawienia (zalecane) |

Odpowiedzi błędów: `401` (brak/zły/przeterminowany token), `429` (limit 5/min per IP).

## Klient JavaScript (frontend / Node) — biblioteka [`jose`](https://github.com/panva/jose)

```js
import { SignJWT } from "jose";

const secret = new TextEncoder().encode(CONTACT_TOKEN_SECRET);

async function sendContactMessage(form) {
  const token = await new SignJWT({ application: "portfolio" })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("5m")
    .sign(secret);

  return fetch("https://api.example.com/contact/messages/create", {
    method: "POST",
    headers: { "X-Contact-Token": token, "Content-Type": "application/json" },
    body: JSON.stringify({
      first_name: form.firstName,
      last_name: form.lastName ?? null,
      phone_number: form.phone,
      email: form.email ?? null,
      description: form.message,
    }),
  });
}
```

## Klient Python (inny backend) — biblioteka `PyJWT`

```python
from datetime import datetime, timedelta, timezone

import jwt
import requests

now = datetime.now(timezone.utc)
token = jwt.encode(
    {"application": "rentals-app", "exp": now + timedelta(minutes=5), "iat": now},
    CONTACT_TOKEN_SECRET,
    algorithm="HS256",
)

requests.post(
    "https://api.example.com/contact/messages/create",
    headers={"X-Contact-Token": token},
    json={
        "first_name": "Jan",
        "phone_number": "+48 500 600 700",
        "description": "Pytanie o wycenę",
    },
)
```

## Charakter zabezpieczenia (świadoma decyzja)

- **Backendy (server-to-server)**: sekret leży na serwerze — pełnoprawna autoryzacja.
- **Frontendy przeglądarkowe**: sekret jest częścią bundla JS, więc token to filtr
  antybotowy (odsiewa skanery i masowy spam), nie uwierzytelnienie. Drugą linią
  jest rate limit `5/minute` per IP (config/rate_limit.py).
