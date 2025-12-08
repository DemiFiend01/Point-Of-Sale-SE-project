from django.contrib import admin
from .models import Employees, OrderItems, Orders, ServingRules, Payments, MenuItems

# now the admin can add new employees (not business models, just in a database)
admin.site.register(Employees)
# in code, when you log in as one of the employees, that emp is converted into a business model related to their role
# and then we operate on the business model, making changes through it
admin.site.register(Orders)
admin.site.register(MenuItems)
admin.site.register(OrderItems)
admin.site.register(ServingRules)
admin.site.register(Payments)
