import Items.Payment as Payment
import Items.Order as Order


class PaymentService:
    def __init__(self):
        print("Business logic for payments and receipts")

    def _pay(self, order: Order.Order, method: str) -> Payment.Payment:  # protected method
        # maybe not order but order_id? to be consistent, but we'll see
        print("paying for an order")

    def _prepare_receipt(self, order: Order.Order) -> Payment.Receipt:  # protected method
        print("preparing a receipt for an order")
