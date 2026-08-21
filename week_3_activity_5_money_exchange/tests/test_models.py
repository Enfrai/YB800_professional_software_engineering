"""
简单单元测试，使用临时内存数据库，验证：
1. 各实体的增删改查
2. 兑换交易的金额计算是否正确
3. 找不到汇率时是否抛出正确异常
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src import Database, Customer, Currency, Employee, ExchangeRate, Transaction
from src.exceptions import RateNotFoundError, InvalidAmountError


class TestMoneyExchangeSystem(unittest.TestCase):
    def setUp(self):
        # 每个测试用例使用独立的内存数据库，互不影响
        self.db = Database(":memory:")
        self.usd = Currency(self.db, code="USD", name="US Dollar", symbol="$").save()
        self.cny = Currency(self.db, code="CNY", name="Chinese Yuan", symbol="\u00a5").save()
        self.customer = Customer(
            self.db, first_name="Test", last_name="User", phone="123",
            email="t@example.com", id_document="ID001", address="NA"
        ).save()
        self.employee = Employee(self.db, first_name="Emp", last_name="One", role="Teller").save()

    def test_currency_crud(self):
        self.assertEqual(len(Currency.get_all(self.db)), 2)
        fetched = Currency.get_by_code(self.db, "usd")
        self.assertEqual(fetched.name, "US Dollar")

    def test_exchange_rate_lookup(self):
        ExchangeRate(
            self.db, from_currency_id=self.usd.currency_id,
            to_currency_id=self.cny.currency_id, rate=7.2
        ).save()
        latest = ExchangeRate.get_latest_rate(self.db, self.usd.currency_id, self.cny.currency_id)
        self.assertAlmostEqual(latest.rate, 7.2)

    def test_execute_exchange_success(self):
        ExchangeRate(
            self.db, from_currency_id=self.usd.currency_id,
            to_currency_id=self.cny.currency_id, rate=7.0
        ).save()
        txn = Transaction.execute_exchange(
            self.db, self.customer, self.employee, self.usd, self.cny, from_amount=100
        )
        self.assertEqual(txn.to_amount, 700.0)
        self.assertEqual(len(Transaction.get_all(self.db)), 1)

    def test_execute_exchange_no_rate_raises(self):
        with self.assertRaises(RateNotFoundError):
            Transaction.execute_exchange(
                self.db, self.customer, self.employee, self.usd, self.cny, from_amount=50
            )

    def test_execute_exchange_invalid_amount_raises(self):
        ExchangeRate(
            self.db, from_currency_id=self.usd.currency_id,
            to_currency_id=self.cny.currency_id, rate=7.0
        ).save()
        with self.assertRaises(InvalidAmountError):
            Transaction.execute_exchange(
                self.db, self.customer, self.employee, self.usd, self.cny, from_amount=-10
            )


if __name__ == "__main__":
    unittest.main()
