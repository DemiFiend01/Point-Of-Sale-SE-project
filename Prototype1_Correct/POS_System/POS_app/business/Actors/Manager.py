from POS_app.business.Actors import User
from POS_app.business.Items import Report
from POS_app.business.Items import Order
# inheritance


class Manager(User.User):
    def __init__(self,  name: str, login: str, password: str, role: User.Role):
        print("Manager")
        super().__init__(name, login, password, role)

    def _manage_menu(self):  # protected method
        print("managing the menu")

    def _generate_report(self) -> Report.Report:  # protected method
        print("Generating")
        report = Report.Report(0, 0, 0, 0, 0)  # placeholders
        return report

    def _view_archived_orders(self) -> list[Order.Order]:  # protected method
        print("Viewing")
        # add menuService here!
        # incorporate database viewing
