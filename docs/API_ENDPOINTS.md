# Dokumentacja API — endpointy dla frontendu

> Wygenerowano na podstawie kodu w `api/endpoints/`, `api/routers.py` i `api/schemas/` (stan: 2026-07-11).
> Brak globalnego prefixu — ścieżki są dokładnie takie, jak podano niżej (router montowany bez `prefix`).

## Informacje wspólne

### Format odpowiedzi (envelope)

Każdy endpoint zwraca wspólną kopertę (`api/response.py`):

```json
// sukces
{
  "status": "SUCCESS",
  "status_code": 200,
  "data": { ... },        // typ zależny od endpointu (patrz "Response data")
  "additional": null
}

// błąd
{
  "status": "ERROR",
  "status_code": 404,
  "data": {
    "message": "opis błędu",
    "type_module": "nazwa_funkcji_zrodla_bledu",
    "type_error": "typ błędu",
    "key_type_error": "NotFound"   // IntegrityError=409, NotFound=404, Forbidden=403, Unauthorized=401, ExternalService=502, Exception=400/500
  },
  "additional": null
}
```

### Autoryzacja — nagłówki

| Mechanizm | Nagłówek | Gdzie używany |
|---|---|---|
| Access token (JWT) | `Authorization: Bearer <access_token>` | Wszystkie endpointy poza publicznymi |
| Refresh token (JWT) | `X-Refresh-Token: <refresh_token>` (bez prefixu `Bearer`) | Tylko `GET /authentication/automatically_login/{user_id}` |
| Contact token (JWT) | `X-Contact-Token: <token>` | Tylko `POST /contact/messages/create` (szczegóły: `docs/CONTACT_TOKEN.md`) |

Role: wymagana rola podana jest przy każdym endpoincie (np. `superadmin`, `admin`). **`superadmin` przechodzi każdy check ról.** Kody: `401` — problem z tokenem, `403` — brak uprawnień.

### Rate limity (`config/rate_limit.py`)

| Limit | Wartość | Zakres |
|---|---|---|
| AUTH | 10/min (per IP) | login, automatically_login |
| READ | 120/min (per user z JWT, fallback IP) | odczyty (GET) |
| WRITE | 60/min (per user z JWT, fallback IP) | zapisy (POST/PUT/PATCH/DELETE) |
| PUBLIC_CONTACT | 5/min (per IP) | publiczny formularz kontaktowy |

Po przekroczeniu limitu: `429` w standardowej kopercie błędu.

### Spis modułów

| Moduł | Prefix ścieżek | Liczba endpointów |
|---|---|---|
| Auth | `/authentication/*` | 2 |
| Logs | `/logs/*` | 1 |
| Fuel Calculator | `/fuel/*` | 1 |
| Calculator Work (Patryk) | `/calculator_work/*` | 3 |
| Tasks | `/tasks/*` | 6 |
| Outstanding Money | `/outstanding_money/*` | 7 |
| Calendar | `/calendar/*` | 10 |
| Rental — słowniki | `/rentals/{apartments,tenants,tenancies,cost_types,apartment_costs,meters}/*` | 30 |
| Rental — rozliczenia | `/rentals/{periods,readings,settlements}/*` | 14 |
| Rental — podział rodzinny | `/rentals/{beneficiaries,allocation_rules,beneficiary_settlements}/*` | 11 |
| Contact | `/contact/messages/*` | 5 |
| **Razem** | | **90** |
## Auth

### POST `/authentication/login`
Zaloguj użytkownika (publiczny).
- **Auth:** Publiczny (bez tokena). Rate limit: `RATE_LIMIT_AUTH`.
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `username` | string | tak | Nazwa użytkownika; max 255 znaków, nie może być pusty |
| `password` | string | tak | Hasło; max 255 znaków, nie może być puste |

- **Response `data`:** `id: string (UUID)`, `username: string`, `access_token: string`, `refresh_token: string`
- **Kody błędów:**
  - `401` — Błędna nazwa użytkownika lub hasło
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### GET `/authentication/automatically_login/{user_id}`
Odśwież sesję refresh tokenem (publiczny — autoryzacja refresh tokenem, nie access tokenem).
- **Auth:** nagłówek **`X-Refresh-Token: <refresh_token>`** (bez prefiksu `Bearer`). Token musi być ważny, a jego claim `id` musi zgadzać się z `user_id` z path. Rate limit: `RATE_LIMIT_AUTH`.
- **Path params:** `user_id` — string (UUID) — id użytkownika, którego sesja jest odświeżana
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `id: string (UUID)`, `username: string`, `access_token: string`, `refresh_token: string` (nowa para tokenów)
- **Kody błędów:**
  - `400` — Niepoprawny format `user_id` (nie-UUID)
  - `401` — Niepoprawny lub cudzy refresh token / user z tokena nie istnieje
  - `404` — User nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

## Logs

### GET `/logs/collection/{number}`
Pobierz logi audytowe (ostatnie N wpisów).
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola **superadmin**
- **Path params:** `number` — int — liczba logów do pobrania
- **Query params:** brak
- **Body:** brak
- **Response `data`:** lista obiektów: `id: string`, `username: string`, `description: string`, `date: datetime | null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

## Fuel Calculator

### POST `/fuel/fuel_calculations`
Oblicz koszt paliwa dla podanej trasy.
- **Auth:** `Authorization: Bearer <access_token>` — dowolny zalogowany użytkownik (bez wymogu roli)
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `way` | float | tak | Dystans w kilometrach; `>= 0` |
| `fuel` | float | tak | Cena paliwa za litr; `>= 0` |
| `combustion` | float | tak | Spalanie na 100 km; `>= 0` |
| `remaining_values` | float | tak | Dodatkowe koszty doliczane do wyniku (może być ujemne) |

- **Response `data`:** `price: float` (obliczony koszt), `pattern: string` (użyty wzór obliczenia)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

## Calculator Work (Patryk)

### GET `/calculator_work/calculator_keys`
Pobierz klucze (cennik/stawki) kalkulatora sprzedaży.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola **admin** (superadmin też przechodzi)
- **Path params:** brak
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `id: string (UUID)`, `income_tax: float`, `vat: float`, `inpost_parcel_locker: float`, `inpost_courier: float`, `inpost_cash_of_delivery_courier: float`, `dpd: float`, `allegro_matt: float`, `without_smart: float`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola admin)
  - `404` — Brak rekordu kluczy kalkulatora
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PUT `/calculator_work/calculator_keys/update`
Zaktualizuj klucze (cennik/stawki) kalkulatora sprzedaży.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola **admin**
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `id` | string | tak | Id rekordu kluczy kalkulatora; walidacja UUID |
| `income_tax` | float | tak | Podatek dochodowy (ułamek, np. 0.12); `>= 0` |
| `vat` | float | tak | VAT (ułamek, np. 0.23); `>= 0` |
| `inpost_parcel_locker` | float | tak | Koszt wysyłki: paczkomat InPost; `>= 0` |
| `inpost_courier` | float | tak | Koszt wysyłki: kurier InPost; `>= 0` |
| `inpost_cash_of_delivery_courier` | float | tak | Koszt wysyłki: kurier InPost za pobraniem; `>= 0` |
| `dpd` | float | tak | Koszt wysyłki: DPD; `>= 0` |
| `allegro_matt` | float | tak | Koszt wysyłki: Allegro Matt; `>= 0` |
| `without_smart` | float | tak | Koszt wysyłki: bez Allegro Smart; `>= 0` |

- **Response `data`:** jak w GET `/calculator_work/calculator_keys` (zaktualizowany rekord)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola admin)
  - `404` — Nie znaleziono rekordu kluczy o podanym id
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/calculator_work/calculator_keys/calculations`
Oblicz zysk ze sprzedaży (na podstawie cennika z kluczy kalkulatora).
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola **admin**
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `gross_sales` | float | tak | Cena sprzedaży brutto; `> 0` |
| `gross_purchase` | float | tak | Cena zakupu brutto; `> 0` |
| `provision` | float | tak | Prowizja w procentach; `>= 0` |
| `distinction` | float | tak | Wyróżnienie w procentach; `>= 0` |
| `referrer` | enum(string) | tak | Sposób wysyłki (klucz cennika); jedno z: `inpost_parcel_locker`, `inpost_courier`, `inpost_cash_of_delivery_courier`, `dpd`, `allegro_matt`, `without_smart` |

