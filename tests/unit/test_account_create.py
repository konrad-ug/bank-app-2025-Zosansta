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

    