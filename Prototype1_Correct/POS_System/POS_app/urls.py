from django.urls import include, path
from django.contrib import admin
from . import views

urlpatterns = [
    path('orders/new/', views.order_create, name='order_create'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    # apparently set automatically, so that is the warning
    path('admin/', admin.site.urls),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('waiter/', views.waiter_dashboard, name='waiter_dashboard'),
    path('cook/', views.cook_dashboard, name='cook_dashboard'),
    path('', views.login_view, name='login_site')
]
