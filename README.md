# Profile Sync Agent

A profile synchronization system that converts a resume into a structured professional profile and safely synchronizes approved changes across external platforms.

The project explores how **AI extraction, canonical data models, change detection, platform adapters, human approval, and external API synchronization** can work together in a real-world AI system.

GitHub is the first supported platform, with the architecture designed to support additional platforms in the future.

---

## Why This Project?

Professional information often exists in multiple places:

- Resume
- GitHub
- Portfolio
- LinkedIn
- Job platforms

Updating the same information manually across every platform becomes repetitive and inconsistent.

Profile Sync Agent treats the resume as an input source and converts it into a **canonical professional profile** that can be mapped and synchronized to different platforms.

```text
Resume
   ↓
Parse
   ↓
AI Structured Extraction
   ↓
Canonical Profile
   ↓
Version + Change Detection
   ↓
Platform Adapter
   ↓
Preview Changes
   ↓
Human Approval
   ↓
Sync
```

---

## Features

### Resume Processing

- Upload PDF or DOCX resumes
- Extract resume text
- Support multiple document parsers through a parser abstraction
- Temporary upload handling

### AI Profile Extraction

- Local LLM extraction using Ollama
- Qwen3:8B
- Structured LLM output
- Pydantic-based validation
- Extracts:
  - Personal information
  - Skills
  - Experience
  - Projects
  - Education

### Canonical Profile

All extracted information is converted into one platform-independent model.

```text
Resume
   ↓
CanonicalProfile
   ├── name
   ├── headline
   ├── summary
   ├── location
   ├── skills
   ├── experience
   ├── projects
   └── education
```

External platforms depend on this model rather than directly on the resume.

### Profile Versioning

Every extracted profile is stored as a new version in SQLite.

This enables:

- Profile history
- Previous/current comparison
- Change tracking
- Future rollback/audit capabilities

### Structured Change Detection

Profile versions can be compared to detect:

- Added information
- Removed information
- Updated information

Changes are detected across:

- Basic profile fields
- Skills
- Experience
- Projects
- Education

### Platform Adapter Architecture

External platforms are isolated behind a common adapter interface.

```text
CanonicalProfile
       ↓
PlatformAdapter
       ↓
 ┌─────────────┐
 │ GitHub      │
 │ LinkedIn*   │
 │ Wellfound*  │
 └─────────────┘
```

`*` Future adapters.

This prevents the core profile system from depending directly on any individual platform.

### GitHub Integration

The current implementation integrates with the GitHub REST API.

It can:

- Authenticate using a GitHub token
- Read the current GitHub profile
- Read the GitHub Profile README
- Compare GitHub state with the canonical profile
- Generate proposed GitHub changes
- Preview changes before synchronization
- Update supported GitHub profile fields
- Update managed Profile README content

### Safe README Synchronization

The agent does not need to own the entire GitHub Profile README.

Only content inside a managed section is synchronized:

```html
<!-- PROFILE_SYNC_START -->

Content managed by Profile Sync Agent

<!-- PROFILE_SYNC_END -->
```

Content outside these markers remains user-controlled.

### Preview Before Write

External changes are separated into two operations:

```text
prepare_changes()
       ↓
Preview
       ↓
Approval
       ↓
sync()
```

This prevents resume extraction or mapping mistakes from immediately modifying external accounts.

### Idempotent Synchronization

The system compares desired state with current platform state before writing.

If GitHub already matches the canonical profile:

```text
Canonical Profile
       ↓
Compare with GitHub
       ↓
No Difference
       ↓
No Update
```

This avoids unnecessary external API writes.

---

## Architecture

