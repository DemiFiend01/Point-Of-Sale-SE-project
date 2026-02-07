from django.db import transaction
from django.utils import timezone
from POS_app.models import Orders, OrderItems, ServingRules, MenuItems, Employees
from POS_app.business.Items import Utils


class OrderService:
    def create(
        self,
        waiter_login: str,
        is_takeaway: bool,
        table_no: int | None,
        notes: str | None,
        items: list[dict],
    ):
        if not items:
            return {"error": "Please select at least one menu item."}

        try:
            waiter = Employees.objects.get(_login=waiter_login)
        except Employees.DoesNotExist:
            return {"error": "Waiter account not found."}

        display_id = Utils.IDGenerate.order_id_generator()

        try:
            with transaction.atomic():
                order = Orders(
                    waiter=waiter,
                    displayed_id=display_id,
                    status=Utils.OrderStatus.AWAITING_PREPARATION.name,
                    is_takeaway=is_takeaway,
                    table_no=table_no or 1,
                    notes=notes or "",
                )
                order.full_clean()
                order.save()

                for position, item in enumerate(items, start=1):
                    menu_item = MenuItems.objects.get(
                        m_id=item["menu_item_id"])
                    order_item = OrderItems(
                        m_id=menu_item,
                        quantity=item["quantity"],
                        status=Utils.OrderStatus.AWAITING_PREPARATION.name,
                    )
                    order_item.full_clean()
                    order_item.save()

                    rule = ServingRules(
                        o_id=order,
                        oi_id=order_item,
                        position=position,
                        course=menu_item.course or "",
                    )
                    rule.full_clean()
                    rule.save()
        except Exception as exc:
            return {"error": str(exc)}

        return {"success": "Order created successfully.", "order": order}

    def list_ready(self):
        return Orders.objects.filter(
            status=Utils.OrderStatus.READY.name,
            delivered_at__isnull=True,
        ).order_by("created_at")

    def list_delivered(self):
        return Orders.objects.filter(
            status=Utils.OrderStatus.DELIVERED.name,
            delivered_at__isnull=False,
        ).order_by("created_at")

    def list_open(self):
        return Orders.objects.filter(
            status__in=[
                Utils.OrderStatus.NEW.name,
                Utils.OrderStatus.AWAITING_PREPARATION.name,
                Utils.OrderStatus.IN_PREPARATION.name,
                Utils.OrderStatus.READY.name,
            ]
        ).order_by("created_at")

    def mark_delivered(self, order_id: int):
        try:
            order = Orders.objects.get(o_id=order_id)
        except Orders.DoesNotExist:
            return {"error": "Order not found."}

        order.status = Utils.OrderStatus.DELIVERED.name
        order.delivered_at = timezone.now()
        order.save()
        return {"success": "Order marked as delivered."}

    def cancel(self, order_id: int):
        try:
            order = Orders.objects.get(o_id=order_id)
        except Orders.DoesNotExist:
            return {"error": "Order not found."}

        if order.status in [Utils.OrderStatus.PAID.name, Utils.OrderStatus.ARCHIVED.name]:
            return {"error": "Finished orders cannot be canceled."}

        order.status = Utils.OrderStatus.CANCELED.name
        order.save()
        return {"success": "Order canceled."}
