# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full Stack Trivia App: a Flask + SQLAlchemy + PostgreSQL backend API paired with a Create React App frontend. Users can view/add/delete trivia questions by category and play a quiz game.

## Architecture

- `backend/models.py` — SQLAlchemy setup (`setup_db`) and the two ORM models, `Question` and `Category`. Both models expose `insert()`/`update()`/`delete()`/`format()` helpers used directly by route handlers (no repository/service layer). The DB connection string is built from `DB_HOST`/`DB_NAME` env vars (defaults: `localhost:5432` / `trivia`).
- `backend/flaskr/__init__.py` — `create_app()` factory defines every route inline (no blueprints). All pagination goes through the shared `get_current_questions(request, search_term=None, category_id=None)` helper (`QUESTIONS_PER_PAGE = 10`). CORS is enabled globally. JSON error handlers exist for 400/404/422 only — an uncaught exception elsewhere will produce a non-JSON 500.
- `backend/test_flaskr.py` — unittest-based API tests hitting a real Postgres test database (`trivia_test`) via Flask's test client; no mocking of the DB layer.
- `frontend/src/components/` — plain React class components consuming the API directly with jQuery AJAX (not fetch): `QuestionView.js` (list/search/delete), `FormView.js` (add question), `QuizView.js` (play flow), `Question.js`, `Search.js`, `Header.js`.
- Frontend dev server proxies API calls to `http://127.0.0.1:5000/` (see `frontend/package.json` `proxy` field), so the Flask backend must be running on port 5000 during frontend development.

### API surface (backend routes, all under `/`, no versioning prefix)

- `GET /categories` → `{success, categories: {id: type}}`
- `GET /questions?page=N` → `{success, questions[], total_questions, categories}`
- `DELETE /questions/<id>`
- `POST /questions` — dual purpose: if body has `searchTerm`, performs a search (ILIKE match); otherwise creates a new question (requires `question`, `answer`, `difficulty`, `category`)
- `GET /categories/<id>/questions` → questions filtered by category
- `POST /quizzes` — body `{previous_questions: [ids], quiz_category: {id, type}}` → returns one unused random question, or `{success: True}` with no `question` key once exhausted

Note: this differs slightly from the frontend README's documented endpoint spoilers (e.g. no `/api/v1.0` prefix, questions are fetched via `GET /questions` not `POST`) — the routes above reflect what is actually implemented in `flaskr/__init__.py`.

## Commands

### Backend (from `backend/`)

```bash
# install deps (ideally inside a virtualenv)
pip install -r requirements.txt

# create/restore the dev database (requires local Postgres)
createdb trivia
psql trivia < trivia.psql

# run the dev server (port 5000)
flask --app flaskr run --reload

# run the full test suite (requires a separate trivia_test DB)
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

# run a single test case
python -m unittest test_flaskr.TriviaTestCase.test_get_paginated_questions
```

### Frontend (from `frontend/`)

```bash
npm install
npm start       # dev server on http://localhost:3000, proxies API calls to :5000
npm test        # CRA/Jest test runner
npm run build   # production build
```

## Notes

- Dependency versions in `backend/requirements.txt` and `frontend/package.json` (including the `overrides` block) have been deliberately bumped past the original Udacity starter versions to close known CVEs — don't downgrade them without checking `SECURITY.md`/prior PR history for why.
- `models.py` has several commented-out lines (auth-related `DB_USER`/`DB_PASSWORD`, an old `database_path`) — leftover from adapting the original starter config to env-var-based config; not dead code to clean up incidentally.
