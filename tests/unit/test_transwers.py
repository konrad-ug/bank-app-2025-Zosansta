# from src.personal_account import PersonalAccount
# from src.company_account import CompanyAccount
# from src.account import Account

# class TestTransfers:

#     def test_incoming_transwer(self):
#         personal_account = PersonalAccount("Bob", "Smith", "12345654321")
#         personal_account.incoming_transwer(100.0)
#         assert personal_account.balance == 100.0

#         company_account = CompanyAccount("Nazwa", "12345654321")
#         company_account.incoming_transwer(100.0)
#         assert company_account.balance == 100.0

#     def test_outgoing_transwer(self):
#         personal_account = PersonalAccount("Bob", "Smith", "12345654321")
#         personal_account.balance = 200.0
#         personal_account.outgoing_transwer(50.0)
#         assert personal_account.balance == 150.0

#         company_account = CompanyAccount("Nazwa", "12345654321")
#         company_account.balance = 200.0
#         company_account.outgoing_transwer(50.0)
#         assert company_account.balance == 150.0

#     def test_transwer_insufficient_funds(self):
#         personal_account = PersonalAccount("Bob", "Smith", "12345654321")
#         personal_account.outgoing_transwer(30.0)
#         assert personal_account.balance == 0.0

#         company_account = CompanyAccount("Nazwa", "12345654321")
#         company_account.outgoing_transwer(30.0)
#         assert company_account.balance == 0.0

#     def test_transwer_insufficient_funds2(self):
#         personal_account = PersonalAccount("Bob", "Smith", "12345654321")
#         personal_account.outgoing_transwer(-20.0)
#         assert personal_account.balance == 0.0

#         company_account = CompanyAccount("Nazwa", "12345654321")
#         company_account.outgoing_transwer(-20.0)
#         assert company_account.balance == 0.0

#     def test_personal_account_express_transfer(self):
#         personal_account = PersonalAccount("Alice", "Kowalski", "61010112345")
#         personal_account.balance = 10.0
#         personal_account.outgoing_express_transwer(10.0)
#         assert personal_account.balance == -1.0

#     def test_company_account_express_transfer(self):
#         account = CompanyAccount("Firma", "12345654321")
#         account.balance = 10.0
#         account.outgoing_express_transwer(10.0)
#         assert account.balance == -5.0

#     def test_express_transfer_insufficient_funds_message(self):
#         personal_account = PersonalAccount("Alice", "Kowalski", "61010112345")
#         personal_account.balance = 5.0
#         result = personal_account.outgoing_express_transwer(10.0)
#         assert result == "Błąd, zbyt mało środków na koncie"


#     def test_express_transfer_negative_amount_message(self):
#         personal_account = PersonalAccount("Alice", "Kowalski", "61010112345")
#         personal_account.balance = 10.0
#         result = personal_account.outgoing_express_transwer(-5.0)
#         assert result == "Błąd, kwota nie może być ujemna"
#         assert personal_account.balance == 10.0

#     def test_express_transfer_fee(self):
#         personal_account = PersonalAccount(first_name="Jan", last_name="Kowalski", pesel="12345678901")
#         personal_account.balance = 100.0
#         personal_account.outgoing_express_transwer(50)
#         assert personal_account.balance == 49

#     def test_history(self):
#         account = PersonalAccount("Jan", "Kowalski", "70010112345")
#         account.incoming_transwer(500.0)
#         account.outgoing_express_transwer(300.0)
#         assert account.historia == [500.0, -300.0, -1.0]

#     def test_histor_transwer(self):
#         account = PersonalAccount("Jan", "Kowalski", "70010112345")
#         account.balance = 100.0
#         account.outgoing_transwer(50.0)
#         assert account.historia == [-50.0]

#     def test_history_company_transwer(self):
#         account = CompanyAccount("Firma", "1234567890")
#         account.balance = 100.0
#         account.outgoing_express_transwer(50.0)
#         assert account.historia == [-50.0, -5.0]


import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

@pytest.fixture
def empty_personal():
    return PersonalAccount("Bob", "Smith", "12345654321")

@pytest.fixture
def empty_company():
    return CompanyAccount("Nazwa", "12345654321")

class TestTransfers:

    @pytest.mark.parametrize("account_type", [
        PersonalAccount("Bob", "Smith", "12345654321"),
        CompanyAccount("Nazwa", "12345654321")
    ])
    def test_incoming_transfer_multi(self, account_type):
        account = account_type
        account.incoming_transwer(100.0)
        assert account.balance == 100.0



    @pytest.mark.parametrize("amount, initial_balance, expected_balance", [
        (50.0, 200.0, 150.0),
        (30.0, 0.0, 0.0),
        (-20.0, 0.0, 0.0) 
    ])
    def test_outgoing_transfers(self, empty_personal, amount, initial_balance, expected_balance):
        empty_personal.balance = initial_balance
        empty_personal.outgoing_transwer(amount)
        assert empty_personal.balance == expected_balance

    # 2. Testy błędów przelewów ekspresowych (sprawdzamy zwracany komunikat)
    @pytest.mark.parametrize("amount, initial_balance, expected_message", [
        (-10.0, 100.0, "Błąd, kwota nie może być ujemna"),
        (1000.0, 100.0, "Błąd, zbyt mało środków na koncie")
    ])
    def test_express_transfer_errors(self, empty_personal, amount, initial_balance, expected_message):
        empty_personal.balance = initial_balance
        result = empty_personal.outgoing_express_transwer(amount)
        assert result == expected_message # Tu porównujemy napisy [cite: 19]

    @pytest.mark.parametrize("account_obj, fee", [
        (PersonalAccount("Alice", "Kowalski", "61010112345"), 1.0),
        (CompanyAccount("Firma", "12345654321"), 5.0)
    ])
    def test_express_transfer_fees(self, account_obj, fee):
        account_obj.balance = 10.0
        account_obj.outgoing_express_transwer(10.0)
        assert account_obj.balance == -fee



    @pytest.mark.parametrize("account_obj, actions, expected_history", [
        (PersonalAccount("Jan", "Kowalski", "70010112345"), 
         [("inc", 500.0), ("exp", 300.0)], [500.0, -300.0, -1.0]),
        (PersonalAccount("Jan", "Kowalski", "70010112345"), 
         [("out", 50.0)], [-50.0]),
        (CompanyAccount("Firma", "1234567890"), 
         [("exp", 50.0)], [-50.0, -5.0])
    ])
    def test_history_combined(self, account_obj, actions, expected_history):
        account_obj.balance = 100.0 if any(a[0] != "inc" for a in actions) else 0.0
        for action_type, val in actions:
            if action_type == "inc": account_obj.incoming_transwer(val)
            elif action_type == "out": account_obj.outgoing_transwer(val)
            elif action_type == "exp": account_obj.outgoing_express_transwer(val)
        
        assert account_obj.historia == expected_history  

