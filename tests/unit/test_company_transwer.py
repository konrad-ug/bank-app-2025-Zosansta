from src.company_account import CompanyAccount


class TestCompanyAccount:
    def test_company_account_creation(self):
            company_account = CompanyAccount("Nazwa_firmy", "1234678915")
            assert company_account.name == "Nazwa_firmy"
            assert company_account.balance == 0.0
            assert company_account.nip == "1234678915"

    def test_nip_too_long(self):
        company_account = CompanyAccount("Nazwa_firmy", "1245789347334")
        assert company_account.nip == "Invalid"
    
    def test_pesel_too_short(self):
        company_account = CompanyAccount("Nazwa_firmy", "124534")
        assert company_account.nip == "Invalid"

    def test_pesel_none(self):
        company_account = CompanyAccount("Nazwa_firmy", None)
        assert company_account.nip == "Invalid"