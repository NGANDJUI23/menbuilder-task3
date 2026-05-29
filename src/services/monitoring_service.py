"""
Service de monitoring - Métriques, logging et alerting
"""

from datetime import datetime
from typing import Dict, List
import time

class MonitoringService:
    """Collecte et expose les métriques de l'application"""
    
    def __init__(self):
        self.metrics = {
            "api_calls": {},
            "errors": {},
            "response_times": [],
            "cache_hits": 0,
            "cache_misses": 0
        }
    
    def record_api_call(self, endpoint: str, duration: float, success: bool):
        """Enregistre un appel API"""
        if endpoint not in self.metrics["api_calls"]:
            self.metrics["api_calls"][endpoint] = {
                "total": 0, "success": 0, "failed": 0
            }
        
        self.metrics["api_calls"][endpoint]["total"] += 1
        if success:
            self.metrics["api_calls"][endpoint]["success"] += 1
        else:
            self.metrics["api_calls"][endpoint]["failed"] += 1
        
        self.metrics["response_times"].append({
            "endpoint": endpoint,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
    
    def record_error(self, error_type: str, details: str):
        """Enregistre une erreur"""
        if error_type not in self.metrics["errors"]:
            self.metrics["errors"][error_type] = []
        
        self.metrics["errors"][error_type].append({
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.metrics["errors"][error_type]) > 100:
            self.metrics["errors"][error_type] = self.metrics["errors"][error_type][-100:]
    
    def record_cache_hit(self):
        self.metrics["cache_hits"] += 1
    
    def record_cache_miss(self):
        self.metrics["cache_misses"] += 1
    
    def get_metrics(self) -> Dict:
        """Retourne les métriques actuelles"""
        return {
            **self.metrics,
            "cache_ratio": self._calculate_cache_ratio(),
            "avg_response_time": self._calculate_avg_response_time()
        }
    
    def _calculate_cache_ratio(self) -> float:
        total = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        if total == 0:
            return 0.0
        return round(self.metrics["cache_hits"] / total * 100, 2)
    
    def _calculate_avg_response_time(self) -> float:
        if not self.metrics["response_times"]:
            return 0.0
        avg = sum(t["duration"] for t in self.metrics["response_times"]) / len(self.metrics["response_times"])
        return round(avg, 3)

monitoring = MonitoringService()