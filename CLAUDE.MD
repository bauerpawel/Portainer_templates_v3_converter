# CLAUDE.MD - Project Context for Claude Code

## Project Overview

**Portainer Templates Converter v2 → v3** is a Python application that automatically converts Portainer application templates from v2 format to v3 format, which is compatible with the latest versions of Portainer.io.

### Key Purpose
Convert Docker/Swarm app templates to the new Portainer v3 format which requires:
- Adding unique `id` fields
- Adding `labels` arrays
- Removing deprecated `restart_policy` and `platform` fields
- Validating against official JSON Schema

### Languages & Technologies
- **Primary**: Python 3.6+
- **Key Libraries**: `requests`, `jsonschema`
- **Format**: JSON template processing
- **Domain**: Docker, Portainer, containerization

## Project Structure

```
.
├── portainer_converter.py      # Main application (PortainerTemplateConverter class)
├── test_converter.py           # Unit tests for the converter
├── schema_v3.json              # Official Portainer v3 JSON Schema for validation
├── templates_v3_converted.json # Output file (generated after conversion)
├── requirements.txt            # Python dependencies
├── README.md                   # Documentation (Polish)
├── README.en.md                # Documentation (English)
├── USAGE_EXAMPLES.md           # Usage examples
├── CHANGELOG.md                # Version history
└── LICENSE                     # Apache-2.0 license
```

## Key Files

### portainer_converter.py
Main application file containing:
- `PortainerTemplateConverter` class - handles all conversion logic
- Known template sources (Lissy93, Portainer Official, SelfHosted, Technorabilia)
- Template downloading, merging, converting, validating, and saving
- CLI argument parsing
- Statistics generation

### schema_v3.json
Official Portainer v3 JSON Schema used for validation. Defines:
- Required fields (`version`, `templates`)
- Template structure (id, type, title, description, image, etc.)
- Data types and formats
- Validation rules

### test_converter.py
Unit tests for the converter functionality

## Architecture & Key Features

### Main Conversion Flow
1. **Download** templates from URL(s) or use known sources
2. **Merge** (if multiple sources) - deduplicates by `(name, image)` combination
3. **Convert** each template:
   - Add unique `id` (integer)
   - Add empty `labels` array
   - Remove `restart_policy` and `platform`
   - Copy all other fields
4. **Validate** against schema_v3.json and business rules
5. **Save** to output file with pretty formatting
6. **Display** statistics (counts, categories, types)

### Known Template Sources
The converter has built-in support for popular template sources:
- **lissy93**: 470+ templates (default)
- **portainer-official**: Official Portainer templates
- **selfhosted**: SelfHosted.show templates
- **technorabilia**: LinuxServer.io based templates

### Deduplication Strategy
When merging multiple sources:
- Templates matched by `(name.lower(), image.lower())`
- Categories are merged (union)
- Longer description is preferred
- First occurrence wins for other fields

## Development Workflow

### Running Conversions

```bash
# Basic conversion (uses Lissy93 source)
python portainer_converter.py

# Custom URL
python portainer_converter.py --url "https://example.com/templates.json"

# Merge multiple sources
python portainer_converter.py --sources lissy93 portainer-official

# Merge all known sources
python portainer_converter.py --all-sources

# Custom output file
python portainer_converter.py --output "my_templates.json"

# List available sources
python portainer_converter.py --list-sources
```

### Testing

```bash
# Run unit tests
python -m pytest test_converter.py

# Or if using unittest
python test_converter.py
```

### Installing Dependencies

```bash
pip install -r requirements.txt
# or manually:
pip install requests jsonschema
```

## Template Format Differences

### V2 Format (Source)
```json
{
  "version": "2",
  "templates": [
    {
      "type": 1,
      "title": "App Name",
      "name": "app",
      "image": "app:latest",
      "restart_policy": "unless-stopped",  // Removed in v3
      "platform": "linux"                  // Removed in v3
    }
  ]
}
```

