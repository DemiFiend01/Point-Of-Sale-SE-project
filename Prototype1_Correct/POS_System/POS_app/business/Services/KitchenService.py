from POS_app.models import Orders, OrderItems
from POS_app.business.Items import Utils
import datetime
from typing import List


class KitchenService:
    def __init__(self):
        print("Business logic for kitchen operations and estimated times of arrivals")
    def _list_pending(self) -> List[Orders]:
        """
        Fetches orders from the database that are waiting for the kitchen.
        Returns a list of Django 'Orders' model objects.
        """
        pending_orders = Orders.objects.filter(
            status__in=[
                Utils.OrderStatus.AWAITING_PREPARATION.name,
                Utils.OrderStatus.IN_PREPARATION.name
            ]
        ).order_by('created_at')

        return list(pending_orders)

    def _mark_item_ready(self, order_id: int, item_id: int) -> bool:
        """
        Marks a specific item (OrderItems) as ready.
        """
        try:
            #Lookup via oi_id
            item = OrderItems.objects.get(oi_id=item_id)
            # Update status
            item.status = Utils.OrderStatus.READY.name
            item.ready_at = datetime.datetime.now()
            item.save()

            print(f"Service: Item {item_id} marked as READY.")
            return True
        except OrderItems.DoesNotExist:
            print(f"Service: Item {item_id} not found.")
            return False

    def _update_estimates(self, order_id: int):
        print("updating the ETA for an order")