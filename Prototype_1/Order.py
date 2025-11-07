import datetime
import Utils
from Utils import OrderStatus
import MenuItem
import Waiter

class OrderItem:
    def __init__(self, id, menu_item, quantity, unit_price, status, ready_at, course):
        self.id = id
        self.menu_item = menu_item
        self.quantity = quantity
        self.unit_price = unit_price
        self.status = status
        self.ready_at = ready_at
        self.course = course

    def _mark_ready(self):
        self.status = OrderStatus.READY

    def subtotal(self):
        return self.quantity * self.unit_price
    
class Order:
    def __init__(self, id, status, is_takeaway, scheduled_pick_up, estimated_pick_up, table_no, notes, waiter, order_items, payment):
        self.id = id
        self.status = status
        self.is_takeaway = is_takeaway
        self.scheduled_pick_up = scheduled_pick_up
        self.estimated_pick_up = estimated_pick_up
        self.table_no = table_no
        self.notes = notes
        self.waiter = waiter
        self.order_items = order_items
        self.payment = payment

    def _add_item(self, menuItem, quantity):
        for i in range(quantity):
            self.order_items.append(menuItem)

    def _remove_item(self, item_id):
        print("jh")
        #access the item_id and delete it
        #remove based on the item_id from the order_items list

    def _confirm(self):
        self.status = OrderStatus.READY

    def _mark_paid(self, payment):
        #?? why is payment here?? if its paid its in full, do we need this here? maybe we should have a wrapper function somewhere that could mark order as paid and then also add money to the account
        self.status = OrderStatus.PAID
    
    def _archive(self):
        self.status = OrderStatus.ARCHIVED
    
    def total(self):
        total = 0
        #go through all the items and sum up the price
    