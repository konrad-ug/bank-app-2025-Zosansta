# from src.account import Account

# class CompanyAccount(Account):
#     express_outgoing_transfer_fee = 5.0

#     def __init__(self, name, nip):
#         self.name = name
#         self.nip = nip if self.is_nip_valid(nip) else "Invalid"
#         self.balance = 0.0
#         self.account_type = "company"
#         self.historia = []

#     def is_nip_valid(self, nip):
#         if isinstance(nip, str) and len(nip) == 10:
#             return True
    
#     def take_loan(self, amount):
#         if self.balance >= 2 * amount and -1775 in self.historia:
#             self.balance += amount
#             return True
        
#         return False

import os
import requests
from datetime import date
from src.account import Account

class CompanyAccount(Account):
    default_url = "https://wl-test.mf.gov.pl/api/search/nip/"

    def __init__(self, name, nip):
        self.name = name
        if len(nip) != 10:
            self.nip = nip
        else:
            if not self.validate_nip_mf(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip
        
        self.balance = 0.0
        self.historia = []

    def validate_nip_mf(self, nip):
        base_url = os.getenv("BANK_APP_MF_URL", self.default_url)
        today = date.today().strftime("%Y-%m-%d")
        full_url = f"{base_url}{nip}?date={today}"

        try:
            response = requests.get(full_url)
            data = response.json()
            

            print(f"MF API Response: {data}")


            if "result" in data and "subject" in data["result"] and data["result"]["subject"] is not None:
                return data["result"]["subject"].get("statusVat") == "Czynny"
            return False
        except Exception:
            return False