from POS_app.business.Services import ReportingService

class OrderHistoryPanel:
    def __init__(self):
        self._reporting_service = ReportingService.ReportingService()
        print("This class will have methods that will call the reporting service (handles the DB) and will manage the view")

    def _list_archived(self):  # protected method
        print("based on the database data list all archived orders")

    def _filter_by_date(self):  # protected method
        print("show orders filtered by date?")

    def _generate_report(self):  # protected method
        # will probably need buttons to show it as string or pdf
        print("Generate the report")

MyOrderHistoryPanel = OrderHistoryPanel()