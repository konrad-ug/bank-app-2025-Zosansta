class Account:
    express_outgoing_transfer_fee = 0

    def incoming_transwer(self, value):
        if value > 0:
            self.balance += value

    def outgoing_transwer(self, value):
        if 0 < value <= self.balance:
            self.balance -= value

    def outgoing_express_transwer(self, value):
        if value <= 0:
            return "Błąd, kwota nie może być mniejsza niż 0 zł"
        total = value + self.express_outgoing_transfer_fee
        if total-self.express_outgoing_transfer_fee <= self.balance:
            self.balance -= total
            return True
        return False
