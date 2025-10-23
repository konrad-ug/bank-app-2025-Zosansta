from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

class TestTransfers:
    def test_incoming_transwer(self):
        personal_account = PersonalAccount("Bob", "Smith", "12345654321")
        personal_account.incoming_transwer(100.0)
        assert personal_account.balance == 100.0

        company_account = CompanyAccount("Nazwa", "12345654321")
        company_account.incoming_transwer(100.0)
        assert company_account.balance == 100.0

    def test_outgoing_transwer(self):
        personal_account = PersonalAccount("Bob", "Smith", "12345654321")
        personal_account.balance = 200.0 #1. set up
        personal_account.outgoing_transwer(50.0) #2. action
        assert personal_account.balance == 150.0 #3. assertion

        company_account = CompanyAccount("Nazwa", "12345654321")
        company_account.balance = 200.0
        company_account.outgoing_transwer(50.0)
        assert company_account.balance == 150.0

    def test_transwer_insufficient_funds(self):
        personal_account = PersonalAccount("Bob", "Smith", "12345654321")
        personal_account.outgoing_transwer(30.0)
        assert personal_account.balance == 0.0

        company_account = CompanyAccount("Nazwa", "12345654321")
        company_account.outgoing_transwer(30.0)
        assert company_account.balance == 0.0

    def test_transwer_insufficient_funds2(self):
        personal_account = PersonalAccount("Bob", "Smith", "12345654321")
        personal_account.outgoing_transwer(-20.0)
        assert personal_account.balance == 0.0

        company_account = CompanyAccount("Nazwa", "12345654321")
        company_account.outgoing_transwer(-20.0)
        assert company_account.balance == 0.0

        

        