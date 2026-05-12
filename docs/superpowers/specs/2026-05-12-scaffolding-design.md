# Scaffolding Design — Chatbot Whitelabel API Notificaciones

## Scope

Create the initial folder structure and empty module files for the project. No business logic — only `__init__.py` files, placeholder files (`.env.example`, `requirements.txt`, `.gitignore`), and the Clean Architecture layer directories.

## Folder Structure

```
src/
  __init__.py
  domain/
    __init__.py
    entities/__init__.py
    models/__init__.py
  application/
    __init__.py
    use_cases/__init__.py
  infrastructure/
    __init__.py
    sheets/__init__.py
    meta/__init__.py
  interfaces/
    __init__.py
    routes/__init__.py
    schemas/__init__.py
    middlewares/__init__.py
tests/
  __init__.py
  unit/__init__.py
  integration/__init__.py
config/
  __init__.py
.env.example
requirements.txt
.gitignore
```

## Layer Responsibilities

- **domain/** — Business entities and pure logical models (no external dependencies)
- **application/use_cases/** — Orchestration: receive → flatten → enrich → notify
- **infrastructure/sheets/** — Google Sheets API v4 adapter
- **infrastructure/meta/** — Meta WhatsApp Cloud API client
- **interfaces/routes/** — FastAPI endpoint definitions
- **interfaces/schemas/** — Pydantic request/response models
- **interfaces/middlewares/** — Auth, logging, and other cross-cutting concerns
- **config/** — Pydantic Settings reading from environment variables
- **tests/unit/** — Fast isolated tests (no external APIs, no .env required)
- **tests/integration/** — Tests against real APIs (requires .env configured)

## Placeholder Files

- `.env.example` — Documents required env vars with fake values (committed to git)
- `.env` — Listed in `.gitignore`, never committed (real secrets live here)
- `requirements.txt` — Empty, to be populated as dependencies are added
- `.gitignore` — Standard Python ignores: `__pycache__`, `*.pyc`, `.env`, `venv/`
