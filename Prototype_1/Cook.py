import Employee

class Cook(Employee):
    def __init__(self):
        print("I have been born as a Cook")

    def viewPendingOrder(self):
        print("viewing pending orders")
    
    def markItemReady(self):
        print("this item is ready")

    def markOrderReady(self):
        print("Mark your order is ready!")

    def viewOrderDetails(self):
        print("viewing order details")