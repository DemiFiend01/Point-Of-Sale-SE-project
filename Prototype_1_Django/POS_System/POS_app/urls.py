from django.urls import path
from . import views

urlpatterns = [
    path('POS_app/', views.POS_app, name='POS_app'),
]
