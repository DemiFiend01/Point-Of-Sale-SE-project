from django.shortcuts import render
from django.shortcuts import redirect
from POS_app.business.Actors.User import Role
from POS_app.business.Services import PaymentService
from POS_app.business.Services import OrderService
from POS_app.business.Panels import OrderCreationPanel
from POS_app.business.Items import Payment
# will for sure need to add Order and Menu and Waiter later on
# also remember about implementing logic inside the Services
from POS_app.views import role_required


class PaymentPanel:
    def __init__(self):
        self._payment_service = PaymentService.PaymentService()
        self._order_service = OrderService.OrderService()
        self._order_creation_panel = OrderCreationPanel.OrderCreationPanel()
        print("This class will have methods that call the service and return templates to view")

    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_payment(self, request):
        errors = None
        success = None

        if request.method == "POST":
            order_id = request.POST.get("order_id")
            if order_id:
                # result = self._order_service.mark_delivered(order_id)
                result = self._payment_service._pay(
                    order_id=order_id, currency=request.POST.get("currency"))
                if "error" in result:
                    errors = result["error"]
                else:
                    success = result["success"]

        orders = self._order_service.list_delivered()
        for o in orders:
            print(
                f"Order ID: {o.o_id}, Status: {o.status}, Delivered at: {o.delivered_at}")
        order_items = self._order_creation_panel._build_order_items_map(orders)

        currencies = []
        for c in Payment.Currency:
            currencies.append([c.name, c.value])
            print(c.name, c.value)

        for order in orders:
            totals = self._payment_service._calculate_total(order.o_id)
            order.default_total = totals['ZLOTY']

        return render(
            request,
            "waiter/Waiter_payment.html",
            {"orders": orders, "order_items": order_items,
                "error": errors, "success": success,
                "currencies": currencies},
        )

    def _list_ready_orders(self):  # protected method
        print("Based on database data list all orders ready for payment")

    def _show_receipt(self):  # protected method
        print("Based on database data show the receipt")

    def _mark_paid(self):  # protected method
        print("mark the order as paid")


MyPaymentPanel = PaymentPanel()
