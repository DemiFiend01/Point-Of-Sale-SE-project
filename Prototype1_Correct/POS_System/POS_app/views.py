from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import loader
from django.contrib.auth.hashers import make_password
from . import models
from .business.Actors.Manager import Manager
from .business.Actors.Cook import Cook
from .business.Actors.Waiter import Waiter
from .business.Actors.User import Role
from functools import wraps
from .models import Orders


# special method to wrap the view methods to restrict access for specific roles


# def role_required(allowed_roles=[]):
#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(request, *args, **kwargs):
#             request = args[0] if hasattr(args[0], "session") else args[1]

#             if request.session.get("user_role") not in allowed_roles:
#                 return redirect("login_site")  # redirect if unauthorized
#             return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator

# def role_required(allowed_roles=None):
#     if allowed_roles is None:
#         allowed_roles = []

#     def decorator(view_func):
#         @wraps(view_func)
#         def wrapper(*args, **kwargs):
#             # Case 1: function-based view → (request)
#             if hasattr(args[0], "session"):
#                 request = args[0]
#                 return view_func(*args, **kwargs)
#             # Case 2: instance method → (self, request)
#             elif len(args) > 1 and hasattr(args[1], "session"):
#                 request = args[1]
#                 self = args[0]

#                 if request.session.get("user_role") not in allowed_roles:
#                     return redirect("login_site")

#                 return view_func(self, request, *args[2:], **kwargs)
#             return redirect("login_site")
#         return wrapper
#     return decorator

def role_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            # Determine request object
            request = None
            if len(args) == 1 and hasattr(args[0], "session"):  # function-based view
                request = args[0]
            elif len(args) >= 2 and hasattr(args[1], "session"):  # instance method
                request = args[1]

            if request is None or request.session.get("user_role") not in allowed_roles:
                return redirect("login_site")

            # Call original function, propagate whatever it returns (render, redirect, etc.)
            return view_func(*args, **kwargs)

        return wrapper

    return decorator


def login_view(request):
    if (request.method == "POST"):
        username = request.POST.get("login")
        password = request.POST.get("password")

        try:
            emp = models.Employees.objects.get(_login=username)
        except models.Employees.DoesNotExist:
            return render(request, "login.html", {"error": "This user does not exist"})

        if not emp.check_password(password):
            return render(request, "login.html", {"error": "Wrong password"})

        request.session["user_name"] = emp._name
        print(emp._name)
        request.session["user_login"] = emp._login
        request.session["user_role"] = emp._role
        print("SESSION CONTENT:", dict(request.session))

        if emp._role == Role.MANAGER.name:
            business_emp = Manager(emp._name, emp._login,
                                   emp._password,
                                   Role.MANAGER)  # unsure on how to handle the business class later on, to be implemented
            # probably it will be contained either as a session variable or just backend method param
            return redirect("manager_dashboard")
        elif emp._role == Role.WAITER.name:
            business_emp = Waiter(emp._name, emp._login,
                                  emp._password, Role.WAITER)
            return redirect("waiter_dashboard")
        elif emp._role == Role.COOK.name:
            business_emp = Cook(emp._name, emp._login,
                                emp._password, Role.COOK)
            return redirect("cook_dashboard")
        else:
            return render(request, "login.html", {"error": "Wrong role"})

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login_site")


@role_required(allowed_roles=[Role.MANAGER.name])
def manager_dashboard(request):
    if (request.method == "POST"):
        action = request.POST.get("action")
        match action:
            case "Log out":
                request.session.flush()
                return redirect("login_site")
            case "Manage menu":
                return redirect("manager_manage_menu")
            case "Generate report":
                return redirect("manager_generate_report")
            case "View archived orders":
                return redirect("manager_archived_orders")
            case "Manage employees":
                return redirect("manager_manage_emp")
    return render(request, "manager/Manager_dashboard.html")


# all of those methods will call the appropriate business panels or they can be rewritten to be inside of those panels in some way!!!!


@role_required(allowed_roles=[Role.MANAGER.name])
def manager_generate_report(request):  # to be implemented, add returning
    return render(request, "manager/Manager_generate_report.html")


@role_required(allowed_roles=[Role.MANAGER.name])
def manager_archived_orders(request):  # to be implemented, add returning
    return render(request, "manager/Manager_archived_orders.html")


@role_required(allowed_roles=[Role.MANAGER.name])
def manager_manage_emp(request):  # to be implemented, add returning
    return render(request, "manager/Manager_manage_emp.html")


@role_required(allowed_roles=[Role.WAITER.name])
def waiter_dashboard(request):
    if request.method == "POST":
        action = request.POST.get("action")
        match action:
            case "Log out":
                request.session.flush()
                return redirect("login_site")

            case "Create new order":
                return redirect("waiter_create_order")

            case "View ready orders":
                return redirect("waiter_view_ready_orders")

            case "Mark order as delivered":
                return redirect("waiter_mark_delivered")

            case "Process payment":
                return redirect("waiter_payment")

            case "Cancel an order":
                return redirect("waiter_cancel_order")

            # Optional: if any old button still posts this
            case "Manage orders":
                return redirect("waiter_dashboard")

    return render(request, "waiter/Waiter_dashboard.html")


@role_required(allowed_roles=[Role.COOK.name])
def cook_dashboard(request):
    if (request.method == "POST"):
        action = request.POST.get("action")
        match action:
            case "Log out":
                request.session.flush()
                return redirect("login_site")
            case "View pending orders":
                return redirect("cook_pending_orders")
            # Redirects for other actions can point to the main list for now
            case "Mark order as ready":
                return redirect("cook_pending_orders")
            case "Mark item as ready":
                return redirect("cook_pending_orders")
    return render(request, "cook/Cook_dashboard.html")


@role_required(allowed_roles=[Role.COOK.name])
def cook_pending_orders(request):
    # 1. Instantiate the Cook Actor using session data
    cook_actor = Cook(
        request.session.get("user_name"),
        request.session.get("user_login"),
        "",  # Password not needed for this action
        Role.COOK
    )

    # 2. Use the Cook Actor to get orders (calls KitchenService -> Database)
    orders = cook_actor._list_pending_order()

    # 3. Pass the orders to the template
    return render(request, "cook/Cook_view_pending_orders.html", {"orders": orders})


@role_required(allowed_roles=[Role.COOK.name])
def cook_mark_order_ready(request):
    if request.method == "POST":
        # The HTML form must send 'order_id'
        order_pk = request.POST.get("order_id")

        cook_actor = Cook(request.session.get("user_name"), request.session.get("user_login"), "", Role.COOK)

        try:
            # Fetch the specific order from the Database
            order = Orders.objects.get(o_id=order_pk)

            # Use the Cook Actor to perform the logic
            cook_actor._mark_order_ready(order)

            # Save the change to the database
            order.save()

        except Orders.DoesNotExist:
            print(f"Order {order_pk} not found!")

    # Redirect back to the list so the order disappears/updates
    return redirect("cook_pending_orders")


@role_required(allowed_roles=[Role.COOK.name])
def cook_mark_item_ready(request):
    if request.method == "POST":
        order_pk = request.POST.get("order_id")
        item_pk = request.POST.get("item_id")

        cook_actor = Cook(request.session.get("user_name"), request.session.get("user_login"), "", Role.COOK)

        # Cook Actor -> KitchenService -> DB Update
        cook_actor._mark_item_ready(order_pk, item_pk)

    return redirect("cook_pending_orders")