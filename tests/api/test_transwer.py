import requests
import pytest

class TestTransfersApi:
    url = "http://127.0.0.1:5000/api/accounts"
    pesel = "12345678901"

    # Fixture, która przygotowuje czyste konto przed każdym testem
    @pytest.fixture(autouse=True)
    def setup_account(self):
        # Usuwamy konto jeśli istnieje (aby testy były powtarzalne)
        requests.delete(f"{self.url}/{self.pesel}")
        # Tworzymy nowe konto
        requests.post(self.url, json={
            "name": "Jan", "surname": "Kowalski", "pesel": self.pesel
        })

    # 1. Test unikatowości PESEL (Feature 16)
    def test_duplicate_pesel_conflict(self):
        # Próba stworzenia konta z tym samym peselem [cite: 1, 2]
        response = requests.post(self.url, json={
            "name": "Adam", "surname": "Nowak", "pesel": self.pesel
        })
        # Oczekujemy kodu 409 [cite: 3]
        assert response.status_code == 409

    # 2. Test przelewu przychodzącego (Feature 17)
    def test_incoming_transfer(self):
        body = {"amount": 500, "type": "incoming"}
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
        assert response.status_code == 200
        
        # Sprawdzamy czy saldo się zgadza
        acc_info = requests.get(f"{self.url}/{self.pesel}").json()
        assert acc_info["balance"] == 500

    # 3. Test przelewu wychodzącego - brak środków
    def test_outgoing_transfer_fail(self):
        body = {"amount": 1000, "type": "outgoing"}
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
        # Oczekujemy 422 przy niepowodzeniu 
        assert response.status_code == 422

    # 4. Test nieistniejącego konta (404)
    def test_transfer_non_existent_account(self):
        body = {"amount": 100, "type": "incoming"}
        response = requests.post(f"{self.url}/00000000000/transfer", json=body)
        assert response.status_code == 404

    # 5. Test nieznanego typu przelewu
    def test_unknown_transfer_type(self):
        body = {"amount": 100, "type": "unknown_type"}
        response = requests.post(f"{self.url}/{self.pesel}/transfer", json=body)
        # Powinieneś zdecydować jaki kod zwrócić - np. 400 (Bad Request) [cite: 16]
        assert response.status_code == 400