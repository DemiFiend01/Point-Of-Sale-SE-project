from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login_site')
]
