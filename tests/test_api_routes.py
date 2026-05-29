"""
Tests d'intégration pour les routes API
"""

import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    from src.api.routes.weather_routes import weather_bp
    app = client.application
    app.register_blueprint(weather_bp)
    
    response = client.get('/api/v1/weather/health')
    assert response.status_code == 200