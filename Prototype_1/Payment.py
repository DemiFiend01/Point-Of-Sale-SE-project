import Utils
from datetime import datetime


class Receipt:
    def __init__(self, order_id, lines, total, tax=23):
        self.order_id = order_id  # string
        self.lines = lines  # list
        self.total = total  # float
        self.tax = tax  # float

    def _to_pdf(self):  # protected method
        print("I am now a pdf")

    def _to_str(self):  # protected method
        print("I am now a string and you can see me in the program")


class Payment:
    def __init__(self, id, method, amount: Utils.Money, receipt_num):
        self.id = id  # string
        self.method = method  # string 'Cash', 'Card' maybe could be Enum later
        self.amount = amount  # Money
        self.paid_at = datetime.datetime  # datetime | none
        self.receipt_number = receipt_num  # string

    def _generate_receipt(self):  # protected method, returns Receipt
        lines = 1
        # i dont know what to do about the lines here, do we extract it from order?
        print("Generating")
        # default tax for now
        receipt = Receipt(self.order_id, lines, self.amount)

    def _refund(self):  # protected method
        print("Refunding the payment")
