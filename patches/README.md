# 📋 Patch Files - System Modyfikacji Szablonów

Sistem patch files pozwala na aplikowanie zmian do szablonów v3 bez konieczności modyfikacji kodu konwertera.

## 📖 Czym są Patch Files?

Patch files to pliki JSON zawierające instrukcje modyfikacji szablonów:
- **UPDATE** - zmiana istniejących szablonów
- **ADD** - dodanie nowych szablonów
- **REMOVE** - usunięcie szablonów

## 🗂️ Struktura Katalogu

```
patches/
├── _patch_loader.py              # Loader patchy
├── __init__.py                   # Package init
├── README.md                     # Ta dokumentacja
├── TEMPLATE.json                 # Wzór do kopiowania
├── ARCHIVED.md                   # Zarchiwizowane patchy (opcjonalnie)
├── 0001-update-trilium-docker-image.json
├── 0002-add-custom-apps.json
└── ...
```

## 🔍 Struktura Patch File'a

### Nazwa Pliku

```
XXXX-description.json
     ↑
     Numeracja (0001, 0002, 0003...)
```

**Reguły:**
- Pliki są ładowane w kolejności numerycznej
- Musi być 4 cyfry + myślnik
- Rozszerzenie `.json`

### Struktura JSON

```json
{
  "metadata": {
    "version": "1",
    "id": "0001-unique-id",
    "title": "Human readable title",
    "description": "What and why",
    "author": "github-username",
    "date": "YYYY-MM-DD",
    "priority": 10,
    "source": "https://github.com/..."
  },
  "operations": [
    { ... }
  ]
}
```

## 📝 Typy Operacji

### 1. UPDATE - Zmiana szablonu

Modyfikuje istniejący szablon spełniający kryteria filtrowania.

```json
{
  "operation": "update",
  "description": "Co robimy",
  "filter": {
    "name": "trilium",
    "title": "Trilium Notes"
  },
  "changes": {
    "image": "triliumnext/trilium:latest",
    "note": "Updated description"
  }
}
```

**Kryteria Filtrowania:**
- `name` - dokładne dopasowanie
- `image` - obsługuje wildcardy (`zadam/*`)
- `id` - dokładne dopasowanie
- `title` - case-insensitive
- Każde inne pole z szablonu

**Zmiana:**
- Każde pole szablonu
- Scalanie pól listy (env, volumes, labels)

### 2. ADD - Dodanie nowego szablonu

Dodaje całkowicie nowy szablon.

```json
{
  "operation": "add",
  "description": "Add new custom app",
  "template": {
    "id": 5001,
    "type": 1,
    "title": "My Custom App",
    "name": "my-custom-app",
    "image": "myrepo/my-app:latest",
    "description": "Custom application",
    "categories": ["Custom"],
    "ports": ["8080:8080"],
    "env": [],
    "volumes": [],
    "labels": [],
    "logo": "https://example.com/logo.png"
  }
}
```

**Wymagane Pola:**
- `id` (musi być unikalne, preferuj 5000+)
- `type` (1=kontener, 2=stack)
- `title`
- `name`
- `image`

**Opcjonalne Pola:**
- `description`
- `categories`
- `ports`
- `env`
- `volumes`
- `labels`
- `logo`
- `maintainer`
- `repository`

### 3. REMOVE - Usunięcie szablonu

Usuwa szablon spełniający kryteria.

```json
{
  "operation": "remove",
  "description": "Remove deprecated app",
  "filter": {
    "name": "old-app"
  },
  "reason": "No longer maintained"
}
```

## 🎯 Praktyczne Przykłady

### Przykład 1: Aktualizacja Docker Image

**Plik:** `patches/0001-update-trilium-docker-image.json`

```json
{
  "metadata": {
    "version": "1",
    "id": "0001-update-trilium-docker-image",
    "title": "Update Trilium to TriliumNext",
    "description": "Project handed over to TriliumNext community",
    "author": "fyliu",
    "date": "2026-01-04",
    "priority": 10,
    "source": "https://github.com/Lissy93/portainer-templates/pull/92"
  },
  "operations": [
    {
      "operation": "update",
      "filter": { "name": "trilium" },
      "changes": { "image": "triliumnext/trilium:latest" }
    }
  ]
}
```

### Przykład 2: Dodanie Nowej Aplikacji

**Plik:** `patches/0003-add-custom-internal-apps.json`

```json
{
  "metadata": {
    "version": "1",
    "id": "0003-add-custom-internal-apps",
    "title": "Add custom internal applications",
    "date": "2026-01-10",
    "author": "your-username"
  },
  "operations": [
    {
      "operation": "add",
      "template": {
        "id": 5001,
        "type": 1,
        "title": "Internal Dashboard",
        "name": "internal-dashboard",
        "image": "internal/dashboard:latest",
        "description": "Internal monitoring dashboard",
        "categories": ["Tools", "Monitoring"],
        "ports": ["3000:3000"],
        "env": [
          {
            "name": "API_KEY",
            "label": "Dashboard API Key",
            "default": ""
          }
        ],
        "labels": [],
        "logo": "https://example.com/dashboard.png"
      }
    },
    {
      "operation": "add",
      "template": {
        "id": 5002,
        "type": 1,
        "title": "Internal Registry",
        "name": "internal-registry",
        "image": "internal/registry:latest",
        "description": "Internal Docker registry",
        "categories": ["Tools"],
        "ports": ["5000:5000"],
        "volumes": [
          {
            "container": "/var/lib/registry",
            "bind": "/mnt/registry"
          }
        ],
        "labels": []
      }
    }
  ]
}
```

