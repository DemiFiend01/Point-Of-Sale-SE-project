class MenuItem:
    def __init__(self, id: str, name: str, price: float, prep_time_min: int, course: str):
        self._id = id  # string ??
        self._name = name  # string
        self._price = price  # float
        self._prep_time_min = prep_time_min  # int
        self._active = True  # bool
        self._course = course  # string

    def _update_details(self, name: str, price: float, prep_time_min: int, course: str):  # protected method
        self._name = name
        self._price = price
        self._prep_time_min = prep_time_min
        self._course = course
