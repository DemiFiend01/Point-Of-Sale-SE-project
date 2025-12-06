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


def order_create(request):
    template = loader.get_template("create_order.html")
    return HttpResponse(template.render())


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

        request.session["user_login"] = emp._login
        request.session["user_role"] = emp._role

        if emp._role == Role.MANAGER.name:
            business_emp = Manager(emp._name, emp._login,
                                   emp._password, Role.MANAGER)
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
    template = loader.get_template("manager_dashboard.html")
    return HttpResponse(template.render())


@role_required(allowed_roles=[Role.WAITER.name])
def waiter_dashboard(request):
    template = loader.get_template("waiter_dashboard.html")
    return HttpResponse(template.render())


@role_required(allowed_roles=[Role.COOK.name])
def cook_dashboard(request):
    template = loader.get_template("cook_dashboard.html")
    return HttpResponse(template.render())


def order_detail(request, order_id):
    return HttpResponse("Hello world! ", order_id)


def POS_app(request):
    return HttpResponse("Hello world!")
