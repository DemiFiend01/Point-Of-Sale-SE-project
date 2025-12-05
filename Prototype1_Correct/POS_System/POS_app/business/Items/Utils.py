from POS_app.business.Items import Order, Utils
from enum import Enum
import datetime


class Money:
    def __init__(self, amount: float, currency: str):
        self._amount = amount  # float
        self._currency = currency  # string

    def _add(self, other: Utils.Money):  # protected method
        if self._currency != other._currency:
            raise ValueError("Currencies must match!")
        return self._amount+other._amount

    def _str(self) -> str:  # protected method
        return ('%4.2f %s' % (self._amount, self._currency))


class PreparationTimeEstimator:
    @staticmethod
    def estimate(order: Order.Order) -> int:  # public method
        print("Predicting total prep time")
        estimated_time = 0  # minutes?
        for item in order._order_items:
            estimated_time += item._prep_time_min
        return estimated_time


class OrderStatus(Enum):
    NEW = 1
    AWAITING_PREPARATION = 2
    IN_PREPARATION = 3
    READY = 4
    PAID = 5
    ARCHIVED = 6
    CANCELED = 7


class IDGenerator:
    def __init__(self):
        self.curr_order_id = 0
        self.today = datetime.datetime.today()

    @staticmethod
    def order_id_generator(self, order: Order.Order) -> int:
        today = datetime.datetime.today()
        if today != self.today:
            self.curr_order_id = 0
            self.today = today

        self.curr_order_id += 1

        if self.curr_order_id >= 99:
            self.curr_order_id == 1

        return self.curr_order_id
