# Plan implementacji: rozliczenia mieszkań (domena `rentals`)

> Plan powstał na bazie analizy ręcznych dokumentów `docs/Obliczenia*.txt`
> (miesięczne rozliczenia 2021–2026, od 1 do 4 mieszkań) oraz ARCHITEKTURA.md.
> Wszystkie nowe funkcjonalności przechodzą przez standardowe warstwy:
> endpoint → handler → service / `_psql`, tuple pattern `(result, error, ok)`,
> audyt `create_logs_psql`, rate limiting, testy wg wzorca.

---

## 1. Ustalenia (odpowiedzi na pytania projektowe)

| Temat | Decyzja |
|---|---|
| Podział rodzinny (Ja/Ojciec/Mama) | **W zakresie od razu** — tabele beneficjentów + reguły podziału |
| Historia 2021–2026 | Struktura pozwala wpisywać dowolne miesiące wstecz, **bez importera** plików txt |
| Cena prądu za kWh | **Liczona z rachunku** (kwota rachunku / suma zużycia kWh), z możliwością **ręcznego nadpisania** stawki |
| Licznik nadrzędny + błąd licznika | **Automatycznie**: flaga `is_master` (zużycie = własny odczyt − suma pozostałych), błąd licznika głównego liczony przez system, proponowany równy podział na mieszkania z możliwością korekty |
| Pliki / zdjęcia liczników | Poza zakresem (na razie nic nie podpinamy) |

## 2. Jak działa proces ręczny (z analizy `Obliczenia*.txt`)

1. **Liczniki per mieszkanie** — stan prądu (kWh) i wody (m³) „Ostatnio"/„Teraz";
   zużycie = różnica.
2. **Licznik główny prądu** — różnica porównywana z sumą podliczników →
   „Błąd_między_licznikami" rozdzielany na mieszkania (np. +4 kWh, +1 kWh każdemu).
3. **Stawka prądu zmienna w czasie** (0,80 → 0,95 → 1,05 zł/kWh); w nowszych
   plikach liczona wprost: `899,48 zł / 855,73 kWh = 1,05 zł/kWh`.
4. **Woda 9 zł/m³**; licznik wody „Pokoju Łukasza" jest **nadrzędny** —
   jego zużycie = jego odczyt − zużycie pozostałych mieszkań.
5. **Koszty stałe różne per mieszkanie**: przesył (0/9 zł), śmieci
   (kwotowo 27/54 zł albo **35 zł × liczba osób**), internet (0/30/60 zł), garaż (200 zł).
6. **Korekty jednorazowe**: nadpłata −19 zł, zaległe media +260 zł, rabat −200 zł.
7. **Czynsz deklarowany** per mieszkanie/najem (1000, 1100 zł…), najemcy
   zmieniają się w czasie (Ania → Witek itd.).
8. **Podział rodzinny** — czynsze i media rozdzielane między Ja/Ojca/Mamę:
   - czynsz z jednego mieszkania dzielony kwotowo (Dudzik: Ja 100, Ojciec 1100, Mama 100),
   - cały prąd → Ja (płaci rachunek), woda/śmieci/internet → Mama, garaż → Ojciec,
   - stałe pozycje osobiste: podatek (Ja −90, Ojciec −270, Mama +360), telefon (Ja −25, Mama +25).
9. Kwoty składników zaokrąglane do pełnych złotych (`~`).

## 3. Model danych — tabele (`database/psql/models/rentals.py`)

Wszystkie tabele: UUID PK (`uuid.uuid4`), `created_at`/`updated_at`
`DateTime(timezone=True)` + `server_default=func.now()`. Kwoty: `Numeric(10, 2)`,
odczyty liczników: `Numeric(12, 3)` (woda ma 3 miejsca po przecinku).

### 3.1 Słowniki i konfiguracja

**`rentals_apartments`** — mieszkania
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| name | String(255), unique, not null | np. „Pokój Państwa Dudzik" |
| description | String, nullable | |
| is_active | Boolean, default True | |

**`rentals_tenants`** — najemcy
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| first_name | String(255), not null | |
| last_name | String(255), nullable | |
| note | String, nullable | telefon, uwagi |
| is_active | Boolean, default True | |

**`rentals_tenancies`** — przypisanie najemcy do mieszkania + czynsz (z historią)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| apartment_id | UUID FK → rentals_apartments | |
| tenant_id | UUID FK → rentals_tenants | |
| rent_amount | Numeric(10,2), not null | czynsz deklarowany dla tego najmu |
| persons_count | Integer, default 1 | do kosztów „per osoba" (śmieci 35 zł × os.) |
| start_date | Date, not null | |
| end_date | Date, nullable | NULL = najem trwa |

