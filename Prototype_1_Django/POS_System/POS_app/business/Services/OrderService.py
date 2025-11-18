import Actors.Waiter as Waiter
import Items.Order as Order
import Items.MenuItem as MenuItem


class OrderService:
    def __init__(self):
        print("Business logic for order lifecycle")

    def _create(self, waiter: Waiter.Waiter, is_takeaway: bool, table_no: str | None, notes: str | None) -> Order.Order:  # protected method
        print("create an order")

    def _add_item(self, order_id: int, item: MenuItem.MenuItem, quantity: int) -> Order.OrderItem:  # protected method
        print("add an item to the order")

    def _remove_item(self, order_id: int, item_id: str):  # protected method
        print("remove an item from an order")

    def _confirm(self, order_id: int):  # protected method
        print("Confirm an order")

    def _set_takeaway(self, order_id: int, is_takeaway: bool):  # protected method
        print("setting takeaway")

    def _archive(self, order_id: int):  # protected method
        print("archiving an order")
