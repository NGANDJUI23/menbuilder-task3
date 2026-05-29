"""
Routes pour l'API météo
Endpoint: /api/v1/weather
"""

from flask import Blueprint, request, jsonify
from src.services.weather_service import WeatherAPIClient
from src.services.monitoring_service import monitoring
from src.api.middleware.rate_limiter import rate_limit
from src.api.middleware.error_handler import handle_errors
import time

weather_bp = Blueprint('weather', __name__, url_prefix='/api/v1/weather')
weather_client = WeatherAPIClient()

@weather_bp.route('/<city>', methods=['GET'])
@rate_limit(limit=30, window=60)
@handle_errors
def get_weather(city):
    """GET /api/v1/weather/paris"""
    start_time = time.time()
    
    data, error = weather_client.get_weather(city)
    
    duration = time.time() - start_time
    monitoring.record_api_call(f"/weather/{city}", duration, success=(error is None))
    
    if error:
        return jsonify({
            "success": False,
            "error": error,
            "city": city
        }), 404
    
    return jsonify({
        "success": True,
        "data": data
    }), 200

@weather_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "weather-api",
        "timestamp": time.time()
    }), 200