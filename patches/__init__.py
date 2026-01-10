#!/usr/bin/env python3
"""
Patches Package

System patch files dla Portainer Templates v3
Obsługuje aplikowanie zmian do wynikowych szablonów bez modyfikacji źródłowych

Typy operacji:
  - update: zmiana istniejącego szablonu
  - add: dodanie nowego szablonu
  - remove: usunięcie szablonu

Struktura patch file'a:
  patches/XXXX-description.json

Format:
  {
    "metadata": {
      "version": "1",
      "id": "XXXX-unique-id",
      "title": "Human readable title",
      "description": "Detailed description",
      "author": "github-username",
      "date": "YYYY-MM-DD",
      "priority": 10,
      "source": "https://github.com/..."
    },
    "operations": [
      {
        "operation": "update|add|remove",
        "filter": { ... },
        "changes": { ... }
      }
    ]
  }
"""

__version__ = "1.0.0"
__author__ = "bauerpawel"

from ._patch_loader import PatchLoader

__all__ = ['PatchLoader']
