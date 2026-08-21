PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS currencies (
    currency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE CHECK (length(code) = 3),
    name TEXT NOT NULL,
    symbol TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS exchange_rates (
    rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_currency_id INTEGER NOT NULL,
    target_currency_id INTEGER NOT NULL,
    rate REAL NOT NULL CHECK (rate > 0),
    effective_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (base_currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (target_currency_id) REFERENCES currencies(currency_id),
    CHECK (base_currency_id <> target_currency_id)
);

CREATE TABLE IF NOT EXISTS exchange_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    rate_id INTEGER NOT NULL,
    source_currency_id INTEGER NOT NULL,
    target_currency_id INTEGER NOT NULL,
    source_amount REAL NOT NULL CHECK (source_amount > 0),
    exchange_rate REAL NOT NULL CHECK (exchange_rate > 0),
    target_amount REAL NOT NULL CHECK (target_amount > 0),
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('BUY', 'SELL')),
    transaction_date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (rate_id) REFERENCES exchange_rates(rate_id),
    FOREIGN KEY (source_currency_id) REFERENCES currencies(currency_id),
    FOREIGN KEY (target_currency_id) REFERENCES currencies(currency_id),
    CHECK (source_currency_id <> target_currency_id)
);

CREATE INDEX IF NOT EXISTS idx_transactions_customer
ON exchange_transactions(customer_id);

CREATE INDEX IF NOT EXISTS idx_rates_currency_pair
ON exchange_rates(base_currency_id, target_currency_id);
