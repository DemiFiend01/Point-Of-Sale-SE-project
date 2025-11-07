import Employee

class Waiter(Employee):
    def __init__(self):
        print("Im a waiter yay")

    def createNewOrder(self):
        print("creating new orderrr")

    def confirmOrder(self):
        print("confirming the order")

    def cancelOrder(self):
        print("canceling the order")

    def markOrderDelivered(self):
        print("the order is now delivered")

    def processPayment(self):
        print("processing the payment")

    def generateReceipt(self):
        print("generating the receipt")

    def addNotesToOrder(self):
        print("client is lactose-intolerant, what a prick")

    def viewReadyOrders(self):
        print("viewing ready orders")