from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount
from src.account import Account

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
        personal_account.balance = 200.0
        personal_account.outgoing_transwer(50.0)
        assert personal_account.balance == 150.0

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

    def test_personal_account_express_transfer(self):
        personal_account = PersonalAccount("Alice", "Kowalski", "61010112345")
        personal_account.balance = 10.0
        personal_account.outgoing_express_transwer(10.0)
        assert personal_account.balance == -1.0

    def test_company_account_express_transfer(self):
        account = CompanyAccount("Firma", "12345654321")
        account.balance = 10.0
        account.outgoing_express_transwer(10.0)
        assert account.balance == -5.0

    def test_express_transfer_insufficient_funds_message(self):
        personal_account = PersonalAccount("Alice", "Kowalski", "61010112345")
        personal_account.balance = 5.0
        result = personal_account.outgoing_express_transwer(10.0)
        assert result == "Błąd, zbyt mało środków na koncie"


    def test_express_transfer_negative_amount_message(self):
        personal_account = PersonalAccount("Alice", "Kowalski", "61010112345")
        personal_account.balance = 10.0
        result = personal_account.outgoing_express_transwer(-5.0)
        assert result == "Błąd, kwota nie może być ujemna"
        assert personal_account.balance == 10.0

    def test_express_transfer_fee(self):
        personal_account = PersonalAccount(first_name="Jan", last_name="Kowalski", pesel="12345678901")
        personal_account.balance = 100.0
        personal_account.outgoing_express_transwer(50)
        assert personal_account.balance == 49

        