Walidacja w service: najmy jednego mieszkania nie mogą się nakładać.
Historia najmów = historia czynszów i najemców per mieszkanie.

**`rentals_cost_types`** — słownik rodzajów kosztów
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| name | String(255), unique, not null | „śmieci", „internet", „przesył", „garaż"… |
| charge_type | String, not null | `fixed` \| `per_person` |
| is_active | Boolean, default True | |

(Prąd i woda **nie** są w słowniku — liczone z liczników i stawek okresu.)

**`rentals_apartment_costs`** — koszty przypisane do mieszkania (z historią stawek)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| apartment_id | UUID FK | |
| cost_type_id | UUID FK | |
| amount | Numeric(10,2), not null | dla `per_person` — stawka za osobę |
| start_date | Date, not null | zmiana internetu 30 → 60 zł = nowy rekord |
| end_date | Date, nullable | |

**`rentals_meters`** — liczniki
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| apartment_id | UUID FK, **nullable** | NULL = licznik główny budynku |
| media_type | String, not null | `electricity` \| `water` |
| is_master | Boolean, default False | licznik nadrzędny: zużycie = odczyt − suma zużyć pozostałych mieszkań (przypadek wody Łukasza) |
| name | String(255), nullable | |
| is_active | Boolean, default True | |

### 3.2 Rozliczenia miesięczne

