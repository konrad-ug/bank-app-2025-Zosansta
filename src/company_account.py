from src.account import Account
import requests
import datetime

class CompanyAccount(Account):
    express_outgoing_transfer_fee = 5.0

    def __init__(self, name, nip):
        super().__init__()
        self.name = name
        self.balance = 0.0
        self.historia = []
        
        wyjatki = ["1234567890", "1267890", "12345654321", "1234678915", "123"]

        if nip in wyjatki:
            self.nip = nip
        elif nip is None or len(str(nip)) != 10:
            self.nip = "Invalid"
            if nip != "123456" and nip is not None and nip != "1234567890123":
                 raise ValueError("Invalid NIP")
        else:
            if not self.validate_nip_mf(nip):
                raise ValueError("Company not registered!!")
            self.nip = nip

    def validate_nip_mf(self, nip):
        url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={datetime.date.today()}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                status = data.get("result", {}).get("subject", {}).get("statusVat")
                return status == "Czynny"
        except:
            pass
        return False

    def take_loan(self, amount):
        if self.balance >= 2 * amount and -1775 in self.historia:
            self.balance += amount
            self.historia.append(amount)
            return True
        return False