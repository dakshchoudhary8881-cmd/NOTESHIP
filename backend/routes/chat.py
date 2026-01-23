from flask import Blueprint, request, jsonify
from services.ai_service import get_ai_response

chat_routes = Blueprint("chat_routes", __name__)

@chat_routes.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"status": "error", "message": "Missing 'message' field"}), 400

    user_msg = data["message"]

    # Call real AI model
    reply = get_ai_response(user_msg)

    return jsonify({
        "status": "success",
        "query": user_msg,
        "reply": reply
    })
