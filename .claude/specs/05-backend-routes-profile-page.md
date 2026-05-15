# Spec: Backend Routes for Profile Page

## Overview
This step replaces all hardcoded data in the `/profile` route with real database queries. The profile page UI (built in Step 4) already renders `user`, `stats`, `expenses`, and `categories` — this step wires those context variables to live SQLite data so every logged-in user sees their own information. New helper functions are added to `database/db.py`; `app.py`'s `/profile` view is updated to call them. No template changes are needed.

## Depends on
- Step 01: Database setup (`users` and `expenses` tables, `get_db()`)
- Step 02: Registration (users and expenses must exist in the DB)
- Step 03: Login and Logout (`session["user_id"]` must be set)
- Step 04: Profile Page UI (template must already exist and accept the same context variables)

## Routes
- `GET /profile` — already exists; update to query real data — logged-in only

No new routes.

## Database changes
No schema changes. Reads from the existing `users` and `expenses` tables.

## Templates
- **Modify:** `templates/profile.html` — format the `member_since` value; it will now be a raw SQLite `datetime` string (`YYYY-MM-DD HH:MM:SS`) instead of the hardcoded `"January 2026"`. Format it in the Jinja template using a `strftime`-style filter or by pre-formatting in Python before passing to the template.

## Files to change
- `database/db.py` — add the following helper functions:
  - `get_user_by_id(user_id)` — returns one `sqlite3.Row` with `id`, `name`, `email`, `created_at`
  - `get_expenses_by_user(user_id)` — returns all expense rows for the user ordered by `date DESC`, each with `id`, `amount`, `category`, `date`, `description`
- `app.py` — update `profile()` view to:
  1. Call `get_user_by_id(session["user_id"])` and 404 / redirect if `None`
  2. Call `get_expenses_by_user(session["user_id"])`
  3. Compute `stats` in Python: sum of all amounts, count of rows, top category by total spend
  4. Compute `categories` list in Python: per-category total and percentage of grand total
  5. Format dates for display before passing to the template
  6. Pass real `user`, `stats`, `expenses`, `categories` dicts to `profile.html`

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` only
- Parameterised queries only — never interpolate `user_id` or any value into SQL strings
- Passwords hashed with werkzeug (no auth changes in this step)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Close every DB connection in a `finally` block
- `get_user_by_id` must select `id, name, email, created_at` — not `password_hash`
- Stats computation (sum, count, top category) must be done in Python, not in raw SQL aggregate queries, to keep the DB layer simple
- `member_since` must be formatted as a human-readable string (e.g. `"May 2026"`) before being passed to the template — the template must not do date parsing
- `amount` values in `expenses` and `categories` must be formatted as `"₹{value:.2f}"` strings in Python before being passed to the template
- `pct` values in `categories` must be integers (0–100); use `round()` and guard against division-by-zero when total spend is 0
- If the logged-in user has no expenses, the profile page must still render without error (empty table, zero stats)

## Definition of done
- [ ] `GET /profile` returns HTTP 200 for the seeded demo user
- [ ] The page shows the demo user's real name and email (not "Demo User" / "demo@spendly.com" hardcoded in Python)
- [ ] `member_since` displays a formatted date derived from `users.created_at` in the DB
- [ ] The transaction history table shows the 8 seeded expense rows (not 5 hardcoded rows)
- [ ] `stats.total_spent` equals the sum of all seeded expense amounts (≈ ₹338.75)
- [ ] `stats.transactions` equals the count of seeded expenses (8)
- [ ] `stats.top_category` equals `"Bills"` for the seeded data set
- [ ] The category breakdown lists every category present in the user's expenses with correct totals and percentages that add up to 100 %
- [ ] A freshly registered user with no expenses sees the profile page without a 500 error (empty state)
- [ ] No hardcoded user data, expense rows, or category data remains in `app.py`
