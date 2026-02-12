from django.urls import include, path
from django.contrib import admin
from . import views
from .business.Panels.KitchenProcessingPanel import MyKitchenProcessingPanel
from .business.Panels.MenuManagmentPanel import MyMenuManagementPanel
from .business.Panels.OrderCreationPanel import MyOrderCreationPanel
from .business.Panels.OrderHistoryPanel import MyOrderHistoryPanel
from .business.Panels.PaymentPanel import MyPaymentPanel
from .business.Panels.EmployeeManagementPanel import MyEmployeeManagementPanel

urlpatterns = [
    # the data will be sent here from the html template?
    path('', views.login_view, name='login_site'),
    # apparently set automatically, so that is the warning
    path("logout/", views.logout_view, name="logout_site"),
    path('admin/', admin.site.urls),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/manage_menu/', MyMenuManagementPanel.manager_manage_menu,
         name='manager_manage_menu'),
    path('manager/generate_report/', views.manager_generate_report,
         name='manager_generate_report'),
    path('manager/archived_orders/', MyOrderCreationPanel.manager_view_archived_orders,
         name='manager_view_archived_orders'),
    path('manager/manage_employees/',
         MyEmployeeManagementPanel.manager_manage_emp, name='manager_manage_emp'),
    path('waiter/', views.waiter_dashboard, name='waiter_dashboard'),
    path('waiter/create_order/', MyOrderCreationPanel.waiter_create_order,
         name='waiter_create_order'),
    path('waiter/mark_delivered/', MyOrderCreationPanel.waiter_mark_delivered,
         name='waiter_mark_delivered'),
    path('waiter/ready_orders/', MyOrderCreationPanel.waiter_view_ready_orders,
         name='waiter_view_ready_orders'),
    path('waiter/cancel_order/', MyOrderCreationPanel.waiter_cancel_order,
         name='waiter_cancel_order'),
    path('waiter/process_payment/',
         MyPaymentPanel.waiter_payment, name='waiter_payment'),
    path('cook/', views.cook_dashboard, name='cook_dashboard'),
    path('cook/view_pending_orders/',
         views.cook_pending_orders, name='cook_pending_orders'),
    path('cook/mark_order_ready', views.cook_mark_order_ready,
         name='cook_mark_order_ready'),
    path('cook/mark_item_ready', views.cook_mark_item_ready,
         name='cook_mark_item_ready')
]
