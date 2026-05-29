"""
Configuration de l'application
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    WEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'demo_key_123')
    WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'https://api.openweathermap.org/data/3.0/weather')
    
    # Cache Configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TTL = int(os.getenv('CACHE_TTL', 300))
    
    # API Rate Limiting
    RATE_LIMIT = int(os.getenv('RATE_LIMIT', 100))
    RATE_WINDOW = int(os.getenv('RATE_WINDOW', 60))
    
    # Timeouts
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # Application
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

settings = Settings()