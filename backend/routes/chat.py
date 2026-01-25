import requests
from flask import Blueprint, jsonify, request
from services.ai_service import get_ai_response

chat_routes = Blueprint("chat_routes", __name__)

@chat_routes.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"status": "error", "message": "Missing 'message' field"}), 400

    user_msg = data["message"]

    # Security: Limit input length to prevent context flooding
    if not isinstance(user_msg, str) or len(user_msg) > 2000:
        return jsonify({"status": "error", "message": "Message too long (max 2000 chars)"}), 400

    try:
        # Call real AI model
        reply = get_ai_response(user_msg)
        
        # Check if service returned an error string
        if reply and (reply.startswith("Request Failed") or reply.startswith("Bytez Error") or reply.startswith("Model API error")):
             print(f"AI Service Logic Error: {reply} | User Message: {user_msg}")
             return jsonify({"status": "error", "message": "AI service unavailable"}), 503

        return jsonify({
            "status": "success",
            "query": user_msg,
            "reply": reply
        })

    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(f"AI Service Error: {e} | User Message: {user_msg}") # using print as simple logger
        return jsonify({"status": "error", "message": "AI service unavailable"}), 503
    except Exception as e:
        print(f"Unexpected Error: {e} | User Message: {user_msg}")
        return jsonify({"status": "error", "message": "AI service unavailable"}), 503
