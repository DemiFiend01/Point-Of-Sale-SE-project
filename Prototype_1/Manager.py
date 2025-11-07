import Employee

#inheritance
class Manager(Employee):
    def __init__(self):
        print("Manager")

    def manageMenu(self):
        print("managing the menu")

    def generateReport(self):
        print("Generating")

    def viewArchivedOrders(self):
        print("Viewing")

    
