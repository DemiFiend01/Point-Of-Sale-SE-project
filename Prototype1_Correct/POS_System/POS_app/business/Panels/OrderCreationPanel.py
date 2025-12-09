from django.shortcuts import render
from django.shortcuts import redirect
from POS_app.business.Items import Order
from POS_app.business.Actors.User import Role
from POS_app.business.Items.Utils import IDGenerate
#will for sure need to add Order and Menu and Waiter later on
from POS_app.views import role_required



#maybe make some functions static? if not all
class OrderCreationPanel:
    def __init__(self):
        print("Need to implement Gui")   
        
    #those methods here are not inside the class diagram, but adding them as static methods helps to organise this class
    @staticmethod
    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_create_order(request):
        order_number = IDGenerate.order_id_generator()
        #there is no need for a redirect to a orders/id other than pure visuals
        #better to stay in this method to avoid further complications
        return render(request, "waiter/Waiter_create_order.html")

    @staticmethod
    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_mark_delivered(request):
        print("There will be a list of all orders that were readied by the cooks.")
        return render(request, "waiter/Waiter_mark_delivered.html")

    @staticmethod
    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_view_ready_orders(request):
        return render(request, "waiter/Waiter_view_ready.html")
    
    @staticmethod
    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_cancel_order(request):
        #list of all unfinished orders, can select one to cancel
        return render(request, "waiter/Waiter_cancel_order.html")
    # those methods will probably be callbacks from buttons/panels that need to be initiated
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
