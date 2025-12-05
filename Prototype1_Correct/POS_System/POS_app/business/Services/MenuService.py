from POS_app.business.Items import MenuItem


class MenuService:
    def __init__(self):
        print("Business logic for menu items")

    def _add(self, item: MenuItem.MenuItem) -> MenuItem.MenuItem:  # protected method
        print("Add to the database the menuitem probably")

    def _remove(self, item_id: str):  # protected method
        print("search for the id in the database and remove an item from the menu")

    def _update(self, item: MenuItem.MenuItem):  # protected method
        print("search for the id in the database and switch the entries?")

    def _list(self) -> list[MenuItem.MenuItem]:  # protected method
        print("Print all menu items")

    def _find(self) -> list[MenuItem.MenuItem]:  # protected method
        print("To be extended and specified. By providing some criteria, find the fitting menu items")