```text
                         Resume
                           │
                           ▼
                  ┌─────────────────┐
                  │ Resume Parsers  │
                  │ PDF / DOCX      │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Local LLM       │
                  │ Ollama + Qwen   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Canonical       │
                  │ Profile         │
                  └────────┬────────┘
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
        ┌───────────────┐     ┌───────────────┐
        │ SQLite        │     │ Profile Diff  │
        │ Versioning    │     │ Engine        │
        └───────────────┘     └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Platform      │
                              │ Adapter       │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ GitHub        │
                              │ Adapter       │
                              └───────┬───────┘
                                      │
                             Preview / Approval
                                      │
                                      ▼
                              GitHub REST API
```

---

## Project Structure

```text
profile-sync-agent/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── llm/
│   │   └── provider.py
│   │
│   ├── parsers/
│   │   ├── base.py
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   └── factory.py
│   │
│   ├── platforms/
│   │   ├── base.py
│   │   ├── models.py
│   │   ├── github.py
│   │   ├── github_client.py
│   │   └── github_mapper.py
│   │
│   ├── profile/
│   │   ├── models.py
│   │   ├── extractor.py
│   │   ├── repository.py
│   │   └── diff.py
│   │
│   └── main.py
│
├── data/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **SQLite**
- **Ollama**
- **Qwen3:8B**
- **LangChain**
- **PyMuPDF**
- **python-docx**
- **HTTPX**
- **GitHub REST API**

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd profile-sync-agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and run Ollama

Make sure Ollama is installed and pull the model:

```bash
ollama pull qwen3:8b
```

Start Ollama if necessary:

```bash
ollama serve
```

### 5. Configure environment variables

Create a `.env` file:

```env
OLLAMA_MODEL=qwen3:8b
OLLAMA_BASE_URL=http://localhost:11434

DATABASE_URL=sqlite:///./data/profile_sync.db

GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_github_username
```

Never commit your `.env` file or GitHub token.

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## API Flow

### Parse Resume

```text
POST /resume/parse
```

Extracts raw text from a PDF or DOCX resume.

### Extract Profile

```text
POST /resume/extract
```

Parses the resume, extracts structured professional information using the local LLM, validates it against the canonical profile model, and stores a new profile version.

### Latest Profile

```text
GET /profiles/latest
```

Returns the latest canonical profile.

### Compare Profile Versions

```text
GET /profiles/diff?old_version=1&new_version=2
```

Returns structured changes between two profile versions.

### GitHub Connection

```text
GET /github/status
```

Verifies the GitHub integration and retrieves the current profile and Profile README.

### Preview GitHub Changes

```text
GET /github/preview
```

Compares the latest canonical profile against the current GitHub state without modifying GitHub.

### Synchronize GitHub

```text
POST /github/sync
```

Applies the prepared GitHub changes after review.

---

## Key System Design Concepts Explored

This project was primarily built as a hands-on AI system design exercise.

Concepts explored include:

- Canonical Data Model
- Single Source of Truth
- Structured LLM Output
- Adapter Pattern
- Parser Abstraction
- Platform-independent architecture
- Profile Versioning
- Structured Diffing
- External API Integration
- Separation of Read and Write Operations
- Human-in-the-Loop approval
- Idempotent synchronization
- Bounded resource ownership
- Optimistic concurrency using GitHub file SHA
- Partial failure in external systems
- Local-first AI architecture

---

## Safety Considerations

Profile Sync Agent follows a **preview-before-write** approach.

External changes should follow:

```text
Generate → Compare → Preview → Approve → Sync
```

Sensitive credentials are kept in environment variables, and the GitHub integration should use the minimum permissions necessary.

---

## Future Improvements

- LangGraph workflow orchestration
- Human approval node
- Streamlit interface
- Per-change approval
- Sync history and audit logs
- Better partial-failure handling
- Retry strategies
- Additional platform adapters
- More advanced profile normalization
- Improved semantic change detection

---

## Project Goal

The goal of this project is not simply to automate a GitHub profile.

It is to understand how to design an AI-powered synchronization system where:

**AI extracts information, a canonical model stores the truth, deterministic logic detects changes, adapters translate those changes for external platforms, and humans remain in control of what gets synchronized.**
