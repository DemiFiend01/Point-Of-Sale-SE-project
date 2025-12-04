import Utils
from datetime import datetime


class Receipt:
    def __init__(self, id: str, order_id: int, lines: list, total: float, tax=23):
        self._id = id # added special id for receipt
        self._order_id = order_id  # string
        self._lines = lines  # list
        self._total = total  # float
        self._tax = tax  # float

    def _to_pdf(self) -> bytes:  # protected method
        print("I am now a pdf")  # bytes? in order to print it

    def _to_str(self) -> str:  # protected method
        print("I am now a string and you can see me in the program")


class Payment:
    def __init__(self, id: str, method: str, amount: Utils.Money, receipt_num: int):
        self._id = id  # string order id? most probably
        self._method = method  # string 'Cash', 'Card' maybe could be Enum later
        self._amount = amount  # Money
        self._paid_at = datetime.datetime  # datetime | none
        self._receipt_number = receipt_num  # int

    def _generate_receipt(self) -> Receipt:  # protected method, returns Receipt
        lines = 1
        # i dont know what to do about the lines here, do we extract it from order?
        print("Generating")
        # default tax for now
        receipt = Receipt(self._receipt_number, self._id, self._lines, self._amount) #i do not know how to fix the id order receipt situation
        return receipt

    def _refund(self):  # protected method
        print("Refunding the payment")
