# Spec: Registration

## Overview
Implement user registration for Spendly — the POST handler for `/register`, form validation, password hashing, and database insertion. This is the first step that writes user data to the database, and it unlocks all future authenticated features. After registering, users are redirected to the login page.

## Depends on
- Step 01 — Database setup (`users` table must exist, `get_db()` must work)

## Routes
- `GET /register` — render the registration form — public (already done)
- `POST /register` — handle form submission, validate input, insert user, redirect — public

## Database changes
No new tables or columns. Uses the existing `users` table:
- `name` TEXT NOT NULL
- `email` TEXT NOT NULL UNIQUE
- `password_hash` TEXT NOT NULL

## Templates
- **Modify:** `templates/register.html` — add the HTML form with fields for name, email, password, confirm password; display flash error/success messages

## Files to change
- `app.py` — implement `POST /register` handler; add `secret_key`, import `session`, `redirect`, `url_for`, `request`, `flash` from Flask; import `generate_password_hash` from werkzeug
- `templates/register.html` — add form markup and flash message display

## Files to create
None

## New dependencies
No new dependencies

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never interpolate user input into SQL strings
- Hash passwords with `werkzeug.security.generate_password_hash` before storing
- Use CSS variables — never hardcode hex values in templates or styles
- All templates extend `base.html`
- `app.secret_key` must be set via `os.environ.get("SECRET_KEY", "dev-secret")` — never hardcode it directly
Validate on the server:
- name, email, and password are required (empty or whitespace-only counts as missing)
- email must contain `@` and a `.` after it — reject malformed addresses without hitting the DB
- password and confirm-password must match
- password must be at least 8 characters
- on any validation failure, re-render the form with name and email pre-filled; never pre-fill password fields
If email is already registered, show a flash error with category `"error"` and re-render the form with name and email pre-filled (do not redirect)
On success, flash a success message with category `"success"` and redirect to `url_for('login')`
Do not log the user in automatically after registration — session management is handled in Step 3 (login); doing it here would duplicate that logic and couple the two steps

## Definition of done
- [ ] `GET /register` renders the form with name, email, password, and confirm-password fields
- [ ] Submitting the form with valid data inserts a new row into `users` with a hashed password
- [ ] Submitting with a duplicate email shows a flash error and does not insert a duplicate row
- [ ] Submitting with mismatched passwords shows a flash error and does not insert any row
- [ ] Submitting with any empty field shows a flash error
- [ ] Successful registration redirects to `/login`
- [ ] The plain-text password is never stored in the database
- [ ] App starts and all existing routes still work
- [ ] Submitting with a password shorter than 8 characters shows a flash error and does not insert any row
- [ ] Submitting with an invalid email format shows a flash error and does not insert any row
