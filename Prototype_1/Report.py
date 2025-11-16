import Order


class Report:
    def __init__(self, p_from, p_to, total_orders, total_revenue, avg_prep_time_min):
        self.period_from = p_from  # datetime
        self.period_to = p_to  # datetime
        self.total_orders = total_orders  # int
        self.total_revenue = total_revenue  # float
        self.avg_prep_time_min = avg_prep_time_min

    # protected method, orders is a list of Orders
    def _generate(self, orders: list[Order.Order]):
        print("will aggregate order data into summary metrics")
