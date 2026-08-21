from .models import Customer, ExchangeRate, ExchangeTransaction
from .repositories import (
    CustomerRepository,
    CurrencyRepository,
    ExchangeRateRepository,
    ExchangeTransactionRepository,
)


class MoneyExchangeService:
    """Provide business operations for the money exchange system."""

    def __init__(self, db):
        self.customers = CustomerRepository(db)
        self.currencies = CurrencyRepository(db)
        self.rates = ExchangeRateRepository(db)
        self.transactions = ExchangeTransactionRepository(db)

    def create_customer(self, first_name, last_name, email, phone=None):
        """Create and persist a customer."""
        customer = Customer(first_name, last_name, email, phone)
        return self.customers.create(customer)

    def add_exchange_rate(self, base_code, target_code, rate):
        """Create a new exchange rate for a currency pair."""
        if rate <= 0:
            raise ValueError("Exchange rate must be greater than zero.")

        base = self.currencies.find_by_code(base_code)
        target = self.currencies.find_by_code(target_code)

        if not base or not target:
            raise ValueError("Both currencies must exist.")

        if base.currency_id == target.currency_id:
            raise ValueError("Base and target currencies must be different.")

        exchange_rate = ExchangeRate(
            base_currency_id=base.currency_id,
            target_currency_id=target.currency_id,
            rate=rate,
        )
        return self.rates.create(exchange_rate)

    def calculate_exchange(self, amount, rate):
        """Calculate the target amount for a given source amount and rate."""
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        if rate <= 0:
            raise ValueError("Exchange rate must be greater than zero.")
        return round(amount * rate, 2)

    def record_exchange(
        self,
        customer_id,
        rate_id,
        source_code,
        target_code,
        source_amount,
        transaction_type="BUY",
    ):
        """Calculate and persist a completed exchange transaction."""
        source = self.currencies.find_by_code(source_code)
        target = self.currencies.find_by_code(target_code)
        rate = self.rates.find_by_id(rate_id)
        customer = self.customers.find_by_id(customer_id)

        if not customer:
            raise ValueError("Customer does not exist.")
        if not source or not target:
            raise ValueError("Both currencies must exist.")
        if not rate:
            raise ValueError("Exchange rate does not exist.")

        if (
            rate.base_currency_id != source.currency_id
            or rate.target_currency_id != target.currency_id
        ):
            raise ValueError("The exchange rate does not match the currency pair.")

        target_amount = self.calculate_exchange(source_amount, rate.rate)

        transaction = ExchangeTransaction(
            customer_id=customer_id,
            rate_id=rate_id,
            source_currency_id=source.currency_id,
            target_currency_id=target.currency_id,
            source_amount=source_amount,
            exchange_rate=rate.rate,
            target_amount=target_amount,
            transaction_type=transaction_type,
        )
        return self.transactions.create(transaction)

    def get_customer_history(self, customer_id):
        """Return all exchanges belonging to a customer."""
        return self.transactions.find_by_customer(customer_id)
