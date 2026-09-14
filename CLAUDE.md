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
