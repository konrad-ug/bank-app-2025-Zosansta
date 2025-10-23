class Account:
    def _init_(self):
        self.balance = 0.0

    def incoming_transwer(self, value):
        if value > 0:
            self.balance += value

    def outgoing_transwer(self, value):
        if 0 < value <= self.balance:
            self.balance -= value