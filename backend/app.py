from flask import Flask, jsonify
from flask_cors import CORS

# Import route blueprints
from routes.base import base_routes

def create_app():
    app = Flask(__name__)

    # Enable CORS for frontend → backend communication
    CORS(app)

    # Register blueprints (API routes)
    app.register_blueprint(base_routes)

    # Global error handler
    @app.errorhandler(Exception)
    def handle_error(e):
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
