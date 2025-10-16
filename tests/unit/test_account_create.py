from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12457897334")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12457897334"

    def test_pesel_too_long(self):
        account = Account("John", "Doe", "12457897334")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = Account("John", "Doe", "127334")
        assert account.pesel == "Invalid"

    def test_pesel_too_long(self):
        account = Account("John", "Doe", None)
        assert account.pesel == "Invalid"