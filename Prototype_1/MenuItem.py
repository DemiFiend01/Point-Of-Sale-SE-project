class MenuItem:
    def __init__(self, id, name, price, prep_time_min, course):
        self.id = id
        self.name = name
        self.price = price
        self.prep_time_min = prep_time_min
        self.active = True
        self.course = course

    def update_details(self,name, price, prep_time_min, course):
        self.name = name
        self.price = price
        self.prep_time_min = prep_time_min
        self.course = course

    def delete_menu_item(self):
        self.active = False
