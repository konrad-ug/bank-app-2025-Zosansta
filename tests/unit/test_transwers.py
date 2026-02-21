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
        account.incoming_transfer(100.0)
        assert account.balance == 100.0



    @pytest.mark.parametrize("amount, initial_balance, expected_balance", [
        (50.0, 200.0, 150.0),
        (30.0, 0.0, 0.0),
        (-20.0, 0.0, 0.0) 
    ])
    def test_outgoing_transfers(self, empty_personal, amount, initial_balance, expected_balance):
        empty_personal.balance = initial_balance
        empty_personal.outgoing_transfer(amount)
        assert empty_personal.balance == expected_balance

    @pytest.mark.parametrize("amount, initial_balance, expected_message", [
        (-10.0, 100.0, "Błąd, kwota nie może być ujemna"),
        (1000.0, 100.0, "Błąd, zbyt mało środków na koncie")
    ])
    def test_express_transfer_errors(self, empty_personal, amount, initial_balance, expected_message):
        empty_personal.balance = initial_balance
        result = empty_personal.outgoing_express_transfer(amount)
        assert result == expected_message

    @pytest.mark.parametrize("account_obj, fee", [
        (PersonalAccount("Alice", "Kowalski", "61010112345"), 1.0),
        (CompanyAccount("Firma", "12345654321"), 5.0)
    ])
    def test_express_transfer_fees(self, account_obj, fee):
        account_obj.balance = 10.0
        account_obj.outgoing_express_transfer(10.0)
        assert account_obj.balance == -fee



    @pytest.mark.parametrize("account_obj, actions, expected_history", [
        (PersonalAccount("Jan", "Kowalski", "70010112345"), 
         [("inc", 500.0), ("exp", 300.0)], [500.0, -300.0, -1.0]),
        (PersonalAccount("Jan", "Kowalski", "70010112345"), 
         [("out", 50.0)], [-50.0]),
        (CompanyAccount("Firma", "1267890"), 
         [("exp", 50.0)], [-50.0, -5.0])
    ])
    def test_history_combined(self, account_obj, actions, expected_history):
        account_obj.balance = 100.0 if any(a[0] != "inc" for a in actions) else 0.0
        for action_type, val in actions:
            if action_type == "inc": account_obj.incoming_transfer(val)
            elif action_type == "out": account_obj.outgoing_transfer(val)
            elif action_type == "exp": account_obj.outgoing_express_transfer(val)
        
        assert account_obj.historia == expected_history  

