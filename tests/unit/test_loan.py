import pytest
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

@pytest.fixture
def account_with_history():
    return PersonalAccount("Jan", "Kowalski", "70010112345")

@pytest.fixture
def company_account():
    return CompanyAccount("Software Sp. z o.o.", "1234567890")

def test_loan_approved_last_three_deposits(account_with_history):
    account = account_with_history
    account.incoming_transfer(100)
    account.incoming_transfer(200)
    account.incoming_transfer(300)
    
    decision = account.submit_for_loan(500)
    
    assert decision is True
    assert account.balance == 1100

@pytest.mark.parametrize("history, loan_amount, expected_result", [
        ([100, 100, 100, 100, 101], 500, True),   
        ([100, 100, -50, 100, 100], 500, False),  
        ([600, 100, 100, -100, 100], 500, True),
        ([100, 100, 100, 201, -1], 500, False),
        ([1000], 500, False),
    ])            
def test_loan_sum_of_last_five(account_with_history, history, loan_amount, expected_result):
    account = account_with_history
    account.historia = history
    
    decision = account.submit_for_loan(loan_amount)
    assert decision == expected_result

class TestCompanyLoan:

    @pytest.mark.parametrize("initial_balance, loan_amount, history, expected_result, expected_balance", [
        (2000, 1000, [-1775], True, 3000),      
        (3000, 1000, [500, -1775, 100], True, 4000), 
        (1999, 1000, [-1775], False, 1999),     
        (5000, 1000, [1000, -500], False, 5000), 
        (2000, 1000, [-1774], False, 2000)      
    ])
    def test_company_take_loan(self, company_account, initial_balance, loan_amount, history, expected_result, expected_balance):
        company_account.balance = initial_balance
        company_account.historia = history
        
        res = company_account.take_loan(loan_amount)
        
        assert res is expected_result
        assert company_account.balance == expected_balance