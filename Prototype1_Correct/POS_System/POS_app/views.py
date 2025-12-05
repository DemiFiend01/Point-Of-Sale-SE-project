from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import loader
from . import models
from .business.Actors.Manager import Manager
from .business.Actors.Cook import Cook
from .business.Actors.Waiter import Waiter
from .business.Actors.User import Role


def order_create(request):
    template = loader.get_template("create_order.html")
    return HttpResponse(template.render())

def login_view(request):
    if(request.method == "POST"):
        username = request.POST.get("login")
        password = request.POST.get("password")

        try:
            emp = models.Employees.objects.get(_login = username, _password = password)
        except models.Employees.DoesNotExist:
            return render(request, "login.html", {"error": "This user does not exist"})
        
        if emp.role == Role.MANAGER:
            business_emp = Manager(emp._name, emp._login, emp._password, Role.MANAGER)
        elif emp.role == Role.COOK:
            business_emp = Cook(emp._name, emp._login, emp._password, Role.COOK)
        elif emp.role == Role.WAITER:
            business_emp = Waiter(emp._name, emp._login, emp._password, Role.WAITER)
        else:
            print("Wrong role")

        request.session["user_login"] =emp._login
        request.session["user_role"] = emp._role

        return redirect("orders/new") #just for now hehehe


    return render(request, "login.html")

def order_detail(request, order_id):
    return HttpResponse("Hello world! ", order_id)


def POS_app(request):
    return HttpResponse("Hello world!")
