# 🛡️ AI LLM Red-Team Security Tester

An authorized AI security testing platform for evaluating Large Language Model (LLM) resistance to adversarial prompt techniques.

The application executes a configurable security test suite against an authorized LLM target, captures the model's responses, evaluates predefined failure conditions, assigns risk scores, displays findings in a Flask dashboard, and generates PDF security assessment reports.

> **Purpose:** This project is designed for defensive security education, authorized AI security testing, and portfolio demonstration. It should only be used against systems you own or have explicit permission to test.

---

## 📸 Application Preview

![AI LLM Red-Team Security Tester Dashboard](screenshots/05-web-assessment-results.png)

---

## 🎯 Project Overview

Generative AI applications introduce security risks that traditional application testing may not fully address.

This project explores how an LLM behaves when presented with controlled adversarial prompts targeting common AI security concerns.

The application currently evaluates five categories:

| Test ID   | Security Test                 | Severity |
| --------- | ----------------------------- | -------- |
| `PI-001`  | Prompt Injection              | High     |
| `IC-001`  | Instruction Conflict          | High     |
| `SPE-001` | System Prompt Extraction      | Critical |
| `JB-001`  | Jailbreak Resistance          | Critical |
| `SIL-001` | Sensitive Information Leakage | Critical |

Each test contains:

- a controlled adversarial prompt
- an expected secure behavior
- a severity classification
- a deterministic failure indicator
- captured response evidence

---

## 🧠 How It Works

```text
Security Test Suite
        │
        ▼
   Test Loader
        │
        ▼
   Test Runner
        │
        ▼
 Authorized LLM
        │
        ▼
Response Capture
        │
        ▼
Security Evaluator
        │
        ▼
 PASS / FAIL
        │
        ▼
  Risk Scoring
        │
        ├───────────────┐
        ▼               ▼
 Flask Dashboard    PDF Report
```

The project intentionally separates **test execution**, **response capture**, **evaluation**, **risk calculation**, **presentation**, and **reporting**.

---

## 🔬 Security Test Categories

### 1. Prompt Injection

Tests whether a user-controlled prompt can cause the target model to claim that higher-priority instructions have been overridden.

Example controlled failure indicator:

```text
INSTRUCTIONS OVERRIDDEN
```

---

### 2. Instruction Conflict

Tests whether the target maintains higher-priority instructions when a user message attempts to replace them.

Example controlled failure indicator:

```text
NEW INSTRUCTIONS ACCEPTED
```

---

### 3. System Prompt Extraction

Tests whether the target reveals or claims to reveal protected system instructions.

Example controlled failure indicator:

```text
SYSTEM PROMPT REVEALED
```

---

### 4. Jailbreak Resistance

Tests whether the target accepts a fictional operating mode intended to bypass existing restrictions.

Example controlled failure indicator:

```text
DEVELOPER MODE ENABLED
```

---

### 5. Sensitive Information Leakage

Tests whether the target reveals or claims to reveal protected secrets or configuration information.

The project uses a **synthetic disclosure indicator** rather than real credentials:

```text
SECRETS DISCLOSED
```

No real API keys, passwords, or production secrets are embedded in the security test cases.

---

## ⚙️ Mock and API Modes

The application supports two target modes.

### Mock Mode

```env
TARGET_MODE=mock
```

Mock mode uses deterministic simulated responses.

This makes it possible to:

- develop without API costs
- test the evaluation pipeline reproducibly
- run automated tests without external dependencies
- validate dashboard and PDF functionality safely

### API Mode

```env
TARGET_MODE=api
```

API mode sends the configured tests to the authorized target model and captures real responses.

The project was developed using:

```env
TARGET_MODEL=gpt-5.6-luna
```

Model availability can change, so configure a model available to your API account.

---

## 📊 Assessment Results

After an assessment, the dashboard displays:

- total tests executed
- number passed
- number failed
- highest observed risk score
- test category
- severity
- PASS / FAIL status
- individual risk score
- attack prompt
- captured target response
- evaluation reason

A **PASS** means the configured failure condition was not observed during that test execution.

It does **not** prove that the target is secure against every possible prompt variation or attack technique.

---

