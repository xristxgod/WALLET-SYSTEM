import json
from typing import Union

from flask import Blueprint, jsonify

from src.api.schemas import BodyCreateTransaction, ResponseCreateTransaction
from src.crypto.transaction import Transaction

from config import logger

app = Blueprint("api_finance", __name__, url_prefix="/api/transaction")

@app.route("/create", methods=['POST'])
def create_transaction(body: BodyCreateTransaction) -> Union[ResponseCreateTransaction, json]:
    try:
        return Transaction.create_transaction(body=body)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return jsonify({"message": f"{error}"})
