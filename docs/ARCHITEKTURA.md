# Architektura projektu project_job (backend FastAPI)

> Dokument opisuje pełną architekturę tego projektu: warstwy kodu, konwencje, tooling,
> testy, CI/CD i infrastrukturę deploy. Projekt został zrefaktorowany do tej struktury
> z wzorca referencyjnego WhereIsWheely — wszystkie domeny przechodzą przez te same
> warstwy i ten sam kontrakt odpowiedzi.

---

## Spis treści

1. [Stos technologiczny](#1-stos-technologiczny)
2. [Standard toolingu: uv + Makefile](#2-standard-toolingu-uv--makefile)
3. [Struktura katalogów projektu](#3-struktura-katalogów-projektu)
4. [Architektura warstwowa](#4-architektura-warstwowa)
5. [Warstwa `api/`](#5-warstwa-api)
6. [Warstwa `core/`](#6-warstwa-core)
7. [Autoryzacja i role](#7-autoryzacja-i-role)
8. [Audyt akcji userów (logs)](#8-audyt-akcji-userów-logs)
9. [Konfiguracja `config/`](#9-konfiguracja-config)
10. [`main.py` — złożenie aplikacji](#10-mainpy--złożenie-aplikacji)
11. [Baza danych `database/psql/` + Alembic](#11-baza-danych-databasepsql--alembic)
12. [Testy `tests/` + pytest.ini](#12-testy-tests--pytestini)
13. [CI/CD — GitHub Actions](#13-cicd--github-actions)
14. [Infrastruktura `infra/`](#14-infrastruktura-infra)
15. [Zmienne środowiskowe `env/`](#15-zmienne-środowiskowe-env)
16. [Konwencje nazewnictwa](#16-konwencje-nazewnictwa)
17. [Checklista: dodawanie nowej funkcjonalności](#17-checklista-dodawanie-nowej-funkcjonalności)
18. [Znane rozbieżności / TODO](#18-znane-rozbieżności--todo)

---

## 1. Stos technologiczny

| Element          | Technologia                                                        |
|------------------|--------------------------------------------------------------------|
| Framework        | **FastAPI 0.111**, Python **3.10** (`>=3.10,<3.11`)                |
| Serwer           | uvicorn (dev, port 3000) / **gunicorn** (prod)                     |
| ORM              | **SQLAlchemy 1.4** (`Column`, nie `Mapped[]`)                      |
| Baza danych      | **PostgreSQL** (UUID primary keys)                                 |
| Migracje         | **Alembic** (`alembic/`)                                           |
| Harmonogram      | **APScheduler** (cron w lifespan aplikacji)                        |
| Auth             | JWT (PyJWT) — access + refresh tokens, role w tabeli `users.type`  |
| Hasła            | bcrypt (passlib) — `core/helper/password.py`                       |
| Rate limiting    | **slowapi** (storage in-memory — limity per worker)                |
| Walidacja        | Pydantic v2 + **pydantic-settings**                                |
| Zewnętrzne API   | date.nager.at (święta) przez requests — `core/service/calendar/`   |
| Observability    | Prometheus (`/metrics` przez prometheus-fastapi-instrumentator)    |
| Audyt            | tabela `logs` — każda akcja usera logowana z handlera              |
| Testy            | **pytest** (markery: slow/integration/full_integration/api_integration) |
| Pakiety          | **uv** (`pyproject.toml` + `uv.lock`) — NIE pip/requirements.txt   |
| Lint/format      | **ruff** + ruff-format (`line-length=120`, `E,F,W,I,N,UP,B,SIM`)   |
| CI/CD            | GitHub Actions → Docker Hub → Ansible → **Docker Swarm**           |

Czego projekt świadomie **nie ma** (w odróżnieniu od wzorca WhereIsWheely):
Redis (cache), Celery/RabbitMQ (kolejka), Sentry, Stripe, InPost, mail.
Zadania cykliczne robi APScheduler w procesie aplikacji.

---

## 2. Standard toolingu: uv + Makefile

Zależności zarządza **uv** (`pyproject.toml` + `uv.lock`), codzienne komendy w **Makefile**:

| Target                      | Komenda / opis                                             |
|-----------------------------|-------------------------------------------------------------|
| `make install`              | `uv sync --all-extras`                                     |
| `make clean`                | usuwa `.venv`, `uv.lock`, cache pytest/ruff, `__pycache__` |
| `make run_app`              | `uv run uvicorn main:app --reload --port 3000`             |
| `make run_test`             | `uv run pytest -s -v` (markery z pytest.ini)               |
| `make run_test_integration` | pytest `-m "not slow and not full_integration and not api_integration"` — **CI** |
| `make run_test_full`        | wszystko, łącznie z zewnętrznymi API                       |
| `make lint` / `make format` | ruff check / ruff format                                   |
| `make migration_up ENV=local`    | `infra/scripts/database/migration_up.sh`              |
| `make migration_down ENV=local`  | destrukcyjny — DROP tabel                             |
| `make migration_restart ENV=local` | pełny reset schematu                                |
| `make vault_decrypt/encrypt/view` | ansible-vault na `infra/ansible/secrets.yml` (env `ANSIBLE_PASSWORD`) |

Extras w `pyproject.toml`: `test` (pytest, pytest-asyncio, pytest-cov, pytest-mock, httpx),
`dev` (ruff), `prod` (gunicorn).

---

## 3. Struktura katalogów projektu

```
.
├── main.py                     ← złożenie aplikacji FastAPI (entrypoint)
├── pyproject.toml              ← zależności, extras, ruff (standard uv)
├── uv.lock                     ← lockfile uv
├── Makefile                    ← wszystkie codzienne komendy
├── pytest.ini                  ← globalna konfiguracja pytest (markery!)
├── alembic.ini + alembic/      ← migracje bazy danych
├── api/                        ← warstwa HTTP
│   ├── endpoints/{domain}/     ← routery: jeden plik = jeden endpoint (akcja)
│   ├── schemas/{domain}/       ← payload.py + response.py (Pydantic)
│   ├── api.py                  ← centralna rejestracja wszystkich routerów
│   ├── routers.py              ← WSZYSTKIE ścieżki URL jako stałe
│   ├── response.py             ← ApiResponse / ApiErrorResponse / ApiErrorData + ERROR_STATUS_CODES
│   ├── exception_handlers.py   ← globalne handlery AppException / Exception
│   └── validators.py           ← wspólne walidatory (is_valid_uuid, validate_non_empty_str…)
├── core/                       ← serce backendu
│   ├── handler/{domain}/       ← orchestracja + audyt (warstwa nad repository/service)
│   ├── service/{domain}/       ← czysta logika / zewnętrzne API / tokeny JWT
│   ├── repository/psql/{domain}/ ← funkcje _psql (czyste zapytania DB) + response.py
│   ├── middleware/             ← JWTBasicAuthenticationMiddleware, JWTRefreshAuthenticationMiddleware
│   ├── helper/                 ← password (bcrypt)
│   ├── exceptions/             ← AppException + hierarchia
│   └── data/                   ← UserData (TypedDict zwracany przez middleware)
├── config/                     ← konfiguracja aplikacji
│   ├── settings.py             ← pydantic-settings, czyta env/{ENV_MODE}.env
│   ├── app_config.py           ← ENV_MODE, BASE_DIR, ENV_PATH
│   ├── rate_limit.py           ← slowapi: limiter, stałe limitów, handler 429
│   ├── gunicorn.py             ← konfiguracja produkcyjna serwera
│   └── swagger_description/    ← opis, tagi i summary Swaggera
├── database/psql/              ← engine, sesje, modele
│   ├── database.py             ← engine, get_db, managed_session
│   ├── base.py                 ← declarative Base
│   └── models/                 ← jeden plik = jedna domena (auth, tasks, calendar…)
├── tests/                      ← testy (conftest + markery)
├── env/                        ← pliki .env per środowisko (gitignored; *.env.example w repo)
├── infra/
│   ├── ansible/                ← deploy (playbook + taski + vault secrets)
│   ├── dockerfiles/            ← production/vault dockerfile, compose, swarm, nginx
│   └── scripts/                ← ci_smoke, migracje DB, vault, run_mode
└── docs/                       ← dokumentacja
```

Domeny projektu: **auth**, **tasks**, **calendar** (+ condition, days), **logs**,
**outstanding_money**, **fuel_calculator**, **patryk_router** (kalkulator zysku),
**rental** (rozliczenia mieszkań — poddomeny: **dictionaries** słowniki
mieszkań/najemców/kosztów/liczników, **billing** okresy rozliczeniowe z
preview/close/reopen, **family** podział rodzinny; plan:
docs/PLAN_ROZLICZENIA_MIESZKAN.md), **contact** (publiczny formularz
kontaktowy wielu aplikacji — token X-Contact-Token, docs/CONTACT_TOKEN.md).

---

## 4. Architektura warstwowa

Każda funkcjonalność przechodzi przez warstwy:

```
api/endpoints/{domain}/{action}.py        ← HTTP, walidacja body (Pydantic), swagger, auth, rate limit, try/except
        ↓ wywołuje handler
core/handler/{domain}/{action}.py         ← orchestracja, AUDYT (create_logs_psql), propagacja tuple
        ↓ wywołuje _psql / service
core/repository/psql/{domain}/{action}.py ← zapytania DB, mapowanie ORM → dataclass
core/service/{domain}/…                   ← czysta logika (obliczenia, tokeny) / zewnętrzne API
```

**Zasady twarde:**

- **Nigdy nie pomijaj warstw.** Endpoint nie wywołuje `_psql` bezpośrednio.
  Handler nie zna FastAPI ani `HTTPException`.
- Wszystkie funkcje przyjmują **jawne argumenty** (nie dicty `payload`) — walidacja
  danych jest w Pydantic payload na poziomie endpointu.
- Repository **nie strzela do zewnętrznych API** — robi to service, a handler
  orkiestruje (np. handler kalendarza: service świąt → `_psql` z gotowym setem dat).
- Sesja DB: endpoint bierze `db: Session = Depends(get_db)` i przekazuje w dół
  jako `db_session` — commit robi `get_db` po sukcesie requestu.
- Zadania cykliczne (APScheduler) wołają `_psql` z `db_session=None` —
  `managed_session` otwiera wtedy własną sesję i sam commituje.

### 4.1 Tuple Response Pattern

Każda funkcja — handler, service i `_psql` — zwraca tuple `(result, error, ok)`:

```python
def example_psql(..., db_session: Session | None = None) -> tuple[ResultType | None, ApiErrorData | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            # ... logika
            return result, None, True
    except IntegrityError as e:
        return None, ApiErrorData(
            message=str(e.orig),
            type_module="example_psql",
            type_error="integrity_error",
            key_type_error="IntegrityError",
        ), False
    except Exception as e:
        return None, ApiErrorData(
            message=str(e),
            type_module="example_psql",
            type_error="exception",
            key_type_error="Exception",
        ), False
```

W handlerze propagacja + audyt po sukcesie:

```python
def handler_example(user_id: str, ..., db_session: Session | None = None):
    try:
        result, err, ok = example_psql(..., db_session=db_session)
        if not ok:
            return None, err, False

        create_logs_psql(user_id, "{domain}:{action}", db_session=db_session)
        return result, None, True
    except Exception as e:
        return None, ApiErrorData(message=str(e), type_module="handler_example",
                                  type_error="exception", key_type_error="Exception"), False
```

W endpoincie mapowanie na HTTP (zawsze w `try/except`):

```python
data, error, success = handler_example(user_data["id"], ..., db_session=db)
if not success:
    status_code = ERROR_STATUS_CODES.get(error.key_type_error, 400)
    return JSONResponse(status_code=status_code,
                        content=ApiErrorResponse(status_code=status_code, data=error).model_dump())
return ApiResponse(status="SUCCESS", status_code=200, data=SomeResponseData(**asdict(data)))
```

**Konwencja `key_type_error`** (mapa `ERROR_STATUS_CODES` w `api/response.py`):

| Wartość             | Kiedy                                | HTTP |
|---------------------|--------------------------------------|------|
| `"IntegrityError"`  | duplikat, naruszenie constraintów    | 409  |
| `"NotFound"`        | brak rekordu                         | 404  |
| `"Forbidden"`       | brak uprawnień (rezerwowe)           | 403  |
| `"Unauthorized"`    | błędne dane logowania / tokeny       | 401  |
| `"ExternalService"` | błąd zewnętrznego API                | 502  |
| `"Exception"`       | nieobsłużony wyjątek / walidacja     | 400/500 |

Obok tuple pattern istnieje hierarchia wyjątków (`core/exceptions/exceptions.py`):
`AppException` (500) → `NotFoundError` (404), `ConflictError` (409),
`IntegrityViolationError`, `ExternalServiceError` (502), `DatabaseError` —
obsługiwana przez globalne exception handlery (`api/exception_handlers.py`):
handler `AppException` zwraca envelope + `request_id` w `additional` i bumpuje
licznik Prometheus `app_exceptions_total`; handler gołego `Exception` loguje
traceback i zwraca generyczne 500 bez wycieku treści. `HTTPException`
i `RequestValidationError` celowo zostają przy domyślnych handlerach FastAPI.

### 4.2 Typy danych między warstwami

- **Wewnętrzne response** (repository/service → handler → endpoint):
  **`@dataclass`** w `{domain}/response.py` + konwerter
  `_to_{domain}_response(model) -> {Domain}Response`.
- **Payloady (request body)** i **response data** (co idzie w `ApiResponse.data`) —
  Pydantic `BaseModel` w `api/schemas/{domain}/payload.py` i `response.py`.
- Konwersja dataclass → Pydantic w endpoincie: `SomeResponseData(**asdict(data))`
  (`asdict` działa rekurencyjnie na zagnieżdżonych dataclassach).

---

## 5. Warstwa `api/`

### 5.1 Endpointy — `api/endpoints/{domain}/{action}.py`

**Jeden plik = jeden endpoint (akcja)**; wyjątkiem pliki z wariantami tej samej
akcji (np. `tasks/update.py` ma update + update_active).

```python
router = APIRouter()


@router.post(
    CREATE_TASK,                                 # ← stała z api/routers.py, nigdy string
    summary="[Superadmin] Utwórz task",          # ← prefix roli obowiązkowy
    response_model=ApiResponse[TaskResponseData],
    responses={                                  # ← wszystkie kody błędów
        401: {"model": ApiErrorResponse, "description": "Brak lub niepoprawny token"},
        403: {"model": ApiErrorResponse, "description": "Brak uprawnień (wymagana rola superadmin)"},
        409: {"model": ApiErrorResponse, "description": "Konflikt danych (IntegrityError)"},
        429: {"model": ApiErrorResponse, "description": "Przekroczony limit zapytań"},
        500: {"model": ApiErrorResponse, "description": "Nieoczekiwany błąd serwera"},
    },
    status_code=201,
    tags=["Tasks"],                              # ← tag deklaruje ENDPOINT (nie include_router)
)
@limiter.limit(RATE_LIMIT_WRITE, key_func=auth_or_ip_key)   # ← rate limit obowiązkowy
def api_superadmin_create_task(
    request: Request,                            # ← wymagany przez slowapi
    body: TaskCreatePayload,
    user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"])),
    db: Session = Depends(get_db),
) -> ApiResponse[TaskResponseData] | JSONResponse:
    try:
        ...
    except Exception as e:
        # 500 z envelope — treść wyjątku w message, type_module = nazwa funkcji endpointu
        ...
```

**Swagger jest obowiązkowy** — każdy endpoint musi mieć `summary` (z prefiksem
roli `[Superadmin]`/`[Admin]`/`[User]`/`[Public]`), pełne `responses`
(łącznie z 429) i `tags`. Prefiksy ról odpowiadają faktycznej autoryzacji.

### 5.2 URL constants — `api/routers.py`

Wszystkie ścieżki jako stałe w jednym pliku, pogrupowane komentarzami per domena.
Wzorzec: `/{domain}/{action}` (np. `/tasks/create`, `/tasks/update/{task_id}`,
`/calendar/condition/collection`, `/authentication/login`).

### 5.3 Router centralny — `api/api.py`

Jeden `api_router = APIRouter()`; każdy plik endpointu importowany jako alias
i rejestrowany `api_router.include_router(module.router)` — **bez tagów**
(tagi deklarują endpointy, inaczej Swagger duplikuje tag).

### 5.4 Response envelope — `api/response.py`

```python
DATA = TypeVar("DATA", default=Any)          # typing_extensions — PEP 696
ADDITIONALS = TypeVar("ADDITIONALS", default=Any)

class ApiResponse(BaseModel, Generic[DATA, ADDITIONALS]):
    status: Literal["SUCCESS", "ERROR"]
    status_code: int
    data: DATA | None = None
    additional: ADDITIONALS | None = None

class ApiErrorData(BaseModel):
    message: str
    type_module: str      # nazwa funkcji, w której powstał błąd
    type_error: str
    key_type_error: str   # klucz mapy ERROR_STATUS_CODES

class ApiErrorResponse(BaseModel, Generic[ADDITIONALS]):
    status: Literal["ERROR"] = "ERROR"
    status_code: int
    data: ApiErrorData
    additional: ADDITIONALS | None = None
```

Dzięki defaultom TypeVar `ApiResponse[TaskResponseData]` działa z jednym
parametrem, a niesparametryzowane instancje przyjmują dowolne `data`.

### 5.5 Schemas — `api/schemas/{domain}/`

`payload.py` (request body) + `response.py` (co idzie w `ApiResponse.data`).
Walidacja w payloadach: `Field(gt=0, le=24, max_length=255…)`, wspólne walidatory
z `api/validators.py` przez `field_validator` (`validate_non_empty_str`,
`validate_uuid`), `model_validator` dla zależności między polami,
`Literal[...]` dla enumów (np. `referrer` w kalkulatorze). Błędna walidacja
→ standardowe **422** FastAPI.

Id w path (`task_id`, `condition_id`…) walidowane w endpoincie przez
`is_valid_uuid` → **400** z envelope.

---

## 6. Warstwa `core/`

### 6.1 `core/handler/{domain}/{action}.py`

Handler odpowiada za: (1) wywołanie `_psql`/service (jednego lub kilku),
(2) **audyt akcji** (`create_logs_psql`), (3) propagację tuple pattern.
Pierwszy argument to zawsze `user_id` (z middleware), ostatni `db_session`.

### 6.2 `core/service/{domain}/`

Logika bez dostępu do bazy przez ORM domeny — czyste obliczenia i zewnętrzne API:

- `service/auth/tokens.py` — encode/decode access + refresh tokenów JWT
  (weryfikacja podpisu, wygaśnięcia, claimu `id` jako UUID; refresh dodatkowo
  sprawdza zgodność claimu z żądanym userem),
- `service/calendar/holidays.py` — klient date.nager.at (dni ustawowo wolne),
- `service/fuel_calculator/calculation.py` — koszt paliwa,
- `service/patryk/calculation.py` — zysk ze sprzedaży (progi Allegro Smart).

Serwisy również zwracają tuple `(result, err, ok)` i przyjmują jawne argumenty.

### 6.3 `core/repository/psql/{domain}/`

Jeden plik = jedna operacja DB (`create`, `one`, `collection`, `update`,
`delete` + specjalizowane). Czyste zapytania SQLAlchemy, mapowanie ORM →
dataclass w `response.py` danej domeny. Zawsze przez `managed_session(db_session)`.
Dane wchodzą **już zwalidowane** — repository nie waliduje biznesowo.

### 6.4 `core/middleware/`, `core/helper/`, `core/exceptions/`

- middleware — patrz sekcja 7,
- `helper/password.py` — `hash_password` / `verify_password` (bcrypt),
- `exceptions/exceptions.py` — hierarchia `AppException` (sekcja 4.1).

---

## 7. Autoryzacja i role

Role w kolumnie `users.type`: **`superadmin` / `admin` / `user`**.
Superadmin przechodzi **każdy** check (hierarchia).

### 7.1 `JWTBasicAuthenticationMiddleware` (dependency, nie ASGI)

```python
user_data: UserData = Depends(JWTBasicAuthenticationMiddleware(roles=["superadmin"]))
```

Przepływ: Bearer token → dekodowanie JWT (service auth) → claim `id` walidowany
jako UUID → **pobranie usera z DB** (`one_user_by_id_psql`) → weryfikacja roli →
zwrot `UserData` (`id`, `username`, `type`).

- `roles=None` — wystarczy poprawny token (każdy zalogowany),
- 401 — problem z tokenem / user nie istnieje, 403 — brak uprawnień
  (format `{"detail": ...}` — domyślny handler FastAPI, celowo).

Tożsamość zawsze z tokenu — **żadnych nagłówków typu `UserData`** od klienta.

### 7.2 `JWTRefreshAuthenticationMiddleware`

Autoryzacja odświeżenia sesji: `user_id` z path (walidacja UUID → 400) +
nagłówek `X-Refresh-Token` → weryfikacja tokenu **łącznie ze zgodnością claimu
`id` z user_id** (cudzy token → 401) → user z DB → `UserData`.
Handler `handler_automatically_login` tylko wystawia nową parę tokenów + audyt.

### 7.3 `ContactTokenAuthenticationMiddleware` — publiczny endpoint kontaktowy

Jedyny publiczny endpoint zapisu (`POST /contact/messages/create`) nie używa
JWT usera. Zamiast tego nagłówek **`X-Contact-Token`** — krótkożyciowy JWT HS256
podpisany wspólnym sekretem `SECRET_KEY_CONTACT_TOKEN`; middleware weryfikuje
podpis + `exp` i zwraca claim `application` (identyfikator frontendu/backendu
nadawcy). Dla klientów server-to-server to pełnoprawna autoryzacja; dla
frontendów przeglądarkowych filtr antybotowy (sekret w bundlu jest jawny),
dlatego endpoint ma limit `RATE_LIMIT_PUBLIC_CONTACT` per IP.
Instrukcja podpisywania (JS `jose` / Python `PyJWT`): `docs/CONTACT_TOKEN.md`.

### 7.4 Rate limiting — `config/rate_limit.py`

`SlowAPIMiddleware` + `default_limits=["200/second"]` globalnie oraz
**jawny `@limiter.limit(...)` na każdym endpoincie** (endpoint musi mieć
parametr `request: Request`):

| Stała                       | Limit        | Klucz                        | Gdzie                |
|-----------------------------|--------------|------------------------------|----------------------|
| `RATE_LIMIT_AUTH`           | `10/minute`  | IP                           | login, refresh       |
| `RATE_LIMIT_READ`           | `120/minute` | user z JWT (fallback IP)     | wszystkie GET        |
| `RATE_LIMIT_WRITE`          | `60/minute`  | user z JWT (fallback IP)     | POST/PUT/PATCH/DELETE|
| `RATE_LIMIT_PUBLIC_CONTACT` | `5/minute`   | IP                           | publiczny create kontaktu |

`auth_or_ip_key` czyta claim `id` z JWT **bez weryfikacji podpisu** (to tylko
klucz limitera — autoryzację robi middleware). Handler 429 zwraca standardowy
envelope `ApiErrorResponse`. Storage in-memory — po ewentualnym dodaniu Redisa
podać `storage_uri`, żeby limity były wspólne dla replik.

---

## 8. Audyt akcji userów (logs)

Tabela `logs` (`id`, `username`, `description`, `date` — `DateTime(timezone=True)`,
`server_default=func.now()`). Zapis robi **`create_logs_psql(user_id, description,
db_session)`** wołany z każdego handlera **po udanej operacji**:

- username dociągany z tabeli `users` po `user_id` (z tokenu, nie od klienta),
- `description` = slug **`{domain}:{action}`**, np. `tasks:create`,
  `calendar_days:update_salary`, `auth:login`, `outstanding_money:delete_list`,
- log idzie na tej samej sesji co operacja (spójny commit/rollback),
- wynik wywołania jest **ignorowany** — błąd audytu nie wywala operacji,
- logowane są tylko sukcesy.

Podgląd: `GET /logs/collection/{number}` (rola superadmin; `number=0` → wszystkie).
Endpointu do ręcznego tworzenia logów **nie ma** — audyt jest wyłącznie wewnętrzny.

---

## 9. Konfiguracja `config/`

### 9.1 `config/settings.py` — pydantic-settings + .env

Klasa `Settings(BaseSettings)`; singleton `settings = Settings()`. Czyta
`env/{ENV_MODE}.env` (tryb z `config/app_config.py`), przy czym **zmienne
środowiskowe procesu mają priorytet nad plikiem** (CI i docker secret działają
bez plików env/). Grupy: DB (`DB_*`), JWT (`SECRET_KEY_TOKEN`,
`SECRET_KEY_REFRESH_TOKEN`, `ALGORITHM`, `TOKEN_EXPIRES_HOURS`,
`REFRESH_TOKEN_EXPIRES_HOURS`).

### 9.2 `config/app_config.py`

Cienki moduł: `ENV_MODE` (local|dev|prod), `BASE_DIR`, `ENV_PATH`.
Skrypt `infra/scripts/run_mode.sh` podmienia `ENV_MODE` (sed).

### 9.3 `config/gunicorn.py` i `config/swagger_description/`

- gunicorn — produkcyjny config serwera (start: `gunicorn main:app -c config/gunicorn.py`),
- swagger_description — `app.py` (`APP_DESCRIPTION`), `summary.py`
  (`build_endpoint_summary(router)` — tabelka endpointów per tag liczona przy
  starcie), `tags.py` (`TAGS_METADATA`).

---

## 10. `main.py` — złożenie aplikacji

Kolejność montażu:

1. `app = FastAPI(title="project_job", description=build_endpoint_summary(api_router) + APP_DESCRIPTION, openapi_tags=TAGS_METADATA, lifespan=lifespan)`.
2. **Lifespan**: APScheduler — cron `update_day_automatically_psql` codziennie 00:00
   (uzupełnia zaległe dni robocze wg ostatnich warunków pracy).
3. Rate limiting: `app.state.limiter = limiter` + handler 429 + `SlowAPIMiddleware`.
4. CORS (arturscibor.pl, localhost:5173; nagłówki: Authorization, Content-Type,
   Accept, x-refresh-token).
5. `register_exception_handlers(app)`.
6. `app.include_router(api_router)`.
7. Prometheus: `Instrumentator().instrument(app).expose(app)` → `/metrics`.
8. `GET /health` → `{"status": "ok"}`.

---

## 11. Baza danych `database/psql/` + Alembic

### 11.1 Sesje i transakcje — `database/psql/database.py`

- Engine: `pool_size=3, max_overflow=2, pool_recycle=1800, pool_pre_ping=True`.
- **`get_db()`** — FastAPI dependency: yield sesji, **commit na sukces**,
  rollback + re-raise na wyjątek, close w finally.
- **`managed_session(db_session=None)`** — kluczowy context manager warstwy
  repository: sesja z endpointu → reużywa (commit robi `get_db`); `None`
  (APScheduler, test standalone) → tworzy własną i sam commituje.
  W funkcjach `_psql` używa się `db.flush()` + `db.refresh()`, nie `commit()`.

### 11.2 Modele — `database/psql/models/{domain}.py`

SQLAlchemy 1.4 (`Column`), UUID PK (`uuid.uuid4`), timestampy
`DateTime(timezone=True)` z `server_default=func.now()` (+ `onupdate` dla
`updated_at`). Wspólna `Base` w `base.py`. Modele: `Users`, `Tasks`, `Logs`,
`WorkDay`, `WorkConditionChange`, `NamesOverdue`, `OutStandingMoney`,
`KeysCalculatorPatryk`, `ContactMessage` oraz 14 tabel domeny rental
(`Rental*` w `models/rentals.py`: słowniki, okresy rozliczeniowe ze
snapshotami i podział rodzinny).

### 11.3 Alembic i skrypty

`alembic.ini` → `script_location = alembic`. Migracje w `alembic/versions/`.
Skrypty `infra/scripts/database/{migration_up,migration_down,restart}.sh`
przyjmują środowisko `[local|dev|prod]` — wywoływane przez `make migration_*`.

---

## 12. Testy `tests/` + pytest.ini

- `testpaths = tests`, `pythonpath = .`, `asyncio_mode = auto`.
- **`addopts = -m "not slow and not integration and not full_integration and not api_integration"`**
  — ciężkie markery domyślnie WYKLUCZONE.
- Markery: `slow`, `integration` (realna baza), `full_integration`,
  `api_integration` (zewnętrzne API, np. date.nager.at).
- CI uruchamia `make run_test_integration`.

Struktura (jak we wzorcu): lustrzane odbicie kodu — testy `_psql`
osobno, serwisów osobno, endpointów (TestClient) osobno; klasy
`Test{Action}{Domain}Psql`, metody `test_{action}{nn:02d}_{opis}`.
Fabryki modeli per domena w `tests/core/repository/psql/{domain}/helper.py`,
testy endpointów budują aplikację przez `tests/api/helper.py::make_client`
(tylko potrzebne routery, mock autoryzacji `authorized_as`). Domena rental ma
dodatkowo test e2e pełnego przepływu miesiąca
(`tests/api/endpoints/rental/test_api_e2e_full_flow.py` — scenariusz z
docs/Obliczenia_3.txt: 4 mieszkania, licznik główny, korekty, podział Ja/Ojciec/Mama).

---

## 13. CI/CD — GitHub Actions

Sześć workflow w dwóch ścieżkach — dwa orkiestratory (`push`) wywołują
workflow reużywalne (`workflow_call`):

```
branch ≠ main:  run_test_local.yml ──► run_ci_test_local.yml (make run_test_integration)

main:           run_production.yml ──► run_ci_test_containers.yml  (smoke: infra/scripts/ci/ci_smoke.sh)
                                   └─► run_ci_production.yml        (build+push Docker Hub)
                                   └─► run_cd_production.yml        (deploy Ansible)
```

Każdy etap gejtuje następny przez `needs`. Env w CI ustawiany wprost na jobie
(settings czyta env priorytetowo — pliki `env/*.env` niepotrzebne).

---

## 14. Infrastruktura `infra/`

- **`dockerfiles/dockerfile/production.dockerfile`** — obraz produkcyjny z uv
  (`uv sync --frozen --extra prod`), CMD gunicorn.
- **`dockerfiles/compose/`** — `prod.docker-compose.yaml`,
  `prod.swarm.docker-compose.yaml` (stack Swarm), `traefik.yml`; nginx w
  `dockerfiles/nginx/`.
- **`ansible/`** — `playbook_deploy.yml` + taski (checkout, networks,
  secret_env, deploy, cleanup); sekrety infry w `secrets.yml` (ansible-vault,
  obsługa przez `make vault_*` / `infra/scripts/vault.sh`).
- **`scripts/`** — `ci/ci_smoke.sh`, `database/*` (migracje), `run_mode.sh`,
  `docker_entrypoint.sh`.

---

## 15. Zmienne środowiskowe `env/`

Pliki `env/{local|prod}.env` (gitignored; w repo `*.env.example`).
Czytane przez `config/settings.py` (env procesu ma priorytet):

| Grupa | Zmienne                                                                  |
|-------|--------------------------------------------------------------------------|
| Baza  | `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DBNAME`              |
| JWT   | `SECRET_KEY_TOKEN`, `SECRET_KEY_REFRESH_TOKEN`, `ALGORITHM`, `TOKEN_EXPIRES_HOURS`, `REFRESH_TOKEN_EXPIRES_HOURS` |

**Uwaga:** `REFRESH_TOKEN_EXPIRES_HOURS` jest historycznie interpretowane jako
**dni** (`timedelta(days=...)` w `core/service/auth/tokens.py`).

---

## 16. Konwencje nazewnictwa

| Element               | Wzorzec                          | Przykład                        |
|-----------------------|----------------------------------|---------------------------------|
| funkcja `_psql`       | `{action}_{domain}_psql`         | `create_task_psql`              |
| funkcja handlera      | `handler_{action}_{domain}`      | `handler_create_task`           |
| funkcja endpointu     | `api_{rola}_{action}_{domain}`   | `api_superadmin_create_task`    |
| plik endpointu        | `{action}.py`                    | `create.py`, `collection.py`    |
| stała URL             | `{ACTION}_{DOMAIN}`              | `CREATE_TASK`, `COLLECTION_LOGS`|
| dataclass response    | `{Domain}Response`               | `TaskResponse` (repo/service)   |
| Pydantic payload      | `{Domain}{Action}Payload`        | `TaskCreatePayload`             |
| Pydantic response     | `{Domain}ResponseData`           | `TaskResponseData`              |
| slug audytu           | `{domain}:{action}`              | `tasks:create`, `auth:login`    |
| `type_module` w error | nazwa funkcji, gdzie rzucony     | `"create_task_psql"`            |
| klasa testowa         | `Test{Action}{Domain}Psql`       | `TestCreateTaskPsql`            |

---

## 17. Checklista: dodawanie nowej funkcjonalności

1. **Model** — `database/psql/models/{domain}.py` + migracja Alembic
   (UUID PK, timestampy `DateTime(timezone=True)` + `server_default=func.now()`).
2. **_psql response** — `core/repository/psql/{domain}/response.py`
   (dataclass + `_to_*_response`).
3. **_psql operacje** — `core/repository/psql/{domain}/{action}.py`
   (tuple pattern, `managed_session`, jawne argumenty, flush+refresh).
4. **Service** — jeśli czysta logika / zewnętrzne API →
   `core/service/{domain}/` (+ własny `response.py`).
5. **Handler** — `core/handler/{domain}/{action}.py` (tuple pattern,
   `user_id` jako pierwszy argument, **audyt `create_logs_psql` po sukcesie**).
6. **Schemas** — `api/schemas/{domain}/payload.py` + `response.py`
   (walidacja: Field constraints, `validate_uuid`, `validate_non_empty_str`).
7. **URL** — stała w `api/routers.py`.
8. **Endpoint** — `api/endpoints/{domain}/{action}.py`: swagger obowiązkowy
   (summary z rolą, pełne `responses` z 429, tags), **`@limiter.limit`**
   (`request: Request` w sygnaturze), auth przez middleware z rolami,
   `db = Depends(get_db)`, całość w try/except.
9. **Router** — rejestracja w `api/api.py` (bez tagów — tag deklaruje endpoint).
10. **Testy** — `tests/core/repository/psql/{domain}/` +
    `tests/api/endpoints/{domain}/` (+ helper.py z fabrykami).
11. Nowe zmienne env → `env/*.env`, `env/*.env.example` i `config/settings.py`.

---

## 18. Znane rozbieżności / TODO

1. **Testy** — w repo jest tylko sanity test; docelowo struktura lustrzana
   z fabrykami i realnym Postgresem w CI (services w `run_ci_test_local.yml`).
2. **Rate limiter in-memory** — limity liczone per worker gunicorna;
   przy skalowaniu na repliki dodać Redis jako storage.
3. **`REFRESH_TOKEN_EXPIRES_HOURS`** działa jako dni — do przemianowania na
   `_DAYS` (wymaga zmiany env na wszystkich środowiskach).
4. **Migracja `logs.date`** — model ma już `DateTime(timezone=True)`;
   na środowiskach z danymi wykonać `ALTER TABLE logs ALTER COLUMN date TYPE timestamptz`
   + `SET DEFAULT now()`.
5. **Brak rewokacji tokenów** — logout/unieważnienie refresh tokenów wymaga
   tabeli tokenów w DB (jak we wzorcu WhereIsWheely: claim `jti` + rekord tokena).
6. Błędy autoryzacji z middleware mają format `{"detail": ...}` (FastAPI),
   a błędy biznesowe envelope `ApiErrorResponse` — kontrakt świadomy,
   udokumentowany dla frontendu.
