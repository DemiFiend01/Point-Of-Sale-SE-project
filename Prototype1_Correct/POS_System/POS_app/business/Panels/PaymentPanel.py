from django.shortcuts import render
from django.shortcuts import redirect
from POS_app.business.Actors.User import Role
from POS_app.business.Services import PaymentService
#will for sure need to add Order and Menu and Waiter later on
#also remember about implementing logic inside the Services
from POS_app.views import role_required


class PaymentPanel:
    def __init__(self):
        self._payment_service = PaymentService.PaymentService()
        print("This class will have methods that call the service and return templates to view")

    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_payment(request):
        return render(request, "waiter/Waiter_payment.html")
    
    def _list_ready_orders(self):  # protected method
        print("Based on database data list all orders ready for payment")

    def _show_receipt(self):  # protected method
        print("Based on database data show the receipt")

    def _mark_paid(self):  # protected method
        print("mark the order as paid")

MyPaymentPanel = PaymentPanel()