from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
from src.mongodb_repository import MongoAccountsRepository
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
        if "balance" in data: account.balance = data["balance"] 
        return jsonify({"message": "Konto zaktualizowane"}), 200
    return jsonify({"message": "Nie znaleziono konta"}), 404

@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_by_pesel(pesel)
    if account:
        registry.get_all().remove(account)
        return jsonify({"message": "Konto usunięte"}), 200
    return jsonify({"message": "Nie znaleziono konta"}), 404

@app.route("/api/accounts/transfer", methods=['POST'])
def transfer_between_accounts():
    data = request.get_json()
    acc_out = registry.find_by_pesel(data["acc_out"])
    acc_in = registry.find_by_pesel(data["acc_in"])
    amount = data["amount"]

    if acc_out and acc_in:
        if acc_out.balance >= amount:
            acc_out.outgoing_transfer(amount)
            acc_in.incoming_transfer(amount)
            return jsonify({"message": "Przelew wykonany"}), 200
        return jsonify({"message": "Brak środków"}), 422
    return jsonify({"message": "Nie znaleziono kont"}), 404


mongo_repo = MongoAccountsRepository()

@app.route("/api/accounts/save", methods=['POST'])
def save_to_db():
    accounts = registry.get_all()
    mongo_repo.save_all(accounts)
    return jsonify({"message": "Konta zapisane w bazie danych"}), 200

@app.route("/api/accounts/load", methods=['POST'])
def load_from_db():
    registry.clear() 
    db_accounts = mongo_repo.load_all()
    
    for data in db_accounts:
        acc = PersonalAccount(data["name"], data["surname"], data["pesel"])
        acc.balance = data["balance"]
        acc.history = data["history"]
        registry.add_account(acc)
        
    return jsonify({"message": "Konta załadowane z bazy danych"}), 200