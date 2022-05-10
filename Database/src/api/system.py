from flask import Blueprint, jsonify

from src.services.coin_to_coin import coin

app = Blueprint("api_system", __name__, url_prefix="/api")

@app.route("/health/check/isWork", methods=["GET"])
def health_here():
    return jsonify({"message": True})

@app.route("/health/check/CoinToCoin/isWork", methods=["GET"])
def get_coin_to_coin_status():
    return jsonify({"message": coin.status_api()})

@app.route("/health/check/database/isWork", methods=["GET"])
def get_database_status():
    pass