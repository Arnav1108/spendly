import os
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email

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

    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "January 2026",
    }
    stats = {
        "total_spent": "₹338.75",
        "transactions": 8,
        "top_category": "Bills",
    }
    expenses = [
        {"date": "May 12, 2026", "description": "Restaurant lunch",  "category": "Food",          "amount": "₹22.00"},
        {"date": "May 11, 2026", "description": "Miscellaneous",     "category": "Other",         "amount": "₹12.50"},
        {"date": "May 10, 2026", "description": "Clothing",          "category": "Shopping",      "amount": "₹65.00"},
        {"date": "May 08, 2026", "description": "Movie tickets",     "category": "Entertainment", "amount": "₹18.00"},
        {"date": "May 07, 2026", "description": "Pharmacy",          "category": "Health",        "amount": "₹25.75"},
    ]
    categories = [
        {"name": "Bills",         "amount": "₹120.00", "pct": 35},
        {"name": "Food",          "amount": "₹67.50",  "pct": 20},
        {"name": "Shopping",      "amount": "₹65.00",  "pct": 19},
        {"name": "Transport",     "amount": "₹30.00",  "pct": 9},
        {"name": "Health",        "amount": "₹25.75",  "pct": 8},
        {"name": "Entertainment", "amount": "₹18.00",  "pct": 5},
        {"name": "Other",         "amount": "₹12.50",  "pct": 4},
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
