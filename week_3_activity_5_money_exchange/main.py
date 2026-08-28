"""
main.py
-------
Demo entry point. Run this after seed_data.py to see the OOP layers work
together: Database -> Repositories -> Service -> Models.

Usage:
    python seed_data.py
    python main.py
"""

from src.database import Database
from src.repositories import CustomerRepository
from src.services import ExchangeService


def main():
    db = Database("money_exchange.db")
    db.initialize_schema()

    customer_repo = CustomerRepository(db)
    alice = customer_repo.get_by_email("alice@example.com")

    if not alice:
        print("No seed data found. Run `python seed_data.py` first.")
        return

    service = ExchangeService(db)

    print(f"Customer: {alice.full_name} ({alice.email})")
    txn = service.perform_exchange(
        customer_id=alice.customer_id,
        from_code="NZD",
        to_code="USD",
        amount=500,
    )
    print(
        f"Exchanged {txn.amount_from} NZD -> {txn.amount_to} USD "
        f"at rate {txn.rate_applied} (txn #{txn.transaction_id})"
    )

    print("\nAll transactions on record:")
    for t in service.transactions.get_all():
        print(f"  #{t.transaction_id}: customer {t.customer_id} | "
              f"{t.amount_from} -> {t.amount_to} @ {t.rate_applied} | {t.transaction_date}")

    db.close()


if __name__ == "__main__":
    main()
