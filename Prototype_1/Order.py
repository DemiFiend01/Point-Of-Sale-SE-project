import datetime
import Utils
from Utils import OrderStatus
import MenuItem
import Waiter
import Payment


class OrderItem:
    def __init__(self, id, menu_item: MenuItem.MenuItem, quantity, unit_price, status: OrderStatus, ready_at, course):
        self.id = id  # string
        self.menu_item = menu_item  # MenuItem
        self.quantity = quantity  # int
        self.unit_price = unit_price  # snapshot at add time
        self.status = status  # OrderStatus
        self.ready_at = ready_at  # datetime | none
        self.course = course  # string

    def _mark_ready(self):  # protected method
        self.status = OrderStatus.READY
        self.ready_at = datetime.date

    def _subtotal(self):  # protected method
        return self.quantity * self.unit_price


class ServingRule:  # i do not quite get how this works. maybe a list of pairs would be a better fit?
    def __init__(self, position, course, items: list[OrderItem]):
        self.position = position
        self.course = course
        self.items = items


class Order:
    def __init__(self, id, status: OrderStatus, is_takeaway, scheduled_pick_up, estimated_pick_up, table_no, notes, waiter: Waiter, order_items: list[OrderItem], payment: Payment):
        self.id = id  # string
        self.created_at = datetime.date  # datetime
        self.status = status  # OrderStatus
        self.is_takeaway = is_takeaway  # bool
        self.scheduled_pick_up = scheduled_pick_up  # datetime | none
        self.estimated_pick_up = estimated_pick_up  # datetime | none
        self.table_no = table_no  # string | none
        self.notes = notes  # string | none
        self.waiter = waiter  # Waiter
        self.order_items = order_items  # list[OrderItem]
        self.payment = payment  # Payment | none
        # the rest: ready_at, delivered_at, paid_at, archived_at
        self.ready_at
        self.delivered_at
        self.paid_at
        self.archived_at

    def _add_item(self, menuItem: MenuItem.MenuItem, quantity):  # protected method
        for i in range(quantity):
            self.order_items.append(menuItem)

    def _remove_item(self, item_id):  # protected method
        print("jh")
        for item in self.order_items:
            if item.id == item_id:
                self.order_items.remove(item)
                return True
        return False  # could not find the item

    # protected method
    def _set_serving_sequence(self, rules: list[ServingRule]):
        print("serving sequence can be also none")

    def _confirm(self):  # protected method
        if self.status != OrderStatus.NEW:
            raise AttributeError("The order is not new")
        self.status = OrderStatus.AWAITING_PREPARATION

    def _mark_paid(self, payment: Payment):  # protected method
        if self.status != OrderStatus.READY:
            raise AttributeError("The order is not ready yet.")
        # ?? why is payment here?? if its paid its in full, do we need this here? maybe we should have a wrapper function somewhere that could mark order as paid and then also add money to the account
        self.status = OrderStatus.PAID
        self.paid_at = datetime.date

    def _archive(self):  # protected method
        if self.status != OrderStatus.PAID:
            raise AttributeError("The order was not paid for, cannot archive.")
        self.status = OrderStatus.ARCHIVED
        self.archived_at = datetime.date

    def _total(self):  # protected method
        total = 0
        for item in self.order_items:
            total += item.unit_price
        return total
