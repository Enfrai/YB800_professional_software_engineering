"""
models.py
---------
Plain OOP entity classes. Each class maps 1:1 to a database table and knows
how to turn itself into/from a dict and a sqlite3.Row. No SQL lives here -
that responsibility belongs to the repository classes (separation of
concerns).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    full_name: str
    email: str
    id_document_number: str
    phone: Optional[str] = None
    customer_id: Optional[int] = None
    created_at: Optional[str] = None

    @staticmethod
    def from_row(row) -> "Customer":
        return Customer(
            customer_id=row["customer_id"],
            full_name=row["full_name"],
            email=row["email"],
            phone=row["phone"],
            id_document_number=row["id_document_number"],
            created_at=row["created_at"],
        )


@dataclass
class Currency:
    code: str          # e.g. "USD"
    name: str          # e.g. "US Dollar"
    symbol: Optional[str] = None
    currency_id: Optional[int] = None

    @staticmethod
    def from_row(row) -> "Currency":
        return Currency(
            currency_id=row["currency_id"],
            code=row["code"],
            name=row["name"],
            symbol=row["symbol"],
        )


@dataclass
class ExchangeRate:
    from_currency_id: int
    to_currency_id: int
    rate: float
    rate_id: Optional[int] = None
    effective_date: Optional[str] = None

    def __post_init__(self):
        if self.rate <= 0:
            raise ValueError("Exchange rate must be a positive number.")

    @staticmethod
    def from_row(row) -> "ExchangeRate":
        return ExchangeRate(
            rate_id=row["rate_id"],
            from_currency_id=row["from_currency_id"],
            to_currency_id=row["to_currency_id"],
            rate=row["rate"],
            effective_date=row["effective_date"],
        )


@dataclass
class Transaction:
    customer_id: int
    from_currency_id: int
    to_currency_id: int
    amount_from: float
    rate_applied: float
    amount_to: float = field(init=False)
    transaction_id: Optional[int] = None
    transaction_date: Optional[str] = None
    status: str = "COMPLETED"

    def __post_init__(self):
        if self.amount_from <= 0:
            raise ValueError("amount_from must be positive.")
        # Business rule lives on the entity itself: OOP encapsulation.
        self.amount_to = round(self.amount_from * self.rate_applied, 2)

    @staticmethod
    def from_row(row) -> "Transaction":
        txn = Transaction(
            customer_id=row["customer_id"],
            from_currency_id=row["from_currency_id"],
            to_currency_id=row["to_currency_id"],
            amount_from=row["amount_from"],
            rate_applied=row["rate_applied"],
        )
        txn.transaction_id = row["transaction_id"]
        txn.amount_to = row["amount_to"]
        txn.transaction_date = row["transaction_date"]
        txn.status = row["status"]
        return txn
