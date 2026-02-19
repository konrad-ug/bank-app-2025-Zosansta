from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount

app = Flask(__name__)
registry = AccountRegistry()

@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    if registry.find_by_pesel(data["pesel"]):
        return jsonify({"message": "Konto z tym numerem PESEL już istnieje"}), 409
    
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Konto utworzone"}), 201

@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def handle_transfer(pesel):
    data = request.get_json()
    account = registry.find_by_pesel(pesel)
    
    if not account:
        return jsonify({"message": "Nie znaleziono konta"}), 404
        
    try:
        amount = data["amount"]
        transfer_type = data["type"]

        if transfer_type == "incoming":
            account.incoming_transfer(amount)
        elif transfer_type == "outgoing":
            if account.balance < amount:
                return jsonify({"message": "Błąd przelewu"}), 422
            account.outgoing_express_transfer(amount)
        elif transfer_type == "express":
            # Sprawdzenie salda dla ekspresowego (zakładając opłatę np. 1 zł)
            if account.balance < amount:
                return jsonify({"message": "Błąd przelewu"}), 422
            account.outgoing_express_transfer(amount)
        else:
            return jsonify({"message": "Nieznany typ przelewu"}), 400
            
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200 
    except Exception:
        return jsonify({"message": "Błąd przelewu"}), 422

@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all()
    accounts_data = [
        {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
        for acc in accounts
    ]
    return jsonify(accounts_data), 200

@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    return jsonify({"count": registry.count()}), 200

@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.find_by_pesel(pesel)
    if account:
        return jsonify({
            "name": account.first_name, "surname": account.last_name,
            "pesel": account.pesel, "balance": account.balance
        }), 200
    return jsonify({"message": "Nie znaleziono konta"}), 404

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    data = request.get_json()
    account = registry.find_by_pesel(pesel)
    if account:
        if "name" in data: account.first_name = data["name"]
        if "surname" in data: account.last_name = data["surname"]
        return jsonify({"message": "Konto zaktualizowane"}), 200
    return jsonify({"message": "Nie znaleziono konta"}), 404

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_by_pesel(pesel)
    if account:
        registry.get_all().remove(account)
        return jsonify({"message": "Konto usunięte"}), 200
    return jsonify({"message": "Nie znaleziono konta"}), 404