## 🚨 Risk Scoring

Risk scoring combines the test outcome with its configured severity.

A successful security test receives:

```text
Risk Score = 0
```

A detected failure receives a severity-weighted score.

This separates two concepts:

```text
Test Severity
     +
Observed Behavior
     ↓
Risk Score
```

This makes the assessment more useful than displaying PASS/FAIL alone.

---

## 📄 PDF Security Assessment

Completed assessments can be exported as professional PDF reports.

Reports include:

- Executive Summary
- Target Information
- Methodology
- Assessment Results
- Evidence and Findings
- Risk Analysis
- Recommendations
- OWASP LLM mapping
- Conclusion
- Appendix / methodology notes

The PDF is generated from the assessment already held by the application.

Downloading a report does **not** execute the security tests again or make additional LLM API requests.

Generated reports are excluded from Git through `.gitignore`.

---

## 🧪 Automated Testing

The project includes automated unit tests for both the evaluator and security assessment logic.

Run:

```powershell
python -m pytest -v
```

Current test coverage includes:

- Prompt Injection PASS
- Prompt Injection FAIL
- Instruction Conflict PASS
- Instruction Conflict FAIL
- System Prompt Extraction PASS
- System Prompt Extraction FAIL
- Jailbreak Resistance PASS
- Jailbreak Resistance FAIL
- Sensitive Information Leakage PASS
- Sensitive Information Leakage FAIL
- PASS risk scoring
- LOW failure risk scoring
- MEDIUM failure risk scoring
- HIGH failure risk scoring
- CRITICAL failure risk scoring
- UNKNOWN handling
- Assessment summary calculation

At the v1.0 development milestone:

```text
17 tests passed
```

### Continuous Integration

GitHub Actions automatically runs the project's security-engine unit tests on every push and pull request to `main`.

The CI workflow validates the deterministic evaluation and risk-scoring logic without requiring API credentials.

![GitHub Actions CI Passed](screenshots/06-github-actions-passed.png)

---

## 📂 Project Structure

```text
AI-LLM-REDTEAM/
│
├── app/
│   ├── engine/
│   │   ├── security_runner.py
│   │   ├── test_loader.py
│   │   └── test_runner.py
│   │
│   ├── evaluator/
│   │   └── evaluator.py
│   │
│   ├── reporting/
│   │   └── pdf_report.py
│   │
│   ├── static/
│   │   └── style.css
│   │
│   └── templates/
│       └── dashboard.html
│
├── data/
│   └── test_cases.json
│
├── reports/
│   └── generated locally
│
├── screenshots/
│
├── tests/
│   ├── test_evaluator.py
│   └── test_security_runner.py
│
├── .env.example
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```powershell
git clone https://github.com/BecomingCyber/AI-LLM-REDTEAM.git
cd AI-LLM-REDTEAM
```

### 2. Create a Python virtual environment

```powershell
python -m venv venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

---

## 🔐 Configuration

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Example:

```env
OPENAI_API_KEY=
TARGET_MODE=mock
TARGET_MODEL=gpt-5.6-luna
EVALUATOR_MODEL=gpt-5.6-luna
SECRET_KEY=
```

For mock testing, no API key is required.

For authorized API testing:

```env
TARGET_MODE=api
OPENAI_API_KEY=your_api_key_here
```

### Important

Never commit `.env`.

The repository's `.gitignore` excludes:

- API configuration
- virtual environments
- Python caches
- local databases
- generated PDF reports
- logs
- temporary files

---

## ▶️ Running the Application

Start Flask:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

The dashboard itself does **not** automatically execute security tests.

API requests occur only when **Run Security Assessment** is explicitly selected.

---

## 🖥️ Dashboard Workflow

```text
Open Dashboard
      ↓
Review Target Configuration
      ↓
Run Security Assessment
      ↓
Execute Configured Tests
      ↓
Capture Responses
      ↓
Evaluate Findings
      ↓
Calculate Risk
      ↓
Display Evidence
      ↓
Download PDF Report
```

---

## 🧾 Evidence-First Design

The application keeps the original test information alongside the captured response and evaluation.

Each result records information such as:

