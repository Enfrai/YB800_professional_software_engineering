"""
test_exchange.py
-----------------
A minimal smoke test using an in-memory SQLite database so it never
touches money_exchange.db on disk.

Usage:
    python -m unittest tests/test_exchange.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import Database
from src.models import Customer, Currency, ExchangeRate
from src.repositories import CustomerRepository, CurrencyRepository, ExchangeRateRepository
from src.services import ExchangeService, RateNotAvailableError


class TestExchangeService(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.db.initialize_schema()

        self.customer_repo = CustomerRepository(self.db)
        self.currency_repo = CurrencyRepository(self.db)
        self.rate_repo = ExchangeRateRepository(self.db)
        self.service = ExchangeService(self.db)

        self.customer = self.customer_repo.create(Customer(
            full_name="Test User", email="test@example.com",
            id_document_number="X0001",
        ))
        self.nzd = self.currency_repo.create(Currency(code="NZD", name="NZ Dollar", symbol="$"))
        self.usd = self.currency_repo.create(Currency(code="USD", name="US Dollar", symbol="$"))
        self.rate_repo.create(ExchangeRate(
            from_currency_id=self.nzd.currency_id,
            to_currency_id=self.usd.currency_id,
            rate=0.6,
        ))

    def test_perform_exchange_calculates_amount_to(self):
        txn = self.service.perform_exchange(self.customer.customer_id, "NZD", "USD", 100)
        self.assertEqual(txn.amount_to, 60.0)
        self.assertEqual(txn.rate_applied, 0.6)

    def test_missing_rate_raises_error(self):
        with self.assertRaises(RateNotAvailableError):
            self.service.perform_exchange(self.customer.customer_id, "USD", "NZD", 100)


if __name__ == "__main__":
    unittest.main()
