"""
Expense Tracker - Flask Mini Project
Routes:
    /          (GET)        Home page with summary
    /about     (GET)        About page
    /expenses  (GET)        List of all expenses (+ optional category filter)
    /add       (GET, POST)  Form to add an expense; POST validates and shows result
    /clear     (POST)       Remove all expenses
Data is kept in a simple Python list (no database needed for this project).
"""
from datetime import date, datetime

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Other"]

# In-memory storage for expenses
expenses = []


def total_amount(items):
    """Return the sum of all amounts in a list of expenses."""
    return round(sum(item["amount"] for item in items), 2)


def validate_expense(form):
    """Validate form data. Returns (cleaned_data, errors)."""
    errors = []

    title = form.get("title", "").strip()
    amount_raw = form.get("amount", "").strip()
    category = form.get("category", "").strip()
    date_raw = form.get("date", "").strip()

    # Title
    if not title:
        errors.append("Please enter a title for the expense.")
    elif len(title) > 50:
        errors.append("Title is too long (maximum 50 characters).")

    # Amount
    amount = None
    if not amount_raw:
        errors.append("Please enter the amount.")
    else:
        try:
            amount = float(amount_raw)
            if amount <= 0:
                errors.append("Amount must be greater than zero.")
                amount = None
            elif amount > 10_000_000:
                errors.append("Amount is too large. Please check the value.")
                amount = None
        except ValueError:
            errors.append("Amount must be a number, for example 250 or 99.50.")

    # Category
    if category not in CATEGORIES:
        errors.append("Please choose a category from the list.")

    # Date (optional: default to today)
    if not date_raw:
        date_raw = date.today().isoformat()
    else:
        try:
            parsed = datetime.strptime(date_raw, "%Y-%m-%d").date()
            if parsed > date.today():
                errors.append("Date cannot be in the future.")
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format.")

    cleaned = {
        "title": title,
        "amount": round(amount, 2) if amount is not None else None,
        "category": category,
        "date": date_raw,
    }
    return cleaned, errors


@app.route("/")
def index():
    """GET: Home page with a quick summary."""
    recent = expenses[-3:][::-1]
    return render_template(
        "index.html",
        count=len(expenses),
        total=total_amount(expenses),
        recent=recent,
    )


@app.route("/about")
def about():
    """GET: About page."""
    return render_template("about.html")


@app.route("/expenses")
def show_expenses():
    """GET: List all expenses, optionally filtered by ?category=..."""
    selected = request.args.get("category", "").strip()
    if selected in CATEGORIES:
        items = [e for e in expenses if e["category"] == selected]
    else:
        selected = ""
        items = expenses
    return render_template(
        "expenses.html",
        items=items,
        total=total_amount(items),
        categories=CATEGORIES,
        selected=selected,
    )


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    """GET: show the form. POST: validate input and show the result."""
    if request.method == "POST":
        cleaned, errors = validate_expense(request.form)
        if errors:
            # Show the form again with friendly messages and keep typed values
            return render_template(
                "add.html",
                errors=errors,
                form=request.form,
                categories=CATEGORIES,
                today=date.today().isoformat(),
            ), 400

        expenses.append(cleaned)
        category_total = total_amount(
            [e for e in expenses if e["category"] == cleaned["category"]]
        )
        return render_template(
            "result.html",
            expense=cleaned,
            total=total_amount(expenses),
            category_total=category_total,
            count=len(expenses),
        )

    return render_template(
        "add.html",
        errors=[],
        form={},
        categories=CATEGORIES,
        today=date.today().isoformat(),
    )


@app.route("/clear", methods=["POST"])
def clear_expenses():
    """POST: remove all expenses and go back to the list."""
    expenses.clear()
    return redirect(url_for("show_expenses"))


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
