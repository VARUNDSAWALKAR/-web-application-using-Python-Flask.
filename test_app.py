"""Simple tests for the Expense Tracker. Run with: python -m unittest -v"""
import unittest

from app import app, expenses


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        expenses.clear()

    def test_pages_open(self):
        for url in ["/", "/about", "/expenses", "/add"]:
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_404_page(self):
        self.assertEqual(self.client.get("/missing").status_code, 404)

    def test_valid_expense(self):
        r = self.client.post("/add", data={
            "title": "Lunch", "amount": "120", "category": "Food"})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b"added successfully", r.data)
        self.assertEqual(len(expenses), 1)

    def test_empty_form(self):
        r = self.client.post("/add", data={})
        self.assertEqual(r.status_code, 400)
        self.assertIn(b"Please enter a title", r.data)
        self.assertEqual(len(expenses), 0)

    def test_non_numeric_amount(self):
        r = self.client.post("/add", data={
            "title": "x", "amount": "abc", "category": "Food"})
        self.assertIn(b"must be a number", r.data)

    def test_negative_amount(self):
        r = self.client.post("/add", data={
            "title": "x", "amount": "-5", "category": "Food"})
        self.assertIn(b"greater than zero", r.data)

    def test_invalid_category(self):
        r = self.client.post("/add", data={
            "title": "x", "amount": "5", "category": "Hacking"})
        self.assertIn(b"choose a category", r.data)

    def test_future_date(self):
        r = self.client.post("/add", data={
            "title": "x", "amount": "5", "category": "Food", "date": "2999-01-01"})
        self.assertIn(b"future", r.data)

    def test_filter_and_clear(self):
        self.client.post("/add", data={"title": "Bus", "amount": "30", "category": "Travel"})
        self.assertIn(b"Bus", self.client.get("/expenses?category=Travel").data)
        self.assertNotIn(b"Bus", self.client.get("/expenses?category=Food").data)
        self.client.post("/clear")
        self.assertEqual(len(expenses), 0)


if __name__ == "__main__":
    unittest.main()
