# Spec: Login and Logout

## Overview
Implement session-based login and logout for Spendly. The POST handler for `/login` validates credentials, writes the authenticated user's ID into Flask's signed session cookie, and redirects to the dashboard placeholder. `GET /logout` clears the session and redirects to the landing page. Together these two routes gate every future authenticated feature — nothing behind a login wall can be built until this step is complete.

## Depends on
- Step 01 — Database setup (`users` table, `get_db()`)
- Step 02 — Registration (users must exist in the database to log in)

## Routes
- `GET /login` — render the login form — public (already done)
- `POST /login` — validate credentials, write session, redirect — public
- `GET /logout` — clear session, redirect to landing — public (no login required to hit it)

## Database changes
No database changes. Reads from the existing `users` table (`email`, `password_hash`).

## Templates
- **Modify:** `templates/login.html` — replace the custom `{% if error %}` block with Flask's flash message pattern (matching `register.html`); ensure the form POSTs to `/login`; pre-fill `email` field on failed attempts

## Files to change
- `app.py` — convert `GET /login` to `GET|POST`, implement POST handler; implement `GET /logout`; add `session` and `check_password_hash` imports; add `redirect` and `url_for` (already imported)
- `templates/login.html` — swap `{% if error %}` for flash message block; add `value="{{ email or '' }}"` to email input

## Files to create
None

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Verify passwords with `werkzeug.security.check_password_hash` — never compare plain text
- Use CSS variables — never hardcode hex values in templates or styles
- All templates extend `base.html`
- Store only `session["user_id"]` (the integer PK) — never store the password hash or plain-text password in the session
- On failed login show a deliberately vague flash error (`"error"` category): "Invalid email or password." — do not reveal whether the email exists
- On successful login set `session["user_id"]` then redirect to `url_for("profile")` (the Step 4 stub is fine for now)
- `GET /logout` must call `session.clear()` then redirect to `url_for("landing")`
- Close the DB connection in a `finally` block after every query

## Definition of done
- [ ] `GET /login` renders the form
- [ ] Submitting valid credentials sets `session["user_id"]` and redirects to `/profile`
- [ ] Submitting an unrecognised email shows "Invalid email or password." flash error and re-renders the form with email pre-filled
- [ ] Submitting a correct email with a wrong password shows the same vague flash error and re-renders the form with email pre-filled
- [ ] Submitting with any empty field shows a flash error and does not query the database
- [ ] `GET /logout` clears the session and redirects to `/`
- [ ] After logout, `session["user_id"]` is no longer set
- [ ] The plain-text password is never written to the session or logged
- [ ] App starts and all existing routes still work
