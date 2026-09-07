# Repository Guidelines

## Project Structure & Module Organization

This repository contains a Flask API and a Create React App client. Backend routes and app creation live in `backend/flaskr/__init__.py`; SQLAlchemy models and database configuration are in `backend/models.py`. The PostgreSQL seed/restore file is `backend/trivia.psql`, and backend tests are in `backend/test_flaskr.py`.

Frontend code lives under `frontend/src/`. Put reusable UI in `src/components/`, component styles in `src/stylesheets/`, static public assets in `frontend/public/`, and imported assets beside the source that uses them. API requests are proxied to `http://127.0.0.1:5000` during development.

## Build, Test, and Development Commands

Run backend commands from `backend/`:

- `pip install -r requirements.txt` installs Python dependencies in the active virtual environment.
- `createdb trivia && psql trivia < trivia.psql` creates and seeds the development database.
- `flask --app flaskr run --reload` starts the API on port 5000.
- `python test_flaskr.py` runs the backend suite after preparing `trivia_test` from `trivia.psql`.

Run frontend commands from `frontend/`:

- `npm install` installs locked dependencies.
- `npm start` starts the client on port 3000.
- `npm test` runs the Jest/React test runner.
- `npm run build` creates the production bundle.

## Coding Style & Naming Conventions

Use four spaces for Python and two spaces for JavaScript/CSS. Follow existing Python conventions: `snake_case` functions and variables, `PascalCase` classes, and route handlers kept near their Flask routes. React components use `PascalCase` filenames (for example, `QuizView.js`); methods and variables use `camelCase`. Keep API JSON keys consistent with existing consumers. The frontend uses Create React App's `react-app` ESLint configuration.

## Testing Guidelines

Backend tests use `unittest`, a real `trivia_test` PostgreSQL database, and methods named `test_*`. Add success and expected-error coverage for every endpoint change. Frontend tests use Jest and React DOM; name test files `*.test.js`. Run both suites before submitting cross-stack changes.

## Commit & Pull Request Guidelines

History uses short, imperative subjects such as `Fix frontend dependency vulnerabilities` and `Add CLAUDE.md file`. Keep each commit focused. Pull requests should explain behavior changes, list commands run, link relevant issues, and include screenshots for visible UI changes. Call out database, API-contract, or dependency changes explicitly; do not downgrade security overrides without documenting the reason.

## Configuration & Security

Configure PostgreSQL with `DB_HOST` and `DB_NAME`; never commit credentials. Review `SECURITY.md` and dependency history before changing pinned versions or `frontend/package.json` overrides.
