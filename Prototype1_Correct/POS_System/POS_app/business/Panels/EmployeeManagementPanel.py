from POS_app.models import Employees
from POS_app.views import role_required
from POS_app.business.Actors.User import Role
from django.shortcuts import render, redirect
import re


def validate_password(password):

    if len(password) < 8:
        return "Weak Password: Must be at least 8 characters long."
    if not re.search(r"\d", password):
        return "Weak Password: Must contain at least one number."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Weak Password: Must contain at least one special symbol."
    return None  # Returns None if the password is perfect


class EmployeeManagementPanel:
    def __init__(self):
        print("Employee Management Panel Initialized")

    @role_required(allowed_roles=[Role.MANAGER.name])
    def manager_manage_emp(self, request):
        errors = None
        success = None

        if request.method == "POST":
            action = request.POST.get("action")

            match action:

                case "add":
                    try:

                        name = request.POST.get("name")
                        login = request.POST.get("login")
                        raw_password = request.POST.get("password")
                        role = request.POST.get("role")

                        if not name or not login or not raw_password:
                            errors = "All fields are required."

                        elif Employees.objects.filter(_login=login).exists():
                            errors = f"Error: The login '{login}' is already taken."

                        elif (pwd_msg := validate_password(raw_password)) is not None:
                            errors = pwd_msg

                        else:
                            new_emp = Employees()
                            new_emp._name = name
                            new_emp._login = login
                            new_emp._role = role
                            new_emp.set_password(raw_password)

                            new_emp.save()
                            success = f"Employee {name} hired successfully."

                    except Exception as e:
                        errors = f"Error adding employee: {str(e)}"

                case "delete":
                    selected_id = request.POST.get("selected_emp_id")
                    current_user_login = request.session.get("user_login")

                    if selected_id:
                        try:
                            emp = Employees.objects.get(e_id=selected_id)

                            if emp.login == current_user_login:
                                errors = "OPERATION DENIED: You cannot delete your own account."

                            elif emp.role == "MANAGER":
                                errors = "ACCESS DENIED: Managers cannot be deleted via this panel."
                            else:
                                emp_name = emp.name
                                emp.delete()
                                success = f"Employee '{emp_name}' has been deleted."

                        except Employees.DoesNotExist:
                            errors = "Employee not found."
                    else:
                        errors = "Please select an employee to delete."

                case "go_back":
                    return redirect('manager_dashboard')

        all_employees = Employees.objects.all().order_by('e_id')

        context = {
            "employees": all_employees,
            "error": errors,
            "success": success,
            "roles": [r.name for r in Role]
        }

        return render(request, "manager/Manager_manage_emp.html", context)

MyEmployeeManagementPanel = EmployeeManagementPanel()