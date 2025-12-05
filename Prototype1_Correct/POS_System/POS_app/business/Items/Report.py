from POS_app.business.Items import Order
from datetime import datetime


class Report:
    def __init__(self, p_from: datetime.date, p_to: datetime.date, total_orders: int, total_revenue: float, avg_prep_time_min: int):
        self.period_from = p_from  # datetime
        self.period_to = p_to  # datetime
        self.total_orders = total_orders  # int
        self.total_revenue = total_revenue  # float
        self.avg_prep_time_min = avg_prep_time_min  # probably int or datetime

    # protected method, orders is a list of Orders
    def _generate(self, orders: list[Order.Order]) -> "Report":
        print("will aggregate order data into summary metrics")
        # return Report apparently
