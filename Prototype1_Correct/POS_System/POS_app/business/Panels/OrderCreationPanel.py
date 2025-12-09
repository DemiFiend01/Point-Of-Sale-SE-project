from POS_app.business.Items import Order
from POS_app.business.Actors.User import Role
#will for sure need to add Order and Menu and Waiter later on
from POS_app.views import role_required

#maybe make some functions static? if not all
class OrderCreationPanel:
    def __init__(self):
        print("Need to implement Gui")

    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_view_ready_orders(request):
        print("return a list")

    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_mark_delivered(request):
        print("")
        
    # those methods will probably be callbacks from buttons/panels that need to be initiated
    @role_required(allowed_roles=[Role.WAITER.name])
    def _start_order(self):  # protected method #waiter_create_order
        #call add product, set takeaway etc 
        print("Starting an order")
        #a special page with multiple buttons and lists 

    def _add_product(self):  # protected method
        #when adding this is VERY IMPORTANT
        #you add by a serving sequence.
        #as in, you create a new serving sequence that is basically a group of at least one product
        #think of it like spaghetti and burger being DINNER, ice cream being DESSERT and then need to have a specific order
        #so this method 
        print("Adding a product to the order")

    def _set_takeaway(self):  # protected method
        print("Setting that this order is a takeaway")

    def _confirm(self):  # protected method
        print("Confirming something???")

    def _set_serving_sequence(self):  # protected method
        print("setting a serving sequence for an order")
