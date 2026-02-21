from behave import *
import requests

URL = "http://localhost:5000"

@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")

@step('I create an account using name: "{name}", last name: "{last_name}", pesel: "{pesel}"')
def create_account(context, name, last_name, pesel):
    json_body = {
        "name": name,
        "surname": last_name,
        "pesel": pesel
    }
    create_resp = requests.post(URL + "/api/accounts", json=json_body)
    assert create_resp.status_code == 201

@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts")
    assert len(response.json()) == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 404

@when('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200

@when('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    json_body = {field: value}
    response = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert response.status_code == 200

@then('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()[field] == value

# --- KROKI DLA PRZELEWÓW ---

@step('Account with pesel "{pesel}" has balance: "{amount}"')
def set_account_balance(context, pesel, amount):
    # Używamy PATCH do ręcznego ustawienia balansu na potrzeby testu
    json_body = {"balance": int(amount)}
    resp = requests.patch(URL + f"/api/accounts/{pesel}", json=json_body)
    assert resp.status_code == 200

@when('I perform a transfer of "{amount}" from "{pesel_out}" to "{pesel_in}"')
def perform_transfer(context, amount, pesel_out, pesel_in):
    json_body = {
        "acc_out": pesel_out,
        "acc_in": pesel_in,
        "amount": int(amount)
    }
    resp = requests.post(URL + "/api/accounts/transfer", json=json_body)
    assert resp.status_code == 200

@then('Account with pesel "{pesel}" has balance equal to "{amount}"')
def check_balance(context, pesel, amount):
    resp = requests.get(URL + f"/api/accounts/{pesel}")
    assert resp.status_code == 200
    assert resp.json()["balance"] == int(amount)