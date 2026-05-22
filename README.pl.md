# Portainer Templates Converter v2 → v3

🔄 **Aplikacja Python do konwersji szablonów Portainer z formatu v2 na v3**

[🇬🇧 English version](README.md) | **🇵🇱 Wersja polska**

---

## Użyj gotowego pliku w Portainer → Settings → App Templates, wklej ten adres:
```bash
https://raw.githubusercontent.com/bauerpawel/Portainer_templates_v3_converter/main/templates_v3_converted.json
 ```
## Opis

Ta aplikacja automatycznie konwertuje szablony aplikacji Portainer z formatu v2 na v3, który jest kompatybilny z najnowszymi wersjami Portainer.io.

### Główne różnice między formatami:

| Cecha             | Format v2             | Format v3         |
|-------------------|-----------------------|-------------------|
| Wersja            | `"version": "2"`      | `"version": "3"`  |
| ID szablonu       | ❌ Brak               | ✅ `"id": 123`    |
| Labels            | ❌ Brak               | ✅ `"labels": []` |
| Restart Policy    | ✅ `"restart_policy"` | ❌ Usunięte       |
| Platform          | ✅ `"platform"`       | ❌ Usunięte       |

## Wymagania

- Python 3.6+
- Biblioteka `requests`
- Biblioteka `jsonschema` (dla walidacji JSON Schema)

## Instalacja

1. **Sklonuj lub pobierz pliki:**
   ```bash
   # Opcja 1: Sklonuj repozytorium
   git clone https://github.com/bauerpawel/Portainer_templates_v3_converter.git
   cd Portainer_templates_v3_converter

   # Opcja 2: Pobierz główny plik
   wget https://raw.githubusercontent.com/bauerpawel/Portainer_templates_v3_converter/refs/heads/main/portainer_converter.py

   # Opcja 3: Lub skopiuj kod do pliku portainer_converter.py
   ```

2. **Zainstaluj wymagane biblioteki:**
   ```bash
   # Opcja 1: Z pliku requirements.txt (zalecane)
   pip install -r requirements.txt

   # Opcja 2: Manualnie
   pip install requests jsonschema
   ```

## Dostępne źródła szablonów

Aplikacja ma wbudowaną listę popularnych źródeł szablonów Portainer:

| Klucz | Nazwa | Opis |
|-------|-------|------|
| `lissy93` | Lissy93 Templates | Duża kolekcja ponad 470 szablonów aplikacji |
| `portainer-official` | Portainer Official | Oficjalne szablony od zespołu Portainer |
| `selfhosted` | SelfHosted.show | Szablony dla aplikacji self-hosted |
| `technorabilia` | Technorabilia | Szablony bazujące na obrazach LinuxServer.io |

### Wyświetlanie dostępnych źródeł
```bash
python portainer_converter.py --list-sources
```

## Użycie

### Podstawowa konwersja
```bash
python portainer_converter.py
```
Pobiera szablony z domyślnego źródła (Lissy93) i zapisuje jako `templates_v3_converted.json`

### Własny URL źródłowy
```bash
python portainer_converter.py --url "https://your-custom-url.com/templates.json"
```

### Własny plik wyjściowy
```bash
python portainer_converter.py --output "my_templates_v3.json"
```

### Scalanie wielu źródeł
```bash
# Scala dwa znane źródła (po kluczu)
python portainer_converter.py --sources lissy93 portainer-official

# Scala wszystkie znane źródła
python portainer_converter.py --all-sources

# Scala znane źródło z własnym URL
python portainer_converter.py --sources lissy93 "https://example.com/templates.json"
```

### Pełna konfiguracja
```bash
python portainer_converter.py \
  --sources lissy93 selfhosted technorabilia \
  --output "merged_templates_v3.json"
```

### Pomoc
```bash
python portainer_converter.py --help
```

## Przykład działania

```
🚀 Portainer Templates Converter v2 -> v3
==================================================
⏰ Start: 2025-08-27 12:00:00

📥 Pobieranie szablonu v2 z: https://raw.githubusercontent.com/...
✅ Pobrano 472 szablonów
🔄 Rozpoczynanie konwersji v2 -> v3...
✅ Konwersja zakończona! Przekonwertowano 472 szablonów
🔍 Walidacja formatu v3...
🔍 Walidacja z JSON Schema...
✅ Walidacja JSON Schema zakończona pomyślnie
🔍 Dodatkowe sprawdzenia biznesowe...
✅ Walidacja zakończona pomyślnie
💾 Zapisywanie do pliku: templates_v3_converted.json
✅ Plik zapisany pomyślnie: templates_v3_converted.json (1.2 MB)

📊 Statystyki konwersji:
   • Szablony źródłowe (v2): 472
   • Szablony docelowe (v3): 472
   • Typy szablonów:
     - Kontenery: 450
     - Stosy Swarm: 22
   • Top 5 kategorii:
     - Other: 89
     - Tools: 67
     - Video: 45
     - Music: 32
     - Books: 28

📋 Podsumowanie:
   • Źródło: https://raw.githubusercontent.com/Lissy93/portainer-templates/...
   • Wersja źródłowa: v2
   • Wersja docelowa: v3
   • Liczba szablonów: 472
   • Plik wyjściowy: templates_v3_converted.json

🎉 Konwersja zakończona pomyślnie!

💡 Jak używać:
   1. Skopiuj plik 'templates_v3_converted.json' na serwer
   2. W Portainer przejdź do Settings -> App Templates
   3. Wklej URL do pliku lub użyj lokalnego pliku
   4. Zapisz ustawienia i ciesz się szablonami v3!
```

## Jak używać w Portainer

1. **Uruchom konwersję:**
   ```bash
   python portainer_converter.py
   ```

