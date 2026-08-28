"""
database.py
-----------
Handles the physical connection to the SQLite database and creation of the
schema (4 tables: customers, currencies, exchange_rates, transactions).

Kept as its own class (encapsulation) so the rest of the application never
talks SQL directly to the file system - it always goes through Database.
"""

import sqlite3
from pathlib import Path


class Database:
    """Wraps a single SQLite connection and knows how to build the schema."""

    def __init__(self, db_path: str = "money_exchange.db"):
        self.db_path = db_path
        self._conn = None

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_path)
            self._conn.execute("PRAGMA foreign_keys = ON;")
            self._conn.row_factory = sqlite3.Row
        return self._conn

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    # Context manager support -> `with Database(...) as db:`
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        self.close()

    def initialize_schema(self):
        """Creates all tables if they do not already exist."""
        conn = self.connect()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name          TEXT NOT NULL,
                email              TEXT NOT NULL UNIQUE,
                phone              TEXT,
                id_document_number TEXT NOT NULL UNIQUE,
                created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS currencies (
                currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
                code        TEXT NOT NULL UNIQUE,   -- ISO 4217, e.g. USD, EUR
                name        TEXT NOT NULL,          -- e.g. 'US Dollar'
                symbol      TEXT                    -- e.g. '$'
            );

            CREATE TABLE IF NOT EXISTS exchange_rates (
                rate_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                from_currency_id  INTEGER NOT NULL,
                to_currency_id    INTEGER NOT NULL,
                rate              REAL NOT NULL CHECK (rate > 0),
                effective_date    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
                FOREIGN KEY (to_currency_id)   REFERENCES currencies(currency_id),
                UNIQUE (from_currency_id, to_currency_id, effective_date)
            );

            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id       INTEGER NOT NULL,
                from_currency_id  INTEGER NOT NULL,
                to_currency_id    INTEGER NOT NULL,
                amount_from       REAL NOT NULL CHECK (amount_from > 0),
                amount_to         REAL NOT NULL,
                rate_applied      REAL NOT NULL,
                transaction_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status            TEXT DEFAULT 'COMPLETED',
                FOREIGN KEY (customer_id)      REFERENCES customers(customer_id),
                FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
                FOREIGN KEY (to_currency_id)   REFERENCES currencies(currency_id)
            );
            """
        )
        conn.commit()

    def reset(self):
        """Drops all tables - useful for tests / re-seeding demos."""
        conn = self.connect()
        conn.executescript(
            """
            DROP TABLE IF EXISTS transactions;
            DROP TABLE IF EXISTS exchange_rates;
            DROP TABLE IF EXISTS currencies;
            DROP TABLE IF EXISTS customers;
            """
        )
        conn.commit()
