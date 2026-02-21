import unittest
from unittest.mock import patch
from datetime import date

from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount


class TestEmailHistory(unittest.TestCase):

    def setUp(self):
        self.email = "test@email.com"

    @patch('smtp.smtp.SMTPClient.send')
    def test_send_history_personal_success(self, mock_send):

        mock_send.return_value = True

        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.historia = [100, -1, 500]

        result = account.send_history_via_email(self.email)

        self.assertTrue(result)

        expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        expected_text = "Personal account history: [100, -1, 500]"

        mock_send.assert_called_once_with(
            expected_subject,
            expected_text,
            self.email
        )


    @patch('smtp.smtp.SMTPClient.send')
    def test_send_history_personal_fail(self, mock_send):

        mock_send.return_value = False

        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.historia = []

        result = account.send_history_via_email(self.email)

        self.assertFalse(result)

        expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        expected_text = "Personal account history: []"

        mock_send.assert_called_once_with(
            expected_subject,
            expected_text,
            self.email
        )


    @patch('src.company_account.CompanyAccount.validate_nip_mf')
    @patch('smtp.smtp.SMTPClient.send')
    def test_send_history_company_success(self, mock_send, mock_nip):

        mock_nip.return_value = True
        mock_send.return_value = True

        account = CompanyAccount("Firma", "8461627563")
        account.historia = [5000, -1000, 500]

        result = account.send_history_via_email(self.email)

        self.assertTrue(result)

        expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        expected_text = "Company account history: [5000, -1000, 500]"

        mock_send.assert_called_once_with(
            expected_subject,
            expected_text,
            self.email
        )


    @patch('src.company_account.CompanyAccount.validate_nip_mf')
    @patch('smtp.smtp.SMTPClient.send')
    def test_send_history_company_fail(self, mock_send, mock_nip):

        mock_nip.return_value = True
        mock_send.return_value = False

        account = CompanyAccount("Firma", "8461627563")

        result = account.send_history_via_email(self.email)

        self.assertFalse(result)

        expected_subject = f"Account Transfer History {date.today().strftime('%Y-%m-%d')}"
        expected_text = "Company account history: []"

        mock_send.assert_called_once_with(
            expected_subject,
            expected_text,
            self.email
        )

    def test_outgoing_express_transfer_negative_amount(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        result = account.outgoing_express_transfer(-100)
        self.assertEqual(result, "Błąd, kwota nie może być ujemna")

    def test_outgoing_express_transfer_insufficient_funds(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 100
        result = account.outgoing_express_transfer(200)
        self.assertEqual(result, "Błąd, zbyt mało środków na koncie")

    def test_incoming_transfer_negative_value(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 100
        account.incoming_transfer(-50)
        self.assertEqual(account.balance, 100) 

    def test_outgoing_transfer_invalid_value(self):
        account = PersonalAccount("Jan", "Kowalski", "12345678901")
        account.balance = 100
        account.outgoing_transfer(150)
        self.assertEqual(account.balance, 100)