"""
Décorateur pour le caching automatique
"""

from functools import wraps
from ..services.cache_service import CacheService

cache_service = CacheService()

def cached(ttl: int = 300, key_prefix: str = ""):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix or func.__name__}:{args}:{kwargs}"
            
            cached_result = cache_service.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(*args, **kwargs)
            cache_service.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator