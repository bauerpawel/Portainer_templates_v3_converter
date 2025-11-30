#!/usr/bin/env python3
"""
Portainer Templates Converter v2 -> v3
Aplikacja konwertująca szablony Portainer z formatu v2 na v3

Użycie:
    python portainer_converter.py [--url URL] [--output PLIK]
    python portainer_converter.py --help

Przykłady:
    # Domyślna konwersja
    python portainer_converter.py

    # Z własnym URL
    python portainer_converter.py --url "https://example.com/templates.json"

    # Z własną nazwą pliku wyjściowego
    python portainer_converter.py --output "my_templates_v3.json"

Autor: Python Script dla konwersji szablonów Portainer
Data: 2025-08-27
Wersja: 1.0.0
"""

import json
import requests
import argparse
import sys
import os
from typing import Dict, Any, Optional
from datetime import datetime
from jsonschema import validate, ValidationError, Draft7Validator

class PortainerTemplateConverter:
    """Klasa do konwersji szablonów Portainer z v2 na v3"""

    def __init__(self):
        self.default_v2_url = "https://raw.githubusercontent.com/Lissy93/portainer-templates/refs/heads/main/templates.json"
        self.default_output_file = "templates_v3_converted.json"
        self.schema_file = os.path.join(os.path.dirname(__file__), "schema_v3.json")
        self.schema = None

        # Lista popularnych źródeł szablonów Portainer v2
        self.known_sources = {
            'lissy93': {
                'name': 'Lissy93 Templates',
                'url': 'https://raw.githubusercontent.com/Lissy93/portainer-templates/refs/heads/main/templates.json',
                'description': 'Duża kolekcja ponad 470 szablonów aplikacji'
            },
            'portainer-official': {
                'name': 'Portainer Official',
                'url': 'https://raw.githubusercontent.com/portainer/templates/master/templates-2.0.json',
                'description': 'Oficjalne szablony od zespołu Portainer'
            },
            'selfhosted': {
                'name': 'SelfHosted.show',
                'url': 'https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/master/Template/portainer-v2.json',
                'description': 'Szablony dla aplikacji self-hosted'
            },
            'technorabilia': {
                'name': 'Technorabilia',
                'url': 'https://raw.githubusercontent.com/technorabilia/portainer-templates/main/lsio/templates/templates.json',
                'description': 'Szablony bazujące na obrazach LinuxServer.io'
            }
        }

    def load_schema(self) -> Dict[str, Any]:
        """
        Ładuje JSON Schema dla Portainer v3 templates
        """
        if self.schema is not None:
            return self.schema

        try:
            with open(self.schema_file, 'r', encoding='utf-8') as f:
                self.schema = json.load(f)
            return self.schema
        except FileNotFoundError:
            print(f"⚠️  Ostrzeżenie: Plik schema nie został znaleziony: {self.schema_file}")
            print("   Walidacja JSON Schema zostanie pominięta")
            return None
        except json.JSONDecodeError as e:
            print(f"⚠️  Ostrzeżenie: Błąd parsowania schema: {e}")
            print("   Walidacja JSON Schema zostanie pominięta")
            return None

    def download_v2_templates(self, url: str, source_name: str = None) -> Optional[Dict[str, Any]]:
        """
        Pobiera szablon v2 z podanego URL
        """
        source_label = f" ({source_name})" if source_name else ""
        print(f"📥 Pobieranie szablonu v2 z: {url}{source_label}")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            if str(data.get('version')) != '2':
                print(f"⚠️  Ostrzeżenie: Oczekiwano wersji '2', znaleziono '{data.get('version')}'")

            templates_count = len(data.get('templates', []))
            print(f"✅ Pobrano {templates_count} szablonów{source_label}")
            return data

        except requests.RequestException as e:
            print(f"⚠️  Błąd pobierania pliku{source_label}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"⚠️  Błąd parsowania JSON{source_label}: {e}")
            return None

    def download_multiple_sources(self, urls: list) -> list:
        """
        Pobiera szablony z wielu źródeł
        Zwraca listę tupli (url, data)
        """
        print(f"📥 Pobieranie szablonów z {len(urls)} źródeł...")
        print()

        results = []
        for i, url in enumerate(urls, 1):
            # Sprawdzamy czy to znane źródło
            source_name = None
            for key, source in self.known_sources.items():
                if source['url'] == url:
                    source_name = source['name']
                    break

            data = self.download_v2_templates(url, source_name)
            if data:
                results.append((url, data))
            print()

        print(f"✅ Pobrano dane z {len(results)}/{len(urls)} źródeł")
        return results

    def merge_templates(self, sources_data: list) -> Dict[str, Any]:
        """
        Scala szablony z wielu źródeł i usuwa duplikaty
        sources_data: lista tupli (url, data)

        Duplikaty są wykrywane na podstawie kombinacji:
        - name (nazwa)
        - image (obraz Docker)
        """
        print("🔄 Scalanie szablonów z wielu źródeł...")

        all_templates = []
        seen_templates = {}  # Klucz: (name, image), wartość: template
        stats = {
            'total_before': 0,
            'total_after': 0,
            'duplicates_removed': 0,
            'sources': {}
        }

        # Zbieramy wszystkie szablony
        for url, data in sources_data:
            templates = data.get('templates', [])
            stats['total_before'] += len(templates)
            stats['sources'][url] = len(templates)

            for template in templates:
                # Tworzymy klucz unikalności
                name = template.get('name', '').lower().strip()
                image = template.get('image', '').lower().strip()

                if not name or not image:
                    # Jeśli brak name lub image, dodajemy zawsze
                    all_templates.append(template)
                    continue

                key = (name, image)

                if key in seen_templates:
                    # Duplikat znaleziony
                    stats['duplicates_removed'] += 1

                    # Możemy scalić informacje (np. kategorie)
                    existing = seen_templates[key]

                    # Scalamy kategorie
                    existing_cats = set(existing.get('categories', []))
                    new_cats = set(template.get('categories', []))
                    merged_cats = list(existing_cats | new_cats)
                    if merged_cats:
                        existing['categories'] = merged_cats

                    # Wybieramy dłuższy opis jeśli dostępny
                    if len(template.get('description', '')) > len(existing.get('description', '')):
                        existing['description'] = template['description']
                else:
                    # Nowy szablon
                    seen_templates[key] = template
                    all_templates.append(template)

        stats['total_after'] = len(all_templates)

        print(f"✅ Scalono szablony:")
        print(f"   • Szablony przed scaleniem: {stats['total_before']}")
        print(f"   • Szablony po scaleniu: {stats['total_after']}")
        print(f"   • Usunięto duplikatów: {stats['duplicates_removed']}")

        # Tworzymy połączony obiekt v2
        merged_data = {
            'version': '2',
            'templates': all_templates
        }

        return merged_data, stats

    def convert_template(self, template: Dict[str, Any], template_id: int) -> Dict[str, Any]:
        """
        Konwertuje pojedynczy szablon z v2 na v3

        Główne zmiany:
        - Dodanie pola 'id' (unikalny identyfikator)
        - Dodanie pola 'labels' (pusta lista domyślnie)
        - Migracja 'restart_policy' do labels jako com.docker.compose.restart-policy
        - Usunięcie pola 'platform'
        """
        v3_template = {}

        # Dodajemy unikalny ID - kluczowa różnica w v3
        v3_template['id'] = template_id

        # Pola do skopiowania bez zmian
        fields_to_copy = [
            'categories', 'description', 'env', 'image', 'logo',
            'maintainer', 'name', 'ports', 'title', 'type', 'volumes',
            'note', 'repository', 'hostname', 'command', 'network_mode',
            'privileged', 'interactive', 'administrator_only'
        ]

        for field in fields_to_copy:
            if field in template:
                value = template[field]
                # Fix None values for required string fields
                if field == 'description' and (value is None or value == ''):
                    # Use title as fallback for description if available
                    value = template.get('title', 'No description available')
                v3_template[field] = value

        # Dodajemy pole labels - nowe w v3
        # Migrujemy restart_policy z v2 do labels w v3
        v3_template['labels'] = []

        if 'restart_policy' in template and template['restart_policy']:
            v3_template['labels'].append({
                'name': 'com.docker.compose.restart-policy',
                'value': template['restart_policy']
            })

        # Pola usuwane w v3 (nie kopiujemy):
        # - 'restart_policy': polityka restartowania - w v3 migrowana do labels
        # - 'platform': informacja o platformie - nie jest używana w v3

        return v3_template

    def convert_v2_to_v3(self, v2_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Główna funkcja konwersji z v2 na v3
        """
        print("🔄 Rozpoczynanie konwersji v2 -> v3...")

        v3_data = {
            "version": "3",
            "templates": []
        }

        # Konwertujemy każdy szablon
        templates = v2_data.get('templates', [])
        for idx, template in enumerate(templates, 1):
            converted_template = self.convert_template(template, idx)
            v3_data['templates'].append(converted_template)

        print(f"✅ Konwersja zakończona! Przekonwertowano {len(templates)} szablonów")
        return v3_data

    def save_v3_templates(self, v3_data: Dict[str, Any], filename: str) -> str:
        """
        Zapisuje szablon v3 do pliku JSON z ładnym formatowaniem
        """
        print(f"💾 Zapisywanie do pliku: {filename}")

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(v3_data, f, indent=2, ensure_ascii=False)

            file_size = round(len(json.dumps(v3_data)) / 1024, 2)
            print(f"✅ Plik zapisany pomyślnie: {filename} ({file_size} KB)")
            return filename

        except IOError as e:
            print(f"❌ Błąd zapisywania pliku: {e}")
            sys.exit(1)

    def validate_with_json_schema(self, v3_data: Dict[str, Any]) -> bool:
        """
        Walidacja z użyciem oficjalnego JSON Schema
        """
        print("🔍 Walidacja z JSON Schema...")

        schema = self.load_schema()
        if schema is None:
            print("⚠️  Pomijam walidację JSON Schema (brak pliku schema)")
            return True

        try:
            # Tworzymy validator
            validator = Draft7Validator(schema)

            # Zbieramy wszystkie błędy
            errors = list(validator.iter_errors(v3_data))

            if errors:
                print(f"❌ Znaleziono {len(errors)} błędów walidacji JSON Schema:")
                # Pokazujemy do 10 najważniejszych błędów
                for i, error in enumerate(errors[:10], 1):
                    # Tworzymy ścieżkę do błędu
                    path = " -> ".join(str(p) for p in error.path) if error.path else "root"
                    print(f"   {i}. {path}: {error.message}")

                if len(errors) > 10:
                    print(f"   ... i {len(errors) - 10} więcej błędów")
                return False

            print("✅ Walidacja JSON Schema zakończona pomyślnie")
            return True

        except Exception as e:
            print(f"❌ Błąd podczas walidacji JSON Schema: {e}")
            return False

    def validate_v3_format(self, v3_data: Dict[str, Any]) -> bool:
        """
        Kompleksowa walidacja formatu v3
        Łączy walidację JSON Schema z dodatkowymi sprawdzeniami
        """
        print("🔍 Walidacja formatu v3...")

        # 1. Walidacja z JSON Schema (jeśli dostępna)
        schema_valid = self.validate_with_json_schema(v3_data)

        # 2. Podstawowa walidacja struktury
        if str(v3_data.get('version')) != '3':
            print("❌ Nieprawidłowa wersja (oczekiwano '3')")
            return False

        templates = v3_data.get('templates', [])
        if not templates:
            print("❌ Brak szablonów")
            return False

        # 3. Dodatkowe sprawdzenia biznesowe
        print("🔍 Dodatkowe sprawdzenia biznesowe...")
        warnings = []
        errors = []

        for i, template in enumerate(templates, 1):
            # Sprawdzenie starych pól z v2
            old_fields = ['restart_policy', 'platform']
            for field in old_fields:
                if field in template:
                    warnings.append(f"Szablon {i} ('{template.get('title', 'unknown')}'): zawiera stare pole '{field}' z v2")

            # Sprawdzenie czy labels jest listą (jeśli istnieje)
            if 'labels' in template and not isinstance(template['labels'], list):
                errors.append(f"Szablon {i} ('{template.get('title', 'unknown')}'): pole 'labels' powinno być listą")

        # Pokazujemy ostrzeżenia
        if warnings:
            print(f"⚠️  Znaleziono {len(warnings)} ostrzeżeń:")
            for warning in warnings[:5]:
                print(f"   • {warning}")
            if len(warnings) > 5:
                print(f"   ... i {len(warnings) - 5} więcej ostrzeżeń")

        # Pokazujemy błędy
        if errors:
            print(f"❌ Znaleziono {len(errors)} błędów:")
            for error in errors[:10]:
                print(f"   • {error}")
            if len(errors) > 10:
                print(f"   ... i {len(errors) - 10} więcej błędów")
            return False

        if not schema_valid:
            return False

        print("✅ Walidacja zakończona pomyślnie")
        return True

    def show_statistics(self, v2_data: Dict[str, Any], v3_data: Dict[str, Any]):
        """
        Pokazuje statystyki konwersji
        """
        print("📊 Statystyki konwersji:")

        v2_templates = v2_data.get('templates', [])
        v3_templates = v3_data.get('templates', [])

        print(f"   • Szablony źródłowe (v2): {len(v2_templates)}")
        print(f"   • Szablony docelowe (v3): {len(v3_templates)}")

        # Statystyki typów
        type_stats = {}
        for template in v3_templates:
            template_type = template.get('type', 'unknown')
            type_stats[template_type] = type_stats.get(template_type, 0) + 1

        print("   • Typy szablonów:")
        type_names = {1: 'Kontenery', 2: 'Stosy Swarm', 3: 'Stosy Compose'}
        for t_type, count in sorted(type_stats.items()):
            type_name = type_names.get(t_type, f'Typ {t_type}')
            print(f"     - {type_name}: {count}")

        # Statystyki kategorii
        categories = {}
        for template in v3_templates:
            for category in template.get('categories', []):
                categories[category] = categories.get(category, 0) + 1

        if categories:
            print(f"   • Top 5 kategorii:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"     - {category}: {count}")

    def list_sources(self):
        """
        Wyświetla listę dostępnych źródeł szablonów
        """
        print("📚 Dostępne źródła szablonów Portainer:")
        print("="*50)
        for key, source in self.known_sources.items():
            print(f"\n🔹 {source['name']} (klucz: {key})")
            print(f"   URL: {source['url']}")
            print(f"   Opis: {source['description']}")
        print()

    def run(self, source_url: Optional[str] = None, output_file: Optional[str] = None,
            multiple_sources: Optional[list] = None, all_sources: bool = False):
        """
        Główna metoda uruchamiająca cały proces konwersji

        Args:
            source_url: pojedynczy URL źródłowy
            output_file: plik wyjściowy
            multiple_sources: lista URL-i lub kluczy źródeł
            all_sources: użyj wszystkich znanych źródeł
        """
        print("🚀 Portainer Templates Converter v2 -> v3")
        print("="*50)
        print(f"⏰ Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Używamy domyślnych wartości jeśli nie podano
        output_file = output_file or self.default_output_file

        try:
            merge_stats = None

            # Określamy źródła do pobrania
            if all_sources:
                # Pobieramy wszystkie znane źródła
                urls = [source['url'] for source in self.known_sources.values()]
                sources_data = self.download_multiple_sources(urls)

                if not sources_data:
                    print("❌ Nie udało się pobrać żadnego źródła")
                    sys.exit(1)

                v2_data, merge_stats = self.merge_templates(sources_data)

            elif multiple_sources:
                # Pobieramy z wielu źródeł
                urls = []
                for source in multiple_sources:
                    # Sprawdzamy czy to klucz znanego źródła
                    if source in self.known_sources:
                        urls.append(self.known_sources[source]['url'])
                    else:
                        # Traktujemy jako URL
                        urls.append(source)

                sources_data = self.download_multiple_sources(urls)

                if not sources_data:
                    print("❌ Nie udało się pobrać żadnego źródła")
                    sys.exit(1)

                v2_data, merge_stats = self.merge_templates(sources_data)

            else:
                # Pojedyncze źródło
                source_url = source_url or self.default_v2_url
                v2_data = self.download_v2_templates(source_url)

                if not v2_data:
                    print("❌ Nie udało się pobrać szablonów")
                    sys.exit(1)

            print()

            # 2. Konwersja v2 -> v3
            v3_data = self.convert_v2_to_v3(v2_data)

            # 3. Walidacja
            if not self.validate_v3_format(v3_data):
                print("❌ Walidacja nie powiodła się")
                sys.exit(1)

            # 4. Zapisywanie do pliku
            output_filename = self.save_v3_templates(v3_data, output_file)

            # 5. Statystyki
            print()
            self.show_statistics(v2_data, v3_data)

            print()
            print("📋 Podsumowanie:")

            if merge_stats:
                print(f"   • Źródła: {len(merge_stats['sources'])} różnych źródeł")
                for url, count in merge_stats['sources'].items():
                    # Znajdź nazwę źródła jeśli znane
                    source_name = None
                    for source in self.known_sources.values():
                        if source['url'] == url:
                            source_name = source['name']
                            break
                    label = f" ({source_name})" if source_name else ""
                    print(f"     - {count} szablonów{label}")
                print(f"   • Duplikaty usunięte: {merge_stats['duplicates_removed']}")
            else:
                print(f"   • Źródło: {source_url}")

            print(f"   • Wersja źródłowa: v{v2_data.get('version')}")
            print(f"   • Wersja docelowa: v{v3_data.get('version')}")
            print(f"   • Liczba szablonów: {len(v3_data['templates'])}")
            print(f"   • Plik wyjściowy: {output_filename}")
            print()
            print("🎉 Konwersja zakończona pomyślnie!")
            print()
            print("💡 Jak używać:")
            print(f"   1. Skopiuj plik '{output_filename}' na serwer")
            print("   2. W Portainer przejdź do Settings -> App Templates")
            print("   3. Wklej URL do pliku lub użyj lokalnego pliku")
            print("   4. Zapisz ustawienia i ciesz się szablonami v3!")

        except KeyboardInterrupt:
            print("\n❌ Operacja anulowana przez użytkownika")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Nieoczekiwany błąd: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

def main():
    """
    Funkcja główna obsługująca argumenty z linii poleceń
    """
    parser = argparse.ArgumentParser(
        description="Konwertuje szablony Portainer z formatu v2 na v3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przykłady użycia:
  %(prog)s
    Konwersja z domyślnego URL do domyślnego pliku

  %(prog)s --url "https://example.com/templates.json"
    Konwersja z własnego URL

  %(prog)s --output "my_templates_v3.json"
    Konwersja do własnego pliku

  %(prog)s --sources lissy93 portainer-official
    Scala szablony z wielu źródeł (po kluczu)

  %(prog)s --sources "https://example.com/templates.json" lissy93
    Scala szablony z URL i znanego źródła

  %(prog)s --all-sources
    Scala szablony ze wszystkich znanych źródeł

  %(prog)s --list-sources
    Wyświetl listę dostępnych źródeł

Główne różnice v2 -> v3:
  • Dodano pole 'id' (unikalny identyfikator)
  • Dodano pole 'labels' (etykiety Docker)
  • Zmigrowano 'restart_policy' do labels jako 'com.docker.compose.restart-policy'
  • Usunięto pole 'platform'
  • Zmieniono wersję na '3'

Scalanie źródeł:
  • Duplikaty są wykrywane po kombinacji (name, image)
  • Kategorie z duplikatów są scalane
  • Wybierany jest dłuższy opis
        """
    )

    parser.add_argument(
        '--url', '-u',
        help='URL do pliku templates.json w formacie v2 '
             '(domyślnie: szablony Lissy93)',
        metavar='URL'
    )

    parser.add_argument(
        '--output', '-o',
        help='Nazwa pliku wyjściowego (domyślnie: templates_v3_converted.json)',
        metavar='PLIK'
    )

    parser.add_argument(
        '--sources', '-s',
        nargs='+',
        help='Lista źródeł do scalenia (klucze lub URL-e)',
        metavar='ŹRÓDŁO'
    )

    parser.add_argument(
        '--all-sources', '-a',
        action='store_true',
        help='Użyj wszystkich znanych źródeł szablonów'
    )

    parser.add_argument(
        '--list-sources', '-l',
        action='store_true',
        help='Wyświetl listę dostępnych źródeł'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Portainer Templates Converter 2.0'
    )

    args = parser.parse_args()

    # Inicjalizujemy konwerter
    converter = PortainerTemplateConverter()

    # Jeśli --list-sources, tylko wyświetlamy źródła
    if args.list_sources:
        converter.list_sources()
        return

    # Sprawdzamy konflikty argumentów
    if args.url and (args.sources or args.all_sources):
        print("❌ Błąd: Nie można użyć --url razem z --sources lub --all-sources")
        sys.exit(1)

    # Uruchamiamy konwersję
    converter.run(
        source_url=args.url,
        output_file=args.output,
        multiple_sources=args.sources,
        all_sources=args.all_sources
    )

if __name__ == "__main__":
    main()
