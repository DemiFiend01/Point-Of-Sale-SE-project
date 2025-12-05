#man, will need to rework it all
# from POS_app.models import Order, OrderItem, MenuItem
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from POS_app.models import Order, MenuItem, OrderItem

# User = get_user_model()


class OrderService:

    def create(self, waiter: str, is_takeaway: bool, table_no: str | None, notes: str | None): #-> Order:
        print("create")
        # """
        # Creates a new order.
        # """
        # order = Order.objects.create(
        #     waiter=waiter,
        #     is_takeaway=is_takeaway,
        #     table_no=table_no,
        #     notes=notes or "",
        # )
        # return order

    def add_item(self, order_id: int, menu_item_id: int, quantity: int): #-> #OrderItem:
        print("add")
        # """
        # Adds an item to the order.
        # """
        # order = Order.objects.get(pk=order_id)
        # menu_item = MenuItem.objects.get(pk=menu_item_id)

        # order_item = OrderItem.objects.create(
        #     order=order,
        #     menu_item=menu_item,
        #     quantity=quantity,
        #     unit_price=menu_item.price,
        #     status='NEW',
        #     course=menu_item.course,
        # )     
        # return order_item

    def remove_item(self, order_id: int, order_item_id: int): #-> bool:
        print("remove")
        # """
        # Removes an OrderItem from an order.
        # """
        # try:
        #     order_item = OrderItem.objects.get(
        #         pk=order_item_id, order_id=order_id)
        # except OrderItem.DoesNotExist:
        #     return False

        # order_item.delete()
        # return True

    # def confirm(self, order_id: int) -> Order:
    #     """
    #     Confirms an order: NEW -> AWAITING_PREPARATION
    #     """
    #     order = Order.objects.get(pk=order_id)
    #     if order.status != 'NEW':
    #         raise ValueError("The order is not new")
    #     order.status = 'AWAITING_PREPARATION'
    #     order.save()
    #     return order

    # def set_takeaway(self, order_id: int, is_takeaway: bool) -> Order:
    #     """
    #     Changes takeaway flag.
    #     """
    #     order = Order.objects.get(pk=order_id)
    #     order.is_takeaway = is_takeaway
    #     order.save()
    #     return order

#     def archive(self, order_id: int) -> Order:
#         """
#         Archives a paid order.
#         """
#         order = Order.objects.get(pk=order_id)
#         if order.status != 'PAID':
#             raise ValueError("The order was not paid for, cannot archive.")
#         order.status = 'ARCHIVED'
#         order.archived_at = timezone.now()
#         order.save()
#         return order


# service = OrderService()


# @login_required
# def order_create(request):
#     """
#     Creates new order for the Waiter
#     """
#     if request.method == 'POST':
#         is_takeaway = request.POST.get('is_takeaway') == 'on'
#         table_no = request.POST.get('table_no') or None
#         notes = request.POST.get('notes') or None

#         order = service.create(
#             waiter=request.user,
#             is_takeaway=is_takeaway,
#             table_no=table_no,
#             notes=notes,
#         )
#         return redirect('order_detail', order_id=order.id)
#     return render(request, 'POS_app/order_create.html', {})


# @login_required
# def order_detail(request, order_id):
#     """
#     Shows order details and allows editing.
#     """
#     order = get_object_or_404(Order, pk=order_id)
#     menu_items = MenuItem.objects.filter(active=True)

#     if request.method == 'POST':
#         # Adding an item
#         menu_item_id = int(request.POST.get('menu_item_id'))
#         quantity = int(request.POST.get('quantity', 1))
#         service.add_item(order_id=order.id,
#                          menu_item_id=menu_item_id, quantity=quantity)
#         return redirect('order_detail', order_id=order.id)

#     return render(request, 'POS_app/order_detail.html', {
#         'order': order,
#         'menu_items': menu_items,
#     })
