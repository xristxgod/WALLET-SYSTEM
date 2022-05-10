from flask import Blueprint, jsonify

app = Blueprint("api_finance", __name__, url_prefix="/api/transaction")

@app.route("/create", methods=['POST'])
def create_transaction():
    pass
