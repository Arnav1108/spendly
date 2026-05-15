import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email, get_user_by_id, get_expenses_by_user

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm:
            flash("All fields are required.", "error")
            return render_template("register.html", name=name, email=email)

        at = email.find("@")
        if at < 1 or "." not in email[at:]:
            flash("Enter a valid email address.", "error")
            return render_template("register.html", name=name, email=email)

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return render_template("register.html", name=name, email=email)

        if password != confirm:
            flash("Passwords do not match.", "error")
            return render_template("register.html", name=name, email=email)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                (name, email, generate_password_hash(password)),
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("An account with that email already exists.", "error")
            return render_template("register.html", name=name, email=email)
        finally:
            db.close()

        flash("Account created! You can now sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("landing"))

    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html", email=email)

        user = get_user_by_email(email)

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html", email=email)

        session["user_id"] = user["id"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user_row = get_user_by_id(session["user_id"])
    if user_row is None:
        session.clear()
        return redirect(url_for("login"))

    expense_rows = get_expenses_by_user(session["user_id"])

    created_dt = datetime.strptime(user_row["created_at"][:10], "%Y-%m-%d")
    user = {
        "name":         user_row["name"],
        "email":        user_row["email"],
        "member_since": f"{created_dt.strftime('%B')} {created_dt.year}",
    }

    cat_totals = {}
    for e in expense_rows:
        cat_totals[e["category"]] = cat_totals.get(e["category"], 0.0) + e["amount"]

    grand_total = sum(cat_totals.values())

    stats = {
        "total_spent":  f"₹{grand_total:.2f}",
        "transactions": len(expense_rows),
        "top_category": max(cat_totals, key=cat_totals.get) if cat_totals else "—",
    }

    expenses = []
    for e in expense_rows:
        dt = datetime.strptime(e["date"], "%Y-%m-%d")
        expenses.append({
            "date":        f"{dt.strftime('%B')} {dt.day}, {dt.year}",
            "description": e["description"] or "",
            "category":    e["category"],
            "amount":      f"₹{e['amount']:.2f}",
        })

    categories = [
        {
            "name":   name,
            "amount": f"₹{amount:.2f}",
            "pct":    round(amount / grand_total * 100) if grand_total else 0,
        }
        for name, amount in sorted(cat_totals.items(), key=lambda x: -x[1])
    ]

    return render_template("profile.html",
                           user=user, stats=stats,
                           expenses=expenses, categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
