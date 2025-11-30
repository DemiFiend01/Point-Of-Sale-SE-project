import Items.Report as Report
import Items.Order as Order


class ReportingService:
    def __init__(self):
        print("Business logic for reporting and analytics")

    def _archived_orders(self) -> list[Order.Order]:  # protected method
        # add an arg called Filter
        print("based on FILTER return a list of archived filters")

    def _sales_summary(self) -> Report.Report:  # protected method
        print("Based on PERIOD argument generate a sales summary and return a report")
