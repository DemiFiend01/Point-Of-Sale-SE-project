from django.shortcuts import render
from django.shortcuts import redirect
from POS_app.business.Actors.User import Role
from POS_app.business.Services import OrderService
from POS_app.models import MenuItems, ServingRules
from POS_app.views import role_required



#maybe make some functions static? if not all
class OrderCreationPanel:
    def __init__(self):
        self._order_service = OrderService.OrderService()
        print("This class will have methods that will handle the GUI and call the appropriate methods of the service which will manage the DB")   
        
    #those methods here are not inside the class diagram
    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_create_order(self,request):
        menu_items = MenuItems.objects.filter(active=True).order_by("name")
        errors = None
        success = None

        if request.method == "POST":
            is_takeaway = request.POST.get("is_takeaway") == "on"
            table_no = request.POST.get("table_no")
            notes = request.POST.get("notes")

            items = []
            for item in menu_items:
                raw_qty = request.POST.get(f"qty_{item.m_id}", "").strip()
                if not raw_qty:
                    continue
                try:
                    quantity = int(raw_qty)
                except ValueError:
                    errors = "Please enter numeric quantities."
                    items = []
                    break
                if quantity > 0:
                    items.append({"menu_item_id": item.m_id, "quantity": quantity})

            if not is_takeaway and not table_no:
                errors = "Table number is required for dine-in orders."
            elif errors is None:
                try:
                    table_no_value = int(table_no) if table_no else None
                except ValueError:
                    errors = "Table number must be a number."
                    table_no_value = None

                if errors is None:
                    result = self._order_service.create(
                        waiter_login=request.session.get("user_login"),
                        is_takeaway=is_takeaway,
                        table_no=table_no_value,
                        notes=notes,
                        items=items,
                    )
                    if "error" in result:
                        errors = result["error"]
                    else:
                        success = f"Order #{result['order'].displayed_id} created."

        context = {
            "menu_items": menu_items,
            "error": errors,
            "success": success,
        }
        return render(request, "waiter/Waiter_create_order.html", context)

    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_mark_delivered(self,request):
        errors = None
        success = None
        if request.method == "POST":
            order_id = request.POST.get("order_id")
            if order_id:
                result = self._order_service.mark_delivered(order_id)
                if "error" in result:
                    errors = result["error"]
                else:
                    success = result["success"]

        orders = self._order_service.list_ready()
        order_items = self._build_order_items_map(orders)
        return render(
            request,
            "waiter/Waiter_mark_delivered.html",
            {"orders": orders, "order_items": order_items, "error": errors, "success": success},
        )

    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_view_ready_orders(self,request):
        orders = self._order_service.list_ready()
        order_items = self._build_order_items_map(orders)
        return render(
            request,
            "waiter/Waiter_view_ready.html",
            {"orders": orders, "order_items": order_items},
        )
    
    @role_required(allowed_roles=[Role.WAITER.name])
    def waiter_cancel_order(self,request):
        errors = None
        success = None
        if request.method == "POST":
            order_id = request.POST.get("order_id")
            if order_id:
                result = self._order_service.cancel(order_id)
                if "error" in result:
                    errors = result["error"]
                else:
                    success = result["success"]

        orders = self._order_service.list_open()
        order_items = self._build_order_items_map(orders)
        return render(
            request,
            "waiter/Waiter_cancel_order.html",
            {"orders": orders, "order_items": order_items, "error": errors, "success": success},
        )
    
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

    def _build_order_items_map(self, orders):
        order_ids = [order.o_id for order in orders]
        if not order_ids:
            return {}

        rules = (
            ServingRules.objects.filter(o_id__in=order_ids)
            .select_related("oi_id__m_id", "o_id")
            .order_by("position")
        )
        order_items = {}
        for rule in rules:
            order_items.setdefault(rule.o_id.o_id, []).append(
                {
                    "name": rule.oi_id.m_id.name,
                    "quantity": rule.oi_id.quantity,
                    "course": rule.course,
                }
            )
        return order_items

MyOrderCreationPanel = OrderCreationPanel()