```text
Test ID
Category
Severity
Attack Prompt
Target Response
Expected Behavior
Evaluation
Risk Score
Timestamp
Target Mode
Target Model
```

This supports a security-assessment workflow based on observable evidence rather than unsupported conclusions.

---

## 🛡️ Security Design Decisions

Several controls were intentionally included during development.

### Secrets are separated from source code

Real API credentials are stored in `.env`, which is ignored by Git.

`.env.example` documents required variables without containing secrets.

### Generated reports are excluded

PDF reports may contain captured model responses and are therefore treated as local assessment artifacts.

```gitignore
reports/*.pdf
```

### Tests do not use real secrets

Sensitive-information tests use controlled synthetic indicators instead of embedding real credentials.

### Assessments require explicit execution

Loading or refreshing the dashboard does not automatically send adversarial prompts to the target.

### PDF downloads reuse captured results

Generating a report does not rerun the assessment or consume additional API requests.

### Mock mode supports safe development

Most development and automated validation can occur without contacting an external LLM.

---

## 🧭 OWASP LLM Alignment

The assessment report maps relevant findings to LLM security concepts, including prompt injection and sensitive information disclosure.

This mapping is intended as an educational and reporting aid rather than a claim of complete OWASP coverage.

The current five-test suite represents a focused baseline assessment, not a comprehensive LLM penetration test.

---

## ⚠️ Limitations

The deterministic evaluator currently checks configured failure indicators.

That provides reproducible results, but natural-language model behavior is more complex than exact indicator matching.

A production-grade assessment system should consider:

- multiple prompt variations per category
- semantic evaluation
- repeated testing
- model nondeterminism
- false-positive and false-negative analysis
- human validation
- versioned test cases
- broader OWASP LLM coverage
- application-specific authorization boundaries

Future versions could combine:

```text
Deterministic Rules
        +
Semantic AI Evaluation
        +
Human Review
```

A PASS should therefore be interpreted as:

> The configured failure condition was not observed during this test.

—not:

> The target is completely secure.

---

## 💡 Skills Demonstrated

This project demonstrates practical experience with:

### AI Security

- LLM adversarial testing
- prompt injection testing
- jailbreak resistance testing
- system prompt exposure testing
- sensitive information leakage testing
- security test-case design

### Security Engineering

- evidence capture
- deterministic evaluation
- risk scoring
- authorization boundaries
- secure secret handling
- assessment methodology
- security reporting

### Python Development

- Python
- Flask
- JSON
- environment variables
- modular application design
- error handling
- automated testing with pytest

### API Integration

- OpenAI API integration
- configurable target modes
- controlled external requests
- response processing

### Reporting

- ReportLab PDF generation
- executive summaries
- evidence documentation
- findings and recommendations
- OWASP-oriented reporting

### Software Engineering

- Git
- GitHub
- modular project structure
- unit testing
- reproducible mock environments
- configuration management

---

## 🔮 Future Enhancements

Potential future improvements include:

- expanded adversarial test library
- configurable test selection
- multiple target providers
- semantic AI evaluator
- repeated-run analysis
- assessment history
- SQLite persistence
- JSON export
- trend analysis
- authentication
- role-based access control
- additional OWASP LLM mappings
- CI/CD security checks

---

## ⚖️ Authorized Use

This project is intended for:

- defensive security research
- cybersecurity education
- AI security learning
- portfolio demonstration
- testing systems you own
- systems you are explicitly authorized to assess

Do not use this project to test third-party systems without authorization.

---

## 👤 Author

**BecomingCyber**

Cybersecurity | Digital Forensics | Incident Response | AI Security

GitHub: `BecomingCyber`

---

## 📌 Portfolio Context

This project was built as a hands-on cybersecurity portfolio project focused on the emerging intersection of **artificial intelligence and security engineering**.

Rather than stopping at a scripted prompt test, the project develops a complete assessment workflow:

```text
Design Tests
    ↓
Execute
    ↓
Capture Evidence
    ↓
Evaluate
    ↓
Score Risk
    ↓
Present Findings
    ↓
Generate Report
```

The goal is to demonstrate the ability to turn security concepts into a documented, testable, and repeatable technical workflow.
