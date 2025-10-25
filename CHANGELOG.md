# Changelog

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

Format bazuje na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
a projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

## [1.0.0] - 2025-10-25

### Dodano
- Podstawowa konwersja szablonów Portainer z formatu v2 na v3
- Automatyczne generowanie unikalnych ID dla szablonów
- Dodawanie pola `labels` do szablonów v3
- Migracja `restart_policy` z v2 do labels jako `com.docker.compose.restart-policy`
- Walidacja z oficjalnym JSON Schema dla Portainer v3 templates
- Obsługa wielu źródeł szablonów z możliwością scalania
- Automatyczne wykrywanie i usuwanie duplikatów przy scalaniu źródeł
- Lista predefiniowanych popularnych źródeł szablonów:
  - Lissy93 Templates (470+ szablonów)
  - Portainer Official
  - SelfHosted.show
  - Technorabilia
- GitHub Actions workflow do automatycznej konwersji szablonów
- Szczegółowe statystyki konwersji (typy, kategorie, duplikaty)
- Pełna dokumentacja w README.md
- Przykłady użycia w USAGE_EXAMPLES.md
- Testy jednostkowe (test_converter.py)

### Zmieniono
- Usuwanie pól `restart_policy` i `platform` ze szablonów (niekompatybilne z v3)

### Naprawiono
- Prawidłowa walidacja struktury szablonów v3
- Obsługa błędów przy pobieraniu zdalnych źródeł

[1.0.0]: https://github.com/bauerpawel/Portainer_templates_v3_converter/releases/tag/v1.0.0
