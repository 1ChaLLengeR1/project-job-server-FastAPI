# Server Python (FastAPI)

## O projekcie

Backend FastAPI dla prywatnej aplikacji do codziennego zarządzania sprawami życiowymi
i zawodowymi — kalendarz pracy, zadania, zaległe płatności, wynajem mieszkań i magazyn
plików w jednym miejscu, zamiast rozproszonych arkuszy i notatek. Projekt jest **stale
rozwijany** — nowe domeny i funkcjonalności dochodzą iteracyjnie, każda przechodzi przez
tę samą, spójną architekturę (patrz [`docs/ARCHITEKTURA.md`](docs/ARCHITEKTURA.md)) i jest
pokryta testami.

To repozytorium to **backend** (API). Frontend to osobny, siostrzany projekt —
[`project-job-website-vue.js`](../project-job-website-vue.js) (Vue 3 + TypeScript) — oba
repozytoria tworzą razem jedną aplikację: frontend konsumuje wyłącznie ten backend
(pojedynczy `VITE_URL_SERVER`), a kontrakt API między nimi jest udokumentowany i
utrzymywany w Swaggerze (`/docs`) po stronie backendu.

---

## Domeny / funkcjonalności

| Sekcja (nazwa w UI) | Co robi |
|---|---|
| **Wynajem mieszkań** (`rentals`) | Pełne rozliczenia najmu: słowniki mieszkań/najemców/liczników/rodzajów kosztów, najmy z historią czynszu, okresy rozliczeniowe z **podglądem na żywo** (bez zapisu) i **zamknięciem** (snapshoty rozliczeń), odczyty liczników, podział rodzinny kosztów między beneficjentami z regułami podziału i historią. |
| **Magazyn plików** (`files`) | Prywatny magazyn dokumentów w S3: upload przez presigned URL wprost z przeglądarki (backend nigdy nie widzi pliku), wymuszone szyfrowanie **SSE-KMS**, w pełni prywatny bucket (Block Public Access, zero gołych URL-i). Zagnieżdżone drzewo „węzłów" (osoba/kategoria), przypisywanie i odpinanie plików od węzła, pliki-dzieci (np. kolejne wersje faktury), opcjonalne śledzenie gwarancji (data ważności, filtr aktywne/wygasłe), podgląd i pobieranie przez krótkoterminowe podpisane linki. |
| **Kalendarz Rozliczeń** (`calendar`) | Kalendarz pracy — generowanie dni roboczych, warunki pracy (norma godzin, stawka) obowiązujące od danej daty, przeliczanie wynagrodzenia i statystyki miesięczne. |
| **Rozliczenia pieniędzy** (`outstanding_money`) | Listy zaległych płatności i ich pozycje — kto, ile, za co. |
| **Zadania** (`tasks`) | Prosty CRUD zadań z oznaczaniem wykonania i statystykami. |
| **Kalkulator Paliw / VAT / Patryk** | Zestaw kalkulatorów pomocniczych (koszt paliwa na trasę, VAT, kalkulator pracy zleceniowej). |
| **Kontakt** (`contact`) | Publiczny formularz kontaktowy (osobny token `X-Contact-Token` per aplikacja, bez logowania) + obsługa zgłoszeń przez superadmina. |
| **Logi** (`logs`) | Audyt — każda akcja zapisujących endpointów loguje się automatycznie w handlerze. |

Pełny, zawsze aktualny opis każdego endpointu jest w Swaggerze pod `/docs` po odpaleniu
aplikacji. Dla domeny `files` dodatkowo pełna historia decyzji projektowych i przyrostów
jest opisana w [`docs/PLAN_MAGAZYN_PLIKOW.md`](docs/PLAN_MAGAZYN_PLIKOW.md).

---

## Architektura

Każda funkcjonalność przechodzi przez te same, konsekwentne warstwy:

```
api/endpoints/{domain}/{action}.py   ← HTTP: walidacja (Pydantic), Swagger, auth, rate limit
        ↓
core/handler/{domain}/{action}.py    ← orkiestracja + audyt (create_logs_psql)
        ↓
core/repository/psql/{domain}/…      ← zapytania DB, wzorzec (result, error, ok)
core/service/{domain}/…              ← czysta logika / zewnętrzne API / tokeny
```

- **Jednolity kontrakt odpowiedzi** — każdy endpoint zwraca ten sam envelope
  (`{status, status_code, data, additional}`), błędy mają wspólny kształt
  `ApiErrorResponse` z mapowaniem na kody HTTP.
- **Role i autoryzacja** — JWT (access + refresh), role trzymane w `users.type`,
  middleware sprawdza rolę per endpoint.
- **Audyt** — każda akcja zapisu leci do tabeli `logs` z poziomu handlera, z użytkownikiem
  i opisem akcji (np. `files:assign`).
- **Rate limiting** — `slowapi`, osobne limity dla odczytu/zapisu, 429 po przekroczeniu.
- **Testy** jako pierwszorzędny obywatel — warstwa `_psql`, service, handler i pełne API
  (`TestClient`) mają osobne testy; integracje z realnymi usługami (S3) są oznaczone
  markerem `full_integration` i odpalane świadomie, osobno od domyślnego CI.

Pełny, szczegółowy opis (struktura katalogów, konwencje nazewnictwa, checklista „jak dodać
nową funkcjonalność", CI/CD, infrastruktura) jest w [`docs/ARCHITEKTURA.md`](docs/ARCHITEKTURA.md).

---

## Stos technologiczny

| Element | Technologia |
|---|---|
| Framework | FastAPI 0.111, Python 3.10 |
| Serwer | uvicorn (dev) / gunicorn (prod) |
| ORM / baza | SQLAlchemy 1.4 + PostgreSQL (UUID primary keys) |
| Migracje | Alembic |
| Auth | JWT (PyJWT), hasła przez bcrypt |
| Walidacja | Pydantic v2 + pydantic-settings |
| Storage plików | AWS S3 (boto3) + szyfrowanie KMS, presigned URL |
| Rate limiting | slowapi |
| Harmonogram | APScheduler (w procesie aplikacji) |
| Observability | Prometheus (`/metrics`) |
| Testy | pytest (markery: `slow`/`full_integration`/`api_integration`) |
| Zarządzanie zależnościami | uv (`pyproject.toml` + `uv.lock`) |
| Lint/format | ruff |
| Sekrety | Doppler (per środowisko, ciągnięte przy deployu) |
| CI/CD | GitHub Actions → Docker Hub → Ansible → Docker Swarm |

Świadomie **bez** Redis, Celery/RabbitMQ, Sentry — projekt jest jednoosobowy, więc te
elementy są rozważane jako ewentualne, przyszłe rozszerzenia „portfolio", nie realna
potrzeba na obecną skalę.

---

## Status

Projekt jest **aktywnie rozwijany** — kolejne domeny i funkcjonalności (ostatnio: cały
magazyn plików w S3) dochodzą iteracyjnie, każda z testami i aktualizowaną dokumentacją.
Decyzje projektowe i historia przyrostów dla większych funkcjonalności są spisywane w
`docs/PLAN_*.md`, żeby kontekst nie ginął między sesjami pracy.
