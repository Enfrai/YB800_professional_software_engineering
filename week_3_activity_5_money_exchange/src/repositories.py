from .models import Customer, Currency, ExchangeRate, ExchangeTransaction
from typing import Optional


class CustomerRepository:
    """Provide CRUD operations for customers."""

    def __init__(self, db):
        self.db = db

    def create(self, customer: Customer) -> Customer:
        with self.db.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO customers (first_name, last_name, email, phone)
                VALUES (?, ?, ?, ?)
                """,
                (customer.first_name, customer.last_name, customer.email, customer.phone),
            )
            customer.customer_id = cursor.lastrowid
        return customer

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        with self.db.connect() as connection:
            row = connection.execute(
                "SELECT * FROM customers WHERE customer_id = ?",
                (customer_id,),
            ).fetchone()
        return Customer(**dict(row)) if row else None

    def list_all(self):
        with self.db.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM customers ORDER BY customer_id"
            ).fetchall()
        return [Customer(**dict(row)) for row in rows]


class CurrencyRepository:
    """Provide read and create operations for currencies."""

    def __init__(self, db):
        self.db = db

    def create(self, currency: Currency) -> Currency:
        with self.db.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO currencies (code, name, symbol)
                VALUES (?, ?, ?)
                """,
                (currency.code.upper(), currency.name, currency.symbol),
            )
            currency.currency_id = cursor.lastrowid
        return currency

    def find_by_code(self, code: str) -> Optional[Currency]:
        with self.db.connect() as connection:
            row = connection.execute(
                "SELECT * FROM currencies WHERE code = ?",
                (code.upper(),),
            ).fetchone()
        return Currency(**dict(row)) if row else None

    def find_by_id(self, currency_id: int) -> Optional[Currency]:
        with self.db.connect() as connection:
            row = connection.execute(
                "SELECT * FROM currencies WHERE currency_id = ?",
                (currency_id,),
            ).fetchone()
        return Currency(**dict(row)) if row else None

    def list_all(self):
        with self.db.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM currencies ORDER BY code"
            ).fetchall()
        return [Currency(**dict(row)) for row in rows]


class ExchangeRateRepository:
    """Provide persistence operations for exchange rates."""

    def __init__(self, db):
        self.db = db

    def create(self, rate: ExchangeRate) -> ExchangeRate:
        with self.db.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO exchange_rates
                (base_currency_id, target_currency_id, rate, effective_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    rate.base_currency_id,
                    rate.target_currency_id,
                    rate.rate,
                    rate.effective_at,
                ),
            )
            rate.rate_id = cursor.lastrowid
        return rate

    def find_by_id(self, rate_id: int) -> Optional[ExchangeRate]:
        with self.db.connect() as connection:
            row = connection.execute(
                "SELECT * FROM exchange_rates WHERE rate_id = ?",
                (rate_id,),
            ).fetchone()
        return ExchangeRate(**dict(row)) if row else None


class ExchangeTransactionRepository:
    """Provide persistence operations for exchange transactions."""

    def __init__(self, db):
        self.db = db

    def create(self, transaction: ExchangeTransaction) -> ExchangeTransaction:
        with self.db.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO exchange_transactions
                (
                    customer_id,
                    rate_id,
                    source_currency_id,
                    target_currency_id,
                    source_amount,
                    exchange_rate,
                    target_amount,
                    transaction_type
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.customer_id,
                    transaction.rate_id,
                    transaction.source_currency_id,
                    transaction.target_currency_id,
                    transaction.source_amount,
                    transaction.exchange_rate,
                    transaction.target_amount,
                    transaction.transaction_type,
                ),
            )
            transaction.transaction_id = cursor.lastrowid
        return transaction

    def find_by_customer(self, customer_id: int):
        with self.db.connect() as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM exchange_transactions
                WHERE customer_id = ?
                ORDER BY transaction_date DESC
                """,
                (customer_id,),
            ).fetchall()
        return [ExchangeTransaction(**dict(row)) for row in rows]
