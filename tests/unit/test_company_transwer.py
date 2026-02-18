import pytest
from src.company_account import CompanyAccount

class TestCompanyAccount:


    def test_company_account_creation(self):
        company_account = CompanyAccount("Nazwa_firmy", "1234678915")
        assert company_account.name == "Nazwa_firmy"
        assert company_account.balance == 0.0
        assert company_account.nip == "1234678915"


    @pytest.mark.parametrize("nip, expected_nip", [
        ("1234567890", "1234567890"),
        ("1234567890123", "Invalid"),
        ("123456", "Invalid"),
        (None, "Invalid")
    ])
    def test_nip_validation(self, nip, expected_nip):
        company_account = CompanyAccount("Nazwa_firmy", nip)
        assert company_account.nip == expected_nip