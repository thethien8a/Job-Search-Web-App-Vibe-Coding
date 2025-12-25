import time
from functools import wraps
from typing import Any, Callable

class TTLCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Any:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl_seconds:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        self.cache[key] = (value, time.time())

    def clear(self):
        self.cache = {}

# Global caches
dropdown_cache = TTLCache(ttl_seconds=3600)  # 1 hour for dropdowns
search_cache = TTLCache(ttl_seconds=60)      # 1 minute for search results

def cache_response(cache: TTLCache, key_builder: Callable = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Exclude 'db' session from cache key usually, but for simple wrapper:
            # We need a robust key. 
            # Ideally use arguments. kwargs + specific args.
            
            # Simple key generation: function name + stringified kwargs (excluding db)
            cache_kwargs = {k: v for k, v in kwargs.items() if k != 'db'}
            
            if key_builder:
                key = key_builder(*args, **kwargs)
            else:
                key = f"{func.__name__}:{str(sorted(cache_kwargs.items()))}"
            
            cached_val = cache.get(key)
            if cached_val:
                return cached_val
            
            result = await func(*args, **kwargs)
            cache.set(key, result)
            return result
        return wrapper
    return decorator
