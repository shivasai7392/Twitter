# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the development server:**
```bash
uv run fastapi dev main.py
```

On Windows, if you get `UnicodeEncodeError` (emoji in FastAPI CLI), use:
```powershell
.\run.ps1
```
or:
```powershell
$env:PYTHONIOENCODING="utf-8"; uv run fastapi dev main.py
```

**Lint:**
```bash
uv run ruff check .
uv run ruff format .
```

**Package management** uses `uv` (not pip). Add dependencies with:
```bash
uv add <package>
```

## Architecture

This is a FastAPI blog/Twitter-clone learning project with server-side rendering via Jinja2 templates.

- **`main.py`** — single-file FastAPI app; all routes defined here. Posts are stored as an in-memory `list[dict]` (no database yet).
- **`templates/`** — Jinja2 HTML templates:
  - `layout.html` — base template with Bootstrap 5 navbar, sidebar, footer, and dark-mode toggle. All pages extend this.
  - `home.html` — lists all posts, extends `layout.html`.
  - `post.html` — single post detail view with edit/delete buttons (auth not yet implemented).
- **`static/`** — served at `/static`; contains `css/main.css`, `js/utils.js`, `profile_pics/`, and PWA icons.

## Ruff Configuration

Ruff is configured in `pyproject.toml` to enforce annotations (`ANN`) and docstrings (`D`) with Google convention. New functions should include type annotations and Google-style docstrings.

## Planned Features (TODOs in code)

- User authentication and authorization (Login/Register buttons are present but non-functional)
- Post create/edit/delete (delete modal exists in `post.html` but form action is `#`)
