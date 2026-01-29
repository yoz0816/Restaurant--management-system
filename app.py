import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database.db import db,migrate
from config import Config
from controllers import api_bp
from utils.exceptions import AppException
from utils.response import error_response
from utils.logging import configure_logging


def create_app():
    app = Flask(__name__)
    configure_logging(app)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)
    JWTManager(app)
    db.init_app(app)
    migrate.init_app(app, db)


    register_blueprints(app)
    register_middlewares(app)
    register_error_handlers(app)
    register_health_check(app)

    return app

def register_blueprints(app):
    app.register_blueprint(api_bp)

def register_middlewares(app):
    @app.before_request
    def log_request():
        app.logger.info(f"{request.method} {request.path}")

def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        return error_response(e.message, e.status_code)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "error": "Method Not Allowed",
            "path": request.path,
            "method_used": request.method,
            "allowed_methods": list(e.valid_methods) if hasattr(e, "valid_methods") else []
        }), 405

    @app.errorhandler(500)
    def server_error(e):
        app.logger.exception("Unhandled server error")
        return error_response("Internal server error", 500)
    
def register_health_check(app):
    @app.get("/api/health")
    def health():
        return jsonify({
            "status": "OK",
            "environment": app.config.get("FLASK_ENV"),
            "message": "Josh Restaurant Management Backend is running."
        })


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=app.config["DEBUG"])
