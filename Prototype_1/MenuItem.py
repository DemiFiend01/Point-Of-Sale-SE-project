class MenuItem:
    def __init__(self, id, name, price, prep_time_min, course):
        self.id = id  # string
        self.name = name  # string
        self.price = price  # float
        self.prep_time_min = prep_time_min  # int
        self.active = True  # bool
        self.course = course  # string

    def _update_details(self, name, price, prep_time_min, course):  # protected method
        self.name = name
        self.price = price
        self.prep_time_min = prep_time_min
        self.course = course
