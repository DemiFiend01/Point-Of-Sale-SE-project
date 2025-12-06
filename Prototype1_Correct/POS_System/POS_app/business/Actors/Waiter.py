from POS_app.business.Actors import User
# from POS_app.business.Items import Order
# from POS_app.business.Items import MenuItem
# from POS_app.business.Items import Payment
from POS_app.business.Items import Utils
import datetime


class Waiter(User.User):
    def __init__(self,  name: str, login: str, password: str, role: User.Role):
        print("Im a waiter yay")
        super().__init__(name, login, password, role)

    # protected method - string type hints

    def _create_order(self, is_takeaway: bool, scheduled_pick_up: datetime.date, estimated_pick_up: datetime.date, table_no: int) -> "Order":
        from POS_app.business.Items import Order
        order = Order.Order(0, Utils.OrderStatus.NEW, is_takeaway,
                            scheduled_pick_up, estimated_pick_up, table_no, "", self)

        # where to store it?
        return order

    def _add_product(self, order: "Order", menu_item: "MenuItem", quantity: int):  # protected method
        order._add_item(menu_item, quantity)
        print("added the menu item")

    def _confirm_order(self, order: "Order"):  # protected method
        print("confirming the order")
        order._confirm()

    def _finalize_payment(self, order: "Order", method: str, currency: str, receipt_id=int) -> "Payment":  # protected method
        from POS_app.business.Items import Payment
        payment = Payment.Payment(order._id, method, Utils.Money(
            order._total(), currency), receipt_id)
        # somehow link receipt and payment here!
        # what is up with receipt id? what comes first???
        # where to store all of this??
        print("processing the payment")
        return payment

    # proposed methods
    def _cancel_product(self, order: "Order", menu_item: "MenuItem"):  # protected method
        order._remove_item(menu_item._id)

    def _cancel_order(self, order: "Order"):  # protected method
        order._cancel_order()
        print("canceling the order")

    def _generate_receipt(self, order: "Order"):  # protected method
        # need to set lines and tax!
        from POS_app.business.Items import Payment
        receipt = Payment.Receipt(order._id, 0, order._total(), 23)
        # can now generate _str or pdf
        print("generating the receipt")

    def _add_notes_to_order(self, order: "Order", notes: str):  # protected method
        order._notes = notes

    def _view_ready_orders(self):  # protected method
        print("viewing ready orders")
