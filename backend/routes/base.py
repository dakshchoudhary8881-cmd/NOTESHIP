from quart import Blueprint, jsonify

base_routes = Blueprint("base_routes", __name__)

@base_routes.route("/", methods=["GET"])
async def home():
    return jsonify({
        "status": "success",
        "message": "NOTESHIP backend running successfully."
    })
