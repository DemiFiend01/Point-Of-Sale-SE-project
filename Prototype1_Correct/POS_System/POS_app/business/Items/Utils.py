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
    DELIVERED = "Delivered"
    PAID = "Paid"
    ARCHIVED = "Archived"
    CANCELED = "Canceled"


class IDGenerator:
    def __init__(self):
        self.curr_order_id = 0

    def order_id_generator(self) -> int:
        self.curr_order_id += 1

        if self.curr_order_id > 999:
            self.curr_order_id = 1

        return self.curr_order_id


IDGenerate = IDGenerator()
