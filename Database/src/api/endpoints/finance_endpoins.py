from flask import Blueprint, jsonify

from src.api.schemas import BodyCreateTransaction, ResponseCreateTransaction

app = Blueprint("api_finance", __name__, url_prefix="/api/transaction")

@app.route("/create", methods=['POST'])
def create_transaction(body: BodyCreateTransaction) -> ResponseCreateTransaction:
    pass
