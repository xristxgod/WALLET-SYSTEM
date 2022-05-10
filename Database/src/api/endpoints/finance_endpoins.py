import json
from typing import Union

from flask import Blueprint, jsonify

from src.api.schemas import BodyTransaction, BodyCreateWallet, BodyCheckBalance, BodyCoinToCoin
from src.api.schemas import (
    ResponseCreateTransaction, ResponseSendTransaction,
    ResponseCreateWallet, ResponseCheckBalance, ResponseCoinToCoin
)
from src.crypto.transaction import Transaction
from src.crypto.wallet import Wallet
from src.services.coin_to_coin import coin

from config import logger

app = Blueprint("api_finance", __name__, url_prefix="/api")

# <<<======================================>>> Coin To Coin <<<======================================================>>>

@app.get("/coinToCoin/price", methods=['POST'])
def check_coin_price(body: BodyCoinToCoin) -> Union[ResponseCoinToCoin, json]:
    try:
        return ResponseCoinToCoin(
            coin=body.coin,
            toCoin=body.toCoin,
            price=coin.get_current_price(
                coin=coin.get_correct_token(coin=body.coin),
                to_coin=coin.get_correct_token(coin=body.toCoin)
            )
        )
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return jsonify({"message": f"{error}"})

# <<<======================================>>> Wallet <<<============================================================>>>

@app.route("/create/wallet", methods=['POST'])
def create_wallet(body: BodyCreateWallet) -> ResponseCreateWallet:
    """Create crypto wallet"""
    try:
        return Wallet.create_wallet(body=body)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseCreateWallet(message=f"{error}")

@app.route("/check/balance", methods=['POST'])
def check_balance(body: BodyCheckBalance) -> Union[ResponseCheckBalance, json]:
    """Check crypto wallet balance"""
    try:
        return Wallet.check_balance(body=body)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return jsonify({"message": f"{error}"})

# <<<======================================>>> Transaction <<<=======================================================>>>

@app.route("/create/transaction", methods=['POST'])
def create_transaction(body: BodyTransaction) -> Union[ResponseCreateTransaction, json]:
    """Create crypto transaction"""
    try:
        return Transaction.create_transaction(body=body)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return jsonify({"message": f"{error}"})

@app.route("/send/transaction", methods=['POST'])
def send_transaction(body: BodyTransaction) -> Union[ResponseSendTransaction, json]:
    """Sign and send transaction"""
    try:
        return Transaction.send_transaction(body=body)
    except Exception as error:
        logger.error(f"ERROR: {error}")
        return ResponseSendTransaction(message=f"{error}")