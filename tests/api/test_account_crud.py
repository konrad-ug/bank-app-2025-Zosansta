import pytest
import requests

class TestAccountApi:
    url = "http://127.0.0.1:5000/api/accounts"
    pesel = "89092909825"

    def test_create_and_get_account_by_pesel(self):
        body = {
            "name": "Jan",
            "surname": "Nowak",
            "pesel": self.pesel
        }
        create_resp = requests.post(self.url, json=body)
        assert create_resp.status_code == 201

        get_resp = requests.get(f"{self.url}/{self.pesel}")
        assert get_resp.status_code == 200
        assert get_resp.json()["name"] == "Jan"

    def test_get_not_found(self):
        resp = requests.get(f"{self.url}/00000000000")
        assert resp.status_code == 404

    def test_update_account_surname(self):
        update_body = {"surname": "Kowalski"}
        patch_resp = requests.patch(f"{self.url}/{self.pesel}", json=update_body)
        assert patch_resp.status_code == 200
        
        get_resp = requests.get(f"{self.url}/{self.pesel}")
        assert get_resp.json()["surname"] == "Kowalski"

    def test_update_name_and_surname(self):
        update_body = {"name": "Marcin", "surname": "Kwiatek"}
        patch_resp = requests.patch(f"{self.url}/{self.pesel}", json=update_body)
        assert patch_resp.status_code == 200
        
        get_resp = requests.get(f"{self.url}/{self.pesel}")
        assert get_resp.json()["name"] == "Marcin"
        assert get_resp.json()["surname"] == "Kwiatek"

    def test_delete_account(self):
        delete_resp = requests.delete(f"{self.url}/{self.pesel}")
        assert delete_resp.status_code == 200
        
        get_resp = requests.get(f"{self.url}/{self.pesel}")
        assert get_resp.status_code == 404

    def test_get_all_accounts(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_accounts_count(self):
        response = requests.get(f"{self.url}/count")
        assert response.status_code == 200
        assert "count" in response.json()

    def test_update_non_existent_account(self):
        response = requests.patch(f"{self.url}/00000000000", json={"name": "Lars"})
        assert response.status_code == 404

    def test_delete_non_existent_account(self):
        response = requests.delete(f"{self.url}/00000000000")
        assert response.status_code == 404

    
