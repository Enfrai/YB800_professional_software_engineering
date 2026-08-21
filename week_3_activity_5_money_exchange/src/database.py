"""
database.py
-----------
负责创建数据库连接、初始化表结构（Schema）。
采用单一职责原则：Database 类只管"连接与建表"，
不掺杂任何业务逻辑（业务逻辑放在 models.py 中的各实体类里）。
"""

import sqlite3
from contextlib import contextmanager


class Database:
    """封装 SQLite 连接与建表逻辑。"""

    def __init__(self, db_path: str = "money_exchange.db"):
        self.db_path = db_path
        # ":memory:" 数据库只在单个连接的生命周期内存在，
        # 如果每次都新开连接会导致每次拿到的是"另一个"空库，
        # 所以对内存库保留一个常驻连接；对文件库则按需开关连接。
        self._persistent_conn = None
        if self.db_path == ":memory:":
            self._persistent_conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._persistent_conn.execute("PRAGMA foreign_keys = ON")
            self._persistent_conn.row_factory = sqlite3.Row
        self._init_schema()

    @contextmanager
    def get_connection(self):
        """提供一个自动提交/回滚的连接上下文管理器。"""
        if self._persistent_conn is not None:
            conn = self._persistent_conn
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            return

        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self):
        """创建 5 张表（若已存在则跳过）。表的设计理由详见 README.md。"""
        schema = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name    TEXT NOT NULL,
            last_name     TEXT NOT NULL,
            phone         TEXT,
            email         TEXT UNIQUE,
            id_document   TEXT NOT NULL,   -- 身份证/护照号，KYC 合规需要
            address       TEXT,
            created_at    TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS currencies (
            currency_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            code          TEXT NOT NULL UNIQUE,   -- 如 USD, EUR, CNY (ISO 4217)
            name          TEXT NOT NULL,
            symbol        TEXT
        );

        CREATE TABLE IF NOT EXISTS employees (
            employee_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name    TEXT NOT NULL,
            last_name     TEXT NOT NULL,
            role          TEXT NOT NULL,           -- teller / manager 等
            hire_date     TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS exchange_rates (
            rate_id           INTEGER PRIMARY KEY AUTOINCREMENT,
            from_currency_id  INTEGER NOT NULL,
            to_currency_id    INTEGER NOT NULL,
            rate              REAL NOT NULL CHECK (rate > 0),
            effective_date    TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
            FOREIGN KEY (to_currency_id)   REFERENCES currencies(currency_id),
            UNIQUE (from_currency_id, to_currency_id, effective_date)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id        INTEGER NOT NULL,
            employee_id        INTEGER NOT NULL,
            from_currency_id   INTEGER NOT NULL,
            to_currency_id     INTEGER NOT NULL,
            from_amount        REAL NOT NULL CHECK (from_amount > 0),
            to_amount          REAL NOT NULL CHECK (to_amount > 0),
            rate_used          REAL NOT NULL,
            transaction_date   TEXT DEFAULT CURRENT_TIMESTAMP,
            status             TEXT DEFAULT 'completed',
            FOREIGN KEY (customer_id)      REFERENCES customers(customer_id),
            FOREIGN KEY (employee_id)      REFERENCES employees(employee_id),
            FOREIGN KEY (from_currency_id) REFERENCES currencies(currency_id),
            FOREIGN KEY (to_currency_id)   REFERENCES currencies(currency_id)
        );
        """
        with self.get_connection() as conn:
            conn.executescript(schema)
