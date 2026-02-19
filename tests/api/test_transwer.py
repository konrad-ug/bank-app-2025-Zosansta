# import requests
# import pytest

# class TestTransfersApi:
#     url = "http://127.0.0.1:5000/api/accounts"
#     pesel = "12345678901"

#     # Fixture, która przygotowuje czyste konto przed każdym testem
#     @pytest.fixture(autouse=True)
#     def setup_account(self):
#         # Usuwamy konto jeśli istnieje (aby testy były powtarzalne)
#         requests.delete(f"{self.url}/{self.pesel}")
#         # Tworzymy nowe konto
#         requests.post(self.url, json={
#             "name": "Jan", "surname": "Kowalski", "pesel": self.pesel
#         })

#     # 1. Test unikatowości PESEL (Feature 16)
#     def test_duplicate_pesel_conflict(self):
#         # Próba stworzenia konta z tym samym peselem [cite: 1, 2]
#         response = requests.post(self.url, json={
#             "name": "Adam", "surname": "Nowak", "pesel": self.pesel
#         })
#         # Oczekujemy kodu 409 [cite: 3]
#         assert response.status_code == 409

#     # 2. Test przelewu przychodzącego (Feature 17)
#     def test_incoming_transfer(self):
#         body = {"amount": 500, "type": "incoming"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
#         assert response.status_code == 200
        
#         # Sprawdzamy czy saldo się zgadza
#         acc_info = requests.get(f"{self.url}/{self.pesel}").json()
#         assert acc_info["balance"] == 500

#     # 3. Test przelewu wychodzącego - brak środków
#     def test_outgoing_transfer_fail(self):
#         body = {"amount": 1000, "type": "outgoing"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
#         # Oczekujemy 422 przy niepowodzeniu 
#         assert response.status_code == 422

#     # 4. Test nieistniejącego konta (404)
#     def test_transfer_non_existent_account(self):
#         body = {"amount": 100, "type": "incoming"}
#         response = requests.post(f"{self.url}/00000000000/transfer", json=body)
#         assert response.status_code == 404

#     # 5. Test nieznanego typu przelewu
#     def test_unknown_transfer_type(self):
#         body = {"amount": 100, "type": "unknown_type"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
#         # Powinieneś zdecydować jaki kod zwrócić - np. 400 (Bad Request) [cite: 16]
#         assert response.status_code == 400

#     def test_outgoing_transfer_insufficient_funds(self):
#         # Pokrywa linię 40 i 43 - brak środków na przelew wychodzący
#         # Zakładamy, że konto ma saldo 0 lub mniej niż 1000000
#         body = {"amount": 1000000, "type": "outgoing"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
#         assert response.status_code == 422
#         assert response.json()["message"] == "Transfer failed"

#     def test_transfer_invalid_type(self):
#         # Pokrywa linie 49-50 - nieznany typ przelewu
#         body = {"amount": 100, "type": "unknown_type_xyz"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
#         assert response.status_code == 400
#         assert response.json()["message"] == "Unknown transfer type"

#     def test_transfer_negative_amount(self):
#         # Dodatkowe sprawdzenie, które może wywołać blok 'except' (422) 
#         # w zależności od tego, jak rygorystyczne jest Twoje src/account.py
#         body = {"amount": -100, "type": "incoming"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
#         # Jeśli Twoje src rzuca wyjątek przy ujemnych kwotach, to wejdzie w except
#         assert response.status_code in [200, 422]

#     def test_transfer_exception_trigger(self):
#         # Wysyłamy dane, które mogą spowodować błąd typu (np. None zamiast liczby)
#         # Jeśli Twoja metoda w src spróbuje dodać None do salda, rzuci wyjątek
#         body = {"amount": None, "type": "incoming"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
        
#         # To powinno wejść w blok 'except Exception' w api.py
#         assert response.status_code == 422
#         assert response.json()["message"] == "Transfer failed"
    
#     def test_outgoing_transfer_success(self):
#         # Najpierw upewnij się, że na koncie są środki (np. przez incoming)
#         requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 1000, "type": "incoming"})
        
#         # Teraz testujemy właściwy przelew wychodzący
#         body = {"amount": 500, "type": "outgoing"}
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
        
#         assert response.status_code == 200
#         assert response.json()["message"] == "Zlecenie przyjęto do realizacji"

#     def test_express_transfer_success(self):
#         # Doładowanie konta
#         requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 1000, "type": "incoming"})
        
#         # Przelew ekspresowy
#         body = {"amount": 100, "type": "express"} # upewnij się, że taki typ obsługujesz w api.py
#         response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
        
#         assert response.status_code == 200
#         assert response.json()["message"] == "Zlecenie przyjęto do realizacji"

import unittest
import requests

class TestTransfersApi(unittest.TestCase):
    url = "http://127.0.0.1:5000/api/accounts"
    pesel = "12345678901"

    def setUp(self):
        requests.post(self.url, json={"name": "Jan", "surname": "Kowalski", "pesel": self.pesel})

    def tearDown(self):
        requests.delete(f"{self.url}/{self.pesel}")

    def test_incoming_transfer(self):
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 1000, "type": "incoming"})
        assert response.status_code == 200
        assert response.json()["message"] == "Zlecenie przyjęto do realizacji"

    def test_outgoing_transfer_success(self):
        requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 1000, "type": "incoming"})
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 500, "type": "outgoing"})
        assert response.status_code == 200
        assert response.json()["message"] == "Zlecenie przyjęto do realizacji"

    def test_outgoing_transfer_fail(self):
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 1000, "type": "outgoing"})
        assert response.status_code == 422
        assert response.json()["message"] == "Błąd przelewu"

    # def test_express_transfer_success(self):
    #     requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 1000, "type": "incoming"})
    #     response = requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 100, "type": "express"})
    #     assert response.status_code == 200
    #     assert response.json()["message"] == "Zlecenie przyjęto do realizacji"

    

    # def test_transfer_account_not_found(self):
    #     response = requests.post(f"{self.url}/99999999999/transfer", json={"amount": 100, "type": "incoming"})
    #     assert response.status_code == 404
    #     assert response.json()["message"] == "Nie znaleziono konta"

    def test_express_transfer_success(self):
        # Używamy unikatowego PESEL, którego na pewno nie ma
        pesel_exp = "88888888888"
        requests.post(self.url, json={"name": "E", "surname": "X", "pesel": pesel_exp})
        requests.post(f"{self.url}/{pesel_exp}/transfer", json={"amount": 1000, "type": "incoming"})
        
        response = requests.post(f"{self.url}/{pesel_exp}/transfer", json={"amount": 100, "type": "express"})
        
        assert response.status_code == 200
        assert response.json()["message"] == "Zlecenie przyjęto do realizacji"

    def test_transfer_account_not_found(self):
        # Używamy PESEL, którego NIGDY nie tworzymy w żadnym teście
        response = requests.post(f"{self.url}/00000000000/transfer", json={"amount": 100, "type": "incoming"})
        assert response.status_code == 404
        assert response.json()["message"] == "Nie znaleziono konta"

    def test_transfer_unknown_type(self):
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json={"amount": 100, "type": "unknown"})
        assert response.status_code == 400
        assert response.json()["message"] == "Nieznany typ przelewu"

    def test_transfer_exception_trigger(self):
        # Wywołanie błędu przez brak klucza 'amount' w JSON
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json={"type": "incoming"})
        assert response.status_code == 422
        assert response.json()["message"] == "Błąd przelewu"