from enum import Enum
import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from POS_app.business.Items.Order import Order


class PreparationTimeEstimator:
    @staticmethod
    def estimate(order: "Order") -> int:  # public method
        print("Predicting total prep time")
        estimated_time = 0  # minutes?
        for item in order._order_items:
            estimated_time += item._prep_time_min
        return estimated_time


class OrderStatus(Enum):
    NEW = "New"
    AWAITING_PREPARATION = "Awaiting preparation"
    IN_PREPARATION = "In preparation"
    READY = "Ready"
    PAID = "Paid"
    ARCHIVED = "Archived"
    CANCELED = "Canceled"


class IDGenerator:
    def __init__(self):
        self.curr_order_id = 0
        self.today = datetime.datetime.today()

    @staticmethod
    def order_id_generator(self, order: "Order") -> int:
        today = datetime.datetime.today()
        if today != self.today:
            self.curr_order_id = 0
            self.today = today

        self.curr_order_id += 1

        if self.curr_order_id >= 99:
            self.curr_order_id == 1

        return self.curr_order_id
