import Employee

class Cook(Employee):
    def __init__(self):
        print("I have been born as a Cook")

    def view_pending_order(self):
        print("viewing pending orders")
    
    def mark_item_ready(self):
        print("this item is ready")

    def mark_order_ready(self):
        print("Mark your order is ready!")

    def view_order_details(self):
        print("viewing order details")