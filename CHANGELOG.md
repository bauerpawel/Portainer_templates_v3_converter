# Changelog

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

Format bazuje na [Keep a Changelog](https://keepachangelog.com/pl/1.0.0/),
a projekt stosuje [Semantic Versioning](https://semver.org/lang/pl/).

## [2.0.0] - 2026-01-10

### Dodano

#### 🔧 System Patch-ów (Główna Nowa Funkcja)
- **Kompleksowy system patch-ów** do modyfikacji szablonów v3 bez edycji kodu
- **PatchLoader** (`patches/_patch_loader.py`) - core implementacja systemu
  - Ładowanie patch files w porządku numerycznym (0001, 0002...)
  - Walidacja struktury JSON patch files
  - Detekcja i reporting błędów
- **Trzy typy operacji:**
  - `UPDATE` - zmiana istniejących szablonów z zaawansowanym filtrowaniem
  - `ADD` - dodanie nowych szablonów
  - `REMOVE` - usunięcie szablonów
- **Zaawansowane filtrowanie:**
  - Dokładne dopasowanie pól (name, id, title)
  - Wsparcie dla wildcards w image field (`zadam/*`)
  - Case-insensitive matching dla string pól
- **Scalanie pól listowych:**
  - Unikanie duplikatów przy UPDATE na env, volumes, labels, categories
  - Inteligentna fuzja zmian
- **Automatyczne ładowanie patchy-ów** podczas konwersji
- **Statystyki patch-ów** z raportem operacji
- **Plik TEMPLATE.json** - szablon do tworzenia nowych patch files
- **Przykładowy patch** (0001-update-trilium-docker-image.json)

#### 📚 Dokumentacja
- **Pełna dokumentacja systemu patch-ów** (PL: `patches/README.md`)
- **English documentation** (EN: `patches/README_EN.md`)
  - Praktyczne przykłady dla każdego typu operacji
  - Instrukcja krok po kroku jak dodać nowy patch
  - Rozbudowane FAQ (8 pytań)
  - Best practices (7 zasad)
  - Checklist przed commitem (9 walidacji)

#### 🛠️ Integracja i Konfiguracja
- **requirements.txt** - zależności projektu:
  - `requests>=2.31.0` - HTTP requests
  - `jsonschema>=4.20.0` - JSON Schema validation
  - `colorama>=0.4.6` - opcjonalnie, kolory w CLI
- **Integracja PatchLoader z konwerterem:**
  - Automatyczne inicjalizowanie patch systemu
  - Ładowanie patchy-ów z folderu `patches/`
  - Aplikowanie patchy-ów do v3 templates po konwersji
  - Error handling i reporting

#### 🎯 Konwerter
- **Nowy krok w workflow konwersji** - aplikowanie patchy-ów
- **Metoda `apply_patches()`** w PortainerTemplateConverter
- **Wyświetlanie statystyk patchy-ów** w podsumowaniu
- **Wsparcie dla patch systemu** w help message
- **Aktualizacja wersji** na 2.0.0

### Zmieniono
- Rozszerzony output konwertera z informacją o patchy-ach
- Ulepszone statystyki konwersji z sekcją patchy-ów
- Help message w CLI z informacją o nowych możliwościach
- Workflow konwersji: v2 -> v3 -> **[APPLY PATCHES]** -> validate -> save

### Bezpieczeństwo
- Walidacja struktury patch files
- Sprawdzanie unikalności ID przy ADD operacji
- Error handling dla malformed JSON
- Try-catch wokół aplikowania każdej operacji
- Logging błędów z opcją pomijania problematycznych patchy-ów

### Dokumentacja
- Zaktualizowany README.md (główny)
- Nowe sekcje w dokumentacji:
  - Patch System Overview
  - Getting Started with Patches
  - Contributing Patches
  - Troubleshooting

---

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

---

## Legenda

- **Dodano** - nowe funkcjonalności
- **Zmieniono** - zmiany istniejących funkcjonalności
- **Naprawiono** - naprawy błędów
- **Usunięto** - usunięte funkcjonalności
- **Bezpieczeństwo** - ulepszenia bezpieczeństwa
- **Dokumentacja** - zmiany w dokumentacji

## Linki do Release'ów

[2.0.0]: https://github.com/bauerpawel/Portainer_templates_v3_converter/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/bauerpawel/Portainer_templates_v3_converter/releases/tag/v1.0.0

## Wersje Przyszłe

### [2.1.0] - Planowane
- Wsparcie dla warunkowych patch-ów (np. `if` conditions)
- CLI do zarządzania patch-ami (listing, validation, applying)
- Test coverage dla patch systemu (unit tests)
- Performance optimization dla dużych zbiorów szablonów
- Wsparcie dla dry-run mode (podgląd zmian bez aplikowania)

### [3.0.0] - Przyszłość
- Rewrite na async/await
- Support dla custom validators
- Integration z GitHub API (automatyczne PR reviews)
- Web UI do zarządzania patch-ami
- Database backend dla tracking zmian

## Jak Zgłaszać Problemy

Jeśli napotkasz problem, otwórz issue na: https://github.com/bauerpawel/Portainer_templates_v3_converter/issues

Proszę zawierać:
- Wersję programu (`python portainer_converter.py --version`)
- Polecenie które zostało wykonane
- Pełny output błędu
- System operacyjny i wersję Pythona

## Licencja

Projekt jest udostępniany na licencji MIT. Patrz [LICENSE](LICENSE) po szczegóły.
