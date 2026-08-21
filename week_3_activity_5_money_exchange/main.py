"""
main.py
-------
演示脚本：
1. 初始化数据库（自动建表）
2. 插入示例客户、货币、员工、汇率
3. 调用 Transaction.execute_exchange() 完成一笔真实的兑换业务
4. 打印所有交易记录，验证数据落库正确
"""

from src import Database, Customer, Currency, Employee, ExchangeRate, Transaction


def seed_data(db: Database):
    """插入初始示例数据（仅在库为空时插入，避免重复运行报错）。"""
    if Currency.get_all(db):
        print("数据库已有数据，跳过初始化。")
        return

    usd = Currency(db, code="USD", name="US Dollar", symbol="$").save()
    eur = Currency(db, code="EUR", name="Euro", symbol="\u20ac").save()
    cny = Currency(db, code="CNY", name="Chinese Yuan", symbol="\u00a5").save()

    alice = Customer(
        db, first_name="Alice", last_name="Wang", phone="0210000000",
        email="alice@example.com", id_document="P123456789", address="Auckland, NZ"
    ).save()

    bob = Employee(db, first_name="Bob", last_name="Lee", role="Teller").save()

    ExchangeRate(db, from_currency_id=usd.currency_id, to_currency_id=cny.currency_id, rate=7.15).save()
    ExchangeRate(db, from_currency_id=eur.currency_id, to_currency_id=usd.currency_id, rate=1.08).save()

    print("初始数据已写入：3 种货币、1 位客户、1 位员工、2 条汇率。")


def demo_transaction(db: Database):
    """演示一次真实的兑换交易：Alice 用 200 美元换人民币。"""
    alice = Customer.get_all(db)[0]
    bob = Employee.get_all(db)[0]
    usd = Currency.get_by_code(db, "USD")
    cny = Currency.get_by_code(db, "CNY")

    txn = Transaction.execute_exchange(
        db, customer=alice, employee=bob,
        from_currency=usd, to_currency=cny, from_amount=200,
    )
    print(
        f"\n交易完成：{alice.full_name} 用 {txn.from_amount} {usd.code} "
        f"兑换得到 {txn.to_amount} {cny.code}（汇率 {txn.rate_used}），"
        f"经手人：{bob.first_name} {bob.last_name}"
    )


def print_all_transactions(db: Database):
    print("\n当前所有交易记录：")
    for t in Transaction.get_all(db):
        print(f"  #{t.transaction_id}: {t.from_amount} -> {t.to_amount}"
              f" (rate={t.rate_used}, status={t.status}, date={t.transaction_date})")


if __name__ == "__main__":
    db = Database("money_exchange.db")
    seed_data(db)
    demo_transaction(db)
    print_all_transactions(db)