2. **Przenieś plik na serwer web (opcjonalnie):**
   ```bash
   # Przykład - skopiuj na serwer Apache/Nginx
   cp templates_v3_converted.json /var/www/html/
   ```

3. **Skonfiguruj Portainer:**
   - Otwórz interfejs Portainer
   - Przejdź do **Settings** → **App Templates**
   - W polu **URL** wklej ścieżkę do pliku:
     ```
     https://twoj-serwer.com/templates_v3_converted.json
     ```
   - Lub dla pliku lokalnego:
     ```
     file:///ścieżka/do/templates_v3_converted.json
     ```
   - Kliknij **Save settings**

4. **Korzystaj z szablonów:**
   - Przejdź do **App Templates**
   - Szablony v3 powinny być teraz dostępne!

## Szczegóły techniczne

### Proces konwersji

1. **Pobieranie szablonów v2** z podanego URL (lub wielu źródeł)
2. **Scalanie źródeł** (jeśli wybrano wiele):
   - Pobieranie szablonów z wszystkich źródeł
   - Wykrywanie duplikatów po kombinacji `(name, image)`
   - Scalanie kategorii z duplikatów
   - Wybieranie dłuższego opisu
   - Usuwanie duplikatów
3. **Konwersja każdego szablonu:**
   - Dodanie unikalnego pola `id`
   - Dodanie pola `labels` z migracją `restart_policy`
   - Usunięcie pól `restart_policy` i `platform`
   - Kopiowanie pozostałych pól
4. **Walidacja** poprawności formatu v3:
   - Walidacja z oficjalnym JSON Schema (plik `schema_v3.json`)
   - Sprawdzenie wymaganych pól
   - Sprawdzenie typów danych
   - Dodatkowe sprawdzenia biznesowe (stare pola z v2, itp.)
5. **Zapisanie** do pliku JSON z ładnym formatowaniem

### Scalanie wielu źródeł

Przy scalaniu szablonów z wielu źródeł:

- **Wykrywanie duplikatów**: Szablony są porównywane po kombinacji pól `name` i `image` (bez rozróżniania wielkości liter)
- **Scalanie danych**: Gdy znaleziono duplikat:
  - Kategorie są łączone (unikalne wartości z obu źródeł)
  - Wybierany jest dłuższy opis
  - Zachowywane są inne pola z pierwszego wystąpienia
- **Statystyki**: Po scaleniu wyświetlane są statystyki pokazujące liczbę usuniętych duplikatów

### Walidacja JSON Schema

Aplikacja wykorzystuje oficjalne JSON Schema dla Portainer templates v3 (`schema_v3.json`), które zapewnia:

- **Automatyczną walidację struktury** - sprawdza czy wszystkie wymagane pola są obecne
- **Walidację typów danych** - weryfikuje czy pola mają poprawne typy (string, integer, array, itp.)
- **Walidację formatów** - sprawdza poprawność URL-i, wzorców portów, itp.
- **Szczegółowe komunikaty błędów** - dokładnie wskazuje co jest nieprawidłowe

Jeśli plik `schema_v3.json` nie jest dostępny, walidacja JSON Schema zostanie pominięta, ale podstawowa walidacja nadal będzie wykonana.

### Obsługiwane pola szablonów

#### Kopiowane bez zmian:
- `categories` - kategorie aplikacji
- `description` - opis aplikacji
- `env` - zmienne środowiskowe
- `image` - obraz Docker
- `logo` - logo aplikacji
- `maintainer` - opiekun szablonu
- `name` - nazwa aplikacji
- `ports` - porty do przekierowania
- `title` - tytuł szablonu
- `type` - typ szablonu (1=kontener, 2=stack)
- `volumes` - wolumeny
- `note` - dodatkowe informacje
- `repository` - repozytorium Git

#### Dodane w v3:
- `id` - unikalny identyfikator (liczba)
- `labels` - etykiety Docker (pusta lista)

#### Usunięte z v2:
- `restart_policy` - polityka restartowania
- `platform` - platforma (linux/windows)

## Rozwiązywanie problemów

### Błąd pobierania pliku
```
❌ Błąd pobierania pliku: HTTPSConnectionPool...
```
**Rozwiązanie:** Sprawdź połączenie internetowe i poprawność URL.

### Błąd parsowania JSON
```
❌ Błąd parsowania JSON: Expecting value...
```
**Rozwiązanie:** Upewnij się, że URL zawiera prawidłowy plik JSON.

### Błąd walidacji
```
❌ Błędy walidacji: Brak pola 'id' w szablonie 1
```
**Rozwiązanie:** To oznacza błąd w kodzie konwertera - zgłoś problem.

### Portainer nie widzi szablonów
1. Sprawdź czy plik jest dostępny pod podanym URL
2. Sprawdź czy Portainer ma dostęp do sieci/pliku
3. Sprawdź logi Portainer w poszukiwaniu błędów

## Wkład i rozwój

Zgłaszaj błędy i sugestie poprzez Issues. Pull requesty są mile widziane!

### TODO / Planowane funkcje:
- [ ] Obsługa szablonów Kubernetes
- [x] Migracja etykiet z pola `restart_policy`
- [x] Walidacja z oficjalnym schema JSON
- [x] Obsługa dodatkowych źródeł szablonów (scalanie wielu źródeł, usuwanie duplikatów)
- [ ] GUI (graficzny interfejs użytkownika)

## Licencja

Apache-2.0 license - zobacz szczegóły w pliku LICENSE.

## Autor

Aplikacja stworzona dla konwersji szablonów Portainer v2 → v3.

---
⭐ Jeśli aplikacja Ci pomogła, zostaw gwiazdkę!
