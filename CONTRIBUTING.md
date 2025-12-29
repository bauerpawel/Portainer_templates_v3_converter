# Contributing to Portainer Templates v3 Converter

We warmly welcome contributions to the Portainer Templates v3 Converter project! This document provides guidelines and instructions for contributing to our project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Style Guide](#style-guide)
- [Questions or Need Help?](#questions-or-need-help)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code:

- Be respectful and inclusive
- Welcome diverse perspectives and experiences
- Provide constructive feedback
- Focus on collaboration and improvement
- Report any inappropriate behavior to the project maintainers

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Portainer_templates_v3_converter.git
   cd Portainer_templates_v3_converter
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/bauerpawel/Portainer_templates_v3_converter.git
   ```
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Environment

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup

1. **Install dependencies**:
   ```bash
   # Option 1: Using requirements.txt (recommended)
   pip install -r requirements.txt

   # Option 2: Manual installation
   pip install requests jsonschema
   ```

2. **Verify installation**:
   ```bash
   python portainer_converter.py --help
   ```

## Making Changes

### Before You Start

- Check existing [Issues](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues) to avoid duplicate work
- For major changes, open an Issue first to discuss your ideas
- Keep changes focused and atomic

### Types of Contributions

We welcome the following types of contributions:

#### 1. Bug Fixes
- Fix errors in template conversion
- Improve error handling
- Fix compatibility issues with Portainer v3

#### 2. New Features
- Support for additional template sources
- New conversion options or flags
- Performance improvements
- Better validation of templates

#### 3. Documentation
- Improve README and guides
- Add usage examples
- Translate documentation
- Fix typos and clarify explanations

#### 4. Template Sources
- Add support for new template repositories
- Update existing template source URLs
- Improve template discovery

#### 5. Testing
- Add test cases
- Improve test coverage
- Report edge cases

## Submitting Changes

### Step-by-Step Guide

1. **Make your changes**:
   - Keep commits small and logical
   - Write clear commit messages
   - Reference relevant Issues in commit messages (e.g., "Fixes #123")

2. **Test your changes**:
   ```bash
   # Run the converter with your changes
   python portainer_converter.py
   
   # Test with different template sources
   python portainer_converter.py --source lissy93
   ```

3. **Sync with upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**:
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch and provide a clear description
   - Reference any related Issues
   - Wait for review and feedback

### Pull Request Guidelines

Please ensure your PR includes:

- **Clear title**: Describe what your PR does
- **Description**: Explain the changes and why they're needed
- **Related Issues**: Link to any related Issues (e.g., "Fixes #123")
- **Testing**: Describe how the changes were tested
- **Screenshots/Examples**: If applicable, provide examples of the changes
- **No breaking changes**: Unless approved and clearly documented

### Commit Message Guidelines

Write clear, descriptive commit messages:

```
type(scope): subject

body

footer
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `style`: Code style changes
- `chore`: Build process, dependencies, or tooling

**Examples**:
- `feat(converter): add support for custom template sources`
- `fix(validation): correct JSON schema validation errors`
- `docs(readme): update installation instructions`

## Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Verify the bug with the latest version
- Try to reproduce the bug consistently

### How to Report

Open a [New Issue](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues/new) with:

1. **Clear title**: Brief description of the bug
2. **Description**: Detailed explanation of the issue
3. **Steps to reproduce**:
   ```
   1. Run command...
   2. Use option...
   3. Observe error...
   ```
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happens
6. **Environment**:
   - Python version
   - OS (Linux, Windows, macOS)
   - Any error messages or logs
7. **Additional context**: Screenshots, example templates, etc.

## Suggesting Enhancements

1. Check existing [Issues](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues) for similar suggestions
2. Open a [New Issue](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues/new) with:
   - **Clear title**: Brief description of the enhancement
   - **Detailed description**: Explain the feature and why it would be useful
   - **Use cases**: Describe scenarios where this would help
   - **Possible implementation**: If you have ideas (optional)

## Project Structure

```
Portainer_templates_v3_converter/
├── portainer_converter.py      # Main converter script
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── LICENSE                      # License information
├── .github/
│   └── workflows/               # GitHub Actions CI/CD
└── tests/                       # Test files (if present)
```

## Testing

### Manual Testing

1. **Test basic conversion**:
   ```bash
   python portainer_converter.py --source lissy93
   ```

2. **Test different sources**:
   ```bash
   python portainer_converter.py --source portainer-official
   python portainer_converter.py --source selfhosted
   python portainer_converter.py --source technorabilia
   ```

3. **Test error handling**:
   ```bash
   python portainer_converter.py --source invalid-source
   ```

### Creating Tests

When adding new features, please include tests:

```python
# Example test structure
def test_converter_with_source(source_name):
    # Test implementation
    pass

def test_error_handling():
    # Error handling tests
    pass
```

## Style Guide

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Use type hints where appropriate

### Example Code Style

```python
def convert_templates(source: str, output_format: str = "json") -> dict:
    """
    Convert Portainer v2 templates to v3 format.
    
    Args:
        source: Template source identifier
        output_format: Output format (json, yaml, etc.)
    
    Returns:
        Dictionary containing converted templates
    """
    # Implementation
    pass
```

### Documentation Style

- Use clear, concise language
- Provide examples for complex features
- Include both Polish and English documentation where applicable
- Keep documentation up-to-date with code changes

## Questions or Need Help?

- **Issues**: Ask questions in [Issues](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues)
- **Discussions**: Use GitHub Discussions if available
- **Email**: Contact the project maintainer if needed

---

## Thank You!

Thank you for considering contributing to Portainer Templates v3 Converter! Your contributions help make this project better for everyone.

Happy coding! 🚀

---

# Jak wnieść wkład w Portainer Templates v3 Converter

Zapraszamy do udziału w projekcie Portainer Templates v3 Converter! Ten dokument zawiera wskazówki i instrukcje dotyczące wkładu w nasz projekt.

## Spis treści

- [Kodeks postępowania](#kodeks-postępowania)
- [Rozpoczęcie pracy](#rozpoczęcie-pracy)
- [Środowisko programistyczne](#środowisko-programistyczne)
- [Wprowadzanie zmian](#wprowadzanie-zmian)
- [Przesyłanie zmian](#przesyłanie-zmian)
- [Zgłaszanie błędów](#zgłaszanie-błędów)
- [Sugerowanie ulepszeń](#sugerowanie-ulepszeń)
- [Struktura projektu](#struktura-projektu)
- [Testowanie](#testowanie)
- [Przewodnik stylu](#przewodnik-stylu)
- [Pytania lub pomoc?](#pytania-lub-pomoc)

## Kodeks postępowania

Ten projekt opiera się na Kodeksie postępowania. Poprzez uczestnictwo akceptujesz ten kodeks:

- Bądź szanujący i inkluzywny
- Powitaj różne perspektywy i doświadczenia
- Dostarczaj konstruktywne informacje zwrotne
- Skup się na współpracy i doskonaleniu
- Zgłaszaj niewłaściwe zachowanie opiekunom projektu

## Rozpoczęcie pracy

1. **Zforkuj repozytorium** na GitHubie
2. **Sklonuj swój fork** lokalnie:
   ```bash
   git clone https://github.com/TWOJA_NAZWA_UZYTKOWNIKA/Portainer_templates_v3_converter.git
   cd Portainer_templates_v3_converter
   ```
3. **Dodaj repozytorium upstream**:
   ```bash
   git remote add upstream https://github.com/bauerpawel/Portainer_templates_v3_converter.git
   ```
4. **Utwórz nową gałąź** dla swoich zmian:
   ```bash
   git checkout -b feature/nazwa-twojej-funkcji
   ```

## Środowisko programistyczne

### Wymagania

- Python 3.8 lub wyższy
- pip (menadżer pakietów Python)
- Git

### Instalacja

1. **Zainstaluj zależności**:
   ```bash
   # Opcja 1: Przy użyciu requirements.txt (zalecane)
   pip install -r requirements.txt

   # Opcja 2: Instalacja manualna
   pip install requests jsonschema
   ```

2. **Sprawdź instalację**:
   ```bash
   python portainer_converter.py --help
   ```

## Wprowadzanie zmian

### Zanim zaczniesz

- Sprawdź istniejące [Issues](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues), aby uniknąć zduplikowanej pracy
- W przypadku dużych zmian otwórz Issue, aby omówić swoje pomysły
- Utrzymuj zmiany skoncentrowane i atomiczne

### Rodzaje wkładów

Przyjmujemy następujące rodzaje wkładów:

#### 1. Poprawki błędów
- Naprawianie błędów w konwersji szablonów
- Улучшение obsługi błędów
- Naprawianie problemów ze zgodnością z Portainer v3

#### 2. Nowe funkcje
- Obsługa dodatkowych źródeł szablonów
- Nowe opcje lub flagi konwersji
- Ulepszenia wydajności
- Lepsza walidacja szablonów

#### 3. Dokumentacja
- Ulepszanie README i przewodników
- Dodawanie przykładów użycia
- Tłumaczenie dokumentacji
- Poprawianie błędów pisowni i wyjaśnianie tekstu

#### 4. Źródła szablonów
- Dodawanie obsługi nowych repozytoriów szablonów
- Aktualizowanie adresów URL istniejących źródeł szablonów
- Ulepszanie odkrywania szablonów

#### 5. Testowanie
- Dodawanie przypadków testowych
- Zwiększanie pokrycia testami
- Raportowanie przypadków granicznych

## Przesyłanie zmian

### Przewodnik krok po kroku

1. **Dokonaj swoich zmian**:
   - Trzymaj commity małe i logiczne
   - Pisz jasne wiadomości commita
   - Odwołuj się do odpowiednich Issues w wiadomościach commita (np. "Fixes #123")

2. **Przetestuj swoje zmiany**:
   ```bash
   # Uruchom konwerter ze swoimi zmianami
   python portainer_converter.py
   
   # Testuj z różnymi źródłami szablonów
   python portainer_converter.py --source lissy93
   ```

3. **Synchronizuj z upstream**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Wyślij do swojego forka**:
   ```bash
   git push origin feature/nazwa-twojej-funkcji
   ```

5. **Utwórz Pull Request**:
   - Przejdź do oryginalnego repozytorium
   - Kliknij "New Pull Request"
   - Wybierz swoją gałąź i podaj jasny opis
   - Odwołuj się do powiązanych Issues
   - Czekaj na przegląd i informacje zwrotne

### Wytyczne dla Pull Requestów

Upewnij się, że Twój PR zawiera:

- **Jasny tytuł**: Opisz, co robi Twój PR
- **Opis**: Wyjaśnij zmiany i dlaczego są potrzebne
- **Powiązane Issues**: Linkuj do powiązanych Issues (np. "Fixes #123")
- **Testowanie**: Opisz, jak zmiany były testowane
- **Zrzuty ekranu/Przykłady**: Jeśli dotyczy, podaj przykłady zmian
- **Brak zmian przełomowych**: Chyba że zatwierdzone i wyraźnie udokumentowane

### Wytyczne dla wiadomości commita

Pisz jasne, opisowe wiadomości commita:

```
typ(zakres): temat

treść

stopka
```

**Typy**:
- `feat`: Nowa funkcja
- `fix`: Poprawka błędu
- `docs`: Zmiany w dokumentacji
- `refactor`: Refaktoryzacja kodu
- `test`: Dodawanie lub aktualizowanie testów
- `style`: Zmiany stylu kodu
- `chore`: Proces budowania, zależności lub narzędzia

**Przykłady**:
- `feat(converter): add support for custom template sources`
- `fix(validation): correct JSON schema validation errors`
- `docs(readme): update installation instructions`

## Zgłaszanie błędów

### Przed zgłoszeniem

- Sprawdź, czy błąd nie został już zgłoszony
- Zweryfikuj błąd w najnowszej wersji
- Spróbuj odtworzyć błąd konsekwentnie

### Jak zgłosić

Otwórz [Nowy Problem](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues/new) z:

1. **Jasny tytuł**: Krótki opis błędu
2. **Opis**: Szczegółowe wyjaśnienie problemu
3. **Kroki do odtworzenia**:
   ```
   1. Uruchom polecenie...
   2. Użyj opcji...
   3. Zaobserwuj błąd...
   ```
4. **Oczekiwane zachowanie**: Co powinno się stać
5. **Rzeczywiste zachowanie**: Co się stało
6. **Środowisko**:
   - Wersja Pythona
   - System operacyjny (Linux, Windows, macOS)
   - Wszelkie komunikaty błędów lub dzienniki
7. **Dodatkowy kontekst**: Zrzuty ekranu, przykładowe szablony itp.

## Sugerowanie ulepszeń

1. Sprawdź istniejące [Issues](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues) pod kątem podobnych sugestii
2. Otwórz [Nowy Problem](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues/new) z:
   - **Jasny tytuł**: Krótki opis ulepszenia
   - **Szczegółowy opis**: Wyjaśnij funkcję i dlaczego byłaby przydatna
   - **Przypadki użycia**: Opisz scenariusze, w których by to pomogło
   - **Możliwa implementacja**: Jeśli masz pomysły (opcjonalne)

## Struktura projektu

```
Portainer_templates_v3_converter/
├── portainer_converter.py      # Główny skrypt konwertera
├── requirements.txt             # Zależności Pythona
├── README.md                    # Dokumentacja projektu
├── LICENSE                      # Informacje o licencji
├── .github/
│   └── workflows/               # GitHub Actions CI/CD
└── tests/                       # Pliki testów (jeśli istnieją)
```

## Testowanie

### Testowanie manualne

1. **Testuj podstawową konwersję**:
   ```bash
   python portainer_converter.py --source lissy93
   ```

2. **Testuj różne źródła**:
   ```bash
   python portainer_converter.py --source portainer-official
   python portainer_converter.py --source selfhosted
   python portainer_converter.py --source technorabilia
   ```

3. **Testuj obsługę błędów**:
   ```bash
   python portainer_converter.py --source invalid-source
   ```

### Tworzenie testów

Dodając nowe funkcje, prosimy include testów:

```python
# Przykładowa struktura testu
def test_converter_with_source(source_name):
    # Implementacja testu
    pass

def test_error_handling():
    # Testy obsługi błędów
    pass
```

## Przewodnik stylu

### Styl kodu Python

- Postępuj zgodnie z wytycznymi [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Użyj 4 spacji do wcięcia
- Maksymalna długość linii: 100 znaków
- Używaj znaczących nazw zmiennych i funkcji
- Dodaj docstringi do funkcji i klas
- Użyj wskazówek typów w stosownych miejscach

### Przykładowy styl kodu

```python
def convert_templates(source: str, output_format: str = "json") -> dict:
    """
    Konwertuj szablony Portainer v2 do formatu v3.
    
    Args:
        source: Identyfikator źródła szablonu
        output_format: Format wyjściowy (json, yaml, itp.)
    
    Returns:
        Słownik zawierający skonwertowane szablony
    """
    # Implementacja
    pass
```

### Styl dokumentacji

- Używaj jasnego, zwięzłego języka
- Podaj przykłady dla złożonych funkcji
- Dołącz dokumentację zarówno w języku polskim jak i angielskim, gdzie ma to zastosowanie
- Utrzymuj dokumentację na bieżąco ze zmianami kodu

## Pytania lub pomoc?

- **Issues**: Zadawaj pytania w [Issues](https://github.com/bauerpawel/Portainer_templates_v3_converter/issues)
- **Dyskusje**: Użyj GitHub Discussions, jeśli dostępne
- **Email**: Skontaktuj się z opiekunem projektu w razie potrzeby

---

## Dziękujemy!

Dziękujemy za rozważenie wkładu w Portainer Templates v3 Converter! Twoje wkłady pomagają uczynić ten projekt lepszym dla wszystkich.

Powodzenia w kodowaniu! 🚀
