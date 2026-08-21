from src.database import DatabaseManager
from src.services import MoneyExchangeService


def main():
    """Run a small demonstration of the Money Exchange System."""
    database = DatabaseManager()
    database.initialize()
    database.seed_data()

    service = MoneyExchangeService(database)

    customer = service.create_customer(
        "John",
        "Smith",
        "john.smith@example.com",
        "+64 21 123 4567",
    )

    rate = service.add_exchange_rate("USD", "NZD", 1.68)

    transaction = service.record_exchange(
        customer_id=customer.customer_id,
        rate_id=rate.rate_id,
        source_code="USD",
        target_code="NZD",
        source_amount=100.00,
        transaction_type="BUY",
    )

    print("Money Exchange System")
    print("---------------------")
    print(f"Customer: {customer.first_name} {customer.last_name}")
    print(f"Transaction ID: {transaction.transaction_id}")
    print(f"Source amount: {transaction.source_amount:.2f} USD")
    print(f"Exchange rate: {transaction.exchange_rate:.6f}")
    print(f"Target amount: {transaction.target_amount:.2f} NZD")


if __name__ == "__main__":
    main()
