from POS_app.business.Actors import User
from POS_app.business.Items import Utils
import datetime

# We use TYPE_CHECKING so we can use "Order" in type hints without circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from POS_app.business.Items import Order


class Cook(User.User):
    def __init__(self, name: str, login: str, password: str, role: User.Role):
        print("I have been born as a Cook")
        super().__init__(name, login, password, role)

    def _list_pending_order(self) -> list["Order.Order"]:
        """
        Connects to KitchenService to retrieve orders from the 'database'.
        """
        from POS_app.business.Services.KitchenService import KitchenService
        ks = KitchenService()
        # The service is responsible for finding where they are stored (DB/List)
        print("Cook: Requesting pending orders from KitchenService...")
        return ks._list_pending()

    def _mark_item_ready(self, order_id: int, item_id: str):
        """
        Delegates the logic of finding and updating the item to KitchenService.
        """
        from POS_app.business.Services.KitchenService import KitchenService
        print(f"Cook: Marking item {item_id} in order {order_id} as ready.")
        ks = KitchenService()
        # ensure we pass an int from view, or may crash
        ks._mark_item_ready(order_id, item_id)

    def _update_estimated_time(self, order_id: int, time: int):
        """
        Updates the estimate via the service.
        """
        from POS_app.business.Services.KitchenService import KitchenService

        print(f"Cook: Updating estimate for order {order_id} to {time} mins.") #not finished, placeholder
        ks = KitchenService()
        ks._update_estimates(order_id)

    def _mark_order_ready(self, order):
        """
        Updates the specific order object status to READY.
        Compatible with both Django Models (.status) and Business Objects (._status).
        """
        #Check for which status
        if hasattr(order, "status"):
            current_status = order.status
        else:
            current_status = order._status

        # Check
        if current_status == Utils.OrderStatus.IN_PREPARATION.name or \
                current_status == Utils.OrderStatus.AWAITING_PREPARATION.name or \
                current_status == Utils.OrderStatus.IN_PREPARATION:

            #Update status
            if hasattr(order, "status"):
                order.status = Utils.OrderStatus.READY.name
                order.ready_at = datetime.datetime.now()
            if hasattr(order, "_status"):
                order._status = Utils.OrderStatus.READY
                order._ready_at = datetime.datetime.now()
            print(f"Cook: Order is marked READY!")
        else:
            print(f"Cook: Error - Order must be in preparation. Current status: {current_status}")

    #not ready
    # def _view_order_details(self, order: "Order.Order"):
    #     """
    #     Returns the items inside the order.
    #     """
    #     print(f"Cook: Viewing details for order {order.displayed_id}")
    #     return order._order_items