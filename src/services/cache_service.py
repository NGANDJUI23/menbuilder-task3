"""
Service de cache - Interface unifiée pour Redis/Memcached/Cache mémoire
"""

from typing import Any, Optional
from datetime import datetime, timedelta
import json

class CacheService:
    """Service de cache avec fallback mémoire"""
    
    def __init__(self, redis_client=None):
        self.redis = redis_client
        self.memory_cache = {}
        self.default_ttl = 300
    
    def get(self, key: str) -> Optional[Any]:
        """Récupère une valeur du cache"""
        if self.redis:
            try:
                value = self.redis.get(key)
                if value:
                    return json.loads(value)
            except Exception:
                pass
        
        if key in self.memory_cache:
            data, expires = self.memory_cache[key]
            if datetime.now() < expires:
                return data
            del self.memory_cache[key]
        
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Stocke une valeur dans le cache"""
        ttl = ttl or self.default_ttl
        
        if self.redis:
            try:
                self.redis.setex(key, ttl, json.dumps(value))
                return
            except Exception:
                pass
        
        expires = datetime.now() + timedelta(seconds=ttl)
        self.memory_cache[key] = (value, expires)
    
    def delete(self, key: str):
        """Supprime une clé du cache"""
        if self.redis:
            try:
                self.redis.delete(key)
            except Exception:
                pass
        
        if key in self.memory_cache:
            del self.memory_cache[key]
    
    def clear_pattern(self, pattern: str):
        """Supprime toutes les clés correspondant à un pattern"""
        if self.redis:
            try:
                keys = self.redis.keys(pattern)
                if keys:
                    self.redis.delete(*keys)
            except Exception:
                pass
        
        keys_to_delete = [k for k in self.memory_cache if pattern in k]
        for k in keys_to_delete:
            del self.memory_cache[k]