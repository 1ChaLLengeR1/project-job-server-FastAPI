TAGS_METADATA = [
    {
        "name": "Auth",
        "description": "Logowanie i automatyczne logowanie (JWT: access + refresh token).",
    },
    {
        "name": "Calendar",
        "description": "Kalendarz pracy - generowanie dni, kolekcja i statystyki.",
    },
    {
        "name": "Calendar/Conditions",
        "description": "Warunki pracy (norma godzin, stawka godzinowa) obowiązujące od danej daty.",
    },
    {
        "name": "Calendar/Days",
        "description": "Aktualizacja pojedynczych dni pracy, przeliczanie stawek i wynagrodzenia.",
    },
    {
        "name": "Tasks",
        "description": "Zadania - CRUD, oznaczanie wykonania i statystyki.",
    },
    {
        "name": "OutstandingMoney",
        "description": "Listy zaległych płatności i ich pozycje.",
    },
    {
        "name": "Logs",
        "description": "Logi aplikacji - zapis i przegląd.",
    },
    {
        "name": "FuelCalculator",
        "description": "Kalkulator kosztów paliwa.",
    },
    {
        "name": "Patryk/Calculator",
        "description": "Kalkulator pracy (klucze i obliczenia).",
    },
    {
        "name": "Rentals/Apartments",
        "description": "Rozliczenia mieszkań - słownik mieszkań.",
    },
    {
        "name": "Rentals/Tenants",
        "description": "Rozliczenia mieszkań - słownik najemców.",
    },
    {
        "name": "Rentals/Tenancies",
        "description": "Rozliczenia mieszkań - najmy (najemca + mieszkanie + czynsz), z historią.",
    },
    {
        "name": "Rentals/CostTypes",
        "description": "Rozliczenia mieszkań - słownik rodzajów kosztów.",
    },
    {
        "name": "Rentals/ApartmentCosts",
        "description": "Rozliczenia mieszkań - koszty przypisane do mieszkań, z historią stawek.",
    },
    {
        "name": "Rentals/Meters",
        "description": "Rozliczenia mieszkań - słownik liczników.",
    },
    {
        "name": "Rentals/Periods",
        "description": "Rozliczenia mieszkań - okresy rozliczeniowe: create/collection/one/update/delete, "
        "preview (na żywo, bez zapisu), close/reopen.",
    },
    {
        "name": "Rentals/MeterReadings",
        "description": "Rozliczenia mieszkań - odczyty liczników w ramach okresu rozliczeniowego.",
    },
    {
        "name": "Rentals/Settlements",
        "description": "Rozliczenia mieszkań - zapisane snapshoty rozliczeń okresu (po close).",
    },
    {
        "name": "Rentals/Beneficiaries",
        "description": "Rozliczenia mieszkań - podział rodzinny: beneficjenci i snapshoty ich rozliczeń.",
    },
    {
        "name": "Rentals/AllocationRules",
        "description": "Rozliczenia mieszkań - podział rodzinny: reguły podziału kosztów (z historią).",
    },
    {
        "name": "Contact",
        "description": "Formularz kontaktowy - publiczny create (token X-Contact-Token, "
        "podpisywany wspólnym sekretem per aplikacja) + obsługa zgłoszeń przez superadmina.",
    },
    {
        "name": "Files",
        "description": "Magazyn plików - init uploadu (presigned PUT do S3), potwierdzenie/edycja "
        "statusu i nazwy, listowanie i usuwanie (rekord + obiekt S3).",
    },
]
