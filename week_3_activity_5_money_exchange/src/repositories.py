"""
repositories.py
----------------
Repository pattern: one repository class per table, each responsible for
all SQL/CRUD operations for its entity. This keeps SQL isolated from
business logic (services.py) and from the plain entity classes (models.py).
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from .database import Database
from .models import Customer, Currency, ExchangeRate, Transaction


class BaseRepository(ABC):
    """Shared behaviour for all repositories."""

    def __init__(self, db: Database):
        self.db = db

    @abstractmethod
    def create(self, entity):
        ...

    @abstractmethod
    def get_all(self) -> List:
        ...


class CustomerRepository(BaseRepository):
    def create(self, customer: Customer) -> Customer:
        conn = self.db.connect()
        cur = conn.execute(
            """INSERT INTO customers (full_name, email, phone, id_document_number)
               VALUES (?, ?, ?, ?)""",
            (customer.full_name, customer.email, customer.phone, customer.id_document_number),
        )
        conn.commit()
        customer.customer_id = cur.lastrowid
        return customer

    def get_by_id(self, customer_id: int) -> Optional[Customer]:
        row = self.db.connect().execute(
            "SELECT * FROM customers WHERE customer_id = ?", (customer_id,)
        ).fetchone()
        return Customer.from_row(row) if row else None

    def get_by_email(self, email: str) -> Optional[Customer]:
        row = self.db.connect().execute(
            "SELECT * FROM customers WHERE email = ?", (email,)
        ).fetchone()
        return Customer.from_row(row) if row else None

    def get_all(self) -> List[Customer]:
        rows = self.db.connect().execute("SELECT * FROM customers").fetchall()
        return [Customer.from_row(r) for r in rows]

    def update(self, customer: Customer) -> None:
        self.db.connect().execute(
            """UPDATE customers SET full_name=?, email=?, phone=?, id_document_number=?
               WHERE customer_id=?""",
            (customer.full_name, customer.email, customer.phone,
             customer.id_document_number, customer.customer_id),
        )
        self.db.connect().commit()

    def delete(self, customer_id: int) -> None:
        self.db.connect().execute(
            "DELETE FROM customers WHERE customer_id = ?", (customer_id,)
        )
        self.db.connect().commit()


class CurrencyRepository(BaseRepository):
    def create(self, currency: Currency) -> Currency:
        conn = self.db.connect()
        cur = conn.execute(
            "INSERT INTO currencies (code, name, symbol) VALUES (?, ?, ?)",
            (currency.code, currency.name, currency.symbol),
        )
        conn.commit()
        currency.currency_id = cur.lastrowid
        return currency

    def get_by_code(self, code: str) -> Optional[Currency]:
        row = self.db.connect().execute(
            "SELECT * FROM currencies WHERE code = ?", (code,)
        ).fetchone()
        return Currency.from_row(row) if row else None

    def get_all(self) -> List[Currency]:
        rows = self.db.connect().execute("SELECT * FROM currencies").fetchall()
        return [Currency.from_row(r) for r in rows]


class ExchangeRateRepository(BaseRepository):
    def create(self, rate: ExchangeRate) -> ExchangeRate:
        conn = self.db.connect()
        cur = conn.execute(
            """INSERT INTO exchange_rates (from_currency_id, to_currency_id, rate)
               VALUES (?, ?, ?)""",
            (rate.from_currency_id, rate.to_currency_id, rate.rate),
        )
        conn.commit()
        rate.rate_id = cur.lastrowid
        return rate

    def get_latest_rate(self, from_currency_id: int, to_currency_id: int) -> Optional[ExchangeRate]:
        row = self.db.connect().execute(
            """SELECT * FROM exchange_rates
               WHERE from_currency_id = ? AND to_currency_id = ?
               ORDER BY effective_date DESC LIMIT 1""",
            (from_currency_id, to_currency_id),
        ).fetchone()
        return ExchangeRate.from_row(row) if row else None

    def get_all(self) -> List[ExchangeRate]:
        rows = self.db.connect().execute("SELECT * FROM exchange_rates").fetchall()
        return [ExchangeRate.from_row(r) for r in rows]


class TransactionRepository(BaseRepository):
    def create(self, txn: Transaction) -> Transaction:
        conn = self.db.connect()
        cur = conn.execute(
            """INSERT INTO transactions
               (customer_id, from_currency_id, to_currency_id,
                amount_from, amount_to, rate_applied, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (txn.customer_id, txn.from_currency_id, txn.to_currency_id,
             txn.amount_from, txn.amount_to, txn.rate_applied, txn.status),
        )
        conn.commit()
        txn.transaction_id = cur.lastrowid
        return txn

    def get_all(self) -> List[Transaction]:
        rows = self.db.connect().execute(
            "SELECT * FROM transactions ORDER BY transaction_date DESC"
        ).fetchall()
        return [Transaction.from_row(r) for r in rows]

    def get_by_customer(self, customer_id: int) -> List[Transaction]:
        rows = self.db.connect().execute(
            "SELECT * FROM transactions WHERE customer_id = ? ORDER BY transaction_date DESC",
            (customer_id,),
        ).fetchall()
        return [Transaction.from_row(r) for r in rows]
