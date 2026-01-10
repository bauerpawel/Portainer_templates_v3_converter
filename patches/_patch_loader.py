#!/usr/bin/env python3
"""
Patch Loader dla Portainer Templates v3
Obsługuje ładowanie i aplikowanie patch files do szablonów

Typy operacji:
  - update: zmiana istniejącego szablonu
  - add: dodanie nowego szablonu
  - remove: usunięcie szablonu
"""

import json
import os
from typing import Dict, Any, List, Tuple
import re
from datetime import datetime


class PatchLoader:
    """Ładuje i aplikuje patch files do szablonów v3"""

    def __init__(self, patches_dir: str = "patches"):
        self.patches_dir = patches_dir
        self.patches = []
        self.stats = {
            'patches_loaded': 0,
            'operations_applied': 0,
            'updates': 0,
            'additions': 0,
            'removals': 0,
            'errors': 0,
            'skipped': 0
        }

    def load_patches(self) -> List[Dict[str, Any]]:
        """
        Ładuje wszystkie patch files z katalogu patches/
        Patch files są ładowane w kolejności numerycznej (XXXX-*.json)
        """
        print("📂 Ładowanie patch files...")

        if not os.path.exists(self.patches_dir):
            print(f"⚠️  Katalog {self.patches_dir} nie istnieje")
            return []

        patch_files = []
        patch_paths = []

        # Zbieramy patch files
        for filename in sorted(os.listdir(self.patches_dir)):
            # Szukamy plików z pattern: XXXX-*.json lub XXXX_*.json
            if filename.endswith('.json') and self._is_valid_patch_file(filename):
                filepath = os.path.join(self.patches_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        patch_data = json.load(f)
                        self._validate_patch_structure(patch_data, filename)
                        self.patches.append(patch_data)
                        patch_files.append(filename)
                        patch_paths.append(filepath)
                except json.JSONDecodeError as e:
                    print(f"❌ Błąd parsowania JSON w {filename}: {e}")
                except ValueError as e:
                    print(f"❌ Błąd walidacji patcha {filename}: {e}")
                except Exception as e:
                    print(f"❌ Błąd ładowania {filename}: {e}")

        self.stats['patches_loaded'] = len(patch_files)

        if patch_files:
            print(f"✅ Załadowano {len(patch_files)} patch files")
            for pf in patch_files:
                patch_id = self._get_patch_id(pf)
                print(f"   • {pf} (ID: {patch_id})")
        else:
            print("⚠️  Nie znaleziono żadnych patch files")

        return self.patches

    def apply_patches(self, templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplikuje wszystkie patch files do szablonów
        Patche są aplikowane w kolejności załadowania
        """
        if not self.patches:
            print("⚠️  Brak patch files do aplikowania")
            return templates

        print("\n🔧 Aplikowanie patch files...")
        print()

        for patch in self.patches:
            patch_id = patch.get('metadata', {}).get('id', 'unknown')
            patch_title = patch.get('metadata', {}).get('title', 'Unknown')
            patch_priority = patch.get('metadata', {}).get('priority', 0)

            print(f"📋 [{patch_id}] {patch_title}")

            operations = patch.get('operations', [])

            for op_idx, op in enumerate(operations, 1):
                operation_type = op.get('operation')
                description = op.get('description', '')

                try:
                    if operation_type == 'update':
                        result = self._apply_update(templates, op)
                        if result:
                            self.stats['updates'] += 1
                            self.stats['operations_applied'] += 1
                            status = "✅"
                        else:
                            self.stats['skipped'] += 1
                            status = "⏭️ "

                    elif operation_type == 'add':
                        result = self._apply_add(templates, op)
                        if result:
                            self.stats['additions'] += 1
                            self.stats['operations_applied'] += 1
                            status = "✅"
                        else:
                            self.stats['errors'] += 1
                            status = "❌"

                    elif operation_type == 'remove':
                        result = self._apply_remove(templates, op)
                        if result:
                            self.stats['removals'] += 1
                            self.stats['operations_applied'] += 1
                            status = "✅"
                        else:
                            self.stats['skipped'] += 1
                            status = "⏭️ "

                    else:
                        print(f"   ❌ Nieznany typ operacji: {operation_type}")
                        self.stats['errors'] += 1
                        status = "❌"
                        result = False

                    # Wyświetl status operacji
                    op_desc = description if description else f"{operation_type}"
                    if result:
                        print(f"   {status} Operacja {op_idx}: {op_desc}")

                except Exception as e:
                    print(f"   ❌ Błąd w operacji {op_idx}: {e}")
                    self.stats['errors'] += 1

            print()

        self._print_statistics()
        return templates

    def _apply_update(self, templates: List[Dict[str, Any]], operation: Dict[str, Any]) -> bool:
        """Aplikuje operację UPDATE - zmienia istniejący szablon"""
        filter_criteria = operation.get('filter', {})
        changes = operation.get('changes', {})

        if not filter_criteria:
            print(f"   ⚠️  Brak kryteriów filtrowania w UPDATE operacji")
            return False

        found_count = 0
        for template in templates:
            if self._matches_filter(template, filter_criteria):
                # Aplikujemy zmiany
                for key, value in changes.items():
                    template[key] = value
                found_count += 1

        if found_count > 0:
            return True
        else:
            print(f"   ⚠️  Nie znaleziono szablonu spełniającego kryteria: {filter_criteria}")
            return False

    def _apply_add(self, templates: List[Dict[str, Any]], operation: Dict[str, Any]) -> bool:
        """Aplikuje operację ADD - dodaje nowy szablon"""
        new_template = operation.get('template', {})

        if not new_template:
            print(f"   ❌ Brak szablonu do dodania")
            return False

        # Sprawdzamy wymagane pola
        required_fields = ['id', 'type', 'title', 'name', 'image']
        for field in required_fields:
            if field not in new_template:
                print(f"   ❌ Szablon brakuje wymagane pole: {field}")
                return False

        # Sprawdzamy czy szablon już istnieje
        new_id = new_template.get('id')
        new_name = new_template.get('name')

        for template in templates:
            if template.get('id') == new_id:
                print(f"   ⚠️  Szablon o ID {new_id} już istnieje (duplikat)")
                return False
            if template.get('name') == new_name:
                print(f"   ⚠️  Szablon o nazwie '{new_name}' już istnieje (duplikat)")
                return False

        # Dodajemy nowy szablon
        templates.append(new_template)
        return True

    def _apply_remove(self, templates: List[Dict[str, Any]], operation: Dict[str, Any]) -> bool:
        """Aplikuje operację REMOVE - usuwa szablon"""
        filter_criteria = operation.get('filter', {})

        if not filter_criteria:
            print(f"   ⚠️  Brak kryteriów filtrowania w REMOVE operacji")
            return False

        templates_to_remove = []
        for i, template in enumerate(templates):
            if self._matches_filter(template, filter_criteria):
                templates_to_remove.append(i)

        if not templates_to_remove:
            print(f"   ⚠️  Nie znaleziono szablonu do usunięcia")
            return False

        # Usuwamy w odwrotnej kolejności aby nie zmieniały się indeksy
        for i in reversed(templates_to_remove):
            templates.pop(i)

        return True

    def _matches_filter(self, template: Dict[str, Any], filter_criteria: Dict[str, Any]) -> bool:
        """Sprawdza czy szablon spełnia kryteria filtrowania"""
        for key, value in filter_criteria.items():
            if key not in template:
                return False

            template_value = template.get(key)

            # Obsługujemy wildcardy (np. "postgres:*")
            if isinstance(value, str) and '*' in value:
                pattern = value.replace('*', '.*')
                if not re.match(pattern, str(template_value), re.IGNORECASE):
                    return False
            else:
                # Porównanie case-insensitive dla stringów
                if isinstance(value, str) and isinstance(template_value, str):
                    if template_value.lower() != value.lower():
                        return False
                else:
                    if template_value != value:
                        return False

        return True

    def _validate_patch_structure(self, patch: Dict[str, Any], filename: str) -> None:
        """Waliduje strukturę patch file'a"""
        # Sprawdzenie metadata
        if 'metadata' not in patch:
            raise ValueError(f"Brak sekcji 'metadata'")

        metadata = patch['metadata']
        if 'id' not in metadata:
            raise ValueError(f"Brak 'id' w metadata")
        if 'version' not in metadata:
            raise ValueError(f"Brak 'version' w metadata")

        # Sprawdzenie operations
        if 'operations' not in patch:
            raise ValueError(f"Brak sekcji 'operations'")

        operations = patch['operations']
        if not isinstance(operations, list):
            raise ValueError(f"'operations' powinna być listą")

        for i, op in enumerate(operations):
            if 'operation' not in op:
                raise ValueError(f"Operacja {i} brakuje pola 'operation'")

            op_type = op['operation']
            if op_type not in ['update', 'add', 'remove']:
                raise ValueError(f"Nieznany typ operacji: {op_type}")

    def _is_valid_patch_file(self, filename: str) -> bool:
        """Sprawdza czy plik to poprawny patch file"""
        # Pattern: XXXX-* lub XXXX_*
        pattern = r'^\d{4}[-_].*\.json$'
        return bool(re.match(pattern, filename))

    def _get_patch_id(self, filename: str) -> str:
        """Wyciąga ID patcha z nazwy pliku"""
        # Usuń rozszerzenie
        name_without_ext = filename[:-5]
        return name_without_ext

    def _print_statistics(self) -> None:
        """Wyświetla statystykę aplikowania patchy"""
        print("✅ Statystyka patchy:")
        print(f"   • Załadowane patch files: {self.stats['patches_loaded']}")
        print(f"   • Aplikowane operacje: {self.stats['operations_applied']}")
        print(f"     - UPDATE: {self.stats['updates']}")
        print(f"     - ADD: {self.stats['additions']}")
        print(f"     - REMOVE: {self.stats['removals']}")
        print(f"   • Pominięte: {self.stats['skipped']}")
        print(f"   • Błędy: {self.stats['errors']}")
