import unittest
import requests

class TestApiPerformance(unittest.TestCase):
    # Poprawiony bazowy adres URL zgodnie z Twoim api.py
    base_url = "http://127.0.0.1:5000/api/accounts"

    def test_create_and_delete_100_times(self):
        # Używamy danych dla PersonalAccount (PESEL zamiast NIP)
        payload = {
            "name": "Jan",
            "surname": "Tester",
            "pesel": "12345678901"
        }
        for i in range(100):
            # Test sprawdza response code 201 i czas < 0.5s [cite: 7, 10]
            res_create = requests.post(self.base_url, json=payload, timeout=0.5)
            self.assertEqual(res_create.status_code, 201)
            
            # Usuwanie konta po PESEL [cite: 6]
            res_delete = requests.delete(f"{self.base_url}/{payload['pesel']}", timeout=0.5)
            self.assertEqual(res_delete.status_code, 200)

    def test_100_incoming_transfers_performance(self):
        pesel = "99010112345"
        # 1. Tworzymy konto do testu przelewów
        requests.post(self.base_url, json={
            "name": "Anna", 
            "surname": "Kowalska", 
            "pesel": pesel
        })

        transfer_data = {"type": "incoming", "amount": 100}
        
        # 2. Wykonujemy 100 przelewów [cite: 7]
        for i in range(100):
            # Ścieżka poprawiona na /api/accounts/<pesel>/transfer [cite: 8, 9]
            res = requests.post(f"{self.base_url}/{pesel}/transfer", json=transfer_data, timeout=0.5)
            self.assertEqual(res.status_code, 200)

        # 3. Sprawdzamy ostateczne saldo (100 * 100 = 10000) [cite: 8]
        res_final = requests.get(f"{self.base_url}/{pesel}", timeout=0.5)
        self.assertEqual(res_final.json()["balance"], 10000)

        # Sprzątanie
        requests.delete(f"{self.base_url}/{pesel}")