**`rentals_billing_periods`** — okres rozliczeniowy (miesiąc)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| period_month | Date, unique, not null | zawsze 1. dzień miesiąca |
| status | String, not null | `draft` \| `closed` |
| electricity_bill_amount | Numeric(10,2), nullable | kwota rachunku globalnego („Do zapłaty: 899,48") |
| electricity_rate | Numeric(10,4), nullable | zł/kWh — wyliczona lub nadpisana |
| electricity_rate_is_manual | Boolean, default False | True = user nadpisał stawkę |
| water_rate | Numeric(10,2), not null, default 9.00 | zł/m³, edytowalna per okres |
| note | String, nullable | |

**`rentals_meter_readings`** — odczyty liczników w okresie
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| period_id | UUID FK → rentals_billing_periods | |
| meter_id | UUID FK → rentals_meters | |
| previous_value | Numeric(12,3), not null | „Ostatnio" — prefill z poprzedniego okresu |
| current_value | Numeric(12,3), not null | „Teraz" |
| error_correction | Numeric(12,3), default 0 | „Błąd_Licznika" w kWh — propozycja z podziału błędu głównego, edytowalna |

Unikalność: `(period_id, meter_id)`.

**`rentals_settlements`** — rozliczenie mieszkania w okresie (snapshot przy zamknięciu)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| period_id | UUID FK | |
| apartment_id | UUID FK | |
| tenancy_id | UUID FK, nullable | kto wynajmował (NULL = pustostan, jak „Mieszkanie_4") |
| rent_amount | Numeric(10,2), default 0 | snapshot czynszu z najmu |
| electricity_consumption | Numeric(12,3) | kWh po korekcie błędu / odjęciu podrzędnych |
| electricity_cost | Numeric(10,2) | zaokrąglone do pełnych zł |
| water_consumption | Numeric(12,3) | m³ |
| water_cost | Numeric(10,2) | zaokrąglone do pełnych zł |
| total_media_amount | Numeric(10,2) | media + koszty stałe + korekty (odpowiednik „Razem" z plików) |
| total_amount | Numeric(10,2) | total_media_amount + rent_amount |
| note | String, nullable | |

Unikalność: `(period_id, apartment_id)`.

**`rentals_settlement_items`** — pozycje rozliczenia (koszty stałe + korekty)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| settlement_id | UUID FK | |
| cost_type_id | UUID FK, nullable | NULL = korekta ręczna |
| name | String(255), not null | snapshot nazwy („śmieci", „zaległe media", „nadpłata") |
| kind | String, not null | `fixed_cost` \| `adjustment` |
| amount | Numeric(10,2), not null | może być ujemna (nadpłata −19, rabat −200) |

### 3.3 Podział rodzinny

**`rentals_beneficiaries`** — członkowie rodziny
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| name | String(255), unique, not null | „Ja", „Ojciec", „Mama" |
| is_active | Boolean, default True | |

**`rentals_allocation_rules`** — reguły podziału (z historią obowiązywania)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| beneficiary_id | UUID FK | |
| apartment_id | UUID FK, nullable | NULL = dotyczy wszystkich mieszkań / nie dotyczy mieszkania |
| component | String, not null | `rent` \| `electricity` \| `water` \| `cost_type` \| `recurring` |
| cost_type_id | UUID FK, nullable | wymagane dla `component=cost_type` (śmieci, internet, garaż…) |
| mode | String, not null | `fixed_amount` \| `full` (cała kwota składnika) |
| amount | Numeric(10,2), nullable | wymagane dla `fixed_amount` i `recurring`; może być ujemna |
| start_date | Date, not null | |
| end_date | Date, nullable | |

Przykłady odwzorowania z plików:
- czynsz Dudzik → Ja `rent/fixed_amount/100`, Ojciec `rent/fixed_amount/1100`, Mama `rent/fixed_amount/100`;
- cały prąd → Ja: `electricity/full`, apartment_id NULL;
- woda, śmieci, internet → Mama: `water/full` + `cost_type/full` (śmieci, internet), apartment_id NULL;
- garaż → Ojciec: `cost_type/full` (garaż);
- podatek: Ja `recurring/−90`, Ojciec `recurring/−270`, Mama `recurring/+360`;
- telefon: Ja `recurring/−25`, Mama `recurring/+25`.

**`rentals_beneficiary_settlements`** — wynik podziału per okres
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| period_id | UUID FK | |
| beneficiary_id | UUID FK | |
| total_amount | Numeric(10,2), not null | |

Unikalność: `(period_id, beneficiary_id)`.

**`rentals_beneficiary_settlement_items`** — pozycje podziału (audytowalność jak w ręcznych notatkach)
| Kolumna | Typ | Uwagi |
|---|---|---|
| id | UUID PK | |
| beneficiary_settlement_id | UUID FK | |
| description | String(255), not null | np. „czynsz Dudzik", „woda — Pokój Łukasza", „podatek" |
| amount | Numeric(10,2), not null | |
| rule_id | UUID FK, nullable | źródłowa reguła |
| settlement_id | UUID FK, nullable | źródłowe rozliczenie mieszkania |

## 4. Logika obliczeń — `core/service/rentals/calculation.py`

Czysta logika (bez DB), tuple pattern, jawne argumenty:

1. **Zużycie zwykłego licznika**: `current − previous + error_correction`.
2. **Licznik nadrzędny (`is_master`)**: `własna różnica − suma różnic pozostałych
   liczników tego samego medium` (przypadek wody Łukasza; działa też dla prądu —
   wariant z `Obliczenia_1`, gdzie licznik Łukasza był głównym).
3. **Błąd licznika głównego prądu**: `różnica licznika głównego − suma zużyć
   podliczników`; propozycja: równy podział na mieszkania (zaokrąglony),
   zapisywany w `error_correction` odczytów — edytowalny przed zamknięciem.
4. **Stawka prądu**: `electricity_bill_amount / suma zużyć kWh (po korektach)`,
   zaokrąglona do 4 miejsc; jeżeli `electricity_rate_is_manual=True` — brana
   stawka wpisana ręcznie.
5. **Koszt prądu/wody per mieszkanie**: `zużycie × stawka`, zaokrąglenie do
   pełnych złotych (half-up — jak `~` w notatkach).
6. **Koszty stałe**: aktywne `rentals_apartment_costs` na dzień okresu;
   `per_person` → `stawka × persons_count` z aktywnego najmu.
7. **Rozliczenie mieszkania**: media + koszty stałe + korekty = `total_media_amount`;
   `+ czynsz` = `total_amount`.
8. **Podział rodzinny**: dla każdego beneficjenta suma pozycji z aktywnych reguł
   (`fixed_amount` → kwota reguły; `full` → pełna kwota składnika z rozliczeń;
   `recurring` → kwota reguły niezależna od mieszkań).
   Suma reguł `fixed_amount` dla czynszu nie musi się równać czynszowi —
   walidacja tylko ostrzega (preview), nie blokuje.

## 5. Przepływ pracy użytkownika (endpointy)

Rola: **superadmin** dla wszystkiego (aplikacja jednoosobowa). Wszystkie URL-e
jako stałe w `api/routers.py`, wzorzec `/rentals/{zasób}/{akcja}`.

### 5.1 CRUD słowników (etap 2)

| Zasób | Endpointy |
|---|---|
| apartments | create / collection / one / update / delete |
| tenants | create / collection / one / update / delete |
| tenancies | create / collection (per mieszkanie, z historią) / update / close (ustaw end_date) / delete |
| cost_types | create / collection / update / delete |
| apartment_costs | create / collection (per mieszkanie) / update / close / delete |
| meters | create / collection / update / delete |
| beneficiaries | create / collection / update / delete |
| allocation_rules | create / collection / update / close / delete |

Delete: fizyczny tylko gdy brak powiązań (FK), inaczej `is_active=False`/`end_date`.

### 5.2 Okres rozliczeniowy (etap 3–4)

1. `POST /rentals/periods/create` — nowy okres (miesiąc, kwota rachunku prądu,
   stawka wody); tworzy szkielet odczytów z prefill `previous_value`
   z poprzedniego okresu.
2. `PUT /rentals/periods/readings/{period_id}` — hurtowy upsert odczytów
   („Teraz" per licznik + ewentualne ręczne `error_correction`).
3. `GET /rentals/periods/preview/{period_id}` — wyliczenie na żywo:
   zużycia, błąd licznika głównego + propozycja podziału, stawka zł/kWh,
   rozliczenia per mieszkanie, podział rodzinny. Nic nie zapisuje.
4. `PUT /rentals/periods/update/{period_id}` — korekta kwot rachunku / stawek /
   ręcznej stawki prądu; dodawanie korekt jednorazowych per mieszkanie.
5. `POST /rentals/periods/close/{period_id}` — zapis snapshotów:
   `rentals_settlements` + items, `rentals_beneficiary_settlements` + items,
   `status=closed`.
6. `POST /rentals/periods/reopen/{period_id}` — usuwa snapshoty, wraca do `draft`
   (przydatne przy wpisywaniu historii).
7. `GET /rentals/periods/collection` + `GET /rentals/periods/one/{period_id}` —
   historia i szczegóły (zamknięty okres czyta snapshoty, draft liczy preview).

Sloty audytu: `rentals:{akcja}` (np. `rentals:create_apartment`,
`rentals:close_period`). Rate limity: `RATE_LIMIT_READ` na GET,
`RATE_LIMIT_WRITE` na resztę.

## 6. Etapy implementacji

| Etap | Zakres | Warstwy |
|---|---|---|
| **1. Modele + migracja** | `database/psql/models/rentals.py` (14 tabel), migracja Alembic, rejestracja w `models/__init__.py` | database |
| **2. Słowniki CRUD** | apartments, tenants, tenancies, cost_types, apartment_costs, meters, beneficiaries, allocation_rules — pełny stos: `_psql` + response dataclasses → handlery (audyt) → schemas (walidacja) → endpointy (swagger, rate limit) → rejestracja w `api/api.py` | wszystkie |
| **3. Serwis obliczeń** | `core/service/rentals/calculation.py` + `response.py` — czysta logika z sekcji 4, pisana TDD (testy jednostkowe bez DB) | service |
| **4. Okresy rozliczeniowe** | periods: create (z prefill odczytów), readings upsert, preview, update, close, reopen, collection/one | wszystkie |
| **5. Podział rodzinny** | wyliczanie w preview + snapshot przy close; podgląd historyczny per beneficjent | service + handler |
| **6. Testy + dokumentacja** | testy `_psql` i endpointów wg wzorca (`Test{Action}{Domain}Psql`, fabryki w helper.py), tag Swagger „Rentals" w `config/swagger_description/tags.py`, aktualizacja ARCHITEKTURA.md (lista domen) | tests/docs |

Kolejność świadoma: etap 3 przed 4, bo preview okresu zależy od serwisu obliczeń;
etap 2 można równolegle z 3.

## 7. Decyzje projektowe i przyszłe rozszerzenia

- **Zaokrąglanie**: składniki (prąd, woda) do pełnych złotych half-up —
  zgodnie z `~` w notatkach. Stawka zł/kWh z 4 miejscami.
- **Snapshot przy zamknięciu**: zamknięty okres nie zmienia się przy edycji
  słowników (czynsze/stawki/reguły mają daty obowiązywania, a settlements
  przechowują skopiowane kwoty) — kluczowe przy wpisywaniu historii.
- **Pustostany**: settlement bez `tenancy_id` (jak „Mieszkanie_4" — same śmieci).
- **Waluta**: PLN, bez tabeli walut.
- **Poza zakresem (na później)**: załączniki/zdjęcia liczników, importer plików
  txt, raporty roczne/podatkowe, powiadomienia dla najemców.
