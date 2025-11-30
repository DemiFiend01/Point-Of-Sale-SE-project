from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def order_create(request):
    return HttpResponse("Hello create")


def order_detail(request, order_id):
    return HttpResponse("Hello world! ", order_id)


def POS_app(request):
    return HttpResponse("Hello world!")
