import json
import redis
from typing import Any, Optional
from app.core.config import settings

class CacheService:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL)
            self.redis_client.ping()  # Test connection
            self.enabled = True
        except:
            print("Redis not available, caching disabled")
            self.redis_client = None
            self.enabled = False
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, expire: int = 3600):
        """Set value in cache with expiration"""
        if not self.enabled:
            return False
        
        try:
            serialized_value = json.dumps(value, default=str)
            self.redis_client.setex(key, expire, serialized_value)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str):
        """Delete key from cache"""
        if not self.enabled:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    async def get_trending_tracks(self):
        """Get cached trending tracks"""
        return await self.get("trending_tracks")
    
    async def set_trending_tracks(self, tracks: list, expire: int = 1800):
        """Cache trending tracks for 30 minutes"""
        return await self.set("trending_tracks", tracks, expire)
    
    async def get_user_playlists(self, user_id: int):
        """Get cached user playlists"""
        return await self.get(f"user_playlists:{user_id}")
    
    async def set_user_playlists(self, user_id: int, playlists: list, expire: int = 600):
        """Cache user playlists for 10 minutes"""
        return await self.set(f"user_playlists:{user_id}", playlists, expire)
    
    async def invalidate_user_cache(self, user_id: int):
        """Invalidate all cache for a user"""
        keys_to_delete = [
            f"user_playlists:{user_id}",
            f"user_favorites:{user_id}",
            f"user_profile:{user_id}"
        ]
        
        for key in keys_to_delete:
            await self.delete(key)

cache_service = CacheService()