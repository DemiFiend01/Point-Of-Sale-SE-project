from POS_app.business.Services import KitchenService

class KitchenProcessingPanel:
    def __init__(self):
        self._kitchen_service = KitchenService.KitchenService()
        print("This class will be visible to cooks and it will manage the GUI via views and urls, and it will call appropriate methods in the service for the DB managment")

    def _list_pending(self):  # protected method
        print("Based on database data list pending orders")

    def _mark_item_ready(self):  # protected method
        print("marking an item in a selected order ready")

    def _mark_order_in_progress(self):  # protected method
        print("Marking an order in progress, taking it on")

MyKitchenProcessingPanel = KitchenProcessingPanel()