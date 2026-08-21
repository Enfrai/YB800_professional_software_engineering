import tempfile
import unittest

from src.database import DatabaseManager
from src.services import MoneyExchangeService


class MoneyExchangeSystemTest(unittest.TestCase):
    """Test the main money exchange business operations."""

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        database_path = f"{self.temp_directory.name}/test.db"

        self.database = DatabaseManager(database_path)
        self.database.initialize()
        self.database.seed_data()
        self.service = MoneyExchangeService(self.database)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_create_customer(self):
        customer = self.service.create_customer(
            "Alice",
            "Brown",
            "alice@example.com",
        )

        self.assertIsNotNone(customer.customer_id)
        self.assertEqual(customer.email, "alice@example.com")

    def test_calculate_exchange(self):
        result = self.service.calculate_exchange(100, 1.68)
        self.assertEqual(result, 168.00)

    def test_record_exchange(self):
        customer = self.service.create_customer(
            "Alice",
            "Brown",
            "alice@example.com",
        )
        rate = self.service.add_exchange_rate("USD", "NZD", 1.68)

        transaction = self.service.record_exchange(
            customer.customer_id,
            rate.rate_id,
            "USD",
            "NZD",
            100,
        )

        self.assertIsNotNone(transaction.transaction_id)
        self.assertEqual(transaction.target_amount, 168.00)

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.service.calculate_exchange(0, 1.68)

    def test_invalid_rate(self):
        with self.assertRaises(ValueError):
            self.service.calculate_exchange(100, 0)

    def test_customer_history(self):
        customer = self.service.create_customer(
            "Alice",
            "Brown",
            "alice@example.com",
        )
        rate = self.service.add_exchange_rate("USD", "NZD", 1.68)

        self.service.record_exchange(
            customer.customer_id,
            rate.rate_id,
            "USD",
            "NZD",
            100,
        )

        history = self.service.get_customer_history(customer.customer_id)

        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].target_amount, 168.00)


if __name__ == "__main__":
    unittest.main()
