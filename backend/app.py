from quart import Quart, jsonify
from quart_cors import cors
from routes.base import base_routes
from routes.chat import chat_routes
from routes.notes import notes_bp


def create_app():
    app = Quart(__name__)
    app = cors(app, allow_origin=["http://127.0.0.1:8000", "http://localhost:8000"])

    app.register_blueprint(base_routes)
    app.register_blueprint(chat_routes)
    app.register_blueprint(notes_bp)

    @app.errorhandler(Exception)
    async def handle_error(e):
        import traceback

        from werkzeug.exceptions import HTTPException
        
        if isinstance(e, HTTPException):
            return jsonify({"status": "error", "message": e.description}), e.code
        
        # Log full traceback for internal errors
        traceback.print_exc()
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

