# 💰 Expense Tracker - Flask Mini Project

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey) ![License](https://img.shields.io/badge/License-MIT-green)

A simple web application built with **Python Flask** to record and view daily expenses.
Built as part of the Unlox Minor Project: Flask Mini Project.

## Features
- Add an expense (title, amount, category, date) using an HTML form (POST)
- Input validation with friendly error messages (empty fields, non-numeric or negative amount, invalid category, bad or future date)
- Result page showing the saved expense, category total and overall total
- View all expenses and filter them by category (GET)
- Clear all expenses
- Simple styling with one CSS file

## Routes
| URL         | Method    | Description                                   |
|-------------|-----------|-----------------------------------------------|
| `/`         | GET       | Home page with count, total and recent items  |
| `/about`    | GET       | About page                                    |
| `/expenses` | GET       | List expenses, optional `?category=Food`      |
| `/add`      | GET, POST | Show form / validate and save the expense     |
| `/clear`    | POST      | Delete all expenses                           |

## Folder Structure
```
expense_tracker/
    app.py
    test_app.py
    requirements.txt
    .gitignore
    LICENSE
    README.md
    templates/
        base.html
        index.html
        about.html
        add.html
        result.html
        expenses.html
        404.html
    static/
        style.css
    screenshots/        (add your screenshots here)
```

## How to Run
1. Open a terminal in the project folder.
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run the app: `python app.py`
5. Open **http://127.0.0.1:5000** in your browser.

## Testing Checklist
| Test | Expected result |
|------|-----------------|
| App starts with `python app.py` | No errors, server runs on port 5000 |
| Open `/`, `/about`, `/expenses`, `/add` | All pages load |
| Add valid expense (Lunch, 120, Food) | Result page with summary and totals |
| Submit empty form | Friendly error messages, form stays |
| Amount = `abc` | "Amount must be a number" message |
| Amount = `-50` or `0` | "Amount must be greater than zero" |
| No category selected | "Please choose a category" |
| Future date | "Date cannot be in the future" |
| Filter by category | Only matching expenses shown |
| Open `/random` | Custom 404 page |

## Run the Automated Tests
```
python -m unittest -v
```
All 9 tests (routes, validation, filtering, clearing) should pass.

## Notes
- Data is stored in memory (a Python list), so it resets when the server restarts. A database is optional for this project.
- No passwords or secret keys are used in the code.

## Screenshots
| Home | Add Expense |
|------|-------------|
| ![Home](screenshots/home.png) | ![Add](screenshots/add.png) |

| Validation Error | Result |
|------------------|--------|
| ![Error](screenshots/error.png) | ![Result](screenshots/result.png) |

| All Expenses |
|--------------|
| ![List](screenshots/expenses.png) |

> Save your screenshots in the `screenshots/` folder with exactly these names: `home.png`, `add.png`, `error.png`, `result.png`, `expenses.png`.

## Author
<Your Name> - <USN> - RV College of Engineering
