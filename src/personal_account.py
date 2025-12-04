from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
        if self.is_promo_code_valid(promo_code) and self.is_after_1960():
            self.balance = 50.0
        else:
            self.balance = 0.0
        self.account_type = "personal"
    

    # def outgoing_express_transwer(self):
        

    def is_pesel_valid(self, pesel):
        if isinstance(pesel, str) and len(pesel) == 11:
            return True
        else:
            return False
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False
    
    def is_after_1960(self):
        if self.pesel == "Invalid":
            return False
        year_prefix = int(self.pesel[:2])
        month = int(self.pesel[2:4])
        if 1 <= month <= 12:
            year = 1900 + year_prefix
        elif 21 <= month <= 32:
            year = 2000 + year_prefix
        else:
            return False

        return year > 1960
    
    