import unittest
from unittest.mock import MagicMock
from src.mongodb_repository import MongoAccountsRepository

class TestMongoAccountsRepository(unittest.TestCase):
    def setUp(self):
        self.repository = MongoAccountsRepository()
        self.repository.collection = MagicMock()

    def test_save_all_clears_db_and_inserts_data(self):
        mock_acc = MagicMock()
        mock_acc.to_dict.return_value = {"name": "Jan", "pesel": "111"}
        
        self.repository.save_all([mock_acc])
        
        self.repository.collection.delete_many.assert_called_once_with({})
        self.repository.collection.insert_one.assert_called()

    def test_load_all_calls_find(self):
        self.repository.collection.find.return_value = [{"name": "Jan"}]
        result = self.repository.load_all()
        
        self.repository.collection.find.assert_called_once()
        self.assertEqual(result, [{"name": "Jan"}])

    def test_personal_account_to_dict(self):
        from src.personal_account import PersonalAccount
        konto = PersonalAccount("Jan", "Kowalski", "11111111111")
        dane = konto.to_dict()
        
        self.assertEqual(dane["name"], "Jan")
        self.assertEqual(dane["pesel"], "11111111111")