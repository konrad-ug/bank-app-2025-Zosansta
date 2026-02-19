import unittest
from app.api import app, registry


class TestApi(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        registry.get_all().clear()

        self.pesel = "12345678901"

        self.client.post("/api/accounts", json={
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": self.pesel
        })

    def tearDown(self):
        registry.get_all().clear()


    # ---------- CREATE ----------

    def test_create_account_success(self):
        response = self.client.post("/api/accounts", json={
            "name": "Anna",
            "surname": "Nowak",
            "pesel": "99999999999"
        })

        self.assertEqual(response.status_code, 201)


    def test_create_account_duplicate(self):
        response = self.client.post("/api/accounts", json={
            "name": "Jan",
            "surname": "Kowalski",
            "pesel": self.pesel
        })

        self.assertEqual(response.status_code, 409)


    # ---------- GET ----------

    def test_get_all_accounts(self):
        response = self.client.get("/api/accounts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)


    def test_get_account_by_pesel(self):
        response = self.client.get(f"/api/accounts/{self.pesel}")
        self.assertEqual(response.status_code, 200)


    def test_get_account_not_found(self):
        response = self.client.get("/api/accounts/00000000000")
        self.assertEqual(response.status_code, 404)


    def test_get_account_count(self):
        response = self.client.get("/api/accounts/count")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["count"], 1)


    # ---------- UPDATE ----------

    def test_update_account(self):
        response = self.client.patch(
            f"/api/accounts/{self.pesel}",
            json={"name": "Adam"}
        )

        self.assertEqual(response.status_code, 200)


    def test_update_account_not_found(self):
        response = self.client.patch(
            "/api/accounts/00000000000",
            json={"name": "Adam"}
        )

        self.assertEqual(response.status_code, 404)


    # ---------- DELETE ----------

    def test_delete_account(self):
        response = self.client.delete(f"/api/accounts/{self.pesel}")
        self.assertEqual(response.status_code, 200)


    def test_delete_account_not_found(self):
        response = self.client.delete("/api/accounts/00000000000")
        self.assertEqual(response.status_code, 404)


    # ---------- TRANSFERS ----------

    def test_incoming_transfer(self):
        response = self.client.post(
            f"/api/accounts/{self.pesel}/transfer",
            json={"amount": 1000, "type": "incoming"}
        )

        self.assertEqual(response.status_code, 200)


    def test_outgoing_transfer_fail(self):
        response = self.client.post(
            f"/api/accounts/{self.pesel}/transfer",
            json={"amount": 1000, "type": "outgoing"}
        )

        self.assertEqual(response.status_code, 422)


    def test_transfer_account_not_found(self):
        response = self.client.post(
            "/api/accounts/00000000000/transfer",
            json={"amount": 100, "type": "incoming"}
        )

        self.assertEqual(response.status_code, 404)


    def test_transfer_unknown_type(self):
        response = self.client.post(
            f"/api/accounts/{self.pesel}/transfer",
            json={"amount": 100, "type": "unknown"}
        )

        self.assertEqual(response.status_code, 400)


    def test_transfer_missing_amount(self):
        response = self.client.post(
            f"/api/accounts/{self.pesel}/transfer",
            json={"type": "incoming"}
        )

        self.assertEqual(response.status_code, 422)
