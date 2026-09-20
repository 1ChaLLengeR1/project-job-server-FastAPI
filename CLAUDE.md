# CLAUDE.md

Zasady pracy Claude w tym repo.

## Git

- **Nigdy nie rób `git commit` samodzielnie.** Commity robi wyłącznie
  użytkownik. Jeśli użytkownik prosi o `git add .` (albo dowolną inną
  pojedynczą komendę git), wykonaj tylko to, o co poprosił — nie idź dalej
  do commita "przy okazji".
- Jeśli użytkownik jednak explicite poprosi o zrobienie commita, rób go
  **bez żadnego podpisu/atrybucji AI** (bez `Co-Authored-By: Claude...`,
  bez `Claude-Session`, bez wzmianki o Claude/Sonnet/AI w treści) — commit
  ma wyglądać tak, jakby zrobił go sam użytkownik.

## `__init__.py`

- W plikach `__init__.py` nigdy nie pisz logiki ani mechanizmów. Mają
  zawierać wyłącznie importy — i to tylko wtedy, gdy są faktycznie
  potrzebne w runtime (np. `database/psql/models/__init__.py` importuje
  moduły modeli, żeby zarejestrować metadane pod Alembica). W pozostałych
  przypadkach `__init__.py` zostaje puste.

## Nie odpalaj testów ani komend `make` samodzielnie

Nie uruchamiaj samodzielnie:
- testów (`pytest`, `python manage.py test` itp.),
- żadnych targetów z `makefile` (`make restart_db`, `make migrate` itp.).

Użytkownik robi to sam, ręcznie. Pisz kod/migracje/testy, ale ich
wykonanie zostaw użytkownikowi.

## Swagger musi być aktualizowany przy każdej zmianie modelu API

W tym repo `summary=`/`description=` siedzą wprost w dekoratorze
(`@router.get(...)`/`@router.post(...)`) w każdym pliku
`api/endpoints/{domain}/...py` — nie ma osobnych stałych
`*_SUMMARY`/`*_DESCRIPTION` ani `router.add_api_operation(...)`.
(`config/swagger_description/summary.py` to tylko auto-generowana tabelka
„ile endpointów per tag" przy starcie, `app.py` to opis całej appki —
obie niezwiązane z dokumentacją per-endpoint.)

Za każdym razem, gdy zmieniasz payload/response endpointu (nowe/usunięte
pole, zmiana typu, nowy query/path param, zmiana zachowania) —
zaktualizuj `summary=`/`description=` w tym samym pliku endpointu, w tym
samym PR, nie później. Dotyczy to też response models: jeśli dodajesz
nowe zagnieżdżone dane (np. nowy obiekt w response), sprawdź czy schema w
`api/schemas/{domain}/response.py` faktycznie je zagnieżdża (nested
`BaseModel`, nie płaski string/ID tam, gdzie sensowniejsza byłaby pełna
struktura) — i dociągnij nesting, jeśli go brakuje, zamiast zostawiać
response płaskim "na razie". Query/path party dokumentuj przez
`Query(..., description=...)`/`Path(..., description=...)`, nie goły typ
bez opisu.

Po każdej takiej zmianie przejrzyj pokrewne endpointy w tej samej domenie
(np. wszystkie endpointy `file`, albo `collection`/`one` w kilku
domenach), czy nie mają tego samego braku — łatwo zmienić jeden endpoint
i zapomnieć o analogicznym w drugim (user/admin, collection/one itp.).
