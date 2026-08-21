"""自定义业务异常，让错误信息比裸露的 sqlite3 报错更有语义。"""


class MoneyExchangeError(Exception):
    """所有业务异常的基类。"""


class RateNotFoundError(MoneyExchangeError):
    """请求的货币对没有可用汇率时抛出。"""


class RecordNotFoundError(MoneyExchangeError):
    """按主键查询不到记录时抛出。"""


class InvalidAmountError(MoneyExchangeError):
    """兑换金额非法（<=0）时抛出。"""
