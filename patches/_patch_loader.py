#!/usr/bin/env python3
"""
PatchLoader - System ładowania i aplikowania patchy-ów dla szablonów v3

Obsługuje operacje:
- UPDATE: zmiana istniejeych szablonów
- ADD: dodanie nowych szablonów  
- REMOVE: usunięcie szablonów

Autor: Patch System v1.0
Data: 2026-01-10
"""

import json
import os
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
import re


class PatchLoader:
    """Ładuje i aplikuje patch-y do szablonów Portainer v3"""

    def __init__(self, patches_dir: str = 'patches'):
        """
        Inicjalizuje loader patchy-ów
        
        Args:
            patches_dir: katalog z plikami patchy-ów
        """
        self.patches_dir = Path(patches_dir)
        self.patches = []
        self.stats = {
            'loaded': 0,
            'applied': 0,
            'operations': {
                'update': 0,
                'add': 0,
                'remove': 0
            },
            'skipped': 0,
            'errors': []
        }

    def load_patches(self) -> List[Dict[str, Any]]:
        """
        Ładuje wszystkie patch files z katalogu
        Pliki są ładowane w porządku numerycznym (0001, 0002...)
        
        Returns:
            Lista załadowanych patchy-ów
        """
        if not self.patches_dir.exists():
            print(f"⚠️  Katalog patchy-ów nie istnieje: {self.patches_dir}")
            return []

        # Zbieramy wszystkie .json files
        patch_files = sorted([
            f for f in self.patches_dir.glob('*.json')
            if f.name != 'TEMPLATE.json' and f.name != 'archived.json'
        ])

        if not patch_files:
            print(f"ℹ️  Brak patch files w {self.patches_dir}")
            return []

        print(f"🔍 Ładowanie patchy-ów z {self.patches_dir}...")

        self.patches = []
        for patch_file in patch_files:
            try:
                with open(patch_file, 'r', encoding='utf-8') as f:
                    patch_data = json.load(f)

                # Walidujemy strukturę patch file
                if not self._validate_patch_structure(patch_data):
                    self.stats['errors'].append(f"Invalid structure: {patch_file.name}")
                    continue

                self.patches.append(patch_data)
                self.stats['loaded'] += 1
                print(f"   ✅ {patch_file.name}: {patch_data['metadata']['title']}")

            except json.JSONDecodeError as e:
                error_msg = f"JSON error in {patch_file.name}: {e}"
                self.stats['errors'].append(error_msg)
                print(f"   ❌ {error_msg}")
            except Exception as e:
                error_msg = f"Error loading {patch_file.name}: {e}"
                self.stats['errors'].append(error_msg)
                print(f"   ❌ {error_msg}")

        return self.patches

    def _validate_patch_structure(self, patch: Dict[str, Any]) -> bool:
        """
        Waliduje strukturę patch file
        
        Returns:
            True jeśli struktura jest poprawna
        """
        # Sprawdzenie wymaganych pól
        required_keys = ['metadata', 'operations']
        for key in required_keys:
            if key not in patch:
                return False

        # Walidacja metadata
        metadata = patch['metadata']
        required_meta = ['version', 'id', 'title', 'description']
        for key in required_meta:
            if key not in metadata:
                return False

        # Walidacja operacji
        operations = patch['operations']
        if not isinstance(operations, list):
            return False

        for op in operations:
            if 'operation' not in op:
                return False
            op_type = op['operation']
            if op_type not in ['update', 'add', 'remove']:
                return False

        return True

    def apply_patches(self, templates: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Aplikuje wszystkie załadowane patchy-y do szablonów
        
        Args:
            templates: lista szablonów v3
            
        Returns:
            Tuple (zmodyfikowane templates, statystyki)
        """
        if not self.patches:
            return templates, self.stats

        print(f"\n🔧 Aplikowanie {len(self.patches)} patch file(ów)...")

        # Resetujemy statystyki operacji
        self.stats['operations'] = {'update': 0, 'add': 0, 'remove': 0}
        self.stats['applied'] = 0
        self.stats['skipped'] = 0

        # Aplikujemy patchy w kolejności
        for patch in self.patches:
            templates = self._apply_single_patch(patch, templates)

        return templates, self.stats

    def _apply_single_patch(self, patch: Dict[str, Any], templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplikuje pojedynczy patch do szablonów
        
        Args:
            patch: patch do aplikowania
            templates: lista szablonów
            
        Returns:
            Zmodyfikowana lista szablonów
        """
        metadata = patch['metadata']
        patch_id = metadata['id']
        patch_title = metadata['title']

        print(f"\n   📋 Patch: {patch_id} - {patch_title}")

        operations = patch['operations']

        for op_idx, operation in enumerate(operations, 1):
            op_type = operation['operation']
            op_desc = operation.get('description', '')

            try:
                if op_type == 'update':
                    templates = self._apply_update(operation, templates)
                elif op_type == 'add':
                    templates = self._apply_add(operation, templates)
                elif op_type == 'remove':
                    templates = self._apply_remove(operation, templates)

                self.stats['operations'][op_type] += 1
                self.stats['applied'] += 1

            except Exception as e:
                error_msg = f"Error in {patch_id} operation {op_idx}: {e}"
                self.stats['errors'].append(error_msg)
                print(f"      ❌ {error_msg}")
                self.stats['skipped'] += 1

        return templates

    def _apply_update(self, operation: Dict[str, Any], templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplikuje operację UPDATE - zmiana istniejących szablonów
        
        Kryteria filtrowania mogą używać dowolnych pól szablonu
        """
        filter_criteria = operation.get('filter', {})
        changes = operation.get('changes', {})
        op_desc = operation.get('description', '')

        if not filter_criteria or not changes:
            raise ValueError("UPDATE requires 'filter' and 'changes'")

        matched = 0
        for template in templates:
            if self._matches_filter(template, filter_criteria):
                # Aplikujemy zmiany
                for key, value in changes.items():
                    if key in ['env', 'volumes', 'labels', 'categories', 'ports']:
                        # Dla pól listowych - scal zamiast zamień
                        if isinstance(value, list):
                            if key not in template:
                                template[key] = []
                            # Scalanie - unikaj duplikatów
                            self._merge_list_field(template, key, value)
                        else:
                            template[key] = value
                    else:
                        # Dla zwykłych pól - zamień
                        template[key] = value

                matched += 1

        if matched > 0:
            print(f"      ✅ UPDATE: zaktualizowano {matched} szablon(ów)")
            if op_desc:
                print(f"         {op_desc}")
        else:
            print(f"      ⚠️  UPDATE: brak szablonów spełniających kryteria")

        return templates

    def _apply_add(self, operation: Dict[str, Any], templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplikuje operację ADD - dodanie nowych szablonów
        """
        new_template = operation.get('template')
        op_desc = operation.get('description', '')

        if not new_template:
            raise ValueError("ADD requires 'template' field")

        # Walidujemy wymagane pola
        # Dla stacków (type 2, 3, 4) image nie jest wymagany — używają repository lub compose
        template_type = new_template.get('type', 1)
        if template_type == 1:
            required_fields = ['id', 'type', 'title', 'name', 'image']
        else:
            required_fields = ['id', 'type', 'title', 'name']
        for field in required_fields:
            if field not in new_template:
                raise ValueError(f"ADD template missing required field: {field}")

        # Sprawdzamy czy template o takim ID już istnieje
        new_id = new_template['id']
        existing = next((t for t in templates if t.get('id') == new_id), None)

        if existing:
            print(f"      ⚠️  ADD: szablon o ID {new_id} już istnieje, pomijam")
            self.stats['skipped'] += 1
            return templates

        # Dodajemy nowy template
        templates.append(new_template)
        print(f"      ✅ ADD: dodano nowy szablon '{new_template['title']}'")
        if op_desc:
            print(f"         {op_desc}")

        return templates

    def _apply_remove(self, operation: Dict[str, Any], templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aplikuje operację REMOVE - usunięcie szablonów
        """
        filter_criteria = operation.get('filter', {})
        reason = operation.get('reason', '')
        op_desc = operation.get('description', '')

        if not filter_criteria:
            raise ValueError("REMOVE requires 'filter'")

        initial_count = len(templates)
        templates = [
            t for t in templates
            if not self._matches_filter(t, filter_criteria)
        ]
        removed_count = initial_count - len(templates)

        if removed_count > 0:
            print(f"      ✅ REMOVE: usunięto {removed_count} szablon(ów)")
            if op_desc:
                print(f"         {op_desc}")
            if reason:
                print(f"         Powód: {reason}")
        else:
            print(f"      ⚠️  REMOVE: brak szablonów spełniających kryteria")

        return templates

    def _matches_filter(self, template: Dict[str, Any], filter_criteria: Dict[str, Any]) -> bool:
        """
        Sprawdza czy szablon spełnia kryteria filtrowania
        
        Obsługuje:
        - Dokładne dopasowanie (name, id, title)
        - Wildcardy dla image (zadam/* -> zadam/*)  
        - Case-insensitive dla string pól
        """
        for key, criteria_value in filter_criteria.items():
            if key not in template:
                return False

            template_value = template[key]

            # Dla image field - obsługuj wildcardy
            if key == 'image' and isinstance(criteria_value, str) and '*' in criteria_value:
                pattern = criteria_value.replace('*', '.*')
                if not re.match(f"^{pattern}$", str(template_value), re.IGNORECASE):
                    return False
            # Dla string pól - case-insensitive
            elif isinstance(criteria_value, str) and isinstance(template_value, str):
                if criteria_value.lower() != template_value.lower():
                    return False
            # Dla pozostałych - dokładne dopasowanie
            else:
                if criteria_value != template_value:
                    return False

        return True

    def _merge_list_field(self, template: Dict[str, Any], field: str, values: List[Any]) -> None:
        """
        Scala wartości listy, unikając duplikatów
        
        Args:
            template: szablon do modyfikacji
            field: pole które zawiera listę
            values: wartości do dodania
        """
        if field not in template:
            template[field] = []

        current = template[field]
        if not isinstance(current, list):
            current = [current]
            template[field] = current

        for value in values:
            if value not in current:
                current.append(value)

    def get_statistics(self) -> Dict[str, Any]:
        """
        Zwraca statystyki aplikowania patchy-ów
        """
        return self.stats.copy()

    def print_statistics(self) -> None:
        """
        Wyświetla statystyki aplikowania patchy-ów
        """
        print("\n📊 Statystyka patchy-ów:")
        print(f"   • Załadowane patch files: {self.stats['loaded']}")
        print(f"   • Aplikowane operacje: {self.stats['applied']}")
        print(f"     - UPDATE: {self.stats['operations']['update']}")
        print(f"     - ADD: {self.stats['operations']['add']}")
        print(f"     - REMOVE: {self.stats['operations']['remove']}")
        print(f"   • Pominięte: {self.stats['skipped']}")
        print(f"   • Błędy: {len(self.stats['errors'])}")

        if self.stats['errors']:
            print("\n   ❌ Błędy:")
            for error in self.stats['errors'][:5]:
                print(f"      • {error}")
            if len(self.stats['errors']) > 5:
                print(f"      ... i {len(self.stats['errors']) - 5} więcej błędów")
