"""
Rate Limiter Middleware
"""

from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
from flask import request, jsonify

request_counts = defaultdict(list)

def rate_limit(limit: int = 100, window: int = 60):
    """Décorateur pour limiter le taux de requêtes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            now = datetime.now()
            
            request_counts[client_ip] = [
                req_time for req_time in request_counts[client_ip]
                if now - req_time < timedelta(seconds=window)
            ]
            
            if len(request_counts[client_ip]) >= limit:
                return jsonify({
                    "error": "Rate limit exceeded",
                    "limit": limit,
                    "window": window,
                    "remaining": 0
                }), 429
            
            request_counts[client_ip].append(now)
            return f(*args, **kwargs)
        return decorated_function
    return decorator