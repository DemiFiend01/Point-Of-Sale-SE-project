from POS_app.business.Actors.User import Role
#will for sure need to add Order and Menu and Waiter later on
from POS_app.views import role_required

@role_required(allowed_roles=[Role.WAITER.name])
def waiter_cancel_order(request):
    print("")

class PaymentPanel:
    def __init__(self):
        print("needs GUI")

    def _list_ready_orders(self):  # protected method
        print("Based on database data list all orders ready for payment")

    def _show_receipt(self):  # protected method
        print("Based on database data show the receipt")

    def _mark_paid(self):  # protected method
        print("mark the order as paid")
