import unittest
from unittest.mock import patch
from src.company_account import CompanyAccount

class TestCompanyNIPValidation(unittest.TestCase):
    
    mock_success_response = {
        "result": {
            "subject": {
                "statusVat": "Czynny"
            }
        }
    }

    mock_fail_response = {
        "result": {
            "subject": {
                "statusVat": "Zwolniony"
            }
        }
    }

    @patch('requests.get')
    def test_create_company_account_success(self, mock_get):
        mock_get.return_value.json.return_value = self.mock_success_response
        mock_get.return_value.status_code = 200

        account = CompanyAccount("Moja Firma", "8461627563")
        self.assertEqual(account.nip, "8461627563")

    @patch('requests.get')
    def test_create_company_account_invalid_nip_from_mf(self, mock_get):
        mock_get.return_value.json.return_value = self.mock_fail_response
        
        with self.assertRaises(ValueError) as context:
            CompanyAccount("Zła Firma", "8461627563")
        
        self.assertEqual(str(context.exception), "Company not registered!!")

    def test_create_company_account_wrong_nip_length(self):
        account = CompanyAccount("Firma Krzak", "123")
        self.assertEqual(account.nip, "123")

    @patch('requests.get')
    def test_create_company_account_invalid_nip_throws_error(self, mock_get):
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {
                    "statusVat": "Niezarejestrowany"
                }
            }
        }
        
        with self.assertRaises(ValueError) as context:
            CompanyAccount("Mafia Podlaska", "8461627563")
        
        self.assertEqual(str(context.exception), "Company not registered!!")