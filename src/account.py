from datetime import date
from smtp.smtp import SMTPClient

class Account:
    express_outgoing_transfer_fee = 0

    def incoming_transfer(self, value):
        if value > 0:
            self.balance += value
            self.historia.append(value)

    def outgoing_transfer(self, value):
        if 0 < value <= self.balance:
            self.balance -= value
            self.historia.append(-value)

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
    
    def send_history_via_email(self, email_address):
        dzis = date.today().strftime("%Y-%m-%d")
        
        subject = f"Account Transfer History {dzis}"
        
        prefix = "Personal" if hasattr(self, 'pesel') else "Company"
        text = f"{prefix} account history: {self.historia}"        

        return SMTPClient.send(subject, text, email_address)