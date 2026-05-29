"""
Schémas Pydantic pour les données météo
"""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class WeatherResponse(BaseModel):
    city: str = Field(..., description="Nom de la ville")
    temperature: float = Field(..., description="Température en °C")
    condition: str = Field(..., description="Condition météo")
    humidity: int = Field(..., ge=0, le=100, description="Humidité en %")
    last_update: datetime = Field(..., description="Dernière mise à jour")
    
    class Config:
        schema_extra = {
            "example": {
                "city": "Paris",
                "temperature": 22.5,
                "condition": "clear",
                "humidity": 65
            }
        }

class WeatherRequest(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)
    units: Optional[str] = Field("metric", regex="^(metric|imperial)$")