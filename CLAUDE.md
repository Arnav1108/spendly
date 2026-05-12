# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**Spendly** is a Flask-based personal expense tracker. This is a structured student project where features are built step-by-step — many routes in `app.py` are stubs with "coming in Step N" placeholders, and `database/db.py` is intentionally left for students to implement.

## Commands

```bash
# Activate the virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the development server (port 5001)
python app.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_auth.py

# Run a specific test
pytest tests/test_auth.py::test_login_success
```

## Architecture

### Entry point
`app.py` — Flask application factory and all route definitions. Routes follow a numbered step plan; stubs return plain strings until implemented.

### Database layer
`database/db.py` — SQLite helpers (not yet implemented). Should expose:
- `get_db()` — returns a `sqlite3.Connection` with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `init_db()` — creates all tables via `CREATE TABLE IF NOT EXISTS`
- `seed_db()` — inserts sample rows for development

The database file (`expense_tracker.db`) is gitignored.

### Templates
Jinja2 templates under `templates/`. All pages extend `base.html`, which provides the navbar, footer, and asset links. Page-specific CSS (e.g. `landing.css`) is loaded via `{% block head %}`.

### Static assets
- `static/css/style.css` — global design tokens (CSS variables) and shared component styles
- `static/css/landing.css` — landing page–only styles
- `static/js/main.js` — shared JS (currently a stub; page-specific JS lives in `{% block scripts %}` in templates)

### Planned route structure
| Route | Step | Status |
|---|---|---|
| `GET /` | — | Done |
| `GET /register`, `POST /register` | 2 | GET done, POST stub |
| `GET /login`, `POST /login` | 2 | GET done, POST stub |
| `GET /logout` | 3 | Stub |
| `GET /profile` | 4 | Stub |
| `GET/POST /expenses/add` | 7 | Stub |
| `GET/POST /expenses/<id>/edit` | 8 | Stub |
| `POST /expenses/<id>/delete` | 9 | Stub |
| `GET /terms`, `GET /privacy` | — | Done |

## Design system

The UI uses a warm paper-toned palette defined in CSS variables in `style.css`. Key tokens: `--ink`, `--paper`, `--accent` (dark green `#1a472a`), `--accent-2` (amber). Fonts: **DM Serif Display** (headings) and **DM Sans** (body), loaded from Google Fonts.
