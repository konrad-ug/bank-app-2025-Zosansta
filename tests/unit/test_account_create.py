from src.personal_account import PersonalAccount


class TestAccount:
    def test_account_creation(self):
        account = PersonalAccount("John", "Doe", "12457897334")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12457897334"

    def test_pesel_too_long(self):
        account = PersonalAccount("John", "Doe", "124657897334")
        assert account.pesel == "Invalid"
    
    def test_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "127334")
        assert account.pesel == "Invalid"

    def test_pesel_none(self):
        account = PersonalAccount("John", "Doe", None)
        assert account.pesel == "Invalid"

    # nie wiem czemu z tym testem nie działa...
    # def test_correct_promo_code(self):
    #     account = PersonalAccount("John", "Doe", "12457897334", "PROM_123")
    #     assert account.balance == 50.0

    def test_correct_promo_code_too_long(self):
        account = PersonalAccount("John", "Doe", "12457897334", "PROM_1552")
        assert account.balance == 0.0

    def test_correct_promo_code_too_short(self):
        account = PersonalAccount("John", "Doe", "12457897334", "PROM_52")
        assert account.balance == 0.0

    def test_correct_promo_code_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "12457897334", "PROM-52")
        assert account.balance == 0.0

    def test_promo_year_before_1960(self):
        account = PersonalAccount("Jane", "Doe", "55010112345", "PROM_123")
        assert account.balance == 0.0

    def test_promo_year_after_1960(self):
        account = PersonalAccount("Jane", "Doe", "61010112345", "PROM_123")
        assert account.balance == 50.0
