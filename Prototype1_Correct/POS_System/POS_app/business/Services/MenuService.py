from POS_app.business.Items import MenuItem
from POS_app.models import MenuItems
from django.core.exceptions import ValidationError

class MenuService:
    def __init__(self):
        print("Business logic for menu items")

    def _add(self, values): #-> MenuItem.MenuItem:  # protected method
        name, price, prep_time_min, active, course, tax = values
        new_item = MenuItems(
            name=name,
            price=price,
            prep_time_min=prep_time_min,
            #currency is PLN by default,
            active=True if active in ("on", "true", "1") else False,
            course=course,
            tax=tax
        )
        try:
            new_item.full_clean()
            new_item.save()
            return {"success": "Menu item added successfully"}
        except ValidationError as e:
            return {"error": e.message_dict}
        except Exception as e:
            return {"error": str(e)}
        
    def _remove(self, menu_id):  # protected method
        try:
            item_to_delete = MenuItems.objects.get(m_id=menu_id)
            item_to_delete.delete()
            return {"success": "Successfully deleted"}
        except Exception as e:
            return {"error": str(e)}

    def _find_item(self, item_id):  # protected method changed the name from _find to _find_item for clarity
        try:
            menu_item = MenuItems.objects.get(m_id=item_id)
            return {
                "name": menu_item.name,
                "price": menu_item.price,
                "prep_time_min": menu_item.prep_time_min,
                "active": menu_item.active,
                "course": menu_item.course,
                "tax": menu_item.tax
            }
        except Exception as e:
            return {"error": str(e)}


    def _update(self, menu_id, menu_item):  # protected method
        try:
            changed_item = MenuItems.objects.get(m_id=menu_id)
            changed_item.name = menu_item["name"]
            changed_item.price = menu_item["price"]
            changed_item.prep_time_min = menu_item["prep_time_min"]
            changed_item.active = menu_item["active"]
            changed_item.course = menu_item["course"]
            changed_item.tax = menu_item["tax"]
            changed_item.full_clean()
            changed_item.save()
            return {"success": "Edited the item successfully"}
        except Exception as e:
            return {"error": str(e)}

    def _list(self, _name: str | None): #-> list[MenuItem.MenuItem]:  # protected method
        if _name is None:
            menu_items = MenuItems.objects.all().order_by("name")
        else:
            menu_items = MenuItems.objects.all().filter(name = _name).order_by("-name")
        return menu_items