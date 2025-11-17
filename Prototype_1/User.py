# Superclass for Waiter, Cook, Manager.
# Defines shared properties (authentication, identification).

class User:
    def __init__(self, name: str, login: str, password: str, role: str):
        self._name = name
        self._login = login
        self._password = password
        self._role = role
