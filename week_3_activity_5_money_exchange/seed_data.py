"""
seed_data.py
------------
Populates the database with a handful of realistic rows so the project can
be demoed immediately after cloning.

Usage:
    python seed_data.py
"""

from src.database import Database
from src.models import Customer, Currency, ExchangeRate
from src.repositories import CustomerRepository, CurrencyRepository, ExchangeRateRepository


def seed():
    db = Database("money_exchange.db")
    db.initialize_schema()

    customer_repo = CustomerRepository(db)
    currency_repo = CurrencyRepository(db)
    rate_repo = ExchangeRateRepository(db)

    # --- Customers ---
    if not customer_repo.get_by_email("alice@example.com"):
        customer_repo.create(Customer(
            full_name="Alice Nguyen",
            email="alice@example.com",
            phone="+64-21-555-0101",
            id_document_number="P1234567",
        ))
    if not customer_repo.get_by_email("ben@example.com"):
        customer_repo.create(Customer(
            full_name="Ben Carter",
            email="ben@example.com",
            phone="+64-21-555-0102",
            id_document_number="P7654321",
        ))

    # --- Currencies ---
    currencies = [
        ("NZD", "New Zealand Dollar", "$"),
        ("USD", "US Dollar", "$"),
        ("EUR", "Euro", "€"),
        ("GBP", "British Pound", "£"),
        ("JPY", "Japanese Yen", "¥"),
    ]
    currency_ids = {}
    for code, name, symbol in currencies:
        existing = currency_repo.get_by_code(code)
        if not existing:
            existing = currency_repo.create(Currency(code=code, name=name, symbol=symbol))
        currency_ids[code] = existing.currency_id

    # --- Exchange rates (illustrative, not live market data) ---
    sample_rates = [
        ("NZD", "USD", 0.60),
        ("USD", "NZD", 1.66),
        ("NZD", "EUR", 0.56),
        ("EUR", "NZD", 1.78),
        ("NZD", "GBP", 0.48),
        ("GBP", "NZD", 2.08),
        ("USD", "JPY", 148.20),
    ]
    for from_code, to_code, rate in sample_rates:
        rate_repo.create(ExchangeRate(
            from_currency_id=currency_ids[from_code],
            to_currency_id=currency_ids[to_code],
            rate=rate,
        ))

    print("Database seeded successfully -> money_exchange.db")


if __name__ == "__main__":
    seed()