- **Response `data`:** `brutto: float`, `na_czysto: float`, `zysk_procentowy: float`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola admin)
  - `404` — Brak rekordu kluczy kalkulatora
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera
## Tasks

### GET `/tasks/collection`
Pobierz listę tasków zalogowanego użytkownika.
- **Auth:** `Authorization: Bearer <access_token>` — każdy zalogowany user
- **Path params:** brak
- **Query params:**
  - `active` — bool — opcjonalny — default: `true` — filtr aktywności tasków
- **Body:** brak
- **Response `data`:** lista obiektów:
  - `id: string (UUID)`, `description: string`, `time: int` (minuty), `active: bool`, `created_at: datetime | null`, `updated_at: datetime | null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/tasks/create`
Utwórz task (tylko superadmin). Zwraca `201`.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `description` | string | tak | Opis taska; max 255 znaków, nie może być pusty |
| `time` | int | tak | Czas w minutach, > 0 |
| `active` | bool | nie (default `true`) | Czy task jest aktywny |

- **Response `data`:** `id: string (UUID)`, `description: string`, `time: int`, `active: bool`, `created_at: datetime | null`, `updated_at: datetime | null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `409` — Konflikt danych (IntegrityError)
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PATCH `/tasks/update/{task_id}`
Zaktualizuj opis i czas taska (tylko superadmin).
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:**
  - `task_id` — string (UUID) — id taska; walidowany format UUID
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `description` | string | tak | Nowy opis taska; max 255 znaków, nie może być pusty |
| `time` | int | tak | Nowy czas w minutach, > 0 |

- **Response `data`:** `id: string (UUID)`, `description: string`, `time: int`, `active: bool`, `created_at: datetime | null`, `updated_at: datetime | null`
- **Kody błędów:**
  - `400` — Niepoprawny format task_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Task nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PATCH `/tasks/update/active/{task_id}`
Zaktualizuj aktywność taska (tylko superadmin).
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:**
  - `task_id` — string (UUID) — id taska; walidowany format UUID
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `active` | bool | tak | Nowy stan aktywności taska |

- **Response `data`:** `id: string (UUID)`, `description: string`, `time: int`, `active: bool`, `created_at: datetime | null`, `updated_at: datetime | null`
- **Kody błędów:**
  - `400` — Niepoprawny format task_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Task nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### DELETE `/tasks/delete/{task_id}`
Usuń task (tylko superadmin). Zwraca dane usuniętego taska.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:**
  - `task_id` — string (UUID) — id taska; walidowany format UUID
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `id: string (UUID)`, `description: string`, `time: int`, `active: bool`, `created_at: datetime | null`, `updated_at: datetime | null`
- **Kody błędów:**
  - `400` — Niepoprawny format task_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Task nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### GET `/tasks/statistics`
Statystyki wykonanych tasków użytkownika w zakresie dat.
- **Auth:** `Authorization: Bearer <access_token>` — każdy zalogowany user
- **Path params:** brak
- **Query params:**
  - `start_date` — datetime — opcjonalny — default: teraz (UTC) — początek zakresu statystyk (format: `yyyy-mm-dd`)
  - `end_date` — datetime — opcjonalny — default: teraz (UTC) — koniec zakresu statystyk (format: `yyyy-mm-dd`)
- **Body:** brak
- **Response `data`:**
  - `total_tasks: int`, `total_time: int`, `average_per_week: float`, `average_time_per_week: float`, `tasks_per_day: dict[string, int]` (klucz = dzień, wartość = liczba tasków)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

## Outstanding Money

### GET `/outstanding_money/collection`
Pobierz listy zaległych płatności użytkownika (z pozycjami i sumą).
- **Auth:** `Authorization: Bearer <access_token>` — każdy zalogowany user
- **Path params:** brak
- **Query params:** brak
- **Body:** brak
- **Response `data`:** lista obiektów:
  - `id_name: string (UUID)` — id listy
  - `name_overdue: string` — nazwa listy
  - `array_items: OutstandingItem[]` — pozycje: `id: string (UUID)`, `amount: float`, `name: string`, `date: date | null`, `id_name: string (UUID)`
  - `full_price: float` — suma pozycji
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/outstanding_money/create_list`
Utwórz listę zaległych płatności z pozycjami startowymi (tylko superadmin). Zwraca `201`.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | Nazwa listy zaległości; max 255 znaków, nie może być pusta |
| `array_object` | array | tak | Pozycje startowe listy |
| `array_object[].amount` | float | tak | Kwota pozycji |
| `array_object[].name` | string | tak | Nazwa pozycji; max 255 znaków, nie może być pusta |

