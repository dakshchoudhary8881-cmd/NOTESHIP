from flask import Blueprint, jsonify, request
from services.ai_service import get_ai_response

notes_bp = Blueprint("notes_routes", __name__)

@notes_bp.route("/notes", methods=["POST"])
def generate_notes():
    data = request.get_json()

    if not data or "topic" not in data:
        return jsonify({"status": "error", "message": "Missing 'topic' field"}), 400

    topic = data["topic"]

    if not isinstance(topic, str):
        return jsonify({"status": "error", "message": "Topic must be a string"}), 400

    topic = topic.strip()
    if not topic:
        return jsonify({"status": "error", "message": "Topic cannot be empty"}), 400
    
    if len(topic) > 120:
        return jsonify({"status": "error", "message": "Topic too long (max 120 chars)"}), 400

    system_prompt = "Act as an expert academic tutor. Your goal is to create structured, high-quality revision notes."

    user_prompt = f"""
    Create a revision sheet for the topic: "{topic}".

    Follow this strict structure:
    1. **Definition/Core Concept** – concise (2–3 sentences)
    2. **Key Formulas/Dates**
    3. **Key Points** – 5–7 bullet points
    4. **Common Mistakes**
    5. **Real-world Example**

    Return clean Markdown.
    """

    try:
        reply = get_ai_response(user_prompt, system_message=system_prompt)

        return jsonify({
            "status": "success",
            "topic": topic,
            "reply": reply
        })
    except Exception as e:
        print(f"Notes API Error: {e} | Topic: {topic}")
        return jsonify({"status": "error", "message": "AI service unavailable"}), 503
