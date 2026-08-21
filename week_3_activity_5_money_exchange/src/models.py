"""
models.py
---------
每张表对应一个 Python 类，每个类负责自己的增删改查（CRUD），
并把领域规则（如"用最新汇率完成一笔兑换"）封装成方法，
而不是把 SQL 散落在调用方代码里。这是本项目 OOP 风格的核心体现。

设计要点：
- BaseModel  提供公共的 save / delete 骨架，避免重复代码（DRY）。
- 每个子类只需声明表名、主键名、字段列表，并可按需覆写方法。
- Transaction 类额外封装了 `execute_exchange()`，
  这是一个"充血模型"（rich domain model）的例子：
  它自己去查最新汇率、校验金额、计算兑换结果、写入交易记录，
  调用方不需要知道任何 SQL 细节。
"""

from __future__ import annotations
from typing import Optional, List
from .database import Database
from .exceptions import RateNotFoundError, RecordNotFoundError, InvalidAmountError


class BaseModel:
    """所有实体模型的公共基类，封装通用的 CRUD 骨架。"""

    table_name: str = ""
    pk_field: str = ""
    fields: List[str] = []   # 除主键外的可写字段，顺序需与 __init__ 一致

    def __init__(self, db: Database, **kwargs):
        self.db = db
        setattr(self, self.pk_field, kwargs.get(self.pk_field))
        for f in self.fields:
            setattr(self, f, kwargs.get(f, ""))

    def save(self):
        """INSERT 一条新记录，并把自增主键写回对象。"""
        placeholders = ", ".join("?" for _ in self.fields)
        columns = ", ".join(self.fields)
        values = [getattr(self, f) for f in self.fields]
        with self.db.get_connection() as conn:
            cur = conn.execute(
                f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
                values,
            )
            setattr(self, self.pk_field, cur.lastrowid)
        return self

    def update(self):
        """UPDATE 当前对象对应的记录。"""
        set_clause = ", ".join(f"{f}=?" for f in self.fields)
        values = [getattr(self, f) for f in self.fields] + [getattr(self, self.pk_field)]
        with self.db.get_connection() as conn:
            conn.execute(
                f"UPDATE {self.table_name} SET {set_clause} WHERE {self.pk_field}=?",
                values,
            )
        return self

    def delete(self):
        """DELETE 当前对象对应的记录。"""
        with self.db.get_connection() as conn:
            conn.execute(
                f"DELETE FROM {self.table_name} WHERE {self.pk_field}=?",
                (getattr(self, self.pk_field),),
            )

    @classmethod
    def get_by_id(cls, db: Database, record_id: int):
        with db.get_connection() as conn:
            row = conn.execute(
                f"SELECT * FROM {cls.table_name} WHERE {cls.pk_field}=?", (record_id,)
            ).fetchone()
        if row is None:
            raise RecordNotFoundError(f"{cls.__name__} #{record_id} 不存在")
        return cls(db, **dict(row))

    @classmethod
    def get_all(cls, db: Database) -> List["BaseModel"]:
        with db.get_connection() as conn:
            rows = conn.execute(f"SELECT * FROM {cls.table_name}").fetchall()
        return [cls(db, **dict(r)) for r in rows]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk_field}={getattr(self, self.pk_field)}>"


class Customer(BaseModel):
    """客户实体：兑换业务的服务对象，KYC 信息也存于此。"""

    table_name = "customers"
    pk_field = "customer_id"
    fields = ["first_name", "last_name", "phone", "email", "id_document", "address"]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Currency(BaseModel):
    """货币实体：系统支持兑换的每一种货币（USD、EUR、CNY……）。"""

    table_name = "currencies"
    pk_field = "currency_id"
    fields = ["code", "name", "symbol"]

    @classmethod
    def get_by_code(cls, db: Database, code: str) -> Optional["Currency"]:
        with db.get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM currencies WHERE code=?", (code.upper(),)
            ).fetchone()
        return cls(db, **dict(row)) if row else None


class Employee(BaseModel):
    """员工实体：记录是谁经手了这笔交易，便于审计和绩效统计。"""

    table_name = "employees"
    pk_field = "employee_id"
    fields = ["first_name", "last_name", "role", "hire_date"]


class ExchangeRate(BaseModel):
    """
    汇率实体：某一时刻，from_currency -> to_currency 的兑换比率。
    每次更新汇率都是新插入一行（而不是覆盖），
    这样可以保留历史汇率，便于对账和审计。
    """

    table_name = "exchange_rates"
    pk_field = "rate_id"
    fields = ["from_currency_id", "to_currency_id", "rate", "effective_date"]

    @classmethod
    def get_latest_rate(cls, db: Database, from_currency_id: int, to_currency_id: int) -> "ExchangeRate":
        """取某货币对最新（effective_date 最大）的一条汇率记录。"""
        with db.get_connection() as conn:
            row = conn.execute(
                """SELECT * FROM exchange_rates
                   WHERE from_currency_id=? AND to_currency_id=?
                   ORDER BY effective_date DESC, rate_id DESC LIMIT 1""",
                (from_currency_id, to_currency_id),
            ).fetchone()
        if row is None:
            raise RateNotFoundError(
                f"未找到货币 {from_currency_id} -> {to_currency_id} 的汇率，请先录入汇率"
            )
        return cls(db, **dict(row))


class Transaction(BaseModel):
    """
    交易实体：一次真实发生的货币兑换记录。
    这是"充血模型"的示例：execute_exchange() 把
    查汇率 -> 校验 -> 计算 -> 落库 这一整套业务规则封装起来。
    """

    table_name = "transactions"
    pk_field = "transaction_id"
    fields = [
        "customer_id", "employee_id",
        "from_currency_id", "to_currency_id",
        "from_amount", "to_amount", "rate_used",
        "transaction_date", "status",
    ]

    @classmethod
    def execute_exchange(
        cls,
        db: Database,
        customer: Customer,
        employee: Employee,
        from_currency: Currency,
        to_currency: Currency,
        from_amount: float,
    ) -> "Transaction":
        """
        执行一笔兑换：
        1. 校验金额合法
        2. 查询最新汇率
        3. 计算兑换后的金额
        4. 写入交易记录并返回该 Transaction 对象
        """
        if from_amount <= 0:
            raise InvalidAmountError("兑换金额必须大于 0")

        rate_obj = ExchangeRate.get_latest_rate(
            db, from_currency.currency_id, to_currency.currency_id
        )
        to_amount = round(from_amount * rate_obj.rate, 2)

        txn = cls(
            db,
            customer_id=customer.customer_id,
            employee_id=employee.employee_id,
            from_currency_id=from_currency.currency_id,
            to_currency_id=to_currency.currency_id,
            from_amount=from_amount,
            to_amount=to_amount,
            rate_used=rate_obj.rate,
            transaction_date=None,   # 交给数据库默认值 CURRENT_TIMESTAMP
            status="completed",
        )
        # transaction_date 用数据库默认值，这里从 fields 中单独处理
        txn.save()
        return txn

    def save(self):
        """覆写 save()：transaction_date 若为空，交给数据库 CURRENT_TIMESTAMP 默认值填充。"""
        columns = [f for f in self.fields if not (f == "transaction_date" and not getattr(self, f))]
        placeholders = ", ".join("?" for _ in columns)
        values = [getattr(self, f) for f in columns]
        with self.db.get_connection() as conn:
            cur = conn.execute(
                f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})",
                values,
            )
            self.transaction_id = cur.lastrowid
        return self
