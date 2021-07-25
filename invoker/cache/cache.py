import json

from redis import Redis
from cachetools import TTLCache


class Cache:

    def __init__(self, redis_host, redis_port, local_cache_size=3, ttl_sec=10) -> None:
        self.local_ttl_cache = TTLCache(maxsize=local_cache_size, ttl=ttl_sec)
        self.redis_cache = Redis(host=redis_host, port=redis_port)

    def get_key(self, viewer_id):
        if viewer_id in self.local_ttl_cache:
            return self.local_ttl_cache[viewer_id]
        else:
            redis_value = self.redis_cache.get(viewer_id)
            key_value = None if redis_value is None else json.loads(redis_value.decode())
            return key_value

    def cache(self, key, value):
        self.local_ttl_cache[key] = value
        self.redis_cache.set(key, json.dumps(value))
