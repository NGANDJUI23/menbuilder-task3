"""
Authentication Middleware
"""

from functools import wraps
from flask import request, jsonify
import os

API_KEY = os.getenv('API_KEY', 'dev-secret-key-123')

def require_api_key(f):
    """Vérifie que la requête contient une clé API valide"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key or api_key != API_KEY:
            return jsonify({
                "error": "Clé API invalide ou manquante"
            }), 401
        
        return f(*args, **kwargs)
    return decorated_function

def require_jwt_token(f):
    """Vérifie le token JWT"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token manquant"}), 401
        
        token = auth_header.split(' ')[1]
        # Vérifier le token (à implémenter avec PyJWT)
        
        return f(*args, **kwargs)
    return decorated_function