- **Response `data`:**
  - `names_overdue: { id: string (UUID), name: string }` — utworzona lista
  - `new_outstanding_money: OutstandingItem[]` — utworzone pozycje (`id`, `amount`, `name`, `date`, `id_name`)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `409` — Konflikt danych (IntegrityError)
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/outstanding_money/add_item`
Dodaj pozycję do istniejącej listy zaległości (tylko superadmin). Zwraca `201`.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `id_name` | string | tak | Id listy (UUID); walidowany format UUID |
| `amount` | float | tak | Kwota pozycji |
| `name` | string | tak | Nazwa pozycji; max 255 znaków, nie może być pusta |

- **Response `data`:** `id: string (UUID)`, `amount: float`, `name: string`, `date: date | null`, `id_name: string (UUID)`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Lista o podanym id_name nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PUT `/outstanding_money/edit_name_list`
Zmień nazwę listy zaległości (tylko superadmin).
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `id` | string | tak | Id listy (UUID); walidowany format UUID |
| `name` | string | tak | Nowa nazwa listy; max 255 znaków, nie może być pusta |

- **Response `data`:** `id: string (UUID)`, `name: string`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Lista o podanym id nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PUT `/outstanding_money/edit_item`
Edytuj pozycję listy zaległości (tylko superadmin).
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `id` | string | tak | Id pozycji (UUID); walidowany format UUID |
| `amount` | float | tak | Nowa kwota pozycji |
| `name` | string | tak | Nowa nazwa pozycji; max 255 znaków, nie może być pusta |

- **Response `data`:** `id: string (UUID)`, `amount: float`, `name: string`, `date: date | null`, `id_name: string (UUID)`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Pozycja o podanym id nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### DELETE `/outstanding_money/delete_list/{id}`
Usuń listę zaległości wraz z pozycjami (tylko superadmin). Zwraca usunięte dane.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:**
  - `id` — string (UUID) — id listy; walidowany format UUID
- **Query params:** brak
- **Body:** brak
- **Response `data`:**
  - `name_overdue: { id: string (UUID), name: string }` — usunięta lista
  - `outstanding_money: OutstandingItem[]` — usunięte pozycje (`id`, `amount`, `name`, `date`, `id_name`)
- **Kody błędów:**
  - `400` — Niepoprawny format id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Lista o podanym id nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### DELETE `/outstanding_money/delete_item/{id}`
Usuń pozycję listy zaległości (tylko superadmin). Zwraca usuniętą pozycję.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:**
  - `id` — string (UUID) — id pozycji; walidowany format UUID
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `id: string (UUID)`, `amount: float`, `name: string`, `date: date | null`, `id_name: string (UUID)`
- **Kody błędów:**
  - `400` — Niepoprawny format id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Pozycja o podanym id nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera
## Calendar

Moduł kalendarza pracy: generowanie kalendarza rocznego, pobieranie dni miesiąca, statystyki, historia warunków pracy (norma godzin + stawka) oraz edycja dni pracy.

### GET `/calendar/collection`
Pobiera kalendarz pracy dla wskazanego miesiąca (dni + statystyki miesięczne i tygodniowe).
- **Auth:** `Authorization: Bearer <access_token>` — każdy zalogowany użytkownik
- **Path params:** brak
- **Query params:**
  - `year` — int — wymagany — zakres 2000–2100 — rok
  - `month` — int — wymagany — zakres 1–12 — miesiąc
- **Body:** brak
- **Response `data`:**
  - `year: int`, `month: int`, `month_name: str`
  - `days: CalendarDayData[]` — każdy: `id: str (uuid)`, `date: date`, `day_number: int`, `day_name: str`, `hours_worked: float`, `is_holiday: bool`, `norm_hours: float`, `hourly_rate: float`, `daily_salary: float`
  - `statistics: MonthStatisticsData` — `total_hours_worked: float`, `total_norm_hours: float`, `total_salary: float`, `weeks: WeekStatisticsData[]` (każdy: `week_number: int`, `total_hours: float`, `total_norm_hours: float`, `hourly_rate: float`, `salary: float`)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `404` — Brak kalendarza dla podanego roku/miesiąca
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### POST `/calendar/generate`
Generuje kalendarz pracy na cały rok (dni robocze, weekendy, święta z zewnętrznego API date.nager.at). Status sukcesu: **201**.
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|------|-----|----------|----------------|
| `year` | int | tak | Rok kalendarza; zakres: 2000 – (bieżący rok + 10) |

- **Response `data`:**
  - `calendar_days: GeneratedDayData[]` — każdy: `date: date`, `hours_worked: float|null`, `is_holiday: bool`, `is_weekend: bool`, `norm_hours: float`, `hourly_rate: float`
  - `inserted_count: int`
  - `summary: GeneratedCalendarSummaryData` — `total_days: int`, `total_holidays: int`, `total_weekends: int`, `year: int`, `days_before_today: int`, `working_days: int`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Brak warunków pracy w bazie
  - `409` — Kalendarz na ten rok już istnieje
  - `429` — Przekroczony limit zapytań
  - `502` — Błąd zewnętrznego API świąt (date.nager.at)
  - `500` — Nieoczekiwany błąd serwera

---

### GET `/calendar/statistics`
Roczne statystyki kalendarza pracy (suma godzin, zarobki, efektywność).
- **Auth:** `Authorization: Bearer <access_token>` — każdy zalogowany użytkownik
- **Path params:** brak
- **Query params:**
  - `year` — int — wymagany — zakres 2000–2100 — rok
- **Body:** brak
- **Response `data`:**
  - `year: int`, `total_hours_worked: float`, `total_earnings: float`, `working_days_count: int`, `total_norm_hours: float`, `hours_difference: float`, `total_holidays: int`, `total_days_in_year: int`, `average_hours_per_working_day: float`, `average_daily_earnings: float`, `work_efficiency_percentage: float`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### GET `/calendar/condition/collection`
Pobiera historię warunków pracy (norma godzin + stawka godzinowa).
- **Auth:** `Authorization: Bearer <access_token>` — każdy zalogowany użytkownik
- **Path params:** brak
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `WorkConditionData[]` — każdy: `id: str (uuid)`, `start_date: date`, `norm_hours: float`, `hourly_rate: float`, `created_at: datetime|null`, `updated_at: datetime|null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### POST `/calendar/condition/create`
Tworzy nowy wpis warunków pracy. Status sukcesu: **201**.
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|------|-----|----------|----------------|
| `norm_hours` | float | tak | Norma godzin dziennie; > 0 |
| `hourly_rate` | float | tak | Stawka godzinowa; > 0 |

- **Response `data`:** `WorkConditionData` — `id: str (uuid)`, `start_date: date`, `norm_hours: float`, `hourly_rate: float`, `created_at: datetime|null`, `updated_at: datetime|null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `409` — Konflikt danych (IntegrityError)
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### PATCH `/calendar/condition/update/{condition_id}`
Aktualizuje istniejące warunki pracy.
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:**
  - `condition_id` — str (uuid) — identyfikator warunków pracy
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|------|-----|----------|----------------|
| `norm_hours` | float | tak | Norma godzin dziennie; > 0 |
| `hourly_rate` | float | tak | Stawka godzinowa; > 0 |

- **Response `data`:** `WorkConditionData` — `id: str (uuid)`, `start_date: date`, `norm_hours: float`, `hourly_rate: float`, `created_at: datetime|null`, `updated_at: datetime|null`
- **Kody błędów:**
  - `400` — Niepoprawny format condition_id (nie-uuid)
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Warunki pracy nie istnieją
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### DELETE `/calendar/condition/delete/{condition_id}`
Usuwa wpis warunków pracy.
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:**
  - `condition_id` — str (uuid) — identyfikator warunków pracy
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `WorkConditionData` (usunięty wpis) — `id: str (uuid)`, `start_date: date`, `norm_hours: float`, `hourly_rate: float`, `created_at: datetime|null`, `updated_at: datetime|null`
- **Kody błędów:**
  - `400` — Niepoprawny format condition_id (nie-uuid)
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Warunki pracy nie istnieją
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### PATCH `/calendar/day/work/update/{day_id}`
Aktualizuje pojedynczy dzień pracy (norma, godziny przepracowane, stawka).
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:**
  - `day_id` — str (uuid) — identyfikator dnia pracy
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|------|-----|----------|----------------|
| `norm_hours` | float | tak | Norma godzin; 0–24 |
| `hours_worked` | float | tak | Godziny przepracowane; 0–24 |
| `hourly_rate` | float | tak | Stawka godzinowa; ≥ 0 |

- **Response `data`:** `WorkDayUpdateData` — `id: str (uuid)`, `date: date`, `norm_hours: float`, `hours_worked: float|null`, `hourly_rate: float`, `updated_at: datetime|null`
- **Kody błędów:**
  - `400` — Niepoprawny format day_id (nie-uuid)
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Dzień pracy nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### PATCH `/calendar/days/work/update`
Aktualizuje zakres dni pracy w miesiącu (od `start_day` do `end_day`) jednymi wartościami.
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|------|-----|----------|----------------|
| `year` | int | tak | Rok; 1900–2100 |
| `month` | int | tak | Miesiąc; 1–12 |
| `start_day` | int | tak | Dzień początkowy; 1–31; musi być ≤ `end_day` |
| `end_day` | int | tak | Dzień końcowy; 1–31 |
| `norm_hours` | float | tak | Norma godzin; 0–24 |
| `hours_worked` | float | tak | Godziny przepracowane; 0–24 |
| `hourly_rate` | float | tak | Stawka godzinowa; ≥ 0 |

- **Response `data`:** `WorkDaysRangeUpdateData` — `updated_count: int`, `start_date: date`, `end_date: date`, `days: date[]`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Brak dni w podanym zakresie
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

---

### PATCH `/calendar/days/work/update/salary`
Przelicza stawkę godzinową wstecz z podanej wypłaty i aktualizuje dni robocze miesiąca.
- **Auth:** `Authorization: Bearer <access_token>` — rola **superadmin**
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|------|-----|----------|----------------|
| `year` | int | tak | Rok; 1900–2100 |
| `month` | int | tak | Miesiąc; 1–12 |
| `salary` | float | tak | Wypłata do rozbicia na stawkę godzinową; ≥ 0 |

- **Response `data`:** `SalaryUpdateData` — `updated_count: int`, `total_hours_worked: float`, `calculated_hourly_rate: float`, `expected_salary: float`, `actual_total_salary: float`, `updated_days: SalaryUpdatedDayData[]` (każdy: `id: str (uuid)`, `date: date`, `hours_worked: float`, `hourly_rate: float`, `daily_salary: float`)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Brak dni roboczych z godzinami w miesiącu
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera
# Rental — słowniki

Wszystkie endpointy w tym module wymagają nagłówka `Authorization: Bearer <access_token>` i roli **superadmin** (`JWTBasicAuthenticationMiddleware(roles=["superadmin"])`). Rate limit: `RATE_LIMIT_READ` dla GET, `RATE_LIMIT_WRITE` dla POST/PUT/DELETE (klucz: user z tokena lub IP).

Wspólny format odpowiedzi: `{ "status": "SUCCESS" | "ERROR", "status_code": int, "data": ..., "additional": null }`.

---

## Rental — słowniki: Mieszkania (apartments)

### POST `/rentals/apartments/create`
Utwórz mieszkanie.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | max 255 znaków, nie może być pusty; np. "Pokój Państwa Dudzik" |
| `description` | string \| null | nie (default `null`) | Opis mieszkania |
| `is_active` | boolean | nie (default `true`) | Czy mieszkanie jest aktywne |

- **Response `data`:** obiekt mieszkania: `id` (string UUID), `name` (string), `description` (string|null), `is_active` (bool), `created_at` (datetime|null), `updated_at` (datetime|null)
- **Sukces:** `201`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `409` — konflikt danych (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera

### GET `/rentals/apartments/collection`
Pobierz listę mieszkań.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:**
  - `is_active` — boolean — opcjonalny — default `null` — filtr aktywności (brak = wszystkie)
- **Body:** brak
- **Response `data`:** lista obiektów mieszkania (pola jak wyżej)
- **Sukces:** `200`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/apartments/one/{apartment_id}`
Pobierz mieszkanie.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `apartment_id` — string (UUID) — identyfikator mieszkania
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt mieszkania (pola jak wyżej)
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `429` — limit zapytań; `500` — błąd serwera

