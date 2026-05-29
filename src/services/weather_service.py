"""
Service d'intégration avec l'API OpenWeatherMap
Gère les appels API, le cache et les erreurs
"""

import requests
import json
from typing import Dict, Optional, Tuple
from datetime import datetime
from ..config.settings import settings
from ..utils.logger import logger
from ..utils.cache_decorator import cached

class WeatherAPIClient:
    """Client pour l'API OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_URL
        self.timeout = settings.REQUEST_TIMEOUT
    
    @cached(ttl=300)
    def get_weather(self, city: str) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Récupère la météo pour une ville.
        
        Returns:
            Tuple (data, error_message)
            - data: {city, temperature, condition, humidity, last_update}
            - error_message: None si succès
        """
        if not city or not isinstance(city, str):
            return None, "Nom de ville invalide"
        
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'fr'
            }
            
            logger.info(f"Appel API météo pour {city}")
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = self._clean_response(response.json(), city)
                logger.info(f"Météo récupérée pour {city}")
                return data, None
                
            elif response.status_code == 401:
                return None, "Clé API invalide"
            elif response.status_code == 404:
                return None, f"Ville '{city}' non trouvée"
            else:
                return None, f"Erreur API: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return None, "Erreur reseau - Impossible de contacter l'API"
        except requests.exceptions.Timeout:
            return None, "Delai d'attente dépassé"
        except requests.exceptions.RequestException as e:
            return None, f"Erreur de requete: {str(e)}"
        except json.JSONDecodeError:
            return None, "Erreur de parsing JSON"
    
    def _clean_response(self, raw_data: Dict, city: str) -> Dict:
        """Nettoie la réponse API pour ne garder que les champs utiles"""
        return {
            "city": raw_data.get('name', city),
            "temperature": round(raw_data.get('main', {}).get('temp', 0), 1),
            "condition": raw_data.get('weather', [{}])[0].get('description', 'Inconnu'),
            "humidity": raw_data.get('main', {}).get('humidity', 0),
            "last_update": datetime.now().isoformat()
        }