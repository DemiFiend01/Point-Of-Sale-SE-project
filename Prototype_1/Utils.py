class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def change_mount(self, amount): #instead of add, you never know lol
        self.amount += amount