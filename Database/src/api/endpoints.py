from flask import Blueprint, jsonify

app = Blueprint("api", __name__, url_prefix="/api")

@app.route("/health/check/isWork")
def health_here():
    return jsonify({"message": True})