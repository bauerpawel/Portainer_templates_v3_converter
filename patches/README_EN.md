# 📋 Patch Files - Template Modification System

The patch file system allows you to apply changes to v3 templates without modifying the converter code.

## 📖 What Are Patch Files?

Patch files are JSON files containing instructions to modify templates:
- **UPDATE** - modify existing templates
- **ADD** - add new templates
- **REMOVE** - remove templates

## 📂 Directory Structure

```
patches/
├── _patch_loader.py              # Patch loader
├── __init__.py                   # Package init
├── README.md                     # Polish documentation
├── README_EN.md                  # English documentation (this file)
├── TEMPLATE.json                 # Template for copying
├── ARCHIVED.md                   # Archived patches (optional)
├── 0001-update-trilium-docker-image.json
├── 0002-add-custom-apps.json
└── ...
```

## 🔍 Patch File Structure

### File Naming

```
XXXX-description.json
     ↑
     Numbering (0001, 0002, 0003...)
```

**Rules:**
- Files are loaded in numerical order
- Must have 4 digits + hyphen
- Extension `.json`

### JSON Structure

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

## 📝 Operation Types

### 1. UPDATE - Modify Template

Modifies an existing template matching the filter criteria.

```json
{
  "operation": "update",
  "description": "What we're doing",
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

**Filter Criteria:**
- `name` - exact match
- `image` - supports wildcards (`zadam/*`)
- `id` - exact match
- `title` - case-insensitive
- Any other template field

**Changes:**
- Any template field
- List fields (env, volumes, labels) are merged

### 2. ADD - Add New Template

Adds a completely new template.

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

**Required Fields:**
- `id` (must be unique, prefer 5000+)
- `type` (1=container, 2=swarm stack)
- `title`
- `name`
- `image`

**Optional Fields:**
- `description`
- `categories`
- `ports`
- `env`
- `volumes`
- `labels`
- `logo`
- `maintainer`
- `repository`

### 3. REMOVE - Remove Template

Removes a template matching the filter criteria.

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

## 🎯 Practical Examples

### Example 1: Update Docker Image

**File:** `patches/0001-update-trilium-docker-image.json`

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

### Example 2: Add New Application

**File:** `patches/0003-add-custom-internal-apps.json`

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

### Example 3: Batch Update

**File:** `patches/0002-batch-update-deprecated-images.json`

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

## 🚀 How to Add a New Patch

1. **Copy the template**
   ```bash
   cp patches/TEMPLATE.json patches/0004-my-description.json
   ```

2. **Edit metadata**
   - `id`: `0004-my-description`
   - `title`: Short title
   - `description`: Detailed description
   - `author`: Your GitHub username
   - `date`: Today's date (YYYY-MM-DD)
   - `source`: Link to PR/Issue if exists

3. **Define operations**
   - Add UPDATE/ADD/REMOVE operations
   - Test filter criteria locally

4. **Validate JSON**
   ```bash
   python -m json.tool patches/0004-my-description.json
   ```

5. **Test locally**
   ```bash
   python portainer_converter.py
   ```

6. **Commit and Push**
   ```bash
   git add patches/0004-my-description.json
   git commit -m "Add patch: My description"
   git push
   ```

7. **Create Pull Request**

## 🔄 Patch Workflow

```
Conversion:
  1. Download v2 templates from source
  2. Convert to v3
  3. [NEW STEP] Load and apply patches
  4. Validate result
  5. Save to templates_v3_final.json
```

## 📋 Change Tracking

Each patch should contain:
- ✅ Unique ID
- ✅ Reference to source (PR/Issue)
- ✅ Author
- ✅ Date
- ✅ Description of what and why

## 📦 Archiving

When a patch is merged into the source templates:

1. Move to `patches/archived/`
2. Document in `patches/ARCHIVED.md`

```markdown
# Archived Patches

## 0001-update-trilium-docker-image.json
- **Date archived**: 2026-02-15
- **Reason**: Merged into Lissy93/portainer-templates#92
- **Commit**: abc123...
```

## ⚙️ Integration with Converter

PatchLoader is automatically loaded in the converter:

```python
from patches._patch_loader import PatchLoader

patch_loader = PatchLoader(patches_dir='patches')
patch_loader.load_patches()
v3_data['templates'] = patch_loader.apply_patches(v3_data['templates'])
```

## 📊 Statistics

After applying patches, the converter displays:

```
✅ Patch Statistics:
   • Loaded patch files: 3
   • Applied operations: 5
     - UPDATE: 3
     - ADD: 2
     - REMOVE: 0
   • Skipped: 0
   • Errors: 0
```

## ❓ FAQ

**Q: What if a patch doesn't apply?**
A: Check logs and:
   - Filter criteria must be exact
   - Templates must exist
   - JSON must be valid

**Q: Can I edit a patch after publishing?**
A: No. Create a new patch. Editing changes the hash and makes auditing difficult.

**Q: How many patches can I have?**
A: Unlimited. The system is scalable.

**Q: Do patches affect security?**
A: No. Patches are only JSON files with validation in the loader.

**Q: Can I use wildcards in filter?**
A: Yes, only for the `image` field: `"image": "zadam/*"`

**Q: What happens if two patches modify the same field?**
A: They are applied sequentially in order (0001, 0002, etc.). Last one wins for non-list fields.

## 🔗 Additional Resources

- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [portainer_converter.py](../portainer_converter.py) - Main converter
- [Lissy93/portainer-templates](https://github.com/Lissy93/portainer-templates) - Templates source
- [PatchLoader Source](./patches/_patch_loader.py) - Implementation details

## 🎯 Best Practices

1. **One patch per change** - Keep patches focused and atomic
2. **Clear description** - Explain what and why
3. **Test before committing** - Validate JSON and test locally
4. **Reference sources** - Link to PR/Issue when applicable
5. **Document everything** - Use meaningful field names and comments
6. **Use priorities** - Set priority for critical patches
7. **Version your patches** - Use semantic versioning in metadata

## 📝 Patch File Checklist

Before committing a patch:

- [ ] Filename follows `XXXX-description.json` pattern
- [ ] `id` matches filename (without .json)
- [ ] All metadata fields filled
- [ ] Operations are valid (UPDATE/ADD/REMOVE)
- [ ] Filter criteria are realistic
- [ ] JSON validates with `python -m json.tool`
- [ ] No TODO comments
- [ ] Tested locally
- [ ] Documented changes

## 🚀 Getting Started

1. Read this documentation
2. Copy `TEMPLATE.json`
3. Create your first patch
4. Test locally
5. Submit PR

That's it! Welcome to the patch community! 🎉