### PUT `/rentals/apartments/update/{apartment_id}`
Zaktualizuj mieszkanie.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `apartment_id` — string (UUID) — identyfikator mieszkania
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | max 255 znaków, nie może być pusty |
| `description` | string \| null | nie (default `null`) | Nowy opis mieszkania |
| `is_active` | boolean | tak | Nowy stan aktywności |

- **Response `data`:** obiekt mieszkania (pola jak wyżej)
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### DELETE `/rentals/apartments/delete/{apartment_id}`
Usuń mieszkanie.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `apartment_id` — string (UUID) — identyfikator mieszkania
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt usuniętego mieszkania (pola jak wyżej)
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

---

## Rental — słowniki: Najemcy (tenants)

Obiekt najemcy w `data`: `id` (string UUID), `first_name` (string), `last_name` (string|null), `note` (string|null), `is_active` (bool), `created_at` (datetime|null), `updated_at` (datetime|null).

### POST `/rentals/tenants/create`
Utwórz najemcę.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `first_name` | string | tak | max 255 znaków, nie może być pusty |
| `last_name` | string \| null | nie (default `null`) | max 255 znaków |
| `note` | string \| null | nie (default `null`) | Notatka (telefon, uwagi) |
| `is_active` | boolean | nie (default `true`) | Czy najemca jest aktywny |

- **Response `data`:** obiekt najemcy
- **Sukces:** `201`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/tenants/collection`
Pobierz listę najemców.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:**
  - `is_active` — boolean — opcjonalny — default `null` — filtr aktywności (brak = wszystkie)
- **Body:** brak
- **Response `data`:** lista obiektów najemcy
- **Sukces:** `200`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/tenants/one/{tenant_id}`
Pobierz najemcę.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `tenant_id` — string (UUID) — identyfikator najemcy
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt najemcy
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `429` — limit zapytań; `500` — błąd serwera

### PUT `/rentals/tenants/update/{tenant_id}`
Zaktualizuj najemcę.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `tenant_id` — string (UUID) — identyfikator najemcy
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `first_name` | string | tak | max 255 znaków, nie może być pusty |
| `last_name` | string \| null | nie (default `null`) | max 255 znaków |
| `note` | string \| null | nie (default `null`) | Nowa notatka (telefon, uwagi) |
| `is_active` | boolean | tak | Nowy stan aktywności |

- **Response `data`:** obiekt najemcy
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### DELETE `/rentals/tenants/delete/{tenant_id}`
Usuń najemcę.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `tenant_id` — string (UUID) — identyfikator najemcy
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt usuniętego najemcy
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

---

## Rental — słowniki: Najmy (tenancies)

Obiekt najmu w `data`: `id` (string UUID), `apartment_id` (string UUID), `tenant_id` (string UUID), `rent_amount` (float), `persons_count` (int), `start_date` (date), `end_date` (date|null), `created_at` (datetime|null), `updated_at` (datetime|null).

### POST `/rentals/tenancies/create`
Utwórz najem (najemca + mieszkanie + czynsz).
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `apartment_id` | string (UUID) | tak | UUID mieszkania (walidacja formatu) |
| `tenant_id` | string (UUID) | tak | UUID najemcy (walidacja formatu) |
| `rent_amount` | float | tak | ≥ 0 — czynsz deklarowany dla tego najmu |
| `persons_count` | int | nie (default `1`) | > 0 — liczba osób (do kosztów per osoba) |
| `start_date` | date (`YYYY-MM-DD`) | tak | Początek najmu |
| `end_date` | date \| null | nie (default `null`) | Koniec najmu (`null` = najem trwa) |

- **Response `data`:** obiekt najmu
- **Sukces:** `201`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — mieszkanie lub najemca nie istnieje; `409` — konflikt danych (np. nakładające się najmy); `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/tenancies/collection`
Pobierz listę najmów (z historią).
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:**
  - `apartment_id` — string (UUID) — opcjonalny — default `null` — filtr po mieszkaniu
  - `tenant_id` — string (UUID) — opcjonalny — default `null` — filtr po najemcy
  - `active_on` — date (`YYYY-MM-DD`) — opcjonalny — default `null` — tylko najmy aktywne w danym dniu
- **Body:** brak
- **Response `data`:** lista obiektów najmu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format `apartment_id` lub `tenant_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/tenancies/one/{tenancy_id}`
Pobierz najem.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `tenancy_id` — string (UUID) — identyfikator najmu
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt najmu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `429` — limit zapytań; `500` — błąd serwera

### PUT `/rentals/tenancies/update/{tenancy_id}`
Zaktualizuj najem (czynsz, osoby, daty). Nie zmienia mieszkania ani najemcy.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `tenancy_id` — string (UUID) — identyfikator najmu
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `rent_amount` | float | tak | ≥ 0 — nowy czynsz deklarowany |
| `persons_count` | int | tak | > 0 — nowa liczba osób |
| `start_date` | date (`YYYY-MM-DD`) | tak | Nowy początek najmu |
| `end_date` | date \| null | nie (default `null`) | Nowy koniec najmu (`null` = najem trwa) |

