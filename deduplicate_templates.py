#!/usr/bin/env python3
"""
Script to remove duplicate templates from the converted Portainer templates v3 file.
Duplicates are identified by the 'name' field.
For templates with null names, the title is used to generate a name.
"""

import json
import sys
from typing import Dict, Any, List

def normalize_name(title: str) -> str:
    """Convert title to a normalized name (lowercase, spaces to hyphens)"""
    return title.lower().replace(' ', '-').replace('_', '-')

def calculate_completeness_score(template: Dict[str, Any]) -> int:
    """
    Calculate a score representing how complete a template is.
    Higher score = more complete template.
    """
    score = 0

    # Basic fields
    if template.get('description'):
        score += 10
    if template.get('logo'):
        score += 5
    if template.get('env'):
        score += len(template.get('env', []))
    if template.get('volumes'):
        score += len(template.get('volumes', []))
    if template.get('ports'):
        score += len(template.get('ports', []))
    if template.get('categories'):
        score += len(template.get('categories', []))

    # Prefer type 1 (containers) over type 3 (stacks) - they're usually more detailed
    template_type = template.get('type', 0)
    if template_type == 1:
        score += 20
    elif template_type == 3:
        score += 10

    # Repository info
    if template.get('repository'):
        score += 5

    return score

def deduplicate_templates(templates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate templates based on the 'name' field.
    For duplicates, keep the most complete one.
    """
    # First pass: fix null names
    for template in templates:
        if template.get('name') is None and template.get('title'):
            # Generate name from title
            template['name'] = normalize_name(template['title'])

    # Second pass: remove duplicates
    seen_names = {}  # name -> template
    unique_templates = []
    duplicates_removed = 0

    for template in templates:
        name = template.get('name')

        if not name:
            # Still no name after fixing - keep it but warn
            print(f"⚠️  Warning: Template without name or title found (id: {template.get('id')})")
            unique_templates.append(template)
            continue

        if name in seen_names:
            # Duplicate found - compare and keep the better one
            existing = seen_names[name]
            existing_score = calculate_completeness_score(existing)
            new_score = calculate_completeness_score(template)

            if new_score > existing_score:
                # Replace with the better one
                seen_names[name] = template
                # Find and replace in unique_templates
                for i, t in enumerate(unique_templates):
                    if t.get('name') == name:
                        unique_templates[i] = template
                        break
                print(f"   Replaced '{name}' with more complete version (score: {existing_score} -> {new_score})")
            else:
                print(f"   Skipped duplicate '{name}' (score: {new_score} vs {existing_score})")

            duplicates_removed += 1
        else:
            # New unique template
            seen_names[name] = template
            unique_templates.append(template)

    return unique_templates, duplicates_removed

def main():
    input_file = 'templates_v3_converted.json'
    output_file = 'templates_v3_converted.json'

    print("🔄 Deduplicating Portainer templates...")
    print("="*60)

    # Load the file
    print(f"📥 Loading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        sys.exit(1)

    original_count = len(data.get('templates', []))
    print(f"✅ Loaded {original_count} templates")
    print()

    # Deduplicate
    print("🔍 Removing duplicates...")
    unique_templates, duplicates_removed = deduplicate_templates(data['templates'])

    print()
    print("📊 Results:")
    print(f"   • Original templates: {original_count}")
    print(f"   • Unique templates: {len(unique_templates)}")
    print(f"   • Duplicates removed: {duplicates_removed}")
    print()

    # Update data
    data['templates'] = unique_templates

    # Reassign IDs to be sequential
    print("🔢 Reassigning template IDs...")
    for idx, template in enumerate(data['templates'], 1):
        template['id'] = idx

    # Save
    print(f"💾 Saving to {output_file}...")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ File saved successfully!")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)

    print()
    print("🎉 Deduplication complete!")
    print()

    # Show some statistics
    print("📈 Top 10 most common applications (after deduplication):")
    name_counts = {}
    for template in data['templates']:
        name = template.get('name', 'unknown')
        name_counts[name] = name_counts.get(name, 0) + 1

    for name, count in sorted(name_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        if count > 1:
            print(f"   ⚠️  {name}: {count} (still duplicate!)")
        else:
            print(f"   ✅ {name}: {count}")

if __name__ == '__main__':
    main()
