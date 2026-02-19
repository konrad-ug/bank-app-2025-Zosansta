# class Account:
#     express_outgoing_transfer_fee = 0

#     def incoming_transfer(self, value):
#         if value > 0:
#             self.balance += value

#     def outgoing_transfer(self, value):
#         if 0 < value <= self.balance:
#             self.balance -= value

#     def outgoing_express_transfer(self, value):
#         if value <= 0:
#             return "Błąd, kwota nie może być ujemna"
        
#         if value <= self.balance:
#             self.balance -= value
            
#             self.balance -= self.express_outgoing_transfer_fee
#             return True
            
#         return "Błąd, zbyt mało środków na koncie"

class Account:
    express_outgoing_transfer_fee = 0

    def incoming_transfer(self, value):
        if value > 0:
            self.balance += value
            self.historia.append(value)

    def outgoing_transfer(self, value):
        if 0 < value <= self.balance:
            self.balance -= value
            self.historia.append(-value) # [cite: 47]

    def outgoing_express_transfer(self, value):
        if value <= 0:
            return "Błąd, kwota nie może być ujemna"
        
        if value <= self.balance:
            self.balance -= value
            self.historia.append(-value)
            
            self.balance -= self.express_outgoing_transfer_fee
            self.historia.append(-self.express_outgoing_transfer_fee)
            return True
            
        return "Błąd, zbyt mało środków na koncie"