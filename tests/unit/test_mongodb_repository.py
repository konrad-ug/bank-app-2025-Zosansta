import unittest
from unittest.mock import MagicMock
from src.mongodb_repository import MongoAccountsRepository

class TestMongoAccountsRepository(unittest.TestCase):
    def setUp(self):
        # Udajemy połączenie z bazą
        self.repository = MongoAccountsRepository()
        self.repository.collection = MagicMock()

    def test_save_all_clears_db_and_inserts_data(self):
        # Tworzymy "udawane" konto
        mock_acc = MagicMock()
        mock_acc.to_dict.return_value = {"name": "Jan", "pesel": "111"}
        
        # Wywołujemy zapis
        self.repository.save_all([mock_acc])
        
        # Sprawdzamy czy wyczyszczono kolekcję (wymóg z PDF)
        self.repository.collection.delete_many.assert_called_once_with({})
        # Sprawdzamy czy wstawiono dane
        self.repository.collection.insert_one.assert_called()