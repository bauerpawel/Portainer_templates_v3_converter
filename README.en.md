# Portainer Templates Converter v2 → v3

🔄 **Python application for converting Portainer templates from v2 to v3 format**

[🇵🇱 Polish version](README.md) | **🇬🇧 English version**

---

## Description

This application automatically converts Portainer application templates from v2 to v3 format, which is compatible with the latest versions of Portainer.io.

### Main differences between formats:

| Feature           | v2 Format             | v3 Format         |
|-------------------|-----------------------|-------------------|
| Version           | `"version": "2"`      | `"version": "3"`  |
| Template ID       | ❌ None               | ✅ `"id": 123`    |
| Labels            | ❌ None               | ✅ `"labels": []` |
| Restart Policy    | ✅ `"restart_policy"` | ❌ Removed        |
| Platform          | ✅ `"platform"`       | ❌ Removed        |

## Requirements

- Python 3.6+
- `requests` library
- `jsonschema` library (for JSON Schema validation)

## Installation

1. **Clone or download files:**
   ```bash
   # Option 1: Clone repository
   git clone https://github.com/bauerpawel/Portainer_templates_v3_converter.git
   cd Portainer_templates_v3_converter

   # Option 2: Download main file
   wget https://raw.githubusercontent.com/bauerpawel/Portainer_templates_v3_converter/refs/heads/main/portainer_converter.py

   # Option 3: Or copy code to portainer_converter.py file
   ```

2. **Install required libraries:**
   ```bash
   # Option 1: From requirements.txt (recommended)
   pip install -r requirements.txt

   # Option 2: Manual installation
   pip install requests jsonschema
   ```

## Available Template Sources

The application has a built-in list of popular Portainer template sources:

| Key | Name | Description |
|-----|------|-------------|
| `lissy93` | Lissy93 Templates | Large collection of over 470 application templates |
| `portainer-official` | Portainer Official | Official templates from Portainer team |
| `selfhosted` | SelfHosted.show | Templates for self-hosted applications |
| `technorabilia` | Technorabilia | Templates based on LinuxServer.io images |

### Display Available Sources
```bash
python portainer_converter.py --list-sources
```

## Usage

### Basic Conversion
```bash
python portainer_converter.py
```
Downloads templates from default source (Lissy93) and saves as `templates_v3_converted.json`

### Custom Source URL
```bash
python portainer_converter.py --url "https://your-custom-url.com/templates.json"
```

### Custom Output File
```bash
python portainer_converter.py --output "my_templates_v3.json"
```

### Merging Multiple Sources
```bash
# Merge two known sources (by key)
python portainer_converter.py --sources lissy93 portainer-official

# Merge all known sources
python portainer_converter.py --all-sources

# Merge known source with custom URL
python portainer_converter.py --sources lissy93 "https://example.com/templates.json"
```

### Full Configuration
```bash
python portainer_converter.py \
  --sources lissy93 selfhosted technorabilia \
  --output "merged_templates_v3.json"
```

### Help
```bash
python portainer_converter.py --help
```

## Example Output

```
🚀 Portainer Templates Converter v2 -> v3
==================================================
⏰ Start: 2025-08-27 12:00:00

📥 Downloading v2 template from: https://raw.githubusercontent.com/...
✅ Downloaded 472 templates
🔄 Starting v2 -> v3 conversion...
✅ Conversion completed! Converted 472 templates
🔍 Validating v3 format...
🔍 Validating with JSON Schema...
✅ JSON Schema validation completed successfully
🔍 Additional business checks...
✅ Validation completed successfully
💾 Saving to file: templates_v3_converted.json
✅ File saved successfully: templates_v3_converted.json (1.2 MB)

📊 Conversion Statistics:
   • Source templates (v2): 472
   • Target templates (v3): 472
   • Template types:
     - Containers: 450
     - Swarm Stacks: 22
   • Top 5 categories:
     - Other: 89
     - Tools: 67
     - Video: 45
     - Music: 32
     - Books: 28

📋 Summary:
   • Source: https://raw.githubusercontent.com/Lissy93/portainer-templates/...
   • Source version: v2
   • Target version: v3
   • Number of templates: 472
   • Output file: templates_v3_converted.json

🎉 Conversion completed successfully!

💡 How to use:
   1. Copy 'templates_v3_converted.json' file to server
   2. In Portainer go to Settings -> App Templates
   3. Paste URL to file or use local file
   4. Save settings and enjoy v3 templates!
```

## How to Use in Portainer

1. **Run conversion:**
   ```bash
   python portainer_converter.py
   ```

2. **Transfer file to web server (optional):**
   ```bash
   # Example - copy to Apache/Nginx server
   cp templates_v3_converted.json /var/www/html/
   ```

3. **Configure Portainer:**
   - Open Portainer interface
   - Go to **Settings** → **App Templates**
   - In **URL** field paste path to file:
     ```
     https://your-server.com/templates_v3_converted.json
     ```
   - Or for local file:
     ```
     file:///path/to/templates_v3_converted.json
     ```
   - Click **Save settings**

4. **Use templates:**
   - Go to **App Templates**
   - v3 templates should now be available!

## Technical Details

### Conversion Process

1. **Download v2 templates** from provided URL (or multiple sources)
2. **Merge sources** (if multiple selected):
   - Download templates from all sources
   - Detect duplicates by combination of `(name, image)`
   - Merge categories from duplicates
   - Choose longer description
   - Remove duplicates
3. **Convert each template:**
   - Add unique `id` field
   - Add `labels` field with `restart_policy` migration
   - Remove `restart_policy` and `platform` fields
   - Copy remaining fields
4. **Validate** v3 format correctness:
   - Validation with official JSON Schema (`schema_v3.json` file)
   - Check required fields
   - Check data types
   - Additional business checks (old v2 fields, etc.)
5. **Save** to JSON file with pretty formatting

### Merging Multiple Sources

When merging templates from multiple sources:

- **Duplicate detection**: Templates are compared by combination of `name` and `image` fields (case-insensitive)
- **Data merging**: When duplicate found:
  - Categories are merged (unique values from both sources)
  - Longer description is chosen
  - Other fields from first occurrence are preserved
- **Statistics**: After merging, statistics showing number of removed duplicates are displayed

### JSON Schema Validation

The application uses official JSON Schema for Portainer templates v3 (`schema_v3.json`), which provides:

- **Automatic structure validation** - checks if all required fields are present
- **Data type validation** - verifies if fields have correct types (string, integer, array, etc.)
- **Format validation** - checks validity of URLs, port patterns, etc.
- **Detailed error messages** - precisely indicates what is incorrect

If `schema_v3.json` file is not available, JSON Schema validation will be skipped, but basic validation will still be performed.

### Supported Template Fields

#### Copied without changes:
- `categories` - application categories
- `description` - application description
- `env` - environment variables
- `image` - Docker image
- `logo` - application logo
- `maintainer` - template maintainer
- `name` - application name
- `ports` - ports to forward
- `title` - template title
- `type` - template type (1=container, 2=stack)
- `volumes` - volumes
- `note` - additional information
- `repository` - Git repository

#### Added in v3:
- `id` - unique identifier (number)
- `labels` - Docker labels (empty list)

#### Removed from v2:
- `restart_policy` - restart policy
- `platform` - platform (linux/windows)

## Troubleshooting

### File Download Error
```
❌ File download error: HTTPSConnectionPool...
```
**Solution:** Check internet connection and URL validity.

### JSON Parsing Error
```
❌ JSON parsing error: Expecting value...
```
**Solution:** Ensure URL contains valid JSON file.

### Validation Error
```
❌ Validation errors: Missing 'id' field in template 1
```
**Solution:** This indicates a bug in converter code - report issue.

### Portainer Doesn't See Templates
1. Check if file is accessible at provided URL
2. Check if Portainer has network/file access
3. Check Portainer logs for errors

## Contributing and Development

Report bugs and suggestions via Issues. Pull requests are welcome!

### TODO / Planned Features:
- [ ] Kubernetes templates support
- [x] Labels migration from `restart_policy` field
- [x] Validation with official JSON schema
- [x] Support for additional template sources (multiple source merging, duplicate removal)
- [ ] GUI (graphical user interface)

## License

Apache-2.0 license - see LICENSE file for details.

## Author

Application created for Portainer v2 → v3 template conversion.

---
⭐ If this application helped you, leave a star!
