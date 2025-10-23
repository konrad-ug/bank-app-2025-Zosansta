from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        self.balance = 50 if self.is_promo_code_valid(promo_code) else 0.0

    # def outgoing_express_transwer(self):
        

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False
    
    