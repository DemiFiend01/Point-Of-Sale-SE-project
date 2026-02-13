from POS_app.business.Items import Payment, Order
from POS_app.models import Orders, ServingRules, Payments
from django.utils import timezone
from POS_app.business.Items import Utils
import requests
from decimal import Decimal


class PaymentService:
    def __init__(self):
        print("Business logic for payments and receipts")

    def _pay(self, order_id: int, currency: str) -> Payment.Payment:  # protected method
        try:
            order = Orders.objects.get(o_id=order_id)
            value = self._calculate_total(order.o_id)

        except Orders.DoesNotExist:
            return {"error": "Order not found."}

        payment = Payments(
            o_id=order,
            total=value["ZLOTY"],
            currency=currency,
            paid_at=timezone.now()
        )

        payment.full_clean()
        payment.save()

        # when generating a report change all orders to archived to then delete them after some time i guess
        order.status = Utils.OrderStatus.PAID.value
        print(order.status)
        order.paid_at = timezone.now()
        order.save()
        return {"success": "Order paid for."}

    def _calculate_total(self, order_id: int):
        try:
            order = Orders.objects.get(o_id=order_id)
        except Orders.DoesNotExist:
            return {"error": "Order not found."}

        serving_rules = ServingRules.objects.filter(
            o_id=order).select_related("oi_id__m_id")

        total = Decimal("0.00")
        for rule in serving_rules:
            order_item = rule.oi_id
            menu_item = order_item.m_id
            quantity = order_item.quantity
            unit_price = menu_item.price

            tax = menu_item.tax / Decimal(100)
            subtotal = quantity * unit_price * (1 + tax)
            total += subtotal

        total_dict = {}
        for curr in Payment.Currency:
            total_dict[curr.name] = round(
                self.convert_currency(total, curr.name), 2)
            print(total_dict[curr.name])

        return total_dict

    def convert_currency(self, value_PLN: float, currency: str) -> float:
        print(currency)
        if currency == "ZLOTY":
            return value_PLN
        if currency == "EURO":
            # at least for now, the APIs needed a key
            return value_PLN * Decimal("0.237113")
        if currency == "KORUNA":
            return value_PLN * Decimal("5.743682")

    def _prepare_receipt(self, order: Order.Order) -> Payment.Receipt:  # protected method
        print("preparing a receipt for an order")
