class Account:
    express_outgoing_transfer_fee = 0

    def incoming_transwer(self, value):
        if value > 0:
            self.balance += value

    def outgoing_transwer(self, value):
        if 0 < value <= self.balance:
            self.balance -= value

    # def outgoing_express_transwer(self, value):
    #     if value <= 0:
    #         return "Błąd, kwota nie może być mniejsza niż 0 zł"
    #     total = value + self.express_outgoing_transfer_fee
    #     if total-self.express_outgoing_transfer_fee <= self.balance:
    #         self.balance -= total
    #         return True
    #     return False
    
    # def outgoing_express_transwer(self, value):
    #     if value <= 0:
    #         return False # Zmieniamy na False dla spójności
    #     total = value + self.express_outgoing_transfer_fee
    #     if total <= self.balance: # Poprawiony warunek
    #         self.balance -= total
    #         return True
    #     return False

    def outgoing_express_transwer(self, value):
        if value <= 0:
            return "Błąd, kwota nie może być ujemna"
        
        # Warunek: saldo musi pozwolić na samą kwotę przelewu
        if value <= self.balance:
            self.balance -= value
            # Tutaj dodamy zapis do historii: -value [cite: 47, 51]
            
            self.balance -= self.express_outgoing_transfer_fee
            # Tutaj dodamy zapis do historii: -fee 
            return True
            
        return "Błąd, zbyt mało środków na koncie"