- **Response `data`:** obiekt najmu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### DELETE `/rentals/tenancies/delete/{tenancy_id}`
Usuń najem.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `tenancy_id` — string (UUID) — identyfikator najmu
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt usuniętego najmu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

---

## Rental — słowniki: Rodzaje kosztów (cost_types)

Obiekt rodzaju kosztu w `data`: `id` (string UUID), `name` (string), `charge_type` (string: `"fixed"` | `"per_person"`), `is_active` (bool), `created_at` (datetime|null), `updated_at` (datetime|null).

### POST `/rentals/cost_types/create`
Utwórz rodzaj kosztu.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | max 255 znaków, nie może być pusty; np. "śmieci", "internet" |
| `charge_type` | `"fixed"` \| `"per_person"` | tak | Sposób naliczania |
| `is_active` | boolean | nie (default `true`) | Czy rodzaj kosztu jest aktywny |

- **Response `data`:** obiekt rodzaju kosztu
- **Sukces:** `201`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/cost_types/collection`
Pobierz listę rodzajów kosztów.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:**
  - `is_active` — boolean — opcjonalny — default `null` — filtr aktywności (brak = wszystkie)
- **Body:** brak
- **Response `data`:** lista obiektów rodzaju kosztu
- **Sukces:** `200`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/cost_types/one/{cost_type_id}`
Pobierz rodzaj kosztu.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `cost_type_id` — string (UUID) — identyfikator rodzaju kosztu
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt rodzaju kosztu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `429` — limit zapytań; `500` — błąd serwera

### PUT `/rentals/cost_types/update/{cost_type_id}`
Zaktualizuj rodzaj kosztu.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `cost_type_id` — string (UUID) — identyfikator rodzaju kosztu
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | max 255 znaków, nie może być pusty |
| `charge_type` | `"fixed"` \| `"per_person"` | tak | Nowy sposób naliczania |
| `is_active` | boolean | tak | Nowy stan aktywności |

- **Response `data`:** obiekt rodzaju kosztu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### DELETE `/rentals/cost_types/delete/{cost_type_id}`
Usuń rodzaj kosztu.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `cost_type_id` — string (UUID) — identyfikator rodzaju kosztu
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt usuniętego rodzaju kosztu
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

---

## Rental — słowniki: Koszty mieszkań (apartment_costs)

Obiekt kosztu mieszkania w `data`: `id` (string UUID), `apartment_id` (string UUID), `cost_type_id` (string UUID), `amount` (float), `start_date` (date), `end_date` (date|null), `created_at` (datetime|null), `updated_at` (datetime|null).

### POST `/rentals/apartment_costs/create`
Przypisz koszt do mieszkania.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `apartment_id` | string (UUID) | tak | UUID mieszkania (walidacja formatu) |
| `cost_type_id` | string (UUID) | tak | UUID rodzaju kosztu (walidacja formatu) |
| `amount` | float | tak | ≥ 0 — kwota (dla `per_person` — stawka za osobę) |
| `start_date` | date (`YYYY-MM-DD`) | tak | Początek obowiązywania stawki |
| `end_date` | date \| null | nie (default `null`) | Koniec obowiązywania (`null` = obowiązuje) |

- **Response `data`:** obiekt kosztu mieszkania
- **Sukces:** `201`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — mieszkanie lub rodzaj kosztu nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/apartment_costs/collection`
Pobierz listę kosztów mieszkań (z historią stawek).
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:**
  - `apartment_id` — string (UUID) — opcjonalny — default `null` — filtr po mieszkaniu
  - `active_on` — date (`YYYY-MM-DD`) — opcjonalny — default `null` — tylko koszty obowiązujące w danym dniu
- **Body:** brak
- **Response `data`:** lista obiektów kosztu mieszkania
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format `apartment_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/apartment_costs/one/{apartment_cost_id}`
Pobierz koszt mieszkania.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `apartment_cost_id` — string (UUID) — identyfikator kosztu mieszkania
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt kosztu mieszkania
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `429` — limit zapytań; `500` — błąd serwera

### PUT `/rentals/apartment_costs/update/{apartment_cost_id}`
Zaktualizuj koszt mieszkania. Nie zmienia mieszkania ani rodzaju kosztu.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `apartment_cost_id` — string (UUID) — identyfikator kosztu mieszkania
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `amount` | float | tak | ≥ 0 — nowa kwota (dla `per_person` — stawka za osobę) |
| `start_date` | date (`YYYY-MM-DD`) | tak | Nowy początek obowiązywania stawki |
| `end_date` | date \| null | nie (default `null`) | Nowy koniec obowiązywania (`null` = obowiązuje) |

- **Response `data`:** obiekt kosztu mieszkania
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### DELETE `/rentals/apartment_costs/delete/{apartment_cost_id}`
Usuń koszt mieszkania.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `apartment_cost_id` — string (UUID) — identyfikator kosztu mieszkania
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt usuniętego kosztu mieszkania
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

---

## Rental — słowniki: Liczniki (meters)

Obiekt licznika w `data`: `id` (string UUID), `apartment_id` (string UUID|null), `media_type` (string: `"electricity"` | `"water"`), `is_master` (bool), `name` (string|null), `is_active` (bool), `created_at` (datetime|null), `updated_at` (datetime|null).

### POST `/rentals/meters/create`
Utwórz licznik.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `media_type` | `"electricity"` \| `"water"` | tak | Rodzaj medium |
| `apartment_id` | string (UUID) \| null | nie (default `null`) | UUID mieszkania (`null` = licznik główny budynku); walidacja formatu UUID |
| `is_master` | boolean | nie (default `false`) | Licznik nadrzędny (zużycie = odczyt − suma pozostałych) |
| `name` | string \| null | nie (default `null`) | max 255 znaków — nazwa licznika |
| `is_active` | boolean | nie (default `true`) | Czy licznik jest aktywny |

- **Response `data`:** obiekt licznika
- **Sukces:** `201`
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — mieszkanie nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/meters/collection`
Pobierz listę liczników.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** brak
- **Query params:**
  - `apartment_id` — string (UUID) — opcjonalny — default `null` — filtr po mieszkaniu
  - `media_type` — `"electricity"` | `"water"` — opcjonalny — default `null` — filtr po medium
  - `is_active` — boolean — opcjonalny — default `null` — filtr aktywności (brak = wszystkie)
- **Body:** brak
- **Response `data`:** lista obiektów licznika
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format `apartment_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `429` — limit zapytań; `500` — błąd serwera

### GET `/rentals/meters/one/{meter_id}`
Pobierz licznik.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `meter_id` — string (UUID) — identyfikator licznika
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt licznika
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `429` — limit zapytań; `500` — błąd serwera

### PUT `/rentals/meters/update/{meter_id}`
Zaktualizuj licznik. Nie zmienia `media_type` ani `apartment_id`.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `meter_id` — string (UUID) — identyfikator licznika
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `is_master` | boolean | tak | Nowy stan flagi licznika nadrzędnego |
| `name` | string \| null | nie (default `null`) | max 255 znaków — nowa nazwa licznika |
| `is_active` | boolean | tak | Nowy stan aktywności |

- **Response `data`:** obiekt licznika
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — limit zapytań; `500` — błąd serwera

### DELETE `/rentals/meters/delete/{meter_id}`
Usuń licznik.
- **Auth:** `Authorization: Bearer <access_token>` — rola: superadmin
- **Path params:** `meter_id` — string (UUID) — identyfikator licznika
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt usuniętego licznika
- **Sukces:** `200`
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień; `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — limit zapytań; `500` — błąd serwera
# Rental — rozliczenia (billing)

Wszystkie endpointy tego modułu wymagają roli **superadmin** i nagłówka `Authorization: Bearer <access_token>`.