### V3 Format (Target)
```json
{
  "version": "3",
  "templates": [
    {
      "id": 1,              // Added in v3
      "type": 1,
      "title": "App Name",
      "name": "app",
      "image": "app:latest",
      "labels": []          // Added in v3
    }
  ]
}
```

## Important Fields

### Copied Without Changes
- `categories` - application categories
- `description` - app description
- `env` - environment variables
- `image` - Docker image
- `logo` - app logo URL
- `maintainer` - template maintainer
- `name` - application name
- `ports` - port mappings
- `title` - template title
- `type` - template type (1=container, 2=swarm stack)
- `volumes` - volume mappings
- `note` - additional notes
- `repository` - Git repository URL

### Added in V3
- `id` - unique integer identifier (auto-generated)
- `labels` - Docker labels array (empty by default)

### Removed from V2
- `restart_policy` - restart policy (deprecated)
- `platform` - platform specification (deprecated)

## Common Tasks

### Adding a New Template Source

Edit `portainer_converter.py` and add to the `known_sources` dict:

```python
self.known_sources = {
    'new-source': {
        'name': 'New Source Name',
        'url': 'https://example.com/templates.json',
        'description': 'Description of this source'
    }
}
```

### Modifying Conversion Logic

The conversion happens in the `convert_template_v2_to_v3()` method. Key areas:
- Line ~150-200: Field mapping
- ID generation uses enumerate index
- Labels are initialized as empty arrays

### Adding Validation Rules

Additional validation is in `validate_templates_v3()` method:
- Check for required fields
- Verify data types
- Business logic validation
- Schema validation (if schema_v3.json available)

## Code Style & Conventions

### Language
- Comments and strings: Polish (Polski)
- Variable names: English
- User-facing output: Polish

### Naming Conventions
- Classes: `PascalCase` (e.g., `PortainerTemplateConverter`)
- Functions/methods: `snake_case` (e.g., `convert_template_v2_to_v3`)
- Constants: `UPPER_SNAKE_CASE`

### Output Style
Uses emojis for visual feedback:
- 🚀 Start
- 📥 Download
- ✅ Success
- ❌ Error
- 🔄 Processing
- 🔍 Validation
- 💾 Saving
- 📊 Statistics
- 💡 Tips

## Testing Approach

The project includes `test_converter.py` for unit testing. Tests should cover:
- Template conversion logic
- Schema validation
- Duplicate detection and merging
- Error handling
- URL downloading

## Important Considerations

### When Making Changes

1. **Validation**: Always maintain compatibility with `schema_v3.json`
2. **Backward Compatibility**: Don't break existing command-line arguments
3. **Error Handling**: Add proper try-except blocks for network/file operations
4. **User Feedback**: Maintain clear Polish language error messages
5. **Statistics**: Update statistics display if adding new features

### Security Considerations

- URL validation before downloading
- JSON parsing error handling
- File system operations are local only
- No user authentication or sensitive data handling

### Performance Notes

- Large template files (1MB+) are handled in memory
- Network timeouts set to 30 seconds
- Duplicate detection is O(n) using dict lookups
- Pretty JSON formatting may increase file size

## Git Workflow

Current branch: `claude/update-claude-md-015g6rqJWGNewNqvpqT8r5NY`

### Making Changes
1. Develop on the designated branch
2. Test changes locally
3. Commit with clear messages
4. Push to origin with the correct branch name

### Commit Message Style
Based on recent commits:
- Clear, descriptive messages
- Focus on what changed and why
- Examples:
  - "Update converted Portainer templates v3"
  - "Fix validation errors in template conversion"
  - "Update URLs for selfhosted and technorabilia templates"

## Future Enhancements (TODO)

- [ ] Kubernetes templates support
- [x] Label migration from `restart_policy`
- [x] Official JSON Schema validation
- [x] Multiple source merging and deduplication
- [ ] GUI (graphical user interface)

## Getting Help

- Check `--help` for CLI usage
- Read README.md (Polish) or README.en.md (English)
- See USAGE_EXAMPLES.md for common scenarios
- Check CHANGELOG.md for version history

## License

Apache-2.0 - See LICENSE file for details
