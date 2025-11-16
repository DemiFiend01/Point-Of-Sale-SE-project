import datetime
import Utils
from Utils import OrderStatus
import MenuItem
import Waiter
import Payment


class OrderItem:
    def __init__(self, id: str, menu_item: MenuItem.MenuItem, quantity: int, unit_price, status: OrderStatus, ready_at: datetime.date, course: str):
        self._id = id  # string
        self._menu_item = menu_item  # MenuItem
        self._quantity = quantity  # int
        self._unit_price = unit_price  # snapshot at add time
        self._status = status  # OrderStatus
        self._ready_at = ready_at  # datetime | none
        self._course = course  # string

    def _mark_ready(self):  # protected method
        self._status = OrderStatus.READY
        self._ready_at = datetime.date

    def _subtotal(self):  # protected method
        return self._quantity * self._unit_price


class ServingRule:  # i do not quite get how this works. maybe a list of pairs would be a better fit?
    def __init__(self, position: int, course: str, items: list[OrderItem]):
        self._position = position
        self._course = course
        self._items = items


class Order:
    def __init__(self, id: str, status: OrderStatus, is_takeaway: bool, scheduled_pick_up: datetime.date, estimated_pick_up: datetime.date, table_no: str, notes: str, waiter: Waiter, order_items: list[OrderItem], payment: Payment):
        self._id = id  # string
        self._created_at = datetime.date  # datetime
        self._status = status  # OrderStatus
        self._is_takeaway = is_takeaway  # bool
        self._scheduled_pick_up = scheduled_pick_up  # datetime | none
        self._estimated_pick_up = estimated_pick_up  # datetime | none
        self._table_no = table_no  # string | none # WHY IS NUMBER A STRING
        self._notes = notes  # string | none
        self._waiter = waiter  # Waiter
        self._order_items = order_items  # list[OrderItem]
        self._payment = payment  # Payment | none
        # the rest: ready_at, delivered_at, paid_at, archived_at
        self._ready_at
        self._delivered_at
        self._paid_at
        self._archived_at

    def _add_item(self, menuItem: MenuItem.MenuItem, quantity: int):  # protected method
        for i in range(quantity):
            self._order_items.append(menuItem)

    def _remove_item(self, item_id):  # protected method
        print("jh")
        for item in self._order_items:
            if item._id == item_id:
                self._order_items.remove(item)
                return True
        return False  # could not find the item

    # protected method
    def _set_serving_sequence(self, rules: list[ServingRule]):
        print("serving sequence can be also none")

    def _confirm(self):  # protected method
        if self._status != OrderStatus.NEW:
            raise AttributeError("The order is not new")
        self._status = OrderStatus.AWAITING_PREPARATION

    def _mark_paid(self, payment: Payment):  # protected method
        if self._status != OrderStatus.READY:
            raise AttributeError("The order is not ready yet.")
        # ?? why is payment here?? if its paid its in full, do we need this here? maybe we should have a wrapper function somewhere that could mark order as paid and then also add money to the account
        self._status = OrderStatus.PAID
        self._paid_at = datetime.date

    def _archive(self):  # protected method
        if self._status != OrderStatus.PAID:
            raise AttributeError("The order was not paid for, cannot archive.")
        self._status = OrderStatus.ARCHIVED
        self._archived_at = datetime.date

    def _total(self):  # protected method
        total = 0
        for item in self._order_items:
            total += item._unit_price
        return total
