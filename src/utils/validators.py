"""
Validateurs pour les données d'entrée
"""

import re
from typing import Optional

def validate_city(city: Optional[str]) -> bool:
    if not city or not isinstance(city, str):
        return False
    
    city = city.strip()
    
    if len(city) < 1 or len(city) > 100:
        return False
    
    pattern = r'^[a-zA-ZÀ-ÿ\s\-\.\']+$'
    return bool(re.match(pattern, city))

def validate_temperature(temp: float) -> bool:
    return -90 <= temp <= 60

def validate_humidity(humidity: int) -> bool:
    return 0 <= humidity <= 100