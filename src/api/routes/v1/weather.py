"""
API Version 1 - Endpoints météo
"""

from flask import Blueprint, jsonify, request
from ....services.weather_service import WeatherAPIClient
from ....utils.validators import validate_city
import time

weather_v1 = Blueprint('weather_v1', __name__)
weather_client = WeatherAPIClient()

@weather_v1.route('/current', methods=['GET'])
def get_current_weather():
    """GET /api/v1/weather/current?city=paris"""
    city = request.args.get('city')
    
    if not validate_city(city):
        return jsonify({
            "error": "Parametre 'city' requis et doit être valide"
        }), 400
    
    data, error = weather_client.get_weather(city)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify({
        "status": "success",
        "data": data,
        "timestamp": time.time()
    }), 200