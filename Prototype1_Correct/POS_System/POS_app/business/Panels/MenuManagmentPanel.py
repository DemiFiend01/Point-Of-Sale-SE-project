from POS_app.business.Services import MenuService
from POS_app.views import role_required
from POS_app.business.Actors.User import Role
from django.shortcuts import render
from django.shortcuts import redirect
from django.core.exceptions import ValidationError

class MenuManagementPanel:  # for manager to use
    def __init__(self ):
        self._menu_service = MenuService.MenuService()
        print("This class will handle the GUI (views and urls) and call appropriate service methods for the DB managment.")

    @role_required(allowed_roles=[Role.MANAGER.name])
    def manager_manage_menu(self,request): #can use self here because an instance has been created
        all_menu_items = self._list_menu(None)
        errors = None
        success = None
        if (request.method == "POST"):
            action = request.POST.get("action")
            match action:
                case "add":
                    values = (request.POST.get("name"), 
                              request.POST.get("price"), 
                              request.POST.get("prep_time_min"), 
                              True if request.POST.get("active") in ("on", "true", "1") else False, 
                              request.POST.get("course"), 
                              request.POST.get("tax"))
                    result = self._add_product(values)
                    if "error" in result:
                        errors = result["error"]
                    elif "success" in result:
                        success = result["success"]
                case "edit":
                    selected = request.POST.get("selected_item_id")
                    print(selected)
                    result = self._find_product(selected)
                    if "error" in result:
                        errors = result["error"]
                    else:
                        context = {
                                "m_id": selected,
                                "name": result["name"], 
                                   "price": result["price"], 
                                   "prep_time_min": result["prep_time_min"],
                                    "active": result["active"],
                                    "course": result["course"],
                                    "tax": result["tax"]}
                        return self._edit_product(request,context,selected)
                        #right now on go_back it goes back to manager_dashboard, just implement a link lol or something
                case "delete":
                    return redirect("manager_dashboard")
                case "go_back":
                    return redirect('manager_dashboard')

        context = {"menu_items": all_menu_items}
        if request.method == "POST":
            context["error"] = errors
            context["success"] = success

        return render(request,"manager/Manager_manage_menu.html", context)

    def _add_product(self, item_id):  # protected method
        return self._menu_service._add(item_id) #actually tries to add it to the database and returns the message whether succeeded
        
    def _find_product(self, item_id):
        return self._menu_service._find_item(item_id)
    
    def _edit_product(self, request, menu_item, menu_id):
        if (request.method == "POST" and request.POST.get("action") == "edit"):
            action = request.POST.get("action")
            match action:
                case "edit":
                    values = {
                                "name": request.POST.get("name") or menu_item["name"],
                                "price": float(request.POST.get("price")) if request.POST.get("price") else menu_item["price"],
                                "prep_time_min": int(request.POST.get("prep_time_min")) if request.POST.get("prep_time_min") else menu_item["prep_time_min"],
                                "active": True if request.POST.get("active") in ("on","true","1") else menu_item["active"],
                                "course": request.POST.get("course") or menu_item["course"],
                                "tax": float(request.POST.get("tax")) if request.POST.get("tax") else menu_item["tax"]
                            }
                    print("id: ",menu_id," values",values)
                    result = self._menu_service._update(menu_id, values)
                    if "error" in result:
                        menu_item["error"] = result["error"]
                    elif "success" in result:
                        menu_item["success"] = result["success"]
                    return render(request, "manager/Manager_manage_menu_edit.html", menu_item)

                case "go_back":
                    return redirect('manager_manage_menu')    
        return render(request, "manager/Manager_manage_menu_edit.html", menu_item)
    
    def _remove_product(self):  # protected method
        print("removing product")

    def _list_menu(self, filter: str | None):  # protected method
        return self._menu_service._list(filter) #no returning of exceptions, need to add that

MyMenuManagementPanel = MenuManagementPanel()