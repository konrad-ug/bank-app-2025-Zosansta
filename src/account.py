class Account:
    def _init_(self):
        self.balance = 0.0

    def incoming_transwer(self, value):
        if value > 0:
            self.balance += value

    def outgoing_transwer(self, value):
        if 0 < value <= self.balance:
            self.balance -= value

    def outgoing_express_transwer(self, value):
        if value <= 0:
            return "Błąd, kwota nie może być mniejsza niż 0 zł"

        if self.account_type == "personal":
            fee = 1.0
        elif self.account_type == "company":
            fee = 5.0
        else:
            fee = 0.0

        self.balance -= value + fee
