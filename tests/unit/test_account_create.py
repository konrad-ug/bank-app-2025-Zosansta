# from src.personal_account import PersonalAccount


# class TestAccount:
#     def test_account_creation(self):
#         account = PersonalAccount("John", "Doe", "12457897334")
#         assert account.first_name == "John"
#         assert account.last_name == "Doe"
#         assert account.balance == 0.0
#         assert account.pesel == "12457897334"
    
#     def test_default_balance(self):
#         account = PersonalAccount("John", "Doe", "12457897334")
#         assert account.balance == 0.0

#     def test_pesel_too_long(self):
#         account = PersonalAccount("John", "Doe", "124657897334")
#         assert account.pesel == "Invalid"
    
#     def test_pesel_too_short(self):
#         account = PersonalAccount("John", "Doe", "127334")
#         assert account.pesel == "Invalid"

#     def test_pesel_none(self):
#         account = PersonalAccount("John", "Doe", None)
#         assert account.pesel == "Invalid"

#     def test_correct_promo_code_too_long(self):
#         account = PersonalAccount("John", "Doe", "12457897334", "PROM_1552")
#         assert account.balance == 0.0

#     def test_correct_promo_code_too_short(self):
#         account = PersonalAccount("John", "Doe", "12457897334", "PROM_52")
#         assert account.balance == 0.0

#     def test_correct_promo_code_wrong_prefix(self):
#         account = PersonalAccount("John", "Doe", "12457897334", "PROM-52")
#         assert account.balance == 0.0

#     def test_promo_year_before_1960(self):
#         account = PersonalAccount("Jane", "Doe", "55010112345", "PROM_123")
#         assert account.balance == 0.0

#     def test_promo_year_after_1960(self):
#         account = PersonalAccount("Jane", "Doe", "61010112345", "PROM_123")
#         assert account.balance == 50.0

#     def test_is_after_1960_invalid_pesel(self):
#         account = PersonalAccount(first_name="Jan", last_name="Kowalski", pesel="Invalid")
#         assert account.is_after_1960() is False

#     def test_is_after_1960_2000(self):
#         account = PersonalAccount(first_name="Jan", last_name="Kowalski", pesel="01220100000")  
#         assert account.is_after_1960() is True

#     def test_is_after_1960_invalid_month(self):
#         account = PersonalAccount(first_name="Jan", last_name="Kowalski", pesel="99350100000")
#         assert account.is_after_1960() is False


import pytest
from src.personal_account import PersonalAccount

class TestAccount:

    @pytest.mark.parametrize("pesel, expected_pesel", [
        ("12457897334", "12457897334"),
        ("124657897334", "Invalid"),
        ("127334", "Invalid"),
        (None, "Invalid")
    ])
    def test_account_creation_pesel(self, pesel, expected_pesel):
        account = PersonalAccount("John", "Doe", pesel)
        assert account.pesel == expected_pesel


    @pytest.mark.parametrize("pesel, promo_code, expected_balance", [
        ("61010112345", "PROM_123", 50.0),
        ("55010112345", "PROM_123", 0.0),
        ("61010112345", "PROM_1552", 0.0),
        ("61010112345", "PROM_52", 0.0),
        ("61010112345", "PROM-52", 0.0),
        ("61010112345", None, 0.0)
    ])
    def test_promo_code_logic(self, pesel, promo_code, expected_balance):
        account = PersonalAccount("Jane", "Doe", pesel, promo_code)
        assert account.balance == expected_balance


    @pytest.mark.parametrize("pesel, expected_result", [
        ("01220100000", True),
        ("99350100000", False),
        ("Invalid", False),
        ("61010112345", True),
        ("59010112345", False)
    ])
    def test_is_after_1960(self, pesel, expected_result):
        account = PersonalAccount("Jan", "Kowalski", pesel)
        assert account.is_after_1960() is expected_result


    def test_account_details(self):
        account = PersonalAccount("John", "Doe", "12457897334")
        assert account.first_name == "John"
        assert account.last_name == "Doe"

    