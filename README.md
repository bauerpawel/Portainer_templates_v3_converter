# Portainer Templates Converter v2 → v3

🔄 **Aplikacja Python do konwersji szablonów Portainer z formatu v2 na v3**

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

## Instalacja

1. **Sklonuj lub pobierz pliki:**
   ```bash
   # Opcja 1: Pobierz główny plik
   wget https://example.com/portainer_converter.py

   # Opcja 2: Lub skopiuj kod do pliku portainer_converter.py
   ```

2. **Zainstaluj wymagane biblioteki:**
   ```bash
   pip install requests
   ```

## Użycie

### Podstawowa konwersja
```bash
python portainer_converter.py
```
Pobiera szablony z domyślnego źródła i zapisuje jako `templates_v3_converted.json`

### Własny URL źródłowy
```bash
python portainer_converter.py --url "https://your-custom-url.com/templates.json"
```

### Własny plik wyjściowy
```bash
python portainer_converter.py --output "my_templates_v3.json"
```

### Pełna konfiguracja
```bash
python portainer_converter.py \
  --url "https://raw.githubusercontent.com/example/templates.json" \
  --output "custom_templates_v3.json"
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

1. **Pobieranie szablonu v2** z podanego URL
2. **Konwersja każdego szablonu:**
   - Dodanie unikalnego pola `id`
   - Dodanie pustego pola `labels`
   - Usunięcie pól `restart_policy` i `platform`
   - Kopiowanie pozostałych pól
3. **Walidacja** poprawności formatu v3
4. **Zapisanie** do pliku JSON z ładnym formatowaniem

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
- [ ] Migracja etykiet z pola `restart_policy`
- [ ] Walidacja z oficjalnym schema JSON
- [ ] Obsługa dodatkowych źródeł szablonów
- [ ] GUI (graficzny interfejs użytkownika)

## Licencja

Apache-2.0 license - zobacz szczegóły w pliku LICENSE.

## Autor

Aplikacja stworzona dla konwersji szablonów Portainer v2 → v3.

---
⭐ Jeśli aplikacja Ci pomogła, zostaw gwiazdkę!