## Rental — okresy rozliczeniowe (periods)

### POST `/rentals/periods/create`
Tworzy nowy okres rozliczeniowy i szkielet odczytów dla aktywnych liczników — pole „Ostatnio" prefillowane z ostatniego okresu danego licznika (0 dla nowego licznika).
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `period_month` | `date` (YYYY-MM-DD) | tak | Miesiąc okresu (zawsze 1. dzień miesiąca) |
| `electricity_bill_amount` | `float \| null` | nie (default `null`) | Kwota rachunku globalnego prądu („Do zapłaty"), `>= 0` |
| `electricity_rate` | `float \| null` | nie (default `null`) | Stawka prądu zł/kWh, `>= 0` |
| `electricity_rate_is_manual` | `bool` | nie (default `false`) | `true` = stawka prądu nadpisana ręcznie |
| `water_rate` | `float` | nie (default `9.00`) | Stawka wody zł/m³, `>= 0` |
| `note` | `string \| null` | nie (default `null`) | Notatka do okresu |

- **Response `data`** (`201`): obiekt okresu — `id: str (UUID)`, `period_month: date`, `status: str` (`draft`/`closed`), `electricity_bill_amount: float|null`, `electricity_rate: float|null`, `electricity_rate_is_manual: bool`, `water_rate: float`, `note: str|null`, `created_at: datetime|null`, `updated_at: datetime|null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `409` — Okres dla tego miesiąca już istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### GET `/rentals/periods/collection`
Pobiera listę okresów rozliczeniowych.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:**
  - `status` — `"draft" | "closed"` — opcjonalny — default `null` — filtr statusu okresu
- **Body:** brak
- **Response `data`** (`200`): lista obiektów okresu (pola jak w POST create)
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### GET `/rentals/periods/one/{period_id}`
Pobiera pojedynczy okres rozliczeniowy.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body:** brak
- **Response `data`** (`200`): obiekt okresu (pola jak w POST create)
- **Kody błędów:**
  - `400` — Niepoprawny format identyfikatora
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Rekord nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PUT `/rentals/periods/update/{period_id}`
Aktualizuje okres rozliczeniowy (kwoty rachunku / stawki / notatka). Zamknięty okres wymaga wcześniejszego reopen.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `electricity_bill_amount` | `float \| null` | nie (default `null`) | Nowa kwota rachunku globalnego prądu, `>= 0` |
| `electricity_rate` | `float \| null` | nie (default `null`) | Nowa stawka prądu zł/kWh, `>= 0` |
| `electricity_rate_is_manual` | `bool` | **tak** | `true` = stawka prądu nadpisana ręcznie |
| `water_rate` | `float` | **tak** | Nowa stawka wody zł/m³, `>= 0` |
| `note` | `string \| null` | nie (default `null`) | Nowa notatka do okresu |

- **Response `data`** (`200`): obiekt okresu (pola jak w POST create)
- **Kody błędów:**
  - `400` — Niepoprawny format period_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres nie istnieje
  - `409` — Okres jest zamknięty
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/rentals/periods/preview/{period_id}`
Wylicza okres „na żywo" — nic nie zapisuje. Pełne wyliczenie: zużycia, błąd licznika głównego z propozycją podziału, stawka zł/kWh, rozliczenia per mieszkanie i podział rodzinny. POST (nie GET), bo body przenosi opcjonalne korekty jednorazowe per mieszkanie.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body** (opcjonalne — default `{"adjustments": []}`):

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `adjustments` | `array` | nie (default `[]`) | Korekty jednorazowe per mieszkanie |
| `adjustments[].apartment_id` | `string (UUID)` | tak | UUID mieszkania, którego dotyczy korekta |
| `adjustments[].name` | `string` | tak | Nazwa korekty, np. „zaległe media", „nadpłata"; max 255 znaków, niepusta |
| `adjustments[].amount` | `float` | tak | Kwota korekty (może być ujemna) |

- **Response `data`** (`200`) — pełne wyliczenie okresu:
  - `period` — obiekt okresu (pola jak w POST create)
  - `electricity_rate: float` — użyta stawka zł/kWh
  - `electricity_total_consumption: float`
  - `main_meter_error: object | null` — `{ main_difference: float, apartments_total: float, error: float, proposals: [{ meter_id: str, apartment_id: str|null, proposed_correction: float }] }`
  - `consumptions: array` — `[{ meter_id: str, apartment_id: str|null, media_type: str, raw_difference: float, consumption: float, error_correction: float, is_master: bool }]`
  - `settlements: array` — `[{ apartment_id: str, apartment_name: str, settlement: { apartment_id: str, tenancy_id: str|null, rent_amount: float, electricity_consumption: float, electricity_cost: float, water_consumption: float, water_cost: float, total_media_amount: float, total_amount: float, items: [{ name: str, kind: str, amount: float, cost_type_id: str|null }] } }]`
  - `beneficiaries: array` — `[{ beneficiary_id: str, beneficiary_name: str, total_amount: float, items: [{ description: str, amount: float, rule_id: str|null, settlement_id: str|null }] }]`
  - `warnings: string[]`
- **Kody błędów:**
  - `400` — Niepoprawny format period_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/rentals/periods/close/{period_id}`
Zamyka okres — wylicza i zapisuje snapshoty: rozliczenia mieszkań z pozycjami i podział rodzinny. Zamknięty okres nie zmienia się przy późniejszej edycji słowników.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body:** jak w preview (opcjonalne `adjustments`, default `[]` — patrz tabela wyżej)
- **Response `data`** (`200`): identyczna struktura jak w preview (pełne wyliczenie okresu)
- **Kody błędów:**
  - `400` — Niepoprawny format period_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres nie istnieje
  - `409` — Okres jest już zamknięty
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### POST `/rentals/periods/reopen/{period_id}`
Ponownie otwiera zamknięty okres — kasuje snapshoty rozliczeń, zostawia odczyty i dane wejściowe; okres wraca do statusu `draft`.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body:** brak
- **Response `data`** (`200`): obiekt okresu (pola jak w POST create)
- **Kody błędów:**
  - `400` — Niepoprawny format period_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres nie istnieje
  - `409` — Okres nie jest zamknięty
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### DELETE `/rentals/periods/delete/{period_id}`
Usuwa okres rozliczeniowy — pełne wycofanie okresu, kasuje odczyty i snapshoty rozliczeń.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body:** brak
- **Response `data`** (`200`): obiekt usuniętego okresu (pola jak w POST create)
- **Kody błędów:**
  - `400` — Niepoprawny format period_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

## Rental — odczyty liczników (readings)

### POST `/rentals/readings/create`
Ręcznie dodaje odczyt licznika w okresie — np. dla licznika założonego po utworzeniu okresu.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `period_id` | `string (UUID)` | tak | UUID okresu rozliczeniowego (walidacja formatu UUID) |
| `meter_id` | `string (UUID)` | tak | UUID licznika (walidacja formatu UUID) |
| `previous_value` | `float` | tak | Odczyt „Ostatnio", `>= 0` |
| `current_value` | `float` | tak | Odczyt „Teraz", `>= 0` |
| `error_correction` | `float` | nie (default `0`) | Korekta błędu licznika (może być ujemna) |

- **Response `data`** (`201`): obiekt odczytu — `id: str (UUID)`, `period_id: str`, `meter_id: str`, `previous_value: float`, `current_value: float`, `error_correction: float`, `created_at: datetime|null`, `updated_at: datetime|null`
- **Kody błędów:**
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres lub licznik nie istnieje
  - `409` — Odczyt tego licznika w tym okresie już istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### GET `/rentals/readings/collection/{period_id}`
Pobiera odczyty liczników w danym okresie.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `period_id` — `string (UUID)` — identyfikator okresu
- **Query params:** brak
- **Body:** brak
- **Response `data`** (`200`): lista obiektów odczytu (pola jak w POST create odczytu)
- **Kody błędów:**
  - `400` — Niepoprawny format period_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Okres nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### PUT `/rentals/readings/update/{reading_id}`
Aktualizuje odczyt licznika — wpisanie odczytu „Teraz" i ewentualnej ręcznej korekty błędu licznika.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `reading_id` — `string (UUID)` — identyfikator odczytu
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `previous_value` | `float` | tak | Nowy odczyt „Ostatnio", `>= 0` |
| `current_value` | `float` | tak | Nowy odczyt „Teraz", `>= 0` |
| `error_correction` | `float` | **tak** | Nowa korekta błędu licznika (może być ujemna) |

- **Response `data`** (`200`): obiekt odczytu (pola jak w POST create odczytu)
- **Kody błędów:**
  - `400` — Niepoprawny format reading_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Odczyt nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### DELETE `/rentals/readings/delete/{reading_id}`
Usuwa odczyt licznika.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `reading_id` — `string (UUID)` — identyfikator odczytu
- **Query params:** brak
- **Body:** brak
- **Response `data`** (`200`): obiekt usuniętego odczytu (pola jak w POST create odczytu)
- **Kody błędów:**
  - `400` — Niepoprawny format reading_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Odczyt nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

## Rental — snapshoty rozliczeń (settlements)

Snapshoty są tworzone automatycznie przy zamykaniu okresu (`POST /rentals/periods/close/{period_id}`) — brak endpointów create/update/delete.

### GET `/rentals/settlements/collection`
Pobiera snapshoty rozliczeń mieszkań zapisane przy zamknięciu okresów — filtrowanie po okresie i/lub mieszkaniu.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** brak
- **Query params:**
  - `period_id` — `string (UUID)` — opcjonalny — default `null` — filtr po okresie
  - `apartment_id` — `string (UUID)` — opcjonalny — default `null` — filtr po mieszkaniu
- **Body:** brak
- **Response `data`** (`200`): lista snapshotów — każdy: `id: str (UUID)`, `period_id: str`, `apartment_id: str`, `tenancy_id: str|null`, `rent_amount: float`, `electricity_consumption: float`, `electricity_cost: float`, `water_consumption: float`, `water_cost: float`, `total_media_amount: float`, `total_amount: float`, `note: str|null`, `created_at: datetime|null`, `updated_at: datetime|null`, `items: [{ id: str, settlement_id: str, cost_type_id: str|null, name: str, kind: str, amount: float, created_at: datetime|null, updated_at: datetime|null }]`
- **Kody błędów:**
  - `400` — Niepoprawny format period_id lub apartment_id
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera

### GET `/rentals/settlements/one/{settlement_id}`
Pobiera pojedynczy snapshot rozliczenia mieszkania.
- **Auth:** `Authorization: Bearer <access_token>` — rola `superadmin`
- **Path params:** `settlement_id` — `string (UUID)` — identyfikator snapshotu
- **Query params:** brak
- **Body:** brak
- **Response `data`** (`200`): obiekt snapshotu (pola jak w collection, wraz z `items`)
- **Kody błędów:**
  - `400` — Niepoprawny format identyfikatora
  - `401` — Brak lub niepoprawny token
  - `403` — Brak uprawnień (wymagana rola superadmin)
  - `404` — Rekord nie istnieje
  - `429` — Przekroczony limit zapytań
  - `500` — Nieoczekiwany błąd serwera
# Rental — podział rodzinny (family) i Contact

## Rental — beneficjenci (beneficiaries)

### POST `/rentals/beneficiaries/create`
Utwórz beneficjenta podziału rodzinnego (np. "Ja", "Ojciec", "Mama").
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | Nazwa beneficjenta; max 255 znaków, nie może być pusta |
| `is_active` | boolean | nie (default `true`) | Czy beneficjent jest aktywny |

- **Response `data`:** `id` (string UUID), `name` (string), `is_active` (boolean), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `409` — konflikt danych (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `201`

### GET `/rentals/beneficiaries/collection`
Pobierz listę beneficjentów.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** brak
- **Query params:**
  - `is_active` — boolean — opcjonalny — default `null` — filtr aktywności (brak = wszystkie)
- **Body:** brak
- **Response `data`:** lista obiektów: `id` (string UUID), `name` (string), `is_active` (boolean), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### GET `/rentals/beneficiaries/one/{beneficiary_id}`
Pobierz pojedynczego beneficjenta.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `beneficiary_id` — string (UUID) — identyfikator beneficjenta
- **Query params:** brak
- **Body:** brak
- **Response `data`:** `id` (string UUID), `name` (string), `is_active` (boolean), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `400` — niepoprawny format identyfikatora (nie-UUID); `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — rekord nie istnieje; `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### PUT `/rentals/beneficiaries/update/{beneficiary_id}`
Zaktualizuj beneficjenta (pełna podmiana pól — oba pola wymagane).
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `beneficiary_id` — string (UUID) — identyfikator beneficjenta
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `name` | string | tak | Nowa nazwa beneficjenta; max 255 znaków, nie może być pusta |
| `is_active` | boolean | tak | Nowy stan aktywności beneficjenta |

- **Response `data`:** `id` (string UUID), `name` (string), `is_active` (boolean), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### DELETE `/rentals/beneficiaries/delete/{beneficiary_id}`
Usuń beneficjenta.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `beneficiary_id` — string (UUID) — identyfikator beneficjenta
- **Query params:** brak
- **Body:** brak
- **Response `data`:** usunięty rekord: `id` (string UUID), `name` (string), `is_active` (boolean), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

## Rental — reguły podziału (allocation_rules)

### POST `/rentals/allocation_rules/create`
Utwórz regułę podziału rodzinnego (kto dostaje jaki składnik rozliczenia).
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `beneficiary_id` | string (UUID) | tak | UUID beneficjenta; walidacja formatu UUID |
| `component` | string enum: `rent` \| `electricity` \| `water` \| `cost_type` \| `recurring` | tak | Składnik podziału |
| `mode` | string enum: `fixed_amount` \| `full` | tak | Tryb: `fixed_amount` (konkretna kwota) lub `full` (cała kwota składnika) |
| `start_date` | date (`YYYY-MM-DD`) | tak | Początek obowiązywania reguły |
| `apartment_id` | string (UUID) \| null | nie (default `null`) | UUID mieszkania (`null` = wszystkie mieszkania); walidacja UUID jeśli podane |
| `cost_type_id` | string (UUID) \| null | nie (default `null`) | UUID rodzaju kosztu (wymagane dla `component = cost_type`); walidacja UUID jeśli podane |
| `amount` | number \| null | nie (default `null`) | Kwota (wymagana dla `mode = fixed_amount` i `component = recurring`; może być ujemna) |
| `description` | string \| null | nie (default `null`) | Etykieta pozycji, np. "podatek"; max 255 znaków |
| `end_date` | date \| null | nie (default `null`) | Koniec obowiązywania (`null` = obowiązuje bezterminowo) |

- **Response `data`:** `id` (string UUID), `beneficiary_id` (string UUID), `apartment_id` (string UUID \| null), `component` (string), `cost_type_id` (string UUID \| null), `mode` (string), `amount` (number \| null), `description` (string \| null), `start_date` (date), `end_date` (date \| null), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — beneficjent, mieszkanie lub rodzaj kosztu nie istnieje; `409` — konflikt danych (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `201`

### GET `/rentals/allocation_rules/collection`
Pobierz listę reguł podziału (z historią — także reguły zakończone).
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** brak
- **Query params:**
  - `beneficiary_id` — string (UUID) — opcjonalny — default `null` — filtr po beneficjencie
  - `apartment_id` — string (UUID) — opcjonalny — default `null` — filtr po mieszkaniu
  - `active_on` — date (`YYYY-MM-DD`) — opcjonalny — default `null` — tylko reguły obowiązujące w danym dniu
- **Body:** brak
- **Response `data`:** lista obiektów reguły (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format `beneficiary_id` lub `apartment_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### GET `/rentals/allocation_rules/one/{rule_id}`
Pobierz pojedynczą regułę podziału.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `rule_id` — string (UUID) — identyfikator reguły
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt reguły (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — rekord nie istnieje; `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### PUT `/rentals/allocation_rules/update/{rule_id}`
Zaktualizuj regułę podziału (pełna podmiana — pola opcjonalne pominięte w body są ustawiane na `null`).
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `rule_id` — string (UUID) — identyfikator reguły
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `component` | string enum: `rent` \| `electricity` \| `water` \| `cost_type` \| `recurring` | tak | Nowy składnik podziału |
| `mode` | string enum: `fixed_amount` \| `full` | tak | Nowy tryb |
| `start_date` | date (`YYYY-MM-DD`) | tak | Nowy początek obowiązywania |
| `apartment_id` | string (UUID) \| null | nie (default `null`) | Nowy UUID mieszkania (`null` = wszystkie mieszkania); walidacja UUID jeśli podane |
| `cost_type_id` | string (UUID) \| null | nie (default `null`) | Nowy UUID rodzaju kosztu (wymagane dla `cost_type`); walidacja UUID jeśli podane |
| `amount` | number \| null | nie (default `null`) | Nowa kwota (może być ujemna) |
| `description` | string \| null | nie (default `null`) | Nowa etykieta pozycji; max 255 znaków |
| `end_date` | date \| null | nie (default `null`) | Nowy koniec obowiązywania (`null` = obowiązuje) |

- **Response `data`:** obiekt reguły (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — rekord nie istnieje; `409` — konflikt danych (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### DELETE `/rentals/allocation_rules/delete/{rule_id}`
Usuń regułę podziału.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `rule_id` — string (UUID) — identyfikator reguły
- **Query params:** brak
- **Body:** brak
- **Response `data`:** usunięty obiekt reguły (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format identyfikatora; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — rekord nie istnieje; `409` — rekord ma powiązania (IntegrityError); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

## Rental — snapshoty podziału (beneficiary_settlements)

### GET `/rentals/beneficiary_settlements/collection`
Pobierz snapshoty podziału rodzinnego — wyniki podziału zapisane przy zamknięciu okresów; filtrowanie po okresie i/lub beneficjencie.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** brak
- **Query params:**
  - `period_id` — string (UUID) — opcjonalny — default `null` — filtr po okresie rozliczeniowym
  - `beneficiary_id` — string (UUID) — opcjonalny — default `null` — filtr po beneficjencie
- **Body:** brak
- **Response `data`:** lista obiektów:
  - `id` (string UUID), `period_id` (string UUID), `beneficiary_id` (string UUID), `total_amount` (number), `created_at` (datetime \| null), `updated_at` (datetime \| null)
  - `items` (lista pozycji, default `[]`), każda pozycja: `id` (string UUID), `beneficiary_settlement_id` (string UUID), `description` (string), `amount` (number), `rule_id` (string UUID \| null), `settlement_id` (string UUID \| null), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `400` — niepoprawny format `period_id` lub `beneficiary_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

## Contact — formularz kontaktowy

### POST `/contact/messages/create`
**[Public]** Wyślij wiadomość kontaktową — publiczny endpoint dla frontendów/backendów, bez JWT usera. Restrykcyjny rate limit per IP (5/min).
- **Auth:** header **`X-Contact-Token`** (zamiast `Authorization`) — krótkożyciowy token JWT **HS256** podpisany wspólnym sekretem `SECRET_KEY_CONTACT_TOKEN` (z env backendu). Frontend generuje token samodzielnie (np. biblioteką `jose`) z claimami: `application` (identyfikator aplikacji nadawcy, np. `"portfolio"` — ląduje w polu `application` wiadomości, NIE przesyła się go w body), `exp` (wymagany — token bez `exp` odrzucany; zalecane 5 min), `iat` (zalecany). Pełna instrukcja z przykładami JS/Python: `docs/CONTACT_TOKEN.md`.
- **Path params:** brak
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `first_name` | string | tak | Imię nadawcy; max 255 znaków, nie może być puste |
| `last_name` | string \| null | nie (default `null`) | Nazwisko nadawcy; max 255 znaków |
| `phone_number` | string | tak | Numer telefonu; max 30 znaków; opcjonalny `+`, 6–15 cyfr, dopuszczalne spacje i myślniki |
| `email` | string (email) \| null | nie (default `null`) | Adres e-mail do odpowiedzi; walidacja formatu e-mail |
| `description` | string | tak | Treść zapytania / opis zadania; max 5000 znaków, nie może być pusta |

- **Response `data`:** `id` (string UUID), `first_name` (string), `last_name` (string \| null), `phone_number` (string), `email` (string \| null), `description` (string), `application` (string — z tokena), `status` (string: `new` \| `read` \| `closed`), `created_at` (datetime \| null), `updated_at` (datetime \| null)
- **Kody błędów:** `401` — brak, niepoprawny lub przeterminowany X-Contact-Token; `429` — przekroczony limit zapytań (per IP); `500` — nieoczekiwany błąd serwera
- **Sukces:** `201`

### GET `/contact/messages/collection`
Pobierz listę wiadomości kontaktowych.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** brak
- **Query params:**
  - `application` — string — opcjonalny — default `null` — filtr po aplikacji nadawcy
  - `status` — string enum: `new` \| `read` \| `closed` — opcjonalny — default `null` — filtr po statusie obsługi
- **Body:** brak
- **Response `data`:** lista obiektów wiadomości (pola jak w POST create powyżej)
- **Kody błędów:** `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### GET `/contact/messages/one/{message_id}`
Pobierz pojedynczą wiadomość kontaktową.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `message_id` — string (UUID) — identyfikator wiadomości
- **Query params:** brak
- **Body:** brak
- **Response `data`:** obiekt wiadomości (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format `message_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — wiadomość nie istnieje; `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### PUT `/contact/messages/update/status/{message_id}`
Zmień status obsługi wiadomości.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `message_id` — string (UUID) — identyfikator wiadomości
- **Query params:** brak
- **Body:**

| Pole | Typ | Wymagane | Opis/walidacja |
|---|---|---|---|
| `status` | string enum: `new` \| `read` \| `closed` | tak | Nowy status obsługi wiadomości |

- **Response `data`:** obiekt wiadomości (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format `message_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — wiadomość nie istnieje; `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`

### DELETE `/contact/messages/delete/{message_id}`
Usuń wiadomość kontaktową.
- **Auth:** `Authorization: Bearer <access_token>` — wymagana rola `superadmin`
- **Path params:** `message_id` — string (UUID) — identyfikator wiadomości
- **Query params:** brak
- **Body:** brak
- **Response `data`:** usunięty obiekt wiadomości (pola jak w POST create powyżej)
- **Kody błędów:** `400` — niepoprawny format `message_id`; `401` — brak lub niepoprawny token; `403` — brak uprawnień (wymagana rola superadmin); `404` — wiadomość nie istnieje; `429` — przekroczony limit zapytań; `500` — nieoczekiwany błąd serwera
- **Sukces:** `200`
