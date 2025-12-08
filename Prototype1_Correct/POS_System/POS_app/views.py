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

# special method to wrap the view methods to restrict access for specific roles


def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = request.session.get("user_role")
            if user_role not in allowed_roles:
                return redirect("login_site")  # redirect if unauthorized
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

#to be rewritten later as a special method for waiters, change the name, add @loginrequited etc
#completely different rules etc
def order_create(request):
    return render(request, "create_order.html")


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
                                   emp._password, Role.MANAGER) #unsure on how to handle the business class later on, to be implemented
            #probably it will be contained either as a session variable or just backend method param
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
    return render(request, "Manager_dashboard.html")

#all of those methods will call the appropriate business panels or they can be rewritten to be inside of those panels in some way!!!!
@role_required(allowed_roles=[Role.MANAGER.name])
def manager_manage_menu(request): #to be implemented, add returning
    return render(request,"Manager_manage_menu.html")

@role_required(allowed_roles=[Role.MANAGER.name])
def manager_generate_report(request): #to be implemented, add returning
    return render(request,"Manager_generate_report.html")

@role_required(allowed_roles=[Role.MANAGER.name])
def manager_archived_orders(request): #to be implemented, add returning
    return render(request,"Manager_archived_orders.html")

@role_required(allowed_roles=[Role.MANAGER.name])
def manager_manage_emp(request): #to be implemented, add returning
    return render(request,"Manager_manage_emp.html")

@role_required(allowed_roles=[Role.WAITER.name])
def waiter_dashboard(request):
    if (request.method == "POST"):
        action = request.POST.get("action")
        match action:
            case "Log out":
                request.session.flush()
                return redirect("login_site")
            case "Manage orders":
                return redirect("waiter_manage_orders")
    return render(request,"Waiter_dashboard.html")

#this method will have many more redirections and calls to the appropriate panels further down the line
@role_required(allowed_roles=[Role.WAITER.name])
def waiter_manage_orders(request):
    return render(request,"Waiter_manage_orders.html")

@role_required(allowed_roles=[Role.COOK.name])
def cook_dashboard(request):
    if (request.method == "POST"):
        action = request.POST.get("action")
        match action:
            case "Log out":
                request.session.flush() #log out basically, will not be able to access any sites basically 
                return redirect("login_site")
            case "View pending orders":
                return redirect("cook_pending_orders")
            case "Mark order as ready":
                return redirect("cook_mark_order_ready")
            case "Mark item as ready":
                return redirect("cook_mark_item_ready")
    return render(request,"Cook_dashboard.html")

@role_required(allowed_roles=[Role.COOK.name])
def cook_pending_orders(request): #list all pending orders
    return render(request, "Cook_view_pending_orders.html")

@role_required(allowed_roles=[Role.COOK.name])
def cook_mark_order_ready(request): #to be frank, this should not be a seperate view. this can be in one big panel like mark items and orders as ready where orders would be auto ready when all items are ready
    return render(request, "Cook_mark_order_as_ready.html")

@role_required(allowed_roles=[Role.COOK.name])
def cook_mark_item_ready(request): 
    return render(request, "Cook_mark_item_as_ready.html")


def order_detail(request, order_id):
    return HttpResponse("Hello world! ", order_id)


def POS_app(request):
    return HttpResponse("Hello world!")
