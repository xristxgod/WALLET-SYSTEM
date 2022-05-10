from flask import Blueprint, jsonify

app = Blueprint("api_system", __name__, url_prefix="/api")

@app.route("/health/check/isWork", methods=["GET"])
def health_here():
    return jsonify({"message": True})

@app.route("/health/check/CoinToCoin/isWork", methods=["GET"])
def get_coin_status():
    pass