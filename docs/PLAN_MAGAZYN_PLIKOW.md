# Plan implementacji: magazyn plików (domena `files`)

> Plan powstał na bazie rozmowy z użytkownikiem (prywatny, szyfrowany magazyn
> plików per osoba/kategoria, S3 + presigned URL) oraz istniejącego w innym
> repo użytkownika systemu `File` (init/update statusu uploadu). Wszystkie
> nowe funkcjonalności przechodzą przez standardowe warstwy: endpoint →
> handler → service / `_psql`, tuple pattern `(result, error, ok)`, audyt
> `create_logs_psql`, rate limiting, testy wg wzorca — zob. `ARCHITEKTURA.md`.
> Wzorzec strukturalny tego dokumentu: `PLAN_ROZLICZENIA_MIESZKAN.md`.

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
