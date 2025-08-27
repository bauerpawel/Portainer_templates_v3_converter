# Przykłady użycia Portainer Templates Converter

## Podstawowe użycie
```bash
python portainer_converter.py
```

## Z własnym URL źródłowym
```bash
python portainer_converter.py --url "https://example.com/templates.json"
```

## Z własnym plikiem wyjściowym
```bash
python portainer_converter.py --output "my_templates_v3.json"
```

## Pełna konfiguracja
```bash
python portainer_converter.py \
  --url "https://raw.githubusercontent.com/example/templates.json" \
  --output "custom_templates_v3.json"
```

## Pomoc
```bash
python portainer_converter.py --help
```

## Instalacja wymagań
```bash
pip install requests
```
