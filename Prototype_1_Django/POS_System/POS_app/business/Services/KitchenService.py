import Items.Order as Order


class KitchenService:
    def __init__(self):
        print("Business logic for kitchen operations and estimated times of arrivals")

    def _list_pending(self) -> list[Order.Order]:  # protected method
        print("listing all pending orders based on their status in a database")

    def _mark_item_ready(self, order_id: int, item_id: str):  # protected method
        print("Marking an item in an order as ready")

    def _update_estimates(self, order_id: int):  # protected method
        print("updating the ETA for an order")
