"""
services.py
-----------
Business logic layer. ExchangeService coordinates the four repositories to
perform a real-world action: "exchange currency X for currency Y for this
customer" - without any of the repositories needing to know about each other.
"""

from .database import Database
from .models import Transaction
from .repositories import (
    CustomerRepository,
    CurrencyRepository,
    ExchangeRateRepository,
    TransactionRepository,
)


class CurrencyNotFoundError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class RateNotAvailableError(Exception):
    pass


class ExchangeService:
    def __init__(self, db: Database):
        self.db = db
        self.customers = CustomerRepository(db)
        self.currencies = CurrencyRepository(db)
        self.rates = ExchangeRateRepository(db)
        self.transactions = TransactionRepository(db)

    def perform_exchange(self, customer_id: int, from_code: str,
                          to_code: str, amount: float) -> Transaction:
        customer = self.customers.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(f"No customer with id {customer_id}")

        from_currency = self.currencies.get_by_code(from_code)
        to_currency = self.currencies.get_by_code(to_code)
        if not from_currency or not to_currency:
            raise CurrencyNotFoundError("One or both currency codes do not exist.")

        rate = self.rates.get_latest_rate(from_currency.currency_id, to_currency.currency_id)
        if not rate:
            raise RateNotAvailableError(
                f"No exchange rate available for {from_code} -> {to_code}"
            )

        txn = Transaction(
            customer_id=customer.customer_id,
            from_currency_id=from_currency.currency_id,
            to_currency_id=to_currency.currency_id,
            amount_from=amount,
            rate_applied=rate.rate,
        )
        return self.transactions.create(txn)
