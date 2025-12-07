from datetime import datetime
from enum import Enum


class Currency(Enum):  # can be modified in order to suit the restaurant's needs
    ZLOTY = "PLN"
    EURO = "EUR"
    KORUNA = "CZK"


class Money:
    def __init__(self, amount: float, currency: Currency):
        self._amount = amount  # float
        self._currency = currency  # string

    def _add(self, other):  # protected method
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValueError("Currencies must match!")
        return self._amount+other._amount

    def _str(self) -> str:  # protected method
        return ('%4.2f %s' % (self._amount, self._currency.value))


class Receipt:
    def __init__(self, id: str, order_id: int, lines: list, total: float):
        self._id = id  # added special id for receipt
        self._order_id = order_id  # string
        # list neednt be used in the model, this i think is purely business inside logic
        self._lines = lines
        self._total = total  # float
        # DELETED TAX FROM RECEIPT, because each menu item could have a different one

    def _to_pdf(self) -> bytes:  # protected method
        print("I am now a pdf")  # bytes? in order to print it

    def _to_str(self) -> str:  # protected method
        print("I am now a string and you can see me in the program")


class Payment:
    def __init__(self, id: str, method: str, amount: Money, receipt_num: int):
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
        # i do not know how to fix the id order receipt situation
        receipt = Receipt(self._receipt_number, self._id,
                          self._lines, self._amount)
        return receipt

    def _refund(self):  # protected method
        print("Refunding the payment")
