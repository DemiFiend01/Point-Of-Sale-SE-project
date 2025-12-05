from POS_app.business.Actors import User
from POS_app.business.Items import Order


class Cook(User.User):
    def __init__(self):
        print("I have been born as a Cook")

    def _list_pending_order(self) -> list[Order.Order]:
        # how to link the cook with the pending orders?
        # where are they stored?
        # how is the cook able to access them?
        print("viewing pending orders")

    def _mark_item_ready(self, order_id: int, item_id: str):
        print("this item is ready")
        # INCORPORATE THE DATABASE LOGIC
        # search for the item id and order id here

    def _update_estimated_time(self, order_id: int, time: int):
        # somehow search for that order id and then update its time
        print("Updating time")

    def _mark_order_ready(self):
        print("Mark your order is ready!")

    def _view_order_details(self):
        print("viewing order details")