### Przykład 3: Batch Update

**Plik:** `patches/0002-batch-update-deprecated-images.json`

```json
{
  "metadata": {
    "version": "1",
    "id": "0002-batch-update-deprecated-images",
    "title": "Batch: Update deprecated Docker images",
    "date": "2026-01-10"
  },
  "operations": [
    {
      "operation": "update",
      "filter": { "name": "trilium" },
      "changes": { "image": "triliumnext/trilium:latest" }
    },
    {
      "operation": "update",
      "filter": { "name": "app2" },
      "changes": { "image": "newrepo/app2:v2" }
    },
    {
      "operation": "update",
      "filter": { "name": "app3" },
      "changes": { "env": [ { "name": "NEW_VAR", "default": "value" } ] }
    }
  ]
}
```

## 🚀 Jak Dodać Nowy Patch

1. **Skopiuj szablon**
   ```bash
   cp patches/TEMPLATE.json patches/0004-my-description.json
   ```

2. **Edytuj metadata**
   - `id`: `0004-my-description`
   - `title`: Krótki tytuł
   - `description`: Szczegółowy opis
   - `author`: Twoja nazwa GitHub
   - `date`: Data dzisiejsza (YYYY-MM-DD)
   - `source`: Link do PR/Issue jeśli istnieje

3. **Zdefiniuj operacje**
   - Dodaj UPDATE/ADD/REMOVE operacje
   - Testuj lokalne kryteria filtrowania

4. **Waliduj JSON**
   ```bash
   python -m json.tool patches/0004-my-description.json
   ```

5. **Przetestuj lokalnie**
   ```bash
   python portainer_converter.py
   ```

6. **Commit i Push**
   ```bash
   git add patches/0004-my-description.json
   git commit -m "Add patch: My description"
   git push
   ```

7. **Utwórz Pull Request**

## 🔄 Workflow Patchy

```
Konwersja:
  1. Pobierz szablony v2 z źródła
  2. Konwertuj na v3
  3. [NOWY KROK] Załaduj i aplikuj patchy
  4. Waliduj wynik
  5. Zapisz do templates_v3_final.json
```

## 📋 Śledzenie Zmian

Każdy patch powinien zawierać:
- ✅ Unikalny ID
- ✅ Referencję do źródła (PR/Issue)
- ✅ Autora
- ✅ Datę
- ✅ Opis co i dlaczego

## 🗂️ Archiwizacja

Gdy patch zostaje już zaaplikowany w źródłowych szablonach:

1. Przenieś do `patches/archived/`
2. Udokumentuj w `patches/ARCHIVED.md`

```markdown
# Archived Patches

## 0001-update-trilium-docker-image.json
- **Date archived**: 2026-02-15
- **Reason**: Merged into Lissy93/portainer-templates#92
- **Commit**: abc123...
```

## ⚙️ Integracja z Konwerterem

PatchLoader jest automatycznie ładowany w konwerterze:

```python
from patches._patch_loader import PatchLoader

patch_loader = PatchLoader(patches_dir='patches')
patch_loader.load_patches()
v3_data['templates'] = patch_loader.apply_patches(v3_data['templates'])
```

## 📊 Statystyka

Po aplikowaniu patchy konwerter wyświetla:

```
✅ Statystyka patchy:
   • Załadowane patch files: 3
   • Aplikowane operacje: 5
     - UPDATE: 3
     - ADD: 2
     - REMOVE: 0
   • Pominięte: 0
   • Błędy: 0
```

## ❓ FAQ

**P: Co jeśli patch się nie aplikuje?**
A: Sprawdź logi i:\n   - Kryteria filtrowania muszą być dokładne
   - Szablony muszą istnieć
   - JSON musi być poprawny

**P: Czy mogę edytować patch po opublikowaniu?**
A: Nie. Utwórz nowy patch. Edytowanie zmienia hash i utrudnia auditowanie.

**P: Ile patchy mogę mieć?**
A: Nieograniczona ilość. System jest skaloowalny.

**P: Czy patchye wpływają na bezpieczeństwo?**
A: Nie. Patchy są tylko JSON files z walidacją w loadererze.

## 🔗 Dodatkowe Zasoby

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Jak wkład do projektu
- [portainer_converter.py](../portainer_converter.py) - Główny konwerter
- [Lissy93/portainer-templates](https://github.com/Lissy93/portainer-templates) - Źródło szablonów
