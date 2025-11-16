import Order
import Utils


class Money:
    def __init__(self, amount, currency):
        self.amount = amount  # float
        self.currency = currency  # string

    def _add(self, other: Utils.Money):  # protected method
        if self.currency != other.currency:
            raise ValueError("Currencies must match!")
        return self.amount+other.amount

    def _str(self):  # protected method
        return ('%4.2f %s' % (self.amount, self.currency))


class PreparationTimeEstimator:
    @staticmethod
    def estimate(order: Order.Order):  # public method
        print("Predicting total prep time")
        estimated_time = 0  # minutes?
        for item in order.order_items:
            estimated_time += item.prep_time_min
        return estimated_time
