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
Wersja: 1.0
"""

import json
import requests
import argparse
import sys
from typing import Dict, Any, Optional
from datetime import datetime

class PortainerTemplateConverter:
    """Klasa do konwersji szablonów Portainer z v2 na v3"""

    def __init__(self):
        self.default_v2_url = "https://raw.githubusercontent.com/Lissy93/portainer-templates/refs/heads/main/templates.json"
        self.default_output_file = "templates_v3_converted.json"

    def download_v2_templates(self, url: str) -> Dict[str, Any]:
        """
        Pobiera szablon v2 z podanego URL
        """
        print(f"📥 Pobieranie szablonu v2 z: {url}")

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            if str(data.get('version')) != '2':
                print(f"⚠️  Ostrzeżenie: Oczekiwano wersji '2', znaleziono '{data.get('version')}'")

            templates_count = len(data.get('templates', []))
            print(f"✅ Pobrano {templates_count} szablonów")
            return data

        except requests.RequestException as e:
            print(f"❌ Błąd pobierania pliku: {e}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Błąd parsowania JSON: {e}")
            sys.exit(1)

    def convert_template(self, template: Dict[str, Any], template_id: int) -> Dict[str, Any]:
        """
        Konwertuje pojedynczy szablon z v2 na v3

        Główne zmiany:
        - Dodanie pola 'id' (unikalny identyfikator)
        - Dodanie pola 'labels' (pusta lista domyślnie)
        - Usunięcie pól 'restart_policy' i 'platform'
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
                v3_template[field] = template[field]

        # Dodajemy puste pole labels - nowe w v3
        # Może być używane dla Docker labels
        v3_template['labels'] = []

        # Pola usuwane w v3 (nie kopiujemy):
        # - 'restart_policy': polityka restartowania - w v3 przeniesiona do innego miejsca
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

    def validate_v3_format(self, v3_data: Dict[str, Any]) -> bool:
        """
        Podstawowa walidacja formatu v3
        """
        print("🔍 Walidacja formatu v3...")

        if str(v3_data.get('version')) != '3':
            print("❌ Nieprawidłowa wersja")
            return False

        templates = v3_data.get('templates', [])
        if not templates:
            print("❌ Brak szablonów")
            return False

        # Sprawdzamy wszystkie szablony
        errors = []
        for i, template in enumerate(templates):
            if 'id' not in template:
                errors.append(f"Brak pola 'id' w szablonie {i+1}")

            if 'labels' not in template:
                errors.append(f"Brak pola 'labels' w szablonie {i+1}")

            # Wymagane pola
            required_fields = ['title', 'description', 'type']
            for field in required_fields:
                if field not in template:
                    errors.append(f"Brak wymaganego pola '{field}' w szablonie {i+1}")

            # Sprawdzamy czy nie ma starych pól
            old_fields = ['restart_policy', 'platform']
            for field in old_fields:
                if field in template:
                    errors.append(f"Szablon {i+1} zawiera stare pole '{field}' z v2")

        if errors:
            print("❌ Błędy walidacji:")
            for error in errors[:10]:  # Pokaż tylko pierwsze 10 błędów
                print(f"   • {error}")
            if len(errors) > 10:
                print(f"   ... i {len(errors) - 10} więcej błędów")
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

    def run(self, source_url: Optional[str] = None, output_file: Optional[str] = None):
        """
        Główna metoda uruchamiająca cały proces konwersji
        """
        print("🚀 Portainer Templates Converter v2 -> v3")
        print("="*50)
        print(f"⏰ Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Używamy domyślnych wartości jeśli nie podano
        source_url = source_url or self.default_v2_url
        output_file = output_file or self.default_output_file

        try:
            # 1. Pobieranie szablonu v2
            v2_data = self.download_v2_templates(source_url)

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

  %(prog)s --url "https://example.com/templates.json" --output "custom_v3.json"
    Pełna własna konfiguracja

Główne różnice v2 -> v3:
  • Dodano pole 'id' (unikalny identyfikator)
  • Dodano pole 'labels' (etykiety Docker)
  • Usunięto pola 'restart_policy' i 'platform'
  • Zmieniono wersję na '3'
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
        '--version', '-v',
        action='version',
        version='Portainer Templates Converter 1.0'
    )

    args = parser.parse_args()

    # Uruchamiamy konwersję
    converter = PortainerTemplateConverter()
    converter.run(source_url=args.url, output_file=args.output)

if __name__ == "__main__":
    main()
