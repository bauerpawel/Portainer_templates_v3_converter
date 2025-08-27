#!/usr/bin/env python3
"""
Test jednostkowy dla Portainer Templates Converter
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Importujemy naszą klasę z aplikacji
exec(open('portainer_converter.py').read())

class TestPortainerConverter(unittest.TestCase):

    def setUp(self):
        self.converter = PortainerTemplateConverter()
        self.sample_v2_template = {
            "type": 1,
            "title": "Test App",
            "description": "Test application",
            "image": "nginx:latest",
            "categories": ["Web"],
            "restart_policy": "unless-stopped",
            "platform": "linux",
            "ports": ["80:80/tcp"],
            "volumes": [],
            "env": []
        }

        self.sample_v2_data = {
            "version": "2",
            "templates": [self.sample_v2_template]
        }

    def test_convert_template(self):
        """Test konwersji pojedynczego szablonu"""
        result = self.converter.convert_template(self.sample_v2_template, 1)

        # Sprawdzamy czy dodano wymagane pola v3
        self.assertIn('id', result)
        self.assertIn('labels', result)
        self.assertEqual(result['id'], 1)
        self.assertEqual(result['labels'], [])

        # Sprawdzamy czy skopiowano właściwe pola
        self.assertEqual(result['title'], 'Test App')
        self.assertEqual(result['type'], 1)
        self.assertEqual(result['categories'], ['Web'])

        # Sprawdzamy czy usunięto stare pola
        self.assertNotIn('restart_policy', result)
        self.assertNotIn('platform', result)

    def test_convert_v2_to_v3(self):
        """Test pełnej konwersji v2 -> v3"""
        result = self.converter.convert_v2_to_v3(self.sample_v2_data)

        self.assertEqual(result['version'], '3')
        self.assertEqual(len(result['templates']), 1)

        template = result['templates'][0]
        self.assertEqual(template['id'], 1)
        self.assertIn('labels', template)

    def test_validate_v3_format(self):
        """Test walidacji formatu v3"""
        # Poprawny format v3
        valid_v3 = {
            "version": "3",
            "templates": [{
                "id": 1,
                "title": "Test",
                "description": "Test desc",
                "type": 1,
                "labels": []
            }]
        }

        self.assertTrue(self.converter.validate_v3_format(valid_v3))

        # Niepoprawny format - brak id
        invalid_v3 = {
            "version": "3",
            "templates": [{
                "title": "Test",
                "description": "Test desc",
                "type": 1,
                "labels": []
            }]
        }

        self.assertFalse(self.converter.validate_v3_format(invalid_v3))

    def test_save_and_load_v3_templates(self):
        """Test zapisywania i wczytywania plików"""
        test_data = {
            "version": "3",
            "templates": [{
                "id": 1,
                "title": "Test",
                "description": "Test description",
                "type": 1,
                "labels": []
            }]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            # Zapisz
            result_file = self.converter.save_v3_templates(test_data, temp_file)
            self.assertEqual(result_file, temp_file)
            self.assertTrue(os.path.exists(temp_file))

            # Wczytaj i sprawdź
            with open(temp_file, 'r') as f:
                loaded_data = json.load(f)

            self.assertEqual(loaded_data['version'], '3')
            self.assertEqual(len(loaded_data['templates']), 1)
            self.assertEqual(loaded_data['templates'][0]['id'], 1)

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

if __name__ == '__main__':
    print("🧪 Uruchamianie testów jednostkowych...")
    unittest.main(verbosity=2)
