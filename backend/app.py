from flask import Flask, jsonify
from flask_cors import CORS

# Import route blueprints
from routes.base import base_routes
from routes.chat import chat_routes

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register API routes
    app.register_blueprint(base_routes)
    app.register_blueprint(chat_routes)

    # Global error handler
    @app.errorhandler(Exception)
    def handle_error(e):
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return app


# -----------------------------
# START FLASK SERVER
# -----------------------------
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
