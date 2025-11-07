import Utils
from datetime import datetime


class Receipt:
    def __init__(self,order_id, lines, total, tax=23):
        self.order_id = order_id
        self.lines = lines #list, i do not understand what it exactly is, the number of lines on the receipt?
        self.total = total
        self.tax = tax

    def to_pdf(self):
        print("I am now a pdf")

    def to_str(self):
        print("I am now a string and you can see me in the program")

class Payment:
    def __init__(self,id,order_id,method, amount, receipt_num):
        self.id = id
        self.order_id = order_id #different than payment id for now, could always be changed
        self.method = method
        self.amount = amount
        self.paid_at = datetime.datetime
        self.receipt_number = receipt_num

    def _generate_receipt(self):
        lines = 1
        print("Generating")  #i dont know what to do about the lines here, do we extract it from order?
        receipt =  Receipt(self.order_id, lines, self.amount) #default tax for now      

