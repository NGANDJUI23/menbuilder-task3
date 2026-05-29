"""
Tests unitaires pour le service météo
"""

from unittest.mock import Mock, patch

class TestWeatherService:
    
    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        from src.services.weather_service import WeatherAPIClient
        client = WeatherAPIClient()
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Paris",
            "main": {"temp": 22.5, "humidity": 65},
            "weather": [{"description": "ciel dégagé"}]
        }
        mock_get.return_value = mock_response
        
        data, error = client.get_weather("Paris")
        
        assert error is None
        assert data["city"] == "Paris"
        assert data["temperature"] == 22.5
    
    @patch('requests.get')
    def test_get_weather_not_found(self, mock_get):
        from src.services.weather_service import WeatherAPIClient
        client = WeatherAPIClient()
        
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        data, error = client.get_weather("VilleInexistante")
        
        assert data is None
        assert "non trouvée" in error