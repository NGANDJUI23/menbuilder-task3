"""
Error Handler Middleware
"""

from functools import wraps
from flask import jsonify
from src.services.monitoring_service import monitoring
import os

class APIError(Exception):
    def __init__(self, message, status_code=400, error_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except APIError as e:
            monitoring.record_error(str(e.status_code), e.message)
            return jsonify({
                "error": e.message,
                "error_code": e.error_code
            }), e.status_code
        except Exception as e:
            monitoring.record_error("500", str(e))
            return jsonify({
                "error": "Erreur interne du serveur"
            }), 500
    return decorated_function