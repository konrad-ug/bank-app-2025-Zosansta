from pymongo import MongoClient

class MongoAccountsRepository:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["bank_app"]
        self.collection = self.db["accounts"]

    def save_all(self, accounts):
        self.collection.delete_many({})
        for account in accounts:
            self.collection.insert_one(account.to_dict())

    def load_all(self):
        return list(self.collection.find({}, {"_id": 0}))