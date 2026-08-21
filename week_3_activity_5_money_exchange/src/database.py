from pathlib import Path
import sqlite3


class DatabaseManager:
    """Manage the SQLite database connection and schema."""

    def __init__(self, database_path: str = "data/money_exchange.db"):
        self.database_path = database_path
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        """Create a configured database connection."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        """Create all required database tables and indexes."""
        schema_path = Path(__file__).resolve().parent.parent / "schema.sql"
        schema = schema_path.read_text(encoding="utf-8")
        with self.connect() as connection:
            connection.executescript(schema)

    def seed_data(self) -> None:
        """Insert initial currencies when the database is empty."""
        currencies = [
            ("USD", "US Dollar", "$"),
            ("NZD", "New Zealand Dollar", "$"),
            ("EUR", "Euro", "€"),
            ("AUD", "Australian Dollar", "$"),
            ("GBP", "British Pound", "£"),
        ]

        with self.connect() as connection:
            count = connection.execute(
                "SELECT COUNT(*) AS count FROM currencies"
            ).fetchone()["count"]

            if count == 0:
                connection.executemany(
                    """
                    INSERT INTO currencies (code, name, symbol)
                    VALUES (?, ?, ?)
                    """,
                    currencies,
                )
