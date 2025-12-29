# Security Policy

## Reporting a Vulnerability

**Please do not publicly disclose security vulnerabilities.** We take security seriously and appreciate responsible disclosure.

If you discover a security vulnerability in Portainer Templates v3 Converter, please report it to us confidentially by:

### Method 1: GitHub Security Advisory (Recommended)
1. Go to the [Security](https://github.com/bauerpawel/Portainer_templates_v3_converter/security) tab
2. Click "Report a vulnerability"
3. Fill out the form with details of the vulnerability
4. Submit your report

### Method 2: Email
Send an email to the project maintainer with:
- **Subject**: `[SECURITY] Vulnerability Report in Portainer Templates v3 Converter`
- **Contact**: [Add maintainer email - e.g., your email]

### Method 3: Private Security Issue
If available for this repository, use the private security issue feature on GitHub to report vulnerabilities.

## What to Include in Your Report

Please provide as much detail as possible to help us understand and address the issue:

- **Description**: Clear explanation of the vulnerability
- **Type**: What type of security issue is it? (e.g., injection, information disclosure, authentication bypass, etc.)
- **Location**: Where in the code the vulnerability exists
- **Steps to reproduce**: How to trigger the vulnerability
- **Impact**: What could an attacker do with this vulnerability?
- **Severity**: Your assessment of the severity (Critical, High, Medium, Low)
- **Proof of concept**: A minimal example demonstrating the vulnerability (optional but helpful)
- **Your contact information**: So we can follow up with you

## Security Vulnerability Severity Levels

We use the following severity classifications:

### Critical
- Remote code execution
- Authentication bypass
- Complete data breach
- Privilege escalation
- Immediate action required

### High
- Significant information disclosure
- Serious denial of service
- Significant data manipulation
- Requires prompt patching

### Medium
- Limited information disclosure
- Partial functionality compromise
- Requires patching in next release

### Low
- Minor information disclosure
- Edge case vulnerabilities
- Can be patched in regular updates

## Our Response Process

1. **Acknowledgment** (within 48-72 hours)
   - We acknowledge receipt of your report
   - Confirm we are investigating the issue

2. **Investigation** (1-2 weeks)
   - We analyze the vulnerability
   - Determine the scope and impact
   - Identify affected versions

3. **Remediation** (timing depends on severity)
   - We develop a patch
   - Test the fix thoroughly
   - Prepare a security release

4. **Disclosure** (coordinated)
   - We provide you with a timeline for the fix
   - We release the patch
   - We publish a security advisory
   - We credit you (if desired)

## Timelines

- **Critical vulnerabilities**: Patch released within 1 week
- **High severity**: Patch released within 2 weeks
- **Medium severity**: Patch released within 1 month
- **Low severity**: Patch released in next regular release

## Security Best Practices

When using Portainer Templates v3 Converter, follow these security practices:

### 1. Keep Software Updated
- Regularly update to the latest version
- Subscribe to security notifications
- Monitor the repository for security advisories

### 2. Input Validation
- Always validate and sanitize template inputs
- Be cautious with user-provided template URLs
- Verify template sources before adding them

### 3. Access Control
- Limit who can modify template configurations
- Use appropriate file permissions
- Protect credentials and sensitive data

### 4. Network Security
- Use HTTPS for template downloads
- Verify SSL/TLS certificates
- Disable insecure protocols

### 5. Code Review
- Review templates before deployment
- Check for malicious or suspicious configurations
- Use version control to track changes

### 6. Secrets Management
- Never commit secrets to repositories
- Use environment variables for sensitive data
- Use secret management tools when appropriate

### 7. Dependency Management
- Keep dependencies up to date
- Monitor for vulnerable dependencies
- Use tools like `pip audit` to check for vulnerabilities

```bash
# Example: Check for vulnerable dependencies
pip install pip-audit
pip-audit
```

## Supported Versions

We provide security updates for:

| Version | Status | Support Until |
|---------|--------|---------------|
| Latest Release | Active | Current + 6 months |
| Previous Release | Limited | 3 months |
| Older versions | Not supported | N/A |

## Security Advisories

Security advisories are published on:
- [GitHub Security Advisories](https://github.com/bauerpawel/Portainer_templates_v3_converter/security/advisories)
- Project README

## Vulnerability Disclosure Policy

We follow a **90-day responsible disclosure** policy:

1. **Day 0**: Vulnerability reported
2. **Day 1-2**: Initial response and acknowledgment
3. **Day 30**: Patch should be ready for release
4. **Day 60**: Patch released if possible
5. **Day 90**: Public disclosure (even if patch not ready)

If you need a different timeline, please discuss it with us in your report.

## Hall of Fame

We appreciate security researchers who responsibly disclose vulnerabilities. With permission, we credit them in our security advisories:

Contributors who report security issues may be listed in our Hall of Fame (opt-in).

## Questions?

If you have questions about our security policy or need clarification, please contact the project maintainer.

---

# Polityka bezpieczeństwa

## Zgłaszanie luki w zabezpieczeniach

**Prosimy nie ujawniać publicznie luk w zabezpieczeniach.** Traktujemy bezpieczeństwo poważnie i doceniamy odpowiedzialne ujawnianie.

Jeśli odkryjesz lukę bezpieczeństwa w Portainer Templates v3 Converter, prosimy zgłosić ją nam poufnie poprzez:

### Metoda 1: GitHub Security Advisory (Zalecana)
1. Przejdź do karty [Security](https://github.com/bauerpawel/Portainer_templates_v3_converter/security)
2. Kliknij "Report a vulnerability"
3. Wypełnij formularz ze szczegółami luki
4. Prześlij raport

### Metoda 2: Email
Wyślij wiadomość e-mail do opiekuna projektu z:
- **Temat**: `[BEZPIECZEŃSTWO] Raport o luce w Portainer Templates v3 Converter`
- **Kontakt**: [Dodaj email opiekuna - np. Twój email]

### Metoda 3: Prywatny problem bezpieczeństwa
Jeśli dostępne dla tego repozytorium, użyj funkcji prywatnego problemu bezpieczeństwa na GitHub-ie do zgłoszenia luk.

## Co uwzględnić w raporcie

Prosimy podać jak najwięcej szczegółów, aby pomóc nam zrozumieć i rozwiązać problem:

- **Opis**: Jasne wyjaśnienie luki w zabezpieczeniach
- **Typ**: Jaki typ problemu bezpieczeństwa to jest? (np. injection, ujawnienie informacji, obejście uwierzytelnienia, itp.)
- **Lokalizacja**: Gdzie w kodzie istnieje luka
- **Kroki do odtworzenia**: Jak sprowokować lukę
- **Wpływ**: Co atakujący mógłby zrobić z tą luką?
- **Waga**: Twoja ocena wagi (Krytyczna, Wysoka, Średnia, Niska)
- **Proof of concept**: Minimalny przykład demonstrujący lukę (opcjonalne, ale przydatne)
- **Twoje informacje kontaktowe**: Abyśmy mogli się z tobą skontaktować

## Poziomy wagi luk bezpieczeństwa

Używamy następujących klasyfikacji wagi:

### Krytyczna
- Zdalne wykonywanie kodu
- Obejście uwierzytelnienia
- Kompletne naruszenie danych
- Eskalacja uprawnień
- Wymagane natychmiastowe działanie

### Wysoka
- Istotne ujawnienie informacji
- Poważna odmowa usługi
- Istotna manipulacja danymi
- Wymaga pilnego łatania

### Średnia
- Ograniczone ujawnienie informacji
- Częściowa utrata funkcjonalności
- Wymaga łatania w następnym wydaniu

### Niska
- Drobne ujawnienie informacji
- Luki granicznego przypadku
- Mogą być łatane w regularnych aktualizacjach

## Nasz proces odpowiedzi

1. **Potwierdzenie** (w ciągu 48-72 godzin)
   - Potwierdzamy otrzymanie Twojego raportu
   - Potwierdzamy, że badamy problem

2. **Dochodzenie** (1-2 tygodnie)
   - Analizujemy lukę
   - Określamy zakres i wpływ
   - Identyfikujemy dotknięte wersje

3. **Naprawianie** (czas zależy od wagi)
   - Opracowujemy poprawkę
   - Dokładnie testujemy naprawę
   - Przygotowujemy wydanie bezpieczeństwa

4. **Ujawnienie** (skoordynowane)
   - Dostarczamy Ci harmonogram naprawy
   - Wydajemy poprawkę
   - Publikujemy poradnik bezpieczeństwa
   - Dziękujemy Ci (jeśli chcesz)

## Harmonogramy

- **Luki krytyczne**: Poprawka wydana w ciągu tygodnia
- **Wysoka waga**: Poprawka wydana w ciągu 2 tygodni
- **Średnia waga**: Poprawka wydana w ciągu miesiąca
- **Niska waga**: Poprawka wydana w następnym regularnym wydaniu

## Najlepsze praktyki bezpieczeństwa

Korzystając z Portainer Templates v3 Converter, postępuj zgodnie z następującymi praktykami bezpieczeństwa:

### 1. Utrzymuj oprogramowanie na bieżąco
- Regularnie aktualizuj do najnowszej wersji
- Subskrybuj powiadomienia o bezpieczeństwie
- Monitoruj repozytorium w poszukiwaniu porad bezpieczeństwa

### 2. Walidacja wejścia
- Zawsze waliduj i oczyszczaj dane wejściowe szablonu
- Bądź ostrożny z adresami URL szablonów dostarczanymi przez użytkownika
- Sprawdź źródła szablonów przed ich dodaniem

### 3. Kontrola dostępu
- Ogranicz, kto może modyfikować konfiguracje szablonów
- Użyj odpowiednich uprawnień pliku
- Chroń poświadczenia i dane wrażliwe

### 4. Bezpieczeństwo sieci
- Używaj HTTPS do pobierania szablonów
- Weryfikuj certyfikaty SSL/TLS
- Wyłącz niebezpieczne protokoły

### 5. Przegląd kodu
- Przejrzyj szablony przed wdrożeniem
- Sprawdź pod kątem złośliwych lub podejrzanych konfiguracji
- Użyj kontroli wersji do śledzenia zmian

### 6. Zarządzanie sekretami
- Nigdy nie commituj sekretów do repozytoriów
- Używaj zmiennych środowiskowych dla danych wrażliwych
- Używaj narzędzi do zarządzania sekretami w razie potrzeby

### 7. Zarządzanie zależnościami
- Utrzymuj zależności na bieżąco
- Monitoruj wrażliwe zależności
- Użyj narzędzi takich jak `pip audit` do sprawdzenia luk

```bash
# Przykład: Sprawdzenie wrażliwych zależności
pip install pip-audit
pip-audit
```

## Obsługiwane wersje

Zapewniamy aktualizacje bezpieczeństwa dla:

| Wersja | Status | Wsparcie do |
|--------|--------|------------|
| Najnowsze wydanie | Aktywne | Obecne + 6 miesięcy |
| Poprzednie wydanie | Ograniczone | 3 miesiące |
| Starsze wersje | Nieobsługiwane | N/A |

## Porady bezpieczeństwa

Porady bezpieczeństwa są publikowane na:
- [GitHub Security Advisories](https://github.com/bauerpawel/Portainer_templates_v3_converter/security/advisories)
- README projektu

## Polityka ujawniania luk

Stosujemy politykę **odpowiedzialnego ujawniania w ciągu 90 dni**:

1. **Dzień 0**: Zgłoszenie luki
2. **Dzień 1-2**: Początkowa odpowiedź i potwierdzenie
3. **Dzień 30**: Poprawka powinna być gotowa do wydania
4. **Dzień 60**: Poprawka wydana, jeśli to możliwe
5. **Dzień 90**: Publiczne ujawnienie (nawet jeśli poprawka nie jest gotowa)

Jeśli potrzebujesz innego harmonogramu, omów to z nami w swoim raporcie.

## Galeria sław

Doceniamy badaczy bezpieczeństwa, którzy odpowiedzialnie ujawniają luki. Za zgodą ich udzielamy im kredytu w naszych poradach bezpieczeństwa:

Współautorzy, którzy zgłaszają problemy bezpieczeństwa, mogą być wymienieni w naszej Galerii sław (opcjonalnie).

## Pytania?

Jeśli masz pytania dotyczące naszej polityki bezpieczeństwa lub potrzebujesz wyjaśnień, skontaktuj się z opiekunem projektu.
