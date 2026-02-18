import pytest
from src.personal_account import PersonalAccount

@pytest.fixture
def account_with_history():
    account = PersonalAccount("Jan", "Kowalski", "70010112345")
    return account

def test_loan_approved_last_three_deposits(account_with_history):
    account = account_with_history
    account.incoming_transwer(100)
    account.incoming_transwer(200)
    account.incoming_transwer(300)
    
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