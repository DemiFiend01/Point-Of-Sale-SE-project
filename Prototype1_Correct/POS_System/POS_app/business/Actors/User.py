# Superclass for Waiter, Cook, Manager.
# Defines shared properties (authentication, identification).
from enum import Enum

class Role(Enum):
    MANAGER = 1
    WAITER = 2
    COOK = 3

class User:
    def __init__(self, name: str, login: str, password: str, role: Role):
        self._name = name
        self._login = login
        self._password = password
        self._role = role
