# Plan implementacji: magazyn plików (domena `files`)

> Plan powstał na bazie rozmowy z użytkownikiem (prywatny, szyfrowany magazyn
> plików per osoba/kategoria, S3 + presigned URL) oraz istniejącego w innym
> repo użytkownika systemu `File` (init/update statusu uploadu). Wszystkie
> nowe funkcjonalności przechodzą przez standardowe warstwy: endpoint →
> handler → service / `_psql`, tuple pattern `(result, error, ok)`, audyt
> `create_logs_psql`, rate limiting, testy wg wzorca — zob. `ARCHITEKTURA.md`.
> Wzorzec strukturalny tego dokumentu: `PLAN_ROZLICZENIA_MIESZKAN.md`.

---

## 0. Status implementacji (2026-09-15)

Pierwszy przyrost zrobiony jako port istniejącego, prostszego modułu S3 z
innego projektu — **odbiega od modelu danych opisanego w sekcji 3** poniżej.
Zrobione:

- `database/psql/models/file.py` — `files` (nie ma podziału na osobny plik
  `files.py`/`files_nodes.py` z sekcji 3 — obie tabele w jednym module): `id`,
  `user_id` (FK → `users.id`, nullable), `original_name`, `name`, `size`,
  `file_type`, `mime_type`, `s3_key` (unique), `s3_prefix`, **`url`** (kolumna
  jednak jest — inaczej niż ustalono w sekcji 3.2 „brak kolumny `url`"),
  `status`, pola pod multipart upload (`multipart_upload_id`, `chunk_size`,
  `total_chunks`, `uploaded_chunks`), `created_at`/`updated_at`. Enumy
  `FileStatus`/`FileType` jak w planie, ale bez `FileType.DOCUMENT` i bez
  słowników `ALLOWED_EXTENSIONS`/`MAX_FILE_SIZE_BYTES`. Brak dat gwarancji,
  brak `CHECK` constraintu.
- **Drzewo podmiotów (`FilesNode`/`files_nodes`)** — dodane w tej samej
  konwencji co planowano (sekcja 3.1): `id`, `name`, `parent_id` (self-FK,
  `RESTRICT`), `description`, `is_active`, `created_at`/`updated_at`,
  `UniqueConstraint(parent_id, name)`. Na `files` dodane `node_id` (FK →
  `files_nodes.id`, `RESTRICT`, nullable) i `parent_file_id` (self-FK,
  **`CASCADE`** — jedyny wyjątek od `RESTRICT` w bazie, plik-dziecko nie ma
  sensu bez rodzica). **Bez M:M** między `files` i `files_nodes` — jeden plik
  = jeden węzeł + opcjonalnie jeden plik-rodzic; potwierdzone end-to-end
  (Artur → Faktura/Faktura 2/Faktura 3 przez `node_id`, Faktura →
  faktura-1-2 przez `parent_file_id`, `RESTRICT` poprawnie blokuje usunięcie
  węzła z przypisanym plikiem). M:M („wolne tagi") zostaje jako opcjonalny
  dodatek na przyszłość (sekcja 7), nie zamiennik.
- `core/repository/psql/file/node/` — podstawowe `_psql` dla węzłów:
  `create_files_node_psql`, `collection_files_nodes_psql` (jeden poziom po
  `parent_id`, bez rekursji po poddrzewie na razie), `update_files_node_psql`
  (partial — `None` = nie dotykaj pola, tak jak `update_file_psql`; **znana
  wada**: nie da się tak przenieść węzła na najwyższy poziom, bo `None` w
  `new_parent_id` znaczy „nie zmieniaj", nie „wyczyść" — do poprawienia przy
  pisaniu handlera/endpointu), `delete_files_node_psql` (`RESTRICT` z bazy →
  `IntegrityError`/409, gdy węzeł ma dzieci-węzły lub przypisane pliki).
  Jeszcze bez handlera/endpointu/schematów — czysta warstwa `_psql`.
- `database/psql/sql/database_down.sql` — dopisane `DROP TABLE
  files`/`files_nodes` (w ogóle ich nie było) oraz `DROP TYPE
  file_type`/`file_status` — `DROP TABLE ... CASCADE` nie usuwa natywnych
  enumów Postgresa, więc kolejny `migration_up` po `migration_restart`
  wybuchał `DuplicateObject: typ "file_type" już istnieje`.
- `config/settings.py` — pola `aws_access_key_id`, `aws_secret_access_key`,
  `aws_region`, `s3_bucket_name` (bez `s3_kms_key_id` i bez pól
  `file_*_url_expire_seconds` z sekcji 4.1 — SSE-KMS jeszcze nieużyty).
- `core/infra/s3/` (nie `core/service/files/s3.py` jak w sekcji 4) —
  `config.py` (`get_s3_client()`), `init.py`
  (`initialization_url_upload_file()` — tworzy rekord `File` przez
  `create_file_psql` i wystawia presigned PUT), `delete.py`
  (`delete_file_s3()` — `head_object` + `delete_object`), `response.py`
  (`S3InitUploadFileResponse`).
- `core/repository/psql/file/` — `create_file_psql`, `collection_files_psql`
  (filtry `file_type`/`original_name`/`catalog`, paginacja), `delete_file_psql`,
  `confirm_file_by_id_psql` (ustawia `status=COMPLETED` — upload potwierdzony,
  zob. status pliku w sekcji 1), `update_file_psql` (edycja `name`/`status`,
  oba parametry opcjonalne — `None` = nie dotykaj pola) — wszystkie zwracają
  jeden wspólny `FileResponse` z `response.py`, wg wzorca `_psql` z
  `ARCHITEKTURA.md` (tuple `(result, error, ok)`, `db.query().filter()`, bez
  ręcznego `db.commit()` — robi to `managed_session`). `check.py` zostawiony
  pusty: nic jeszcze nie referencjonuje `files.id` z innej tabeli, więc nie ma
  czego sprawdzać pod „plik w użyciu" — dopisać, gdy pojawi się pierwsza
  domena konsumująca pliki (i wtedy też przełącznik na `CONFIRMED` przy
  podpięciu).
- `core/service/file/delete.py` (+ `response.py`) — usuwa rekord przez
  `delete_file_psql`, potem obiekt z S3 przez `delete_file_s3`; bez kroku
  „w użyciu" (patrz wyżej).
- **Handler + endpoint (etapy 4–6, bez węzłów/assign)** — pierwszy kawałek
  modułu wywoływalny przez HTTP: `core/handler/file/` (`init.py`,
  `update.py`, `delete.py`, `collection.py`, audyt `create_logs_psql` ze
  slotami `files:init`/`files:update`/`files:delete_file`/`files:collection`)
  → `api/schemas/file/` (`payload.py`, `response.py`) → `api/endpoints/file/`
  → `POST /files/init`, `PUT /files/update/{file_id}`,
  `DELETE /files/delete/{file_id}`, `GET /files/collection` (stałe w
  `api/routers.py`, wpięte w `api/api.py`, tag Swagger „Files" w
  `config/swagger_description/tags.py`). Rola superadmin dla wszystkiego,
  `RATE_LIMIT_WRITE`/`RATE_LIMIT_READ` jak w `rentals`. Szczególny przypadek
  w `handler_update_file`: gdy w body przyjdzie `status="confirmed"`, handler
  odpala `confirm_file_by_id_psql` (dedykowana ścieżka „upload potwierdzony");
  dla każdego innego statusu (albo samej `name`) idzie ogólny
  `update_file_psql`. Brak testów dla handlera/endpointu — na razie
  zweryfikowane ręcznie przez `main.app.openapi()` + pełny test suite (bez
  regresji).
- Konfiguracja AWS zweryfikowana end-to-end na realnym koncie: dedykowany
  user IAM (nie root) z inline policy ograniczoną do jednego bucketu
  (`s3:PutObject`/`GetObject`/`DeleteObject`/`ListBucket` na
  `storage-fastapi-s3`), klucze w `env/local.env`. Wszystkie zmienne env
  (nie tylko AWS/S3) dostały prefiks `BACKEND_SERVER_JOB_` —
  `config/settings.py` czyta go teraz przez `env_prefix` w `model_config`
  (bez `validation_alias` na polach, gdzie nazwa pola pokrywa się z nazwą
  zmiennej; wyjątek: `db_name` → `DB_DBNAME`, jawny pełny alias, bo
  `env_prefix` nie dokłada się automatycznie do pól z ustawionym aliasem).
- `tests/core/infra/s3/test_init.py` + `test_delete.py` — testy integracyjne
  oznaczone `@pytest.mark.full_integration` (realny S3, poza domyślnym
  zakresem `make run_test`/`run_test_integration`, odpalane ręcznie przez
  `make run_test_full` albo `-m full_integration`): upload realnego pliku
  przez wystawiony presigned PUT + `head_object`, usuwanie obiektu i
  ścieżka błędu `NotFound` dla brakującego klucza. Każdy test sam czyści po
  sobie obiekty wgrane na S3 (`finally`/bezpiecznik).

- **Handler/endpoint/schematy dla węzłów (sekcja 5.1, pełny CRUD)** —
  `core/handler/file/node/` (`create`/`collection`/`one`/`update`/`delete`,
  audyt `create_logs_psql` ze slotami `files:create_node`/`collection_nodes`/
  `one_node`/`update_node`/`delete_node`) → `api/schemas/file/node/`
  (`payload.py`, `response.py`) → `api/endpoints/file/node/` →
  `POST /files/nodes/create`, `GET /files/nodes/collection` (filtr
  `parent_id`, jeden poziom), `GET /files/nodes/one/{node_id}` (bez
  breadcrumb na razie — zwykłe pobranie rekordu), `PUT
  /files/nodes/update/{node_id}`, `DELETE /files/nodes/delete/{node_id}`.
  Stałe w `api/routers.py`, wpięte w `api/api.py`, tag Swagger
  „Files/Nodes" w `config/swagger_description/tags.py`. Rola superadmin,
  `RATE_LIMIT_WRITE`/`RATE_LIMIT_READ` jak wszędzie.
  - Przy okazji naprawiona **znana wada** z `update_files_node_psql`
    (przenoszenie węzła na najwyższy poziom): repo dostało nowy parametr
    `clear_parent_id: bool`, a endpoint update odróżnia „pominięty
    `parent_id`" od „jawne `parent_id: null`" przez `body.model_fields_set`
    (oba dają `None` w Pythonie, więc nie da się tego rozróżnić samą
    wartością).
  - Dopisana też brakująca `one_files_node_psql` (repo miało dotąd tylko
    create/collection/update/delete) — `core/repository/psql/file/node/one.py`.
  - Bez testów handlera/endpointu na razie — zweryfikowane ręcznie przez
    `main.app.openapi()` (wszystkie 5 ścieżek widoczne) + pełny test suite
    (489 passed, bez regresji).
- **Testy `_psql` dla węzłów** — `tests/core/repository/psql/file/node/`
  (`helper.py` z fabryką `make_files_node`, po 3–4 testy na
  `create`/`collection`/`one`/`update`/`delete`, wzorowane na
  `tests/core/repository/psql/rental/dictionaries/`), łącznie 16 testów.
  Pokrywają m.in. `UniqueConstraint(parent_id, name)` (duplikat pod tym
  samym rodzicem → `IntegrityError`), `RESTRICT` przy węźle z dzieckiem
  oraz nowo naprawione `clear_parent_id` (przeniesienie węzła na najwyższy
  poziom). Pełny test suite: 505 passed, bez regresji.
- **Repository dla `assign`/`metadata` na plikach (sekcja 5.3, tylko warstwa
  `_psql` — bez handlera/endpointu na razie)**:
  - `database/psql/models/file.py` — dopisane kolumny `description`,
    `guarantee_start_date`, `guarantee_end_date` na `files` (zgodnie z
    sekcją 3.2 — świadomie **na pliku**, nie na `files_nodes`: węzeł to
    osoba/kategoria, różne pliki pod tym samym węzłem mogą mieć różne albo
    żadne gwarancje, a filtr `guarantee_status` z sekcji 5.5 i tak działa
    na kolekcji plików). Dodany też `CHECK
    (status != 'CONFIRMED' OR node_id IS NOT NULL)` z sekcji 3.2
    (`ck_files_confirmed_requires_node`) — uwaga: natywny enum Postgresa
    trzyma **wielkie litery** (`'CONFIRMED'`, nie `'confirmed'`), bo
    SQLAlchemy domyślnie mapuje `.name` enuma, nie `.value`. Migracja
    Alembic (`alembic/versions/9507ebdeec64_init.py`) zaktualizowana
    ręcznie w tym samym `create_table('files', ...)` — repo ma jedną
    squashniętą migrację `init`, regenerowaną przez `make
    migration_restart` (nie osobne rewizje per feature). Migracja
    zmieniona tylko w pliku - nie odpalona na żadnej realnej bazie w tej
    sesji.
  - `FileResponse`/`_to_file_response` — doszły `node_id`, `parent_file_id`,
    `description`, `guarantee_start_date`, `guarantee_end_date`.
  - Nowa `assign_file_psql` (`core/repository/psql/file/assign.py`) —
    pierwsze przypisanie pliku do węzła, wymaga `status=COMPLETED`
    (inaczej `IntegrityError`/409 — konwencja „konflikt stanu" jak w
    `handler_close_billing_period` dla rentals), ustawia `node_id` (+
    opcjonalnie `parent_file_id`), `status=CONFIRMED`.
  - `update_file_psql` rozszerzony o `node_id`/`parent_file_id`/
    `description`/daty gwarancji. `node_id` celowo **bez** `clear_node_id`
    — nie da się tą funkcją odczepić potwierdzonego pliku od węzła (to
    robi tylko `assign_file_psql` przy pierwszym przypisaniu); pozostałe
    pola nullable (`parent_file_id`, `description`, daty gwarancji) mają
    dedykowane flagi `clear_*`, tym samym trickiem co `clear_parent_id`
    przy węzłach.
  - Testy: `tests/core/repository/psql/file/test_assign.py` (4 na
    `assign_file_psql` + 1 bezpośredni test samego `CHECK` constraintu
    przez `make_file(status=CONFIRMED)` bez `node_id`), rozszerzony
    `test_update.py` (+4 przypadki: `node_id`/`parent_file_id`,
    `clear_parent_file_id`, opis, daty gwarancji). Pełny test suite: 514
    passed, bez regresji.
- **Handler/endpoint/schematy dla `assign`/`metadata` (dokończenie sekcji
  5.3)** — `core/handler/file/assign.py` (`handler_assign_file`, audyt
  `files:assign`) i `core/handler/file/metadata.py`
  (`handler_update_file_metadata`, audyt `files:update_metadata`, cienka
  warstwa nad `update_file_psql`) → `api/schemas/file/payload.py`
  (`FileAssignPayload`, `FileMetadataPayload`) → `api/endpoints/file/`
  (`assign.py`, `metadata.py`) → `PUT /files/assign/{file_id}`,
  `PUT /files/metadata/{file_id}`. Stałe w `api/routers.py`, wpięte w
  `api/api.py`, tag Swagger „Files" (bez nowego taga - to ten sam zasób).
  - `update_file_psql` dostał dodatkowo `new_original_name` (metadata
    edytuje `original_name` - nazwę wyświetlaną, zgodnie z sekcją 3.2/5.3
    - a nie `name`, które edytuje już istniejący `PUT /files/update/{id}`
    ze statusowego flow).
  - `FileResponseData` (API-facing schema) rozszerzone o `node_id`,
    `parent_file_id`, `description`, daty gwarancji - wcześniej te pola
    były tylko w wewnętrznym `FileResponse` (repo), nieeksponowane w API;
    teraz widoczne też w istniejących `collection`/`update`.
  - Endpoint metadata używa tego samego tricku `model_fields_set` co
    `PUT /files/nodes/update/{node_id}` do rozróżnienia „pominięte pole"
    od „jawne `null`" dla `parent_file_id`/`description`/dat gwarancji.
    `node_id` bez opcji czyszczenia (zgodnie z ustaleniem).
  - Bez testów handlera/endpointu na razie — zweryfikowane przez
    `main.app.openapi()` (obie ścieżki widoczne) + pełny test suite (514
    passed, bez regresji).

- **Czytelny błąd przy usuwaniu węzła z przypisanymi plikami** —
  `delete_files_node_psql` dostał jawny pre-check (`SELECT COUNT ... WHERE
  files.node_id = :node_id`) przed `DELETE`: gdy węzeł ma choć jeden
  przypisany plik, zwraca `IntegrityError`/409 z czytelnym komunikatem
  „Węzeł {id} ma przypisane pliki ({n}) - nie można usunąć." zamiast
  surowego błędu Postgresa. `RESTRICT` z bazy zostaje jako druga linia
  obrony (np. dzieci-węzły - tam komunikat wciąż jest z samej bazy).
  Testy: blokada z przypisanym plikiem (sprawdzone dosłowne "przypisane
  pliki" w komunikacie) + happy path po odczepieniu ostatniego pliku.
  Pełny test suite: 516 passed, bez regresji.

- **Test e2e całego przepływu magazynu plików, realny S3** —
  `tests/api/endpoints/file/notes/test_api_e2e_full_flow.py`, oznaczony
  `@pytest.mark.full_integration` (bije w prawdziwy bucket S3 i realną
  bazę, tak jak strzelałby frontend - wzorzec:
  `tests/api/endpoints/rental/test_api_e2e_full_flow.py` dla HTTP przez
  `TestClient`/`authorized_as`/`make_client`,
  `tests/core/infra/s3/test_init.py` dla prawdziwego `PUT` na presigned
  URL). Flow: `POST /files/nodes/create` → per plik (x3) `POST
  /files/init` → prawdziwy `requests.put` na S3 → `PUT
  /files/update/{id}` (`status=confirmed` → wewnętrznie `completed`) →
  `PUT /files/assign/{id}` (→ `confirmed`, `node_id` ustawiony) → próba
  `DELETE /files/nodes/delete/{node_id}` z podpiętymi plikami (409,
  asercja na treść komunikatu „przypisane pliki" - weryfikuje e2e
  checker z poprzedniego przyrostu) → `DELETE /files/delete/{id}`
  pojedynczo dla każdego pliku (asercja, że obiekt realnie zniknął z S3
  przez `head_object` → `ClientError` 404) → `DELETE
  /files/nodes/delete/{node_id}` teraz przechodzi (200). `finally` z
  bezpiecznikiem czyszczącym S3, gdyby asercja wybuchła w środku. Domyślny
  test suite bez zmian (516 passed, nowy test poprawnie odseparowany
  marker-em, nie odpala się bez `-m full_integration`).

- **Kaskada S3 przy delete plików-dzieci (dokończenie sekcji 5)** —
  `delete_file_psql` zbiera teraz `child_s3_keys` (BFS po `parent_file_id`,
  wszystkie poziomy zagnieżdżenia - baza i tak kasuje rekordy dzieci sama
  przez `ondelete=CASCADE`, ale nie ich obiekty S3). `delete_file_service`
  usuwa z S3 najpierw plik główny, potem best-effort wszystkie
  `child_s3_keys` - `NotFound` dla dziecka (nigdy nie dokończyło uploadu)
  to nie błąd, realny błąd S3 na dziecku owszem (`S3DeleteFailed`).
  Testy: `tests/core/repository/psql/file/test_delete.py` (BFS zbiera
  dzieci i wnuki, cascade w bazie potwierdzony), nowy
  `tests/core/service/file/test_delete.py` (mock `delete_file_s3` -
  wywołania dla rodzica+dzieci, `NotFound` tolerowany, realny błąd nie).
- **Odczyt: filtry w `collection` + `GET /files/one/{id}` + `GET
  /files/unassigned` (sekcja 5.4/6)** — `collection_files_psql` dostał
  `node_id` (+ `recursive` - BFS po drzewie węzłów, cały poddrzew),
  `created_at_from`/`created_at_to` (zakres dat, `created_at_to`
  włącznie - `< to + 1 dzień`, nie ostre `<=`). **Uwaga:** zakres dat
  porównywany jest w timezone sesji DB (`Europe/Warsaw`, nie UTC) - dzień
  kalendarzowy liczy się lokalnie, co wyszło na jaw dopiero przy pisaniu
  testu (błędnie dobrany czas w UTC "przeskakiwał" na kolejny dzień
  lokalnie). Nowa `one_file_psql` (`GET /files/one/{file_id}`) - szczegóły
  + lista **bezpośrednich** plików-dzieci (bez wnuków, bez breadcrumb
  węzła - ta sama decyzja co przy węzłach). Nowa
  `collection_unassigned_files_psql` (`GET /files/unassigned`) - skrót
  `status=COMPLETED AND node_id IS NULL`. Pełny stos (handler → schema →
  endpoint → routers.py/api.py) dla obu nowych endpointów, filtry
  wpięte w istniejący `GET /files/collection`. Testy: `test_collection.py`
  (node_id/recursive/daty), `test_one.py`, `test_unassigned.py` - 10
  testów. Pełny test suite: 534 passed, bez regresji; e2e
  `full_integration` (S3) też bez regresji.

- **Gwarancje (etap 8, dokończenie sekcji 5.5)** — bez nowego endpointu do
  zapisu: `PUT /files/metadata/{file_id}` (a pod spodem `update_file_psql`)
  już od przyrostu 5 umiał ustawiać/czyścić `guarantee_start_date`/
  `guarantee_end_date`, więc etap 8 to wyłącznie odczyt/filtrowanie.
  `collection_files_psql` dostał `guarantee_status: active|expired|none`
  (liczone względem `guarantee_end_date` i `date.today()` w timezone sesji
  DB): `active` = `end_date >= dziś`, `expired` = `end_date < dziś`,
  `none` = brak `end_date` (**ustalone z użytkownikiem**: plik z samym
  `guarantee_start_date`, ale bez `end_date`, też liczy się jako `none` -
  bez daty końca nie da się ocenić aktywności). Nowy `GET
  /files/guarantees/expiring` (`core/repository/psql/file/guarantees.py`,
  `collection_expiring_guarantees_psql`) - sztywne 30 dni
  (`EXPIRING_WITHIN_DAYS`, bez parametru w API - **ustalone z
  użytkownikiem**, na razie brak potrzeby na konfigurowalność), plik ma
  gwarancję kończącą się w `[dziś, dziś+30]` (obie granice włącznie),
  posortowane rosnąco po `guarantee_end_date` (najpilniejsze pierwsze).
  Pełny stos (repo → handler → schema reużyta `FileCollectionResponseData`
  → endpoint → `routers.py`/`api.py`), audyt `files:guarantees_expiring`.
  Testy: 5 nowych w `tests/core/repository/psql/file/`
  (`test_collection.py` +2 dla `guarantee_status`, nowy
  `test_guarantees.py` +3 dla granic okna 30 dni). Pełny test suite: 539
  passed, bez regresji.

- **Preview + download (etap 7)** — `config/settings.py` dostał
  `file_preview_url_expire_seconds` (domyślnie 180) i
  `file_download_url_expire_seconds` (domyślnie 60), oba z defaultem w
  Pythonie (zgodnie z planem sekcja 4.1) - nie trzeba nic dopisywać w
  `env/*.env`. Nowa `core/infra/s3/get.py::generate_get_presigned_url` -
  wspólna funkcja dla podglądu (`disposition="inline"`) i pobierania
  (`disposition="attachment"`, wymusza nazwę pliku przez
  `ResponseContentDisposition`), zgodnie z planem sekcja 4 pkt 3. Nowa
  `core/repository/psql/file/view.py::get_viewable_file_psql` - wspólny
  warunek dla obu (status `COMPLETED`/`CONFIRMED`, inaczej
  `IntegrityError`/409 - `PENDING`/`FAILED` nie mają gotowego obiektu na
  S3), reużywany przez oba service'y. `core/service/file/{preview,download}.py`
  orkiestrują repo (status check) + S3 (presigned GET), zwracają wspólny
  `ServiceFileUrlResponse`. **`GET /files/preview/{file_id}`** zwraca URL w
  zwykłym `ApiResponse` (JSON, do embedowania np. w `<img src>`).
  **`GET /files/download/{file_id}`** robi prawdziwy **302 redirect**
  (`RedirectResponse`) na presigned URL - zgodnie z planem sekcja 1
  („Pobieranie: Redirect..."), wymagał `response_model=None` w FastAPI
  (Union `RedirectResponse | JSONResponse` nie jest polem Pydantic).
  **Uwaga dla frontendu**: `/files/download/{id}` wymaga nagłówka
  `Authorization: Bearer` (jak każdy inny endpoint) - zwykłe
  `<a href="...">`/nawigacja przeglądarki tego nie wyśle; trzeba strzelić
  przez `fetch()` z tokenem, a potem albo pozwolić mu podążyć za
  redirectem, albo odczytać `Location`/URL z odpowiedzi i użyć go wprost.
  Testy: `test_view.py` (5, granice statusów), `test_preview.py`/
  `test_download.py` (mock S3, po 3 - poprawny URL+expiry, blokada bez
  wołania S3, propagacja błędu S3), plus `tests/core/infra/s3/test_get.py`
  (`full_integration`, realny S3: pobranie treści + poprawny
  `Content-Disposition`). Pełny test suite: 550 passed, bez regresji.

- **Usunięty goły URL S3 z `files`** — `url` w tabeli `files` (i w
  odpowiedziach API: `FileResponseData.url`, `FileInitResponseData.url`)
  zawsze `None` teraz - `initialization_url_upload_file` już nie buduje
  `https://{bucket}.s3.{region}.amazonaws.com/{key}`, bo bucket jest
  prywatny i ten link i tak nie działał bez podpisu (był tylko myslący
  „że coś działa"; jedyny działający dostęp to `signed_url` przy
  uploadzie i `preview`/`download` po fakcie). `create_file_psql` i
  `S3InitUploadFileResponse.url` przełączone na `str | None`. Sprawdzone
  na realnym S3 (`test_init.py`, e2e S3) - bez regresji, 550 passed.
  **Uwaga**: kolumna `url` w bazie nadal istnieje (nullable, nic nie
  usuwa istniejących wartości u istniejących rekordów) - to nie jest
  migracja czyszcząca stare dane, tylko zmiana zachowania dla nowych.

- **Bucket S3 zamknięty na produkcji** — `Block all public access` włączone,
  usunięta bucket policy z `Principal: "*"` (jawnie zezwalała każdemu w
  internecie na `GetObject`/`PutObject` bez podpisu - realna dziura,
  znaleziona przy weryfikacji konsoli AWS), dopisany CORS na buckecie pod
  `https://praca.strona.arturscibor.pl` (+ localhost pod dev) dla
  `PUT`/`GET`/`HEAD` - wymagane, żeby frontend mógł wgrywać pliki na
  `signed_url` z `/files/init` (S3 ma własny, osobny CORS, niezależny od
  `CORSMiddleware` w `main.py`, który dotyczy tylko wołań do naszego API).
  Zweryfikowane: wszystkie testy `full_integration` (realny S3) przeszły
  po zablokowaniu publicznego dostępu.
- **Testy `_psql` dla `create_file_psql`/`confirm_file_by_id_psql`** —
  jedyne dwie funkcje repo w całej domenie `files` bez własnych testów
  (istniały od pierwszego przyrostu). Nowy
  `tests/core/repository/psql/file/test_create.py` (3: pola +
  domyślny status `PENDING`, realny `user_id`, duplikat `s3_key` →
  `IntegrityError` z `UniqueConstraint`). `confirm_file_by_id_psql`
  dostał nową klasę `TestConfirmFileByIdPsql` w istniejącym
  `test_update.py` (3: `PENDING→COMPLETED`, `NotFound`, idempotencja gdy
  już `COMPLETED`). Pełny test suite: 556 passed, bez regresji.

- **Testy API (TestClient) dla `init`/`update`/`delete` plików, bez
  mocków poza JWT (full_integration)** — nowy
  `tests/api/endpoints/file/test_api_init_update_delete.py`. Wzorzec:
  `make_client`/`authorized_as` z `tests/api/helper.py` (JWT mockowane
  przez podmianę lookupu usera w middleware, reszta - baza `db_session` i
  S3 - prawdziwa), nie testy handlerów (handler to cienka warstwa
  orkiestracji/audytu, logika biznesowa jest w repo/service, więc testy
  handlerów byłyby w dużej mierze duplikatem testów repo-level).
  10 testów: `init` (rekord `PENDING` bez `url`, realny PUT na S3 +
  `head_object`, 422 przy złym payloadzie, 401 bez auth), `update`
  (`confirmed`→`completed`, rename bez ruszania statusu, 400 zły format
  id, 404 nie istnieje), `delete` (rekord + realny obiekt S3 znika,
  **kaskada S3 dla plików-dzieci przetestowana na realnym S3 pierwszy
  raz** - wcześniej tylko mock na poziomie service, 404 nie istnieje).
  Pełny test suite: 556 passed (bez zmian - nowe testy `full_integration`,
  domyślnie odseparowane), wszystkie `full_integration` razem: 15 passed.

- **Testy API dla reszty domeny files** — dociągnięte wg tego samego
  wzorca (`make_client`/`authorized_as`, bez mocków poza JWT):
  - `tests/api/endpoints/file/node/test_api_node.py` (17) - pełny CRUD
    węzłów: create/collection/one/update/delete, duplikat nazwy pod tym
    samym rodzicem (409 - **uwaga**: dwa węzły najwyższego poziomu z tą
    samą nazwą NIE kolidują, `NULL != NULL` w Postgresie, test musiał to
    uwzględnić), `clear`/pominięty `parent_id` przy update, `RESTRICT`
    (dziecko-węzeł i przypisany plik, z asercją na treść komunikatu),
    400/404/401/403, audit log
  - `tests/api/endpoints/file/test_api_assign_metadata.py` (15) - `assign`
    (completed→confirmed, `parent_file_id`, zły status→409, 400/404/422,
    audit log), `metadata` (rename, zmiana węzła, `clear`/pominięty
    `parent_file_id`, opis/gwarancje, 400/404, audit log)
  - `tests/api/endpoints/file/test_api_collection_one_unassigned_guarantees.py`
    (13) - filtry `collection` (`file_type`, `node_id`+`recursive`,
    zakres dat, `guarantee_status`, paginacja), `one` (plik + dzieci
    bezpośrednie, 404/400), `unassigned`, `guarantees/expiring`
  - `tests/api/endpoints/file/test_api_preview_download.py` (8,
    `full_integration`, realny S3) - `preview`/`download` zwracają
    faktycznie działający presigned URL (pobrane bajty == wgrane bajty,
    poprawny `Content-Disposition`), `download` weryfikowany przez
    prawdziwy redirect (`follow_redirects=False` + ręczne podążenie),
    zły status→409, 400/404

  Węzły/assign/metadata/collection/one/unassigned/guarantees nie dotykają
  S3, więc bez markera `full_integration` (jak testy `rentals`) - realna
  baza wystarczy. Pełny domyślny suite: 601 passed (+45), wszystkie
  `full_integration` razem: 23 passed (+8), zero leftoverów na buckecie.
- **Breadcrumb dla `GET /files/nodes/one/{node_id}`** — response
  zmieniony z gołego rekordu węzła na `{node, breadcrumb}`. `breadcrumb`
  to lista od korzenia do węzła włącznie (`[{id, name}, ...]`) - budowana
  prostą pętlą po `parent_id` w górę (`_build_breadcrumb` w
  `core/repository/psql/file/node/one.py`), nie BFS (to zawsze jeden
  łańcuch, bez rozgałęzień, w przeciwieństwie do zejścia po poddrzewie w
  `collection_files_psql?recursive=true`). Nowe dataclassy
  `FilesNodeBreadcrumbItem`/`FilesNodeWithBreadcrumbResponse`
  (`core/repository/psql/file/node/response.py`) i odpowiadające im
  schematy Pydantic w `api/schemas/file/node/response.py`. **Breaking
  change kształtu odpowiedzi** `GET /files/nodes/one/{node_id}` — dane
  węzła teraz pod kluczem `data.node`, nie płasko pod `data` (frontend
  musi się dostosować, jeśli już korzysta z tego endpointu). Testy: 2
  nowe w `test_one.py` (korzeń ma breadcrumb z samym sobą, 3-poziomowy
  łańcuch w poprawnej kolejności) + 1 API (`test_api_node.py`). Pełny
  suite: 604 passed, bez regresji.

- **SSE-KMS (dokończenie etapu 2)** — presigned PUT wymusza teraz szyfrowanie
  kluczem zarządzanym w KMS (CMK, alias `zaq12wsxXSWQAXCZASD312`) zamiast
  polegania na domyślnym szyfrowaniu bucketu. `config/settings.py` dostał
  `s3_kms_key_id` (env `BACKEND_SERVER_JOB_S3_KMS_KEY_ID`, w `local.env` jako
  `alias/...`), `initialization_url_upload_file`
  (`core/infra/s3/init.py`) dodaje `ServerSideEncryption: "aws:kms"` +
  `SSEKMSKeyId` do `Params` w `generate_presigned_url("put_object", ...)`. Po
  stronie AWS: nowy customer managed key w KMS, w jego Key policy dodany jako
  Key user dedykowany IAM user backendu (`ArturScibor` — zweryfikowane
  `sts.get_caller_identity()` na kluczach z `local.env`); bez tego backend
  dostałby `AccessDenied` na `kms:GenerateDataKey`. **Odkryte przy
  testach**: presigned URL nie zaszywa wartości nagłówków SSE w query
  stringu — klient (frontend, i każdy test robiący realny `requests.put`)
  musi wysłać dokładnie `x-amz-server-side-encryption: aws:kms` i
  `x-amz-server-side-encryption-aws-kms-key-id: {key}` w headerach PUT,
  inaczej S3 zwraca `403 SignatureDoesNotMatch` (nie `AccessDenied` — łatwo
  pomylić przy debugowaniu). Zweryfikowane end-to-end na realnym S3
  (`head_object` po uploadzie potwierdza `ServerSideEncryption=aws:kms` +
  poprawny ARN klucza). Zaktualizowane 4 pliki testowe robiące realny PUT
  (`tests/core/infra/s3/test_init.py`,
  `tests/api/endpoints/file/test_api_preview_download.py`,
  `tests/api/endpoints/file/test_api_init_update_delete.py`,
  `tests/api/endpoints/file/notes/test_api_e2e_full_flow.py`) o te same
  nagłówki. Pełny test suite (`-m ""`, łącznie z `full_integration`): 629
  passed.

- **`kms_key_id` w odpowiedzi `POST /files/init` + limit rozmiaru 50 MB** —
  zaczęta budowa frontendu magazynu plików (drugie repo,
  `project-job-website-vue.js`, plan: `docs/PLAN_MAGAZYN_PLIKOW.md` tamtego
  repo) wymagała rozstrzygnięcia, skąd frontend ma znać
  `x-amz-server-side-encryption-aws-kms-key-id` do nagłówków przy PUT na
  `signed_url` — zdecydowano: backend zwraca go wprost (opcja „jedno miejsce
  prawdy" zamiast duplikowania aliasu klucza w env frontendu).
  `S3InitUploadFileResponse`/`FileInitResponseData` dostały nowe pole
  `kms_key_id` (`core/infra/s3/response.py`, `api/schemas/file/response.py`),
  `initialization_url_upload_file` (`core/infra/s3/init.py`) wypełnia je z
  `settings.s3_kms_key_id`. Przy okazji dodany twardy limit rozmiaru pliku:
  `FileInitPayload.size` (`api/schemas/file/payload.py`) ma teraz
  `le=MAX_FILE_SIZE_BYTES` (50 MB, `50 * 1024 * 1024`) — wcześniej
  jedynym ograniczeniem było `gt=0` (brak górnego limitu w ogóle, mimo że
  oryginalny plan sekcja 3.3 zakładał słowniki `MAX_FILE_SIZE_BYTES` per
  `file_type`, nigdy niezaimplementowane — to uproszczona wersja, jeden
  wspólny limit, nie per-typ). Zaktualizowany `summary`/`description`
  endpointu w swaggerze (`api/endpoints/file/init.py`) o oba fakty. Testy
  robiące realny PUT (`test_init.py`, `test_api_init_update_delete.py`,
  `test_api_preview_download.py`, `test_api_e2e_full_flow.py`) przełączone
  z `settings.s3_kms_key_id` na `kms_key_id` z odpowiedzi API (testuje
  realny kontrakt, nie wartość configu bezpośrednio); nowy
  `test_init04_size_over_50mb_returns_422`. **Nieodpalone w tej sesji** —
  zmiana nieskończona `make run_test_full` (backend ma teraz zasadę w
  CLAUDE.md: nie odpalać testów/make samodzielnie, robi to użytkownik).

Nie zrobione jeszcze: `docs/ARCHITEKTURA.md` — sekcja o SSE-KMS w TODO do
zaktualizowania (samo SSE-KMS już zrobione, patrz wpis wyżej; ewentualnie
opcjonalne „Default encryption" na buckecie jako druga linia obrony, jeszcze
nieustawione).
Sekcje 1–9 poniżej to **oryginalny plan docelowy** (jedno drzewo podmiotów,
brak publicznych URL, SSE-KMS) — przy dalszej pracy albo dociągamy obecny
model do tego planu, albo świadomie go uprościmy i zaktualizujemy ten
dokument.

---

## 1. Ustalenia (odpowiedzi na pytania projektowe)

| Temat | Decyzja |
|---|---|
| Osoby vs kategorie | **Jeden byt** — generyczne, zagnieżdżone drzewo „podmiotów" (self-FK), bez rozróżniania typu węzła. „Ja", „Mama", „Praca 2025-2026" to węzły tego samego drzewa |
| Pliki-dzieci pod plikiem | Self-FK na `files.parent_file_id` (mechanika jak wątki komentarzy) — niezależna od drzewa podmiotów |
| Status pliku | Reużyty 1:1 z istniejącego repo: `PENDING` (init, czeka na S3) → `COMPLETED` (S3 przyjęło) → `CONFIRMED` (przypisany do podmiotu) / `FAILED` |
| Upload | Frontend → S3 bezpośrednio (presigned), backend tylko `init` / `update` / `assign` |
| Szyfrowanie | S3 SSE-KMS, bucket w pełni prywatny (Block Public Access), brak publicznych URL |
| Podgląd | Endpoint generujący krótkoterminowy presigned GET (2–4 min, konfigurowalne), tylko inline |
| Pobieranie | Redirect na krótkoterminowy presigned GET z `Content-Disposition: attachment` |
| Gwarancje | Opcjonalne `guarantee_start_date` / `guarantee_end_date` na pliku, filtrowalne po statusie aktywności |
| Rola | Superadmin dla wszystkiego (aplikacja jednoosobowa, jak `rentals`) |

## 2. Analiza wymagań (z rozmowy z użytkownikiem)

1. Pliki są dziś ręcznie trzymane per osoba/temat (np. „Ja": świadectwo
   pracy, faktura AGD, pdf, wideo; „Mama": faktury, dokumenty Tauron).
   Niektóre pliki mają logiczne „dzieci" (np. „dokument Tauron" →
   „dokument Tauron dwa/trzy") — to osobna relacja od przypisania do
   osoby/kategorii, zrealizowana jako self-FK na tabeli plików.
2. Podział na „osobę" i „kategorię" (np. „Praca 2025-2026") okazał się w
   rozmowie tym samym pojęciem — użytkownik chce jednego, zagnieżdżonego
   drzewa węzłów, po którym rozpina pliki, niezależnie czy węzeł
   koncepcyjnie reprezentuje osobę czy temat/projekt.
3. Pliki mają być w S3, zaszyfrowane, bez publicznego URL — dostęp tylko
   przez czasowe, podpisane linki (podgląd 2–4 min, pobieranie krócej,
   z wymuszonym pobraniem).
4. Upload idzie bezpośrednio z frontendu do S3 (nie przez backend) — backend
   tylko wystawia dane do uploadu i odbiera potwierdzenia statusu. Wzorzec
   `init`/`update` użytkownik ma już wdrożony w innym projekcie (sklepowym)
   — tu przenosimy tę samą semantykę statusów, ale zastępujemy sklepową
   relację `categories`/`directory` drzewem podmiotów odpowiednim dla tej
   domeny.
5. Potrzebne funkcje: wyszukiwarka po nazwie pliku, pobieranie plików per
   osoba/rodzina (czyli po węźle i jego poddrzewie), sortowanie/filtrowanie
   po dacie dodania (od–do), opcjonalne śledzenie gwarancji (data
   początku/końca, widoczność czy aktywna).
6. Klasyczny CRUD pod frontend: create/read/update/delete zarówno dla
   węzłów, jak i plików, z usuwaniem rekordu w bazie **i** obiektu w S3.

## 3. Model danych — `database/psql/models/files.py`

Konwencja jak w `rentals.py`: UUID PK (`uuid.uuid4`), `created_at` /
`updated_at` jako `DateTime(timezone=True)` + `server_default=func.now()`,
FK domyślnie `ondelete="RESTRICT"` (chyba że opisano inaczej),
`passive_deletes=True` na relacjach ORM.

### 3.1 `files_nodes` — drzewo podmiotów (osoba lub kategoria — ten sam byt)

| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| name | String(255), not null | „Ja", „Mama", „Praca 2025-2026" |
| parent_id | UUID FK → files_nodes.id, nullable | NULL = węzeł najwyższego poziomu |
| description | String, nullable | |
| is_active | Boolean, default True | |
| created_at / updated_at | DateTime tz | |

`UniqueConstraint(parent_id, name)` — bez duplikatów nazw w obrębie tego
samego rodzica. Usuwanie: `RESTRICT`, gdy węzeł ma dzieci-węzły lub
przypisane pliki (spójne z `rentals`) — trzeba najpierw opróżnić/przenieść
zawartość.

### 3.2 `files` — plik (adaptacja modelu podanego przez użytkownika)

| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| node_id | UUID FK → files_nodes.id, **nullable** | NULL dopóki plik nie jest `CONFIRMED` (widok „plików osieroconych") |
| parent_file_id | UUID FK → files.id, nullable, **ondelete CASCADE** | plik-dziecko (np. „dokument Tauron dwa/trzy"); jedyne miejsce z CASCADE — dzieci nie mają sensu bez rodzica; usunięcie obiektów S3 dzieci obsługiwane w warstwie service |
| original_name | String(255), not null | nazwa wyświetlana użytkownikowi |
| s3_key | String(512), not null | klucz obiektu w buckecie — **brak** kolumny `url` (brak publicznych URL) |
| size | BigInteger, not null | |
| mime_type | String(255), nullable | |
| file_type | Enum(`FileType`), not null | patrz 3.3 |
| status | Enum(`FileStatus`), not null, default `PENDING` | patrz 3.3 |
| description | String, nullable | notatka użytkownika |
| guarantee_start_date | Date, nullable | |
| guarantee_end_date | Date, nullable | |
| created_at / updated_at | DateTime tz | |

`CHECK (status != 'confirmed' OR node_id IS NOT NULL)` — pilnowanie na
poziomie bazy niezmiennika „confirmed ⇒ przypisany do węzła". Indeksy:
`status`, `file_type`, `node_id`, `parent_file_id`; wyszukiwanie po
`original_name` na start przez zwykły B-tree + `ILIKE` (jeśli wyszukiwarka
zwolni przy większej liczbie plików, do rozważenia indeks `pg_trgm`).

### 3.3 Enumy i słowniki rozszerzeń (`database/psql/models/files.py`)

```python
class FileStatus(str, enum.Enum):
    PENDING = "pending"      # init, presigned URL wydany, czeka na upload
    COMPLETED = "completed"  # S3 potwierdziło przyjęcie obiektu
    CONFIRMED = "confirmed"  # przypisany do węzła (node_id ustawiony)
    FAILED = "failed"


class FileType(str, enum.Enum):
    PHOTO = "photo"
    GIF = "gif"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"    # NOWE względem wzorca z drugiego repo — pdf/doc/xls itp.


ALLOWED_EXTENSIONS: dict[FileType, set[str]] = {
    FileType.PHOTO: {".jpg", ".jpeg", ".png", ".webp"},
    FileType.GIF: {".gif"},
    FileType.VIDEO: {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"},
    FileType.AUDIO: {".mp3", ".wav", ".aac", ".m4a"},
    FileType.DOCUMENT: {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".odt"},
}

MAX_FILE_SIZE_BYTES: dict[FileType, int] = {
    FileType.PHOTO: 25 * 1024 * 1024,
    FileType.GIF: 25 * 1024 * 1024,
    FileType.VIDEO: 500 * 1024 * 1024,
    FileType.AUDIO: 100 * 1024 * 1024,
    FileType.DOCUMENT: 25 * 1024 * 1024,
}
```

Klucz S3: `files/{file_id}/{sanitized_original_name}` — stabilny, nie zależy
od `node_id` (który może się zmienić przy re-assign pliku do innego węzła).

## 4. Serwis S3 — `core/service/files/s3.py` (+ `core/service/files/response.py`)

Czysta logika/integracja zewnętrzna (bez ORM, tuple pattern), analogicznie
do `core/service/rentals/calculation.py`:

1. `build_s3_key(file_id, original_name) -> str`.
2. `generate_upload_presigned_post(key, mime_type, max_size) -> dict` —
   presigned POST z wymuszonym SSE-KMS (`x-amz-server-side-encryption`,
   `x-amz-server-side-encryption-aws-kms-key-id` w conditions), limit
   rozmiaru per `FileType` z `MAX_FILE_SIZE_BYTES`.
3. `generate_get_presigned_url(key, expires_seconds, disposition) -> str` —
   wspólna funkcja dla podglądu (`disposition="inline"`) i pobierania
   (`disposition="attachment"`, `response-content-disposition` override).
4. `head_object(key) -> bool | dict` — weryfikacja istnienia obiektu (użycie
   w `update`, opcjonalnie, jeśli chcemy backend-side potwierdzenia zamiast
   ufać wyłącznie frontendowi).
5. `delete_object(key)` — użycie w handlerze `delete` (plik i jego dzieci).

**Ważne wyjaśnienie architektoniczne**: presigned GET wystawiony dla obiektu
zaszyfrowanego SSE-KMS działa dla dowolnego posiadacza linku bez własnych
poświadczeń AWS, ponieważ S3 sprawdza uprawnienia (`kms:Decrypt`)
*podpisującego* (czyli roli/klucza backendu) w momencie **generowania**
podpisu, a nie w momencie, gdy ktoś ten link faktycznie otwiera. To trzeba
mieć jasno w głowie przy konfiguracji IAM/KMS policy przy wdrożeniu —
backend musi mieć `kms:Decrypt` i `kms:GenerateDataKey` na kluczu, viewer
(np. przeglądarka) — nic.

### 4.1 Nowa konfiguracja — `config/settings.py`

Wzorcem `Field(validation_alias=...)`, czytane z `env/{ENV_MODE}.env`:

| Pole | Uwagi |
|---|---|
| `aws_region` | region bucketu |
| `s3_bucket_name` | |
| `s3_kms_key_id` | ARN/ID klucza CMK do SSE-KMS |
| `aws_access_key_id` / `aws_secret_access_key` | opcjonalne — tylko dev/local; w prod preferowana rola IAM instancji (uwaga w kodzie, nie wymuszać wymagalności pola) |
| `file_preview_url_expire_seconds` | domyślnie `180` (3 min, w widełkach 2–4 min ustalonych z użytkownikiem) |
| `file_download_url_expire_seconds` | domyślnie `60` |
| `file_upload_url_expire_seconds` | domyślnie `900` (czas na wykonanie presigned POST po `init`) |

## 5. Przepływ pracy użytkownika (endpointy)

Rola: **superadmin** dla wszystkiego (aplikacja jednoosobowa, jak
`rentals`). Wszystkie URL-e jako stałe w `api/routers.py`, wzorzec
`/files/{zasób}/{akcja}`.

### 5.1 Węzły (drzewo osób/kategorii) — etap 3

| Endpoint | Opis |
|---|---|
| `POST /files/nodes/create` | nowy węzeł (opcjonalny `parent_id`) |
| `GET /files/nodes/collection` | drzewo (opcjonalnie od `parent_id`) |
| `GET /files/nodes/one/{node_id}` | szczegóły + breadcrumb |
| `PUT /files/nodes/update/{node_id}` | zmiana nazwy / opisu / rodzica |
| `DELETE /files/nodes/delete/{node_id}` | `RESTRICT`, gdy ma dzieci-węzły lub przypisane pliki |

### 5.2 Upload — status flow reużyty z istniejącego systemu (etap 4)

| Endpoint | Opis |
|---|---|
| `POST /files/init` | `{original_name, size, mime_type, file_type}` → `File(status=PENDING)` + presigned POST do S3 |
| `PUT /files/update/{file_id}` | frontend potwierdza zakończenie uploadu → backend (opcjonalnie `head_object`) → `COMPLETED` / `FAILED` |

### 5.3 Przypisanie, metadane, usuwanie — nowe w tym module (etap 5)

| Endpoint | Opis |
|---|---|
| `PUT /files/assign/{file_id}` | `{node_id, parent_file_id?}`, wymaga `status=COMPLETED` → ustawia `node_id` (+ opcjonalnie `parent_file_id`), `status=CONFIRMED` |
| `PUT /files/metadata/{file_id}` | edycja `original_name` / `description` / dat gwarancji / `node_id` / `parent_file_id` |
| `DELETE /files/delete/{file_id}` | kasuje rekord + obiekt S3; kaskadowo dzieci (`parent_file_id`) + ich obiekty S3 |

### 5.4 Odczyt, wyszukiwanie, podgląd, pobieranie (etap 6–7)

| Endpoint | Opis |
|---|---|
| `GET /files/collection` | filtry: `node_id` (opcja rekurencyjna po poddrzewie — `WITH RECURSIVE`), `search` (ILIKE po `original_name`), `created_at_from` / `created_at_to`, `status`, `file_type`, `guarantee_status` (`active`\|`expired`\|`none`); sortowanie po `created_at` / `original_name` / `size` |
| `GET /files/one/{file_id}` | szczegóły + lista plików-dzieci + breadcrumb węzła |
| `GET /files/unassigned` | skrót: `status=completed AND node_id IS NULL` (pliki „osierocone", czekające na przypisanie) |
| `GET /files/preview/{file_id}` | presigned GET `inline`, ważny `file_preview_url_expire_seconds`; tylko dla `COMPLETED`/`CONFIRMED` |
| `GET /files/download/{file_id}` | 302 → presigned GET `attachment`, ważny `file_download_url_expire_seconds` |

### 5.5 Gwarancje (etap 8)

| Endpoint | Opis |
|---|---|
| `GET /files/collection?guarantee_status=active` | filtr istniejącego endpointu — aktywne gwarancje |
| `GET /files/guarantees/expiring` | (opcjonalnie) lista gwarancji kończących się w najbliższych N dniach |

Audyt (`create_logs_psql`): sloty `files:create_node`, `files:init`,
`files:update_status`, `files:assign`, `files:update_metadata`,
`files:delete_node`, `files:delete_file`. Rate limity: `RATE_LIMIT_READ` na
GET, `RATE_LIMIT_WRITE` na resztę — wzorzec z `rentals`.

## 6. Etapy implementacji

| Etap | Zakres | Warstwy |
|---|---|---|
| **1. Modele + migracja** | `database/psql/models/files.py` (`files_nodes`, `files`, enumy), rejestracja w `models/__init__.py`, migracja Alembic z `CHECK` constraint | database |
| **2. Konfiguracja + serwis S3** | `config/settings.py` (nowe pola), `core/service/files/s3.py` (boto3, presign POST/GET, SSE-KMS, head/delete) — testowalne bez DB | service |
| **3. Węzły CRUD** | pełny stos (`_psql` + response dataclass → handler z audytem → schema walidacji → endpoint) dla `nodes` | wszystkie |
| **4. Upload + status flow** | `init`, `update` — reużycie wzorca z istniejącego repo, dopasowane do tej domeny | wszystkie |
| **5. Assign + metadane + delete** | `assign`, `metadata`, `delete` (kaskada S3 dla dzieci) | wszystkie |
| **6. Odczyt: collection / one / unassigned** | filtry, wyszukiwarka, sortowanie, rekursja po poddrzewie węzła | wszystkie |
| **7. Preview + download** | presigned GET, redirecty, walidacja statusu (`COMPLETED`/`CONFIRMED`) | wszystkie |
| **8. Gwarancje** | filtr `guarantee_status` w `collection`, ewentualnie `GET /files/guarantees/expiring` | service + handler |
| **9. Testy + dokumentacja** | testy wg wzorca (`Test{Action}FilesPsql`, fabryki w `helper.py`, mock S3 przez `moto`/`pytest-mock`), tag Swagger „Files" w `config/swagger_description/tags.py`, aktualizacja `ARCHITEKTURA.md` (lista domen) | tests/docs |

Kolejność świadoma: etap 2 (serwis S3) przed etapem 4 (upload), bo `init`
zależy od `generate_upload_presigned_post`; etap 3 może iść równolegle z 2.

## 7. Decyzje projektowe i przyszłe rozszerzenia

- **Brak publicznych URL** — zawsze presigned, krótkoterminowe (podgląd
  2–4 min, pobieranie krócej); brak kolumny `url` w tabeli `files`.
- **`CASCADE` tylko na `parent_file_id`** — świadomy, jedyny wyjątek od
  domyślnego `RESTRICT` używanego wszędzie indziej w bazie: dziecko-plik nie
  ma sensu bez rodzica.
- **Stabilny klucz S3 po `file_id`** — nie zależy od `node_id`, więc
  przetrwa re-assign pliku do innego węzła bez przenoszenia obiektu w S3.
- **Niezmiennik `confirmed ⇒ node_id NOT NULL`** wymuszony `CHECK`-em w
  bazie, nie tylko w warstwie service — spójność nawet przy ręcznych
  operacjach na DB.
- **Jedno drzewo zamiast Osoba + Kolekcja** — uproszczenie ustalone w
  rozmowie: „Ja", „Mama", „Praca 2025-2026" to węzły tego samego,
  generycznego drzewa (`files_nodes`), bez pola rozróżniającego typ węzła.
- **Waluta pominięta** — moduł nie liczy żadnych kwot (w przeciwieństwie do
  `rentals`), więc brak potrzeby na `Numeric`/zaokrąglenia.

### Pomysły na przyszłość (nieobowiązkowe, do rozważenia później)

- Soft-delete / kosz z retencją przed fizycznym usunięciem obiektu z S3
  (bezpieczniej niż natychmiastowy hard-delete).
- Skanowanie antywirusowe po uploadzie (S3 event → Lambda/ClamAV) zanim
  plik będzie można przełączyć w `CONFIRMED`.
- Powiadomienie / lista „gwarancje wygasające w ciągu najbliższych 30 dni".
- Wolne tagi (relacja many-to-many) jako uzupełnienie drzewa węzłów, gdyby
  jeden plik miał pasować do kilku „szufladek" naraz.
- Statystyki zużycia miejsca (suma `size`) per węzeł i globalnie.
- Jawne wersjonowanie tego samego pliku (kolejny upload = nowy rekord z
  `parent_file_id` na poprzednią wersję) — częściowo już pokryte mechaniką
  plików-dzieci, ale można to nazwać wprost (`kind=version` vs
  `kind=attachment` na `parent_file_id`).
- OCR / pełnotekstowe przeszukiwanie treści PDF — osobny etap w przyszłości.
