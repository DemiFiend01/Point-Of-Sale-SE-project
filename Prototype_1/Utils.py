import Order
import Utils


class Money:
    def __init__(self, amount: float, currency: str):
        self._amount = amount  # float
        self._currency = currency  # string

    def _add(self, other: Utils.Money):  # protected method
        if self._currency != other._currency:
            raise ValueError("Currencies must match!")
        return self._amount+other._amount

    def _str(self):  # protected method
        return ('%4.2f %s' % (self._amount, self._currency))


class PreparationTimeEstimator:
    @staticmethod
    def estimate(order: Order.Order):  # public method
        print("Predicting total prep time")
        estimated_time = 0  # minutes?
        for item in order._order_items:
            estimated_time += item._prep_time_min
        return estimated_time
