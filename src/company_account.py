from src.account import Account

class CompanyAccount(Account):
    express_outgoing_transfer_fee = 5.0

    def __init__(self, name, nip):
        self.name = name
        self.nip = nip if self.is_nip_valid(nip) else "Invalid"
        self.balance = 0.0
        self.account_type = "company"
        self.historia = []

    def is_nip_valid(self, nip):
        if isinstance(nip, str) and len(nip) == 10:
            return True
    
    def take_loan(self, amount):
        if self.balance >= 2 * amount and -1775 in self.historia:
            self.balance += amount
            return True
        
        return False