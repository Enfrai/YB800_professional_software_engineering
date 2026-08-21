from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    """Represent a money exchange customer."""

    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    customer_id: Optional[int] = None
    created_at: Optional[str] = None


@dataclass
class Currency:
    """Represent a supported currency."""

    code: str
    name: str
    symbol: str
    currency_id: Optional[int] = None


@dataclass
class ExchangeRate:
    """Represent an exchange rate between two currencies."""

    base_currency_id: int
    target_currency_id: int
    rate: float
    effective_at: str = datetime.now().isoformat()
    rate_id: Optional[int] = None


@dataclass
class ExchangeTransaction:
    """Represent a completed currency exchange."""

    customer_id: int
    rate_id: int
    source_currency_id: int
    target_currency_id: int
    source_amount: float
    exchange_rate: float
    target_amount: float
    transaction_type: str
    transaction_id: Optional[int] = None
    transaction_date: Optional[str] = None
