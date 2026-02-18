import pytest
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

@pytest.fixture
def registry():
    return AccountRegistry()

@pytest.fixture
def account_jan():
    return PersonalAccount("Jan", "Kowalski", "70010112345")

@pytest.fixture
def account_anna():
    return PersonalAccount("Anna", "Nowak", "80010112345")

class TestAccountRegistry:

    def test_add_account(self, registry, account_jan):
        registry.add_account(account_jan)
        assert registry.count() == 1
        assert account_jan in registry.get_all()

    def test_find_account_by_pesel(self, registry, account_jan, account_anna):
        registry.add_account(account_jan)
        registry.add_account(account_anna)
        
        found = registry.find_by_pesel("70010112345")
        assert found == account_jan
        assert found.first_name == "Jan"

    def test_find_account_non_existent(self, registry):
        assert registry.find_by_pesel("00000000000") is None

    def test_get_all_accounts(self, registry, account_jan, account_anna):
        registry.add_account(account_jan)
        registry.add_account(account_anna)
        
        all_accounts = registry.get_all()
        assert len(all_accounts) == 2
        assert account_jan in all_accounts
        assert account_anna in all_accounts

    def test_registry_count(self, registry, account_jan):
        assert registry.count() == 0
        registry.add_account(account_jan)
        assert registry.count